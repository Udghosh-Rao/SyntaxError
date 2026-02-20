from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.payment import Payment
from app.models.registration import Registration
from datetime import datetime
import os

payments_ns = Namespace('payments', description='Payment operations')

payment_model = payments_ns.model('Payment', {
    'id': fields.Integer(),
    'registration_id': fields.Integer(required=True),
    'amount': fields.Float(required=True),
    'payment_method': fields.String(required=True),
    'status': fields.String(enum=['pending', 'completed', 'failed', 'refunded']),
    'transaction_id': fields.String(),
    'payment_date': fields.DateTime()
})

@payments_ns.route('')
class PaymentList(Resource):
    @jwt_required()
    @payments_ns.response(200, 'Payments retrieved')
    def get(self):
        """Get user's payments"""
        user_id = get_jwt_identity()
        
        # Get all registrations for the user
        registrations = Registration.query.filter_by(user_id=user_id).all()
        registration_ids = [reg.id for reg in registrations]
        
        # Get payments for those registrations
        payments = Payment.query.filter(Payment.registration_id.in_(registration_ids)).all()
        
        return {
            'payments': [payment.to_dict() for payment in payments]
        }, 200
    
    @jwt_required()
    @payments_ns.expect(payment_model)
    @payments_ns.response(201, 'Payment initiated')
    def post(self):
        """Initiate a payment"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Verify registration exists and belongs to user
        registration = Registration.query.get(data['registration_id'])
        if not registration or registration.user_id != user_id:
            return {'message': 'Invalid registration'}, 400
        
        # Check if payment already exists
        existing_payment = Payment.query.filter_by(registration_id=data['registration_id']).first()
        if existing_payment:
            return {'message': 'Payment already exists for this registration'}, 400
        
        payment = Payment(
            registration_id=data['registration_id'],
            amount=data['amount'],
            payment_method=data['payment_method'],
            status='pending'
        )
        
        try:
            db.session.add(payment)
            db.session.commit()
            return {
                'message': 'Payment initiated',
                'payment': payment.to_dict(),
                'razorpay_order_id': f"order_{payment.id}"
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating payment: {str(e)}'}, 400

@payments_ns.route('/<int:payment_id>')
class PaymentDetail(Resource):
    @jwt_required()
    @payments_ns.response(200, 'Payment retrieved')
    def get(self, payment_id):
        """Get payment details"""
        user_id = get_jwt_identity()
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return {'message': 'Payment not found'}, 404
        
        # Verify user owns this payment
        registration = Registration.query.get(payment.registration_id)
        if not registration or registration.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        return {'payment': payment.to_dict()}, 200

@payments_ns.route('/verify/<int:payment_id>')
class PaymentVerify(Resource):
    @jwt_required()
    @payments_ns.response(200, 'Payment verified')
    def post(self, payment_id):
        """Verify and complete payment (Razorpay webhook simulation)"""
        user_id = get_jwt_identity()
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return {'message': 'Payment not found'}, 404
        
        # Verify user owns this payment
        registration = Registration.query.get(payment.registration_id)
        if not registration or registration.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        data = request.get_json()
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        
        try:
            # In production, verify signature with Razorpay
            # For MVP, we'll just update status
            payment.status = 'completed'
            payment.transaction_id = razorpay_payment_id
            payment.payment_date = datetime.now()
            
            db.session.commit()
            return {'message': 'Payment verified and completed', 'payment': payment.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error verifying payment: {str(e)}'}, 400

@payments_ns.route('/refund/<int:payment_id>')
class PaymentRefund(Resource):
    @jwt_required()
    @payments_ns.response(200, 'Refund initiated')
    def post(self, payment_id):
        """Initiate refund"""
        user_id = get_jwt_identity()
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return {'message': 'Payment not found'}, 404
        
        # Verify user owns this payment
        registration = Registration.query.get(payment.registration_id)
        if not registration or registration.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        if payment.status != 'completed':
            return {'message': 'Only completed payments can be refunded'}, 400
        
        try:
            payment.status = 'refunded'
            db.session.commit()
            return {'message': 'Refund initiated', 'payment': payment.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error initiating refund: {str(e)}'}, 400
