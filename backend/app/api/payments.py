from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.registration import Registration
from app.models.payment import Payment
from app.models.event import Event
from app.models.user import User
from app.models.wallet import Wallet, WalletTransaction
from app.services.razorpay_service import RazorpayService
from app.utils.decorators import role_required

payments_ns = Namespace('payments', description='Payment operations')
rzp_service = RazorpayService()

REFERRAL_DISCOUNT = 0.05
REFERRAL_BONUS    = 0.05


def _get_or_create_wallet(user_id):
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        wallet = Wallet(user_id=user_id, balance=0.0)
        db.session.add(wallet)
        db.session.flush()
    return wallet


@payments_ns.route('/create-order')
class CreateOrder(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """
        Create Razorpay order using the discounted final price.
        Accepts optional referral_code and wallet_used to compute the
        actual amount charged via Razorpay.
        """
        user_id  = int(get_jwt_identity())
        data     = request.get_json()
        event_id = data.get('event_id')

        event = Event.query.get(event_id)
        if not event or event.seats_remaining <= 0:
            return {'message': 'Invalid event or sold out'}, 400

        reg = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if not reg:
            reg = Registration(user_id=user_id, event_id=event_id, status='pending')
            db.session.add(reg)
            db.session.commit()

        if reg.status == 'confirmed':
            return {'message': 'Already registered and confirmed'}, 400

        # ── Compute discounted price ──────────────────────────────────────────
        base_price     = event.price
        referral_code  = (data.get('referral_code') or '').strip().upper()
        wallet_used    = float(data.get('wallet_used', 0))
        discount_amount = 0.0
        referrer        = None

        if referral_code:
            referrer = User.query.filter_by(referral_code=referral_code).first()
            if referrer and referrer.id != user_id:
                discount_amount = round(base_price * REFERRAL_DISCOUNT, 2)

        price_after_discount = round(base_price - discount_amount, 2)

        # Clamp wallet_used to available balance and remaining price
        if wallet_used > 0:
            user_wallet = _get_or_create_wallet(user_id)
            wallet_used = min(wallet_used, user_wallet.balance, price_after_discount)
            wallet_used = round(wallet_used, 2)

        final_price = round(price_after_discount - wallet_used, 2)
        final_price = max(0.0, final_price)

        # ── Create Razorpay order for the final (discounted) price ────────────
        try:
            order_id, amount_paise = rzp_service.create_order(final_price, reg.id)
        except Exception as e:
            import traceback; traceback.print_exc()
            return {'message': f'Payment gateway error: {str(e)}'}, 502

        fee, payout = rzp_service.calculate_payouts(final_price)

        payment = Payment.query.filter_by(registration_id=reg.id).first()
        if not payment:
            payment = Payment(
                registration_id   = reg.id,
                razorpay_order_id = order_id,
                amount            = final_price,
                platform_fee      = fee,
                organizer_payout  = payout,
                status            = 'created',
            )
            db.session.add(payment)
        else:
            payment.razorpay_order_id = order_id
            payment.amount            = final_price
            payment.platform_fee      = fee
            payment.organizer_payout  = payout

        # Store discount metadata on the registration for audit
        details = reg.role_details or {}
        details.update({
            'referral_code':   referral_code or None,
            'discount_amount': discount_amount,
            'wallet_used':     wallet_used,
            'final_price':     final_price,
        })
        reg.role_details = details

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {
            'order_id':        order_id,
            'amount':          amount_paise,
            'currency':        'INR',
            'key_id':          rzp_service.key_id,
            'final_price':     final_price,
            'discount_amount': discount_amount,
            'wallet_used':     wallet_used,
        }, 200


@payments_ns.route('/verify')
class VerifyPayment(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """Verify Razorpay signature and confirm registration"""
        data = request.get_json()
        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')

        payment = Payment.query.filter_by(razorpay_order_id=order_id).first()
        if not payment:
            return {'message': 'Payment record not found'}, 404

        valid = rzp_service.verify_payment_signature(order_id, payment_id, signature)
        if not valid:
            payment.status = 'failed'
            reg = payment.registration
            reg.status = 'payment_failed'

            # Wallet is only deducted after successful verify — since we're
            # in the failure branch, nothing was deducted yet, so no refund needed.
            # Clear wallet_used so a retry re-evaluates balance fresh.
            details = reg.role_details or {}
            details['wallet_used'] = 0
            reg.role_details = details

            db.session.commit()
            return {'message': 'Invalid payment signature'}, 400

        payment.status              = 'paid'
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature  = signature

        reg     = payment.registration
        details = reg.role_details or {}

        # Deduct wallet if it was used
        wallet_used = float(details.get('wallet_used', 0))
        if wallet_used > 0:
            user_wallet = _get_or_create_wallet(reg.user_id)
            user_wallet.balance = max(0, user_wallet.balance - wallet_used)
            db.session.add(WalletTransaction(
                wallet_id   = user_wallet.id,
                amount      = -wallet_used,
                type        = 'debit',
                description = f'Wallet used for event registration (reg #{reg.id})',
            ))

        # Credit referrer's wallet bonus
        referral_code = details.get('referral_code') or ''
        if referral_code:
            referrer = User.query.filter_by(referral_code=referral_code.upper()).first()
            if referrer and referrer.id != reg.user_id:
                bonus = round(reg.event.price * REFERRAL_BONUS, 2)
                ref_wallet = _get_or_create_wallet(referrer.id)
                ref_wallet.balance += bonus
                db.session.add(WalletTransaction(
                    wallet_id   = ref_wallet.id,
                    amount      = bonus,
                    type        = 'referral_bonus',
                    description = f'Referral bonus for event "{reg.event.title}" (reg #{reg.id})',
                ))

        reg.status = 'confirmed'
        db.session.commit()
        return {'message': 'Payment successful', 'registration_id': reg.id}, 200


@payments_ns.route('/fail')
class FailPayment(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """
        Called by the frontend when a Razorpay payment is abandoned or fails
        on the client side (modal dismissed, gateway error, etc.).
        Resets the registration to payment_failed and refunds any wallet
        amount that was reserved for this order.
        """
        user_id  = int(get_jwt_identity())
        data     = request.get_json()
        order_id = data.get('order_id')

        payment = Payment.query.filter_by(razorpay_order_id=order_id).first()
        if not payment:
            return {'message': 'Payment record not found'}, 404

        reg = payment.registration
        if reg.user_id != user_id:
            return {'message': 'Forbidden'}, 403

        # Only act on orders that haven't already been confirmed or refunded
        if reg.status in ('confirmed', 'cancelled'):
            return {'message': f'Registration already {reg.status}'}, 400

        payment.status = 'failed'
        reg.status     = 'payment_failed'

        # ACID note: wallet is only deducted inside /verify (after Razorpay confirms).
        # At this point (payment abandoned/failed before verify), the wallet balance
        # was never touched, so there is nothing to refund here.
        # Clear wallet_used metadata so a retry starts fresh.
        details = reg.role_details or {}
        details['wallet_used'] = 0
        reg.role_details = details

        db.session.commit()
        return {'message': 'Payment cancelled. Your registration is pending — you can retry.'}, 200