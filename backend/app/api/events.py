from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.extensions import db
from app.models.event import Event
from app.models.user import User
from app.services.recommendation import RecommendationService
from app.utils.decorators import role_required
from datetime import datetime

events_ns = Namespace('events', description='Event operations')

@events_ns.route('')
class EventList(Resource):
    def get(self):
        """Get all events with Feature 1-4 recommendation scoring (Spec 6.2)"""
        user = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = int(get_jwt_identity())
            if user_id:
                user = User.query.get(user_id)
        except Exception:
            pass

        events = RecommendationService.get_recommended(user, limit=50)
        return [e.to_dict() for e in events], 200

    @jwt_required()
    @role_required('organizer', 'admin')
    def post(self):
        """Create a new event (Spec 6.2) — organizers and admins allowed"""
        user_id = int(get_jwt_identity())
        data = request.get_json()
        user = User.query.get(user_id)

        # Admin can assign event to a specific organizer via organizer_id,
        # otherwise the event is assigned to the caller themselves.
        organizer_id = int(data['organizer_id']) if data.get('organizer_id') else user_id

        try:
            event = Event(
                title=data['title'],
                sport_category=data['sport_category'],
                description=data.get('description'),
                venue_city=data.get('venue_city'),
                venue_address=data.get('venue_address'),
                event_date=datetime.fromisoformat(data['event_date'].replace('Z', '+00:00')),
                capacity=int(data['capacity']),
                price=float(data['price']),
                tags=data.get('tags', []),
                banner_url=data.get('banner_url'),
                organizer_id=organizer_id,
                is_active=True
            )
            event.save()  # Computes price_tier and commits
            return event.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400


@events_ns.route('/<int:id>')
class EventDetail(Resource):
    def get(self, id):
        """Get full details of a single event (Spec 6.2)"""
        event = Event.query.get(id)
        if not event or not event.is_active:
            return {'message': 'Event not found'}, 404
        return event.to_dict(), 200

    @jwt_required()
    @role_required('organizer', 'admin')
    def put(self, id):
        """Update an existing event (Spec 6.2) — admin can edit any event"""
        user_id = int(get_jwt_identity())
        event = Event.query.get(id)
        if not event:
            return {'message': 'Event not found'}, 404

        user = User.query.get(user_id)
        # Organizers can only edit their own events; admins can edit any event
        if user.role != 'admin' and event.organizer_id != user_id:
            return {'message': 'Forbidden'}, 403

        data = request.get_json()
        event.title = data.get('title', event.title)
        event.sport_category = data.get('sport_category', event.sport_category)
        event.description = data.get('description', event.description)
        event.venue_city = data.get('venue_city', event.venue_city)
        event.venue_address = data.get('venue_address', event.venue_address)
        if 'event_date' in data:
            event.event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
        event.capacity = int(data.get('capacity', event.capacity))
        event.price = float(data.get('price', event.price))
        event.tags = data.get('tags', event.tags)

        event.save()
        return event.to_dict(), 200

    @jwt_required()
    @role_required('organizer', 'admin')
    def delete(self, id):
        """Soft delete an event by making it inactive (Spec 6.2)"""
        user_id = int(get_jwt_identity())
        event = Event.query.get(id)
        if not event:
            return {'message': 'Event not found'}, 404

        user = User.query.get(user_id)
        if user.role != 'admin' and event.organizer_id != user_id:
            return {'message': 'Forbidden'}, 403

        event.is_active = False
        db.session.commit()
        return {'message': 'Event deleted'}, 200


@events_ns.route('/<int:id>/similar')
class EventSimilar(Resource):
    def get(self, id):
        """Get similar events (Feature 5)"""
        event = Event.query.get(id)
        if not event:
            return {'message': 'Event not found'}, 404

        similar = RecommendationService.get_similar(event, limit=5)
        return [e.to_dict() for e in similar], 200