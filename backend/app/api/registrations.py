from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User

registrations_ns = Namespace('registrations', description='Registration operations')

registration_model = registrations_ns.model('Registration', {
    'id': fields.Integer(),
    'user_id': fields.Integer(required=True),
    'event_id': fields.Integer(required=True),
    'registration_date': fields.DateTime(),
    'status': fields.String(enum=['registered', 'cancelled', 'completed'])
})

@registrations_ns.route('')
class RegistrationList(Resource):
    @jwt_required()
    @registrations_ns.response(200, 'Registrations retrieved')
    def get(self):
        """Get user's registrations"""
        user_id = get_jwt_identity()
        registrations = Registration.query.filter_by(user_id=user_id).all()
        return {
            'registrations': [reg.to_dict() for reg in registrations]
        }, 200
    
    @jwt_required()
    @registrations_ns.expect(registration_model)
    @registrations_ns.response(201, 'Registered successfully')
    def post(self):
        """Register for an event"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if user already registered
        existing = Registration.query.filter_by(
            user_id=user_id,
            event_id=data['event_id']
        ).first()
        
        if existing:
            return {'message': 'Already registered for this event'}, 400
        
        # Check if event exists
        event = Event.query.get(data['event_id'])
        if not event:
            return {'message': 'Event not found'}, 404
        
        # Check if event is full
        if event.current_participants >= event.max_participants:
            return {'message': 'Event is full'}, 400
        
        registration = Registration(
            user_id=user_id,
            event_id=data['event_id'],
            status='registered'
        )
        
        try:
            event.current_participants += 1
            db.session.add(registration)
            db.session.commit()
            return {
                'message': 'Registered successfully',
                'registration': registration.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error registering: {str(e)}'}, 400

@registrations_ns.route('/<int:registration_id>')
class RegistrationDetail(Resource):
    @jwt_required()
    @registrations_ns.response(200, 'Registration retrieved')
    def get(self, registration_id):
        """Get registration details"""
        user_id = get_jwt_identity()
        registration = Registration.query.get(registration_id)
        
        if not registration:
            return {'message': 'Registration not found'}, 404
        
        if registration.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        return {'registration': registration.to_dict()}, 200
    
    @jwt_required()
    @registrations_ns.response(200, 'Registration cancelled')
    def delete(self, registration_id):
        """Cancel registration"""
        user_id = get_jwt_identity()
        registration = Registration.query.get(registration_id)
        
        if not registration:
            return {'message': 'Registration not found'}, 404
        
        if registration.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        try:
            event = Event.query.get(registration.event_id)
            if event:
                event.current_participants = max(0, event.current_participants - 1)
            
            db.session.delete(registration)
            db.session.commit()
            return {'message': 'Registration cancelled'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error cancelling registration: {str(e)}'}, 400

@registrations_ns.route('/event/<int:event_id>')
class EventRegistrations(Resource):
    @registrations_ns.response(200, 'Event registrations retrieved')
    def get(self, event_id):
        """Get all registrations for an event"""
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
        
        registrations = Registration.query.filter_by(event_id=event_id).all()
        return {
            'event_id': event_id,
            'registrations': [reg.to_dict() for reg in registrations],
            'total': len(registrations)
        }, 200
