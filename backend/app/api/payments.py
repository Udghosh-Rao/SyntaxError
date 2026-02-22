from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.registration import Registration
from app.models.payment import Payment
from app.models.event import Event
from app.services.razorpay_service import RazorpayService
from app.utils.decorators import role_required

payments_ns = Namespace('payments', description='Payment operations')
rzp_service = RazorpayService()

@payments_ns.route('/create-order')
class CreateOrder(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """Create Razorpay order (Spec 6.4)"""
        user_id = get_jwt_identity()
        data = request.get_json()
        event_id = data.get('event_id')
        
        event = Event.query.get(event_id)
        if not event or event.seats_remaining <= 0:
            return {'message': 'Invalid event or sold out'}, 400
            
        # Create pending registration
        reg = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if not reg:
            reg = Registration(user_id=user_id, event_id=event_id, status='pending')
            db.session.add(reg)
            db.session.commit() # Need reg.id to create payment

        if reg.status == 'confirmed':
            return {'message': 'Already confirmed'}, 400

        # Feature 6 - Payment Flow
        order_id, amount_paise = rzp_service.create_order(event.price, reg.id)
        fee, payout = rzp_service.calculate_payouts(event.price)
        
        payment = Payment.query.filter_by(registration_id=reg.id).first()
        if not payment:
            payment = Payment(
                registration_id=reg.id,
                razorpay_order_id=order_id,
                amount=event.price,
                platform_fee=fee,
                organizer_payout=payout,
                status='created'
            )
            db.session.add(payment)
        else:
            payment.razorpay_order_id = order_id
            
        try:
            db.session.commit()
            return {
                'order_id': order_id,
                'amount': amount_paise,
                'currency': 'INR',
                'key_id': rzp_service.key_id
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

@payments_ns.route('/verify')
class VerifyPayment(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """Verify Razorpay signature and confirm registration (Spec 6.4)"""
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
            db.session.commit()
            return {'message': 'Invalid payment signature'}, 400
            
        payment.status = 'paid'
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        
        reg = payment.registration
        reg.status = 'confirmed'
        
        db.session.commit()
        return {'message': 'Payment successful', 'registration_id': reg.id}, 200
