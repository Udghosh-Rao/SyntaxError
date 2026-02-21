"""
Payments Blueprint — Feature 6: Razorpay Payment Gateway
Endpoints:
  POST /api/payments/create-order  — Create Razorpay order, Registration and Payment records
  POST /api/payments/verify        — Verify HMAC signature, confirm payment + registration
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.event import Event
from ..models.registration import Registration
from ..models.payment import Payment
from ..services.razorpay_service import create_razorpay_order, verify_razorpay_signature
from ..utils.decorators import role_required

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/payments/create-order', methods=['POST'])
@jwt_required()
@role_required('user')
def create_order():
    """
    Feature 6 – Step 1:
    Accept event_id. Create Razorpay order. Create Registration (pending) + Payment (created).
    Return order_id, amount, currency, key_id to frontend.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data or not data.get('event_id'):
        return jsonify({'error': 'event_id is required'}), 400

    event_id = int(data['event_id'])
    event = Event.query.get_or_404(event_id)

    if not event.is_active:
        return jsonify({'error': 'Event is not active'}), 400

    if event.seats_remaining <= 0:
        return jsonify({'error': 'No seats remaining'}), 400

    # Prevent paying for same event twice
    existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing and existing.status == 'confirmed':
        return jsonify({'error': 'Already registered and paid for this event'}), 409

    # Create or reuse pending registration
    if existing and existing.status == 'pending':
        registration = existing
    else:
        registration = Registration(user_id=user_id, event_id=event_id, status='pending')
        db.session.add(registration)
        db.session.flush()

    # Calculate fees
    amount = event.price
    platform_fee_pct = current_app.config.get('PLATFORM_FEE_PERCENT', 0.15)
    platform_fee = round(amount * platform_fee_pct, 2)
    organizer_payout = round(amount - platform_fee, 2)

    # Create Razorpay order
    order = create_razorpay_order(amount_inr=amount)

    # Create Payment record
    payment = Payment(
        registration_id=registration.id,
        razorpay_order_id=order['id'],
        amount=amount,
        platform_fee=platform_fee,
        organizer_payout=organizer_payout,
        status='created',
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'order_id': order['id'],
        'amount': order['amount'],  # in paise
        'currency': order['currency'],
        'key_id': current_app.config.get('RAZORPAY_KEY_ID', ''),
        'registration_id': registration.id,
    }), 200


@payments_bp.route('/payments/verify', methods=['POST'])
@jwt_required()
@role_required('user')
def verify_payment():
    """
    Feature 6 – Step 2:
    Accept razorpay_order_id, razorpay_payment_id, razorpay_signature.
    Verify HMAC-SHA256. On success, update Payment → paid, Registration → confirmed.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
    for f in required:
        if not data.get(f):
            return jsonify({'error': f'{f} is required'}), 400

    order_id = data['razorpay_order_id']
    payment_id = data['razorpay_payment_id']
    signature = data['razorpay_signature']

    # Verify HMAC signature
    if not verify_razorpay_signature(order_id, payment_id, signature):
        return jsonify({'error': 'Invalid payment signature'}), 400

    # Find Payment record
    payment = Payment.query.filter_by(razorpay_order_id=order_id).first()
    if not payment:
        return jsonify({'error': 'Payment record not found'}), 404

    # Update payment
    payment.razorpay_payment_id = payment_id
    payment.razorpay_signature = signature
    payment.status = 'paid'

    # Update registration
    payment.registration.status = 'confirmed'

    db.session.commit()

    return jsonify({
        'message': 'Payment verified. Registration confirmed!',
        'registration_id': payment.registration_id,
        'payment_status': 'paid',
    }), 200
