from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User
from app.models.wallet import Wallet, WalletTransaction
from app.utils.decorators import role_required

registrations_ns = Namespace('registrations', description='Registration operations')

REFERRAL_DISCOUNT = 0.05   # 5 % off for the registrant
REFERRAL_BONUS    = 0.05   # 5 % of ticket price credited to referrer's wallet


def get_or_create_wallet(user_id: int) -> Wallet:
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        wallet = Wallet(user_id=user_id, balance=0.0)
        db.session.add(wallet)
        db.session.flush()          # get id without full commit
    return wallet


@registrations_ns.route('')
class RegistrationCreate(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """
        Create a registration.

        Optional fields:
          referral_code  — apply 5 % discount and credit referrer's wallet
          use_wallet     — boolean; if true, deduct available wallet balance first
        """
        user_id = int(get_jwt_identity())
        data    = request.get_json()
        event_id = data.get('event_id')

        event = Event.query.get(event_id)
        if not event or not event.is_active:
            return {'message': 'Event not found or inactive'}, 404

        if event.seats_remaining <= 0:
            return {'message': 'Event is sold out'}, 400

        existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if existing and existing.status != 'cancelled':
            return {'message': 'Already registered'}, 400

        role         = data.get('role', 'athlete')
        role_details = data.get('role_details', {})
        base_price   = event.price

        # ── Referral code handling ────────────────────────────────────────────
        referral_code  = (data.get('referral_code') or '').strip().upper()
        referrer        = None
        discount_amount = 0.0

        if referral_code:
            referrer = User.query.filter_by(referral_code=referral_code).first()
            if not referrer:
                return {'message': 'Invalid referral code'}, 400
            if referrer.id == user_id:
                return {'message': 'You cannot use your own referral code'}, 400
            discount_amount = round(base_price * REFERRAL_DISCOUNT, 2)

        price_after_discount = round(base_price - discount_amount, 2)

        # ── Wallet deduction ─────────────────────────────────────────────────
        use_wallet    = bool(data.get('use_wallet', False))
        wallet_used   = 0.0
        final_price   = price_after_discount

        if use_wallet and price_after_discount > 0:
            wallet = get_or_create_wallet(user_id)
            wallet_used = min(wallet.balance, price_after_discount)
            wallet_used = round(wallet_used, 2)
            final_price = round(price_after_discount - wallet_used, 2)

        # ── Create or reuse registration ─────────────────────────────────────
        # If a cancelled row exists, update it in place — a DB-level UNIQUE
        # constraint on (user_id, event_id) prevents a new INSERT.
        status = 'confirmed' if final_price == 0 else 'pending'
        if existing and existing.status == 'cancelled':
            reg = existing
            reg.status       = status
            reg.role         = role
            reg.role_details = {
                **role_details,
                'referral_code':   referral_code or None,
                'discount_amount': discount_amount,
                'wallet_used':     wallet_used,
                'final_price':     final_price,
            }
        else:
            reg = Registration(
                user_id      = user_id,
                event_id     = event_id,
                status       = status,
                role         = role,
                role_details = {
                    **role_details,
                    'referral_code':   referral_code or None,
                    'discount_amount': discount_amount,
                    'wallet_used':     wallet_used,
                    'final_price':     final_price,
                }
            )
            db.session.add(reg)

        try:
            db.session.flush()      # get reg.id before committing

            # Deduct wallet if applicable
            if wallet_used > 0:
                wallet = get_or_create_wallet(user_id)
                wallet.balance -= wallet_used
                db.session.add(WalletTransaction(
                    wallet_id   = wallet.id,
                    amount      = -wallet_used,
                    type        = 'debit',
                    description = f'Registration payment for "{event.title}" (₹{wallet_used} from wallet)',
                ))

            # Credit referrer's wallet
            if referrer and discount_amount > 0:
                ref_wallet = get_or_create_wallet(referrer.id)
                bonus = round(base_price * REFERRAL_BONUS, 2)
                ref_wallet.balance += bonus
                db.session.add(WalletTransaction(
                    wallet_id   = ref_wallet.id,
                    amount      = bonus,
                    type        = 'referral_bonus',
                    description = f'Referral bonus: {User.query.get(user_id).name} registered for "{event.title}"',
                ))

            db.session.commit()
            return {
                'message':         'Registration created',
                'registration_id': reg.id,
                'final_price':     final_price,
                'discount_amount': discount_amount,
                'wallet_used':     wallet_used,
                'status':          status,
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400


@registrations_ns.route('/validate-referral')
class ValidateReferral(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """
        Validate a referral code and return the discount preview.
        Called on-the-fly when user types a code in the registration form.
        """
        user_id = int(get_jwt_identity())
        data    = request.get_json()
        code    = (data.get('referral_code') or '').strip().upper()
        price   = float(data.get('price', 0))

        if not code:
            return {'valid': False, 'message': 'No code provided'}, 400

        referrer = User.query.filter_by(referral_code=code).first()
        if not referrer:
            return {'valid': False, 'message': 'Invalid referral code'}, 200
        if referrer.id == user_id:
            return {'valid': False, 'message': 'Cannot use your own code'}, 200

        discount = round(price * REFERRAL_DISCOUNT, 2)
        return {
            'valid':    True,
            'discount': discount,
            'message':  f'✓ Code applied — ₹{discount} off!',
        }, 200


@registrations_ns.route('/my')
class MyRegistrations(Resource):
    @jwt_required()
    @role_required('user')
    def get(self):
        """Get authenticated user's registrations."""
        user_id = int(get_jwt_identity())
        regs    = Registration.query.filter_by(user_id=user_id).all()
        return [r.to_dict() for r in regs], 200


@registrations_ns.route('/<int:id>/cancel')
class RegistrationCancel(Resource):
    @jwt_required()
    @role_required('user')
    def put(self, id):
        """Cancel a confirmed registration and refund wallet usage + claw back referrer bonus."""
        user_id = int(get_jwt_identity())
        reg     = Registration.query.get(id)

        if not reg:
            return {'message': 'Registration not found'}, 404
        if reg.user_id != user_id:
            return {'message': 'Forbidden'}, 403
        if reg.status == 'cancelled':
            return {'message': 'Already cancelled'}, 400

        details      = reg.role_details or {}
        wallet_used  = float(details.get('wallet_used', 0))
        refund_amount = 0.0

        # ── Refund wallet amount that was used at checkout ────────────────────
        if wallet_used > 0:
            user_wallet = get_or_create_wallet(user_id)
            user_wallet.balance += wallet_used
            refund_amount = wallet_used
            db.session.add(WalletTransaction(
                wallet_id   = user_wallet.id,
                amount      = wallet_used,
                type        = 'credit',
                description = f'Refund: cancelled registration for "{reg.event.title}" (reg #{reg.id})',
            ))

        # ── Claw back referrer bonus if a referral code was used ──────────────
        referral_code = (details.get('referral_code') or '').strip().upper()
        if referral_code and reg.status == 'confirmed':
            referrer = User.query.filter_by(referral_code=referral_code).first()
            if referrer and referrer.id != user_id:
                bonus = round(reg.event.price * REFERRAL_BONUS, 2)
                ref_wallet = get_or_create_wallet(referrer.id)
                # Only claw back up to what's available (never go negative)
                clawback = min(bonus, ref_wallet.balance)
                if clawback > 0:
                    ref_wallet.balance -= clawback
                    db.session.add(WalletTransaction(
                        wallet_id   = ref_wallet.id,
                        amount      = -clawback,
                        type        = 'debit',
                        description = f'Referral bonus reversed: registration for "{reg.event.title}" was cancelled (reg #{reg.id})',
                    ))

        reg.status = 'cancelled'
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {
            'message':        'Registration cancelled' + (f'. ₹{refund_amount:.2f} refunded to your wallet.' if refund_amount > 0 else '.'),
            'refund_amount':  refund_amount,
            'registration':   reg.to_dict(),
        }, 200