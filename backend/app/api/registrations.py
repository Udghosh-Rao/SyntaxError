from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.registration import Registration
from app.models.event import Event
from app.utils.decorators import role_required

registrations_ns = Namespace('registrations', description='Registration operations')

@registrations_ns.route('')
class RegistrationCreate(Resource):
    @jwt_required()
    @role_required('user')
    def post(self):
        """Create a new registration (Spec 6.3)"""
        user_id = get_jwt_identity()
        data = request.get_json()
        event_id = data.get('event_id')
        
        event = Event.query.get(event_id)
        if not event or not event.is_active:
            return {'message': 'Event not found or inactive'}, 404
            
        if event.seats_remaining <= 0:
            return {'message': 'Event is sold out'}, 400
            
        existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
        if existing:
            return {'message': 'Already registered'}, 400
            
        role = data.get('role', 'athlete')
        role_details = data.get('role_details', {})

        status = 'confirmed' if event.price == 0 else 'pending'
        reg = Registration(
            user_id=user_id,
            event_id=event_id,
            status=status,
            role=role,
            role_details=role_details
        )
        try:
            db.session.add(reg)
            db.session.commit()
            return {'message': 'Registration created', 'registration_id': reg.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400

@registrations_ns.route('/my')
class MyRegistrations(Resource):
    @jwt_required()
    @role_required('user')
    def get(self):
        """Get authenticated user's registrations (Spec 6.3)"""
        user_id = get_jwt_identity()
        regs = Registration.query.filter_by(user_id=user_id).all()
        return [r.to_dict() for r in regs], 200

@registrations_ns.route('/<int:id>/cancel')
class RegistrationCancel(Resource):
    @jwt_required()
    @role_required('user')
    def put(self, id):
        """Cancel a registration (Spec 6.3)"""
        user_id = get_jwt_identity()
        reg = Registration.query.get(id)
        
        if not reg:
            return {'message': 'Registration not found'}, 404
            
        if reg.user_id != user_id:
            return {'message': 'Forbidden'}, 403
            
        if reg.status == 'cancelled':
            return {'message': 'Already cancelled'}, 400
            
        reg.status = 'cancelled'
        db.session.commit()
        return {'message': 'Registration cancelled', 'registration': reg.to_dict()}, 200
