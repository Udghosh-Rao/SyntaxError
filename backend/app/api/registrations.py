"""
Registrations Blueprint
Endpoints:
  POST /api/registrations              — Register user for event (user only)
  GET  /api/registrations/my           — Get user's registrations (user only)
  PUT  /api/registrations/:id/cancel   — Cancel a registration (user only)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.registration import Registration
from ..models.event import Event
from ..utils.decorators import role_required

registrations_bp = Blueprint('registrations', __name__)


@registrations_bp.route('/registrations', methods=['POST'])
@jwt_required()
@role_required('user')
def create_registration():
    """Create a registration for the authenticated user. Checks seats & prevents duplicates."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data or not data.get('event_id'):
        return jsonify({'error': 'event_id is required'}), 400

    event_id = int(data['event_id'])
    event = Event.query.get_or_404(event_id)

    if not event.is_active:
        return jsonify({'error': 'Event is not active'}), 400

    # Check seats
    if event.seats_remaining <= 0:
        return jsonify({'error': 'No seats remaining for this event'}), 400

    # Check duplicate registration
    existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing and existing.status != 'cancelled':
        return jsonify({'error': 'You are already registered for this event'}), 409

    # Create new registration (status: pending — confirmed after payment)
    registration = Registration(
        user_id=user_id,
        event_id=event_id,
        status='pending',
    )
    db.session.add(registration)
    db.session.commit()

    return jsonify({
        'message': 'Registration created. Proceed to payment.',
        'registration_id': registration.id,
        'status': registration.status,
    }), 201


@registrations_bp.route('/registrations/my', methods=['GET'])
@jwt_required()
@role_required('user')
def get_my_registrations():
    """Return all registrations for the authenticated user with event and payment details."""
    user_id = int(get_jwt_identity())
    registrations = Registration.query.filter_by(user_id=user_id).all()
    return jsonify([r.to_dict(include_event=True, include_payment=True) for r in registrations]), 200


@registrations_bp.route('/registrations/<int:reg_id>/cancel', methods=['PUT'])
@jwt_required()
@role_required('user')
def cancel_registration(reg_id):
    """Cancel a registration. Only the owning user may cancel."""
    user_id = int(get_jwt_identity())
    reg = Registration.query.get_or_404(reg_id)

    if reg.user_id != user_id:
        return jsonify({'error': 'Forbidden: not your registration'}), 403

    if reg.status == 'cancelled':
        return jsonify({'error': 'Registration already cancelled'}), 400

    reg.status = 'cancelled'
    db.session.commit()

    return jsonify({'message': 'Registration cancelled successfully', 'registration_id': reg_id}), 200
