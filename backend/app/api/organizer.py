from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User
from app.services.algolia_sync import AlgoliaSyncService
from app.utils.decorators import role_required
from sqlalchemy import func

organizer_ns = Namespace('organizer', description='Organizer dashboard operations')

@organizer_ns.route('/dashboard')
class OrganizerDashboard(Resource):
    @jwt_required()
    @role_required('organizer')
    def get(self):
        """Get event list with KPIs (Spec 6.6 / Feature 8 & 9)"""
        uid = int(get_jwt_identity())
        events = Event.query.filter_by(organizer_id=uid, is_active=True).all()
        
        return [{
            'event_id': e.id,
            'title': e.title,
            'event_date': e.event_date.isoformat(),
            'venue_city': e.venue_city,
            'registrations': e.seats_sold,
            'seats_remaining': e.seats_remaining,
            'capacity': e.capacity,
            'revenue': e.revenue,
            'fill_rate': e.fill_rate,
            'performance_label': e.performance_label,
            'is_featured': e.is_featured
        } for e in events], 200

@organizer_ns.route('/trend/<int:event_id>')
class RegistrationTrend(Resource):
    @jwt_required()
    @role_required('organizer')
    def get(self, event_id):
        """Get daily registration counts for line chart (Spec 6.6 / Feature 10)"""
        uid = int(get_jwt_identity())
        event = Event.query.get(event_id)
        if not event or event.organizer_id != uid:
            return {'message': 'Forbidden or not found'}, 403
            
        rows = db.session.query(
            func.date(Registration.created_at).label('day'),
            func.count(Registration.id).label('count')
        ).filter(
            Registration.event_id == event_id,
            Registration.status == 'confirmed'
        ).group_by(func.date(Registration.created_at)).order_by('day').all()

        return [{'day': str(r.day), 'count': r.count} for r in rows], 200

@organizer_ns.route('/ticket-summary')
class TicketSummary(Resource):
    @jwt_required()
    @role_required('organizer')
    def get(self):
        """Get ticket sales summary across events (Spec 6.6 / Feature 11)"""
        uid = int(get_jwt_identity())
        events = Event.query.filter_by(organizer_id=uid, is_active=True).all()
        
        return [{
            'title': e.title,
            'capacity': e.capacity,
            'seats_sold': e.seats_sold,
            'percentage_filled': e.fill_rate,
            'revenue': e.revenue
        } for e in events], 200

@organizer_ns.route('/category-insight')
class CategoryInsight(Resource):
    @jwt_required()
    @role_required('organizer')
    def get(self):
        """Get registrations grouped by sport category (Spec 6.6 / Feature 12)"""
        uid = int(get_jwt_identity())
        rows = db.session.query(
            Event.sport_category,
            func.count(Registration.id).label('registrations')
        ).join(Registration, Registration.event_id == Event.id)\
         .filter(Event.organizer_id == uid, Registration.status == 'confirmed')\
         .group_by(Event.sport_category).all()

        return [{'category': r.sport_category, 'registrations': r.registrations} for r in rows], 200

@organizer_ns.route('/events/<int:event_id>/feature')
class FeatureEvent(Resource):
    @jwt_required()
    @role_required('founder', 'admin', 'organizer')
    def post(self, event_id):
        """Toggle is_featured for an event (US-09)"""
        uid = int(get_jwt_identity())
        user = User.query.get(uid)
        
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
            
        if user.role not in ['founder', 'admin'] and event.organizer_id != uid:
            return {'message': 'Forbidden'}, 403
            
        event.is_featured = not event.is_featured
        db.session.commit()
        AlgoliaSyncService().index_event(event)
        
        return {
            'message': 'Event feature status toggled', 
            'is_featured': event.is_featured,
            'snapshot_registrations': event.seats_sold
        }, 200
