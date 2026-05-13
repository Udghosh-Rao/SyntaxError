from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.wallet import Wallet, WalletTransaction
from app.services.razorpay_service import RazorpayService
from app.utils.decorators import role_required

wallet_ns  = Namespace('wallet', description='Wallet operations')
rzp_service = RazorpayService()


def get_or_create_wallet(user_id: int) -> Wallet:
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        wallet = Wallet(user_id=user_id, balance=0.0)
        db.session.add(wallet)
        db.session.commit()
    return wallet


@wallet_ns.route('')
class WalletResource(Resource):
    @jwt_required()
    def get(self):
        """Get wallet balance + recent transactions."""
        user_id = int(get_jwt_identity())
        wallet  = get_or_create_wallet(user_id)
        txns    = WalletTransaction.query \
                    .filter_by(wallet_id=wallet.id) \
                    .order_by(WalletTransaction.created_at.desc()) \
                    .limit(20).all()
        return {
            'wallet':       wallet.to_dict(),
            'transactions': [t.to_dict() for t in txns],
        }, 200


@wallet_ns.route('/add-funds')
class AddFunds(Resource):
    @jwt_required()
    def post(self):
        """
        Create a Razorpay order to top up the wallet.
        Frontend calls this, completes Razorpay checkout,
        then calls /wallet/verify to credit the balance.
        """
        user_id = int(get_jwt_identity())
        data    = request.get_json()
        amount  = float(data.get('amount', 0))

        if amount < 1:
            return {'message': 'Minimum top-up is ₹1'}, 400

        try:
            order_id, amount_paise = rzp_service.create_order(amount, None)
        except Exception as e:
            return {'message': f'Payment gateway error: {str(e)}'}, 502

        return {
            'order_id': order_id,
            'amount':   amount_paise,
            'currency': 'INR',
            'key_id':   rzp_service.key_id,
        }, 200


@wallet_ns.route('/verify-topup')
class VerifyTopup(Resource):
    @jwt_required()
    def post(self):
        """Verify Razorpay signature and credit wallet."""
        user_id = int(get_jwt_identity())
        data    = request.get_json()

        order_id   = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature  = data.get('razorpay_signature')
        amount     = float(data.get('amount', 0))   # amount in INR (not paise)

        if not rzp_service.verify_payment_signature(order_id, payment_id, signature):
            return {'message': 'Invalid payment signature'}, 400

        wallet = get_or_create_wallet(user_id)
        wallet.balance += amount

        txn = WalletTransaction(
            wallet_id   = wallet.id,
            amount      = amount,
            type        = 'credit',
            description = f'Wallet top-up via Razorpay ({payment_id})',
        )
        db.session.add(txn)
        db.session.commit()

        return {'message': 'Wallet credited', 'wallet': wallet.to_dict()}, 200