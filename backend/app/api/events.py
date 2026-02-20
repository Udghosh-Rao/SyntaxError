from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.event import Event
from datetime import datetime
from sqlalchemy import or_

events_ns = Namespace('events', description='Event operations')

event_model = events_ns.model('Event', {
    'id': fields.Integer(),
    'title': fields.String(required=True),
    'description': fields.String(),
    'date': fields.DateTime(required=True),
    'location': fields.String(required=True),
    'category': fields.String(required=True),
    'max_participants': fields.Integer(),
    'current_participants': fields.Integer(),
    'organizer_id': fields.Integer(),
    'status': fields.String(enum=['upcoming', 'ongoing', 'completed', 'cancelled'])
})

@events_ns.route('')
class EventList(Resource):
    @events_ns.response(200, 'Events retrieved successfully')
    def get(self):
        """Get all events"""
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        query = Event.query
        
        if search:
            query = query.filter(or_(Event.title.ilike(f'%{search}%'), Event.description.ilike(f'%{search}%')))
        
        if category:
            query = query.filter_by(category=category)
        
        events = query.paginate(page=page, per_page=10)
        
        return {
            'events': [event.to_dict() for event in events.items],
            'total': events.total,
            'pages': events.pages,
            'current_page': page
        }, 200
    
    @jwt_required()
    @events_ns.expect(event_model)
    @events_ns.response(201, 'Event created successfully')
    def post(self):
        """Create a new event"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        event = Event(
            title=data['title'],
            description=data.get('description'),
            date=datetime.fromisoformat(data['date']),
            location=data['location'],
            category=data['category'],
            max_participants=data.get('max_participants'),
            organizer_id=user_id
        )
        
        try:
            db.session.add(event)
            db.session.commit()
            return {'message': 'Event created successfully', 'event': event.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating event: {str(e)}'}, 400

@events_ns.route('/<int:event_id>')
class EventDetail(Resource):
    @events_ns.response(200, 'Event retrieved successfully')
    @events_ns.response(404, 'Event not found')
    def get(self, event_id):
        """Get event by ID"""
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
        return {'event': event.to_dict()}, 200
    
    @jwt_required()
    @events_ns.expect(event_model)
    @events_ns.response(200, 'Event updated successfully')
    def put(self, event_id):
        """Update event"""
        user_id = get_jwt_identity()
        event = Event.query.get(event_id)
        
        if not event:
            return {'message': 'Event not found'}, 404
        
        if event.organizer_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        data = request.get_json()
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.location = data.get('location', event.location)
        event.category = data.get('category', event.category)
        event.max_participants = data.get('max_participants', event.max_participants)
        
        try:
            db.session.commit()
            return {'message': 'Event updated successfully', 'event': event.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating event: {str(e)}'}, 400
    
    @jwt_required()
    @events_ns.response(200, 'Event deleted successfully')
    def delete(self, event_id):
        """Delete event"""
        user_id = get_jwt_identity()
        event = Event.query.get(event_id)
        
        if not event:
            return {'message': 'Event not found'}, 404
        
        if event.organizer_id != user_id:
            return {'message': 'Unauthorized'}, 403
        
        try:
            db.session.delete(event)
            db.session.commit()
            return {'message': 'Event deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting event: {str(e)}'}, 400
