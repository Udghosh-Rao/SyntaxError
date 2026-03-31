from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration
from app.models.payment import Payment
from app.models.escalation import EscalationTicket
from app.utils.decorators import role_required
from sqlalchemy import func, extract

admin_ns = Namespace('admin', description='Admin operations')

@admin_ns.route('/dashboard')
class AdminDashboard(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Unified Admin Dashboard metrics (US-07)"""
        total_users = User.query.count()
        total_events = Event.query.count()
        total_reg = Registration.query.filter_by(status='confirmed').count()
        
        revenue_row = db.session.query(func.sum(Event.price)).join(Registration, Registration.event_id == Event.id).filter(Registration.status == 'confirmed').first()
        total_revenue = float(revenue_row[0] or 0)
        
        sport_row = db.session.query(
            Event.sport_category,
            func.count(Registration.id).label('cnt')
        ).join(Registration, Registration.event_id == Event.id)\
         .filter(Registration.status == 'confirmed')\
         .group_by(Event.sport_category)\
         .order_by(func.count(Registration.id).desc()).first()
         
        popular_sport = sport_row.sport_category if sport_row else None
        
        city_rows = db.session.query(
            User.city, func.count(User.id).label('count')
        ).filter(User.city.isnot(None))\
         .group_by(User.city).all()
        city_distribution = [{'city': r.city, 'user_count': r.count} for r in city_rows]

        return {
            'total_users': total_users,
            'total_events': total_events,
            'total_registrations': total_reg,
            'total_revenue': total_revenue,
            'most_popular_sport': popular_sport,
            'city_distribution': city_distribution
        }, 200

@admin_ns.route('/popular-sport')
class PopularSport(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Get most popular sport categories (Spec 6.7 / Feature 14)"""
        rows = db.session.query(
            Event.sport_category,
            func.count(Registration.id).label('cnt')
        ).join(Registration, Registration.event_id == Event.id)\
         .filter(Registration.status == 'confirmed')\
         .group_by(Event.sport_category)\
         .order_by(func.count(Registration.id).desc()).all()

        return [{'sport_category': r.sport_category, 'registration_count': r.cnt} for r in rows], 200

@admin_ns.route('/city-distribution')
class CityDistribution(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Get user distribution by city (Spec 6.7 / Feature 15)"""
        rows = db.session.query(
            User.city, func.count(User.id).label('count')
        ).filter(User.city.isnot(None))\
         .group_by(User.city).all()

        return [{'city': r.city, 'user_count': r.count} for r in rows], 200

@admin_ns.route('/fill-rate')
class EventFillRates(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Get platform-wide event fill rates (Spec 6.7 / Feature 16)"""
        events = Event.query.filter_by(is_active=True).all()
        return [{
            'event_id': e.id,
            'title': e.title,
            'organizer_name': e.organizer.name,
            'capacity': e.capacity,
            'seats_filled': e.seats_sold,
            'seats_remaining': e.seats_remaining,
            'fill_rate': e.fill_rate
        } for e in events], 200

@admin_ns.route('/monthly-trend')
class MonthlyTrend(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Get monthly registration trend (Spec 6.7 / Feature 17)"""
        rows = db.session.query(
            extract('year', Registration.created_at).label('year'),
            extract('month', Registration.created_at).label('month'),
            func.count(Registration.id).label('count')
        ).filter(Registration.status == 'confirmed')\
         .group_by('year', 'month').order_by('year', 'month').all()

        return [{'year': int(r.year), 'month': int(r.month), 'count': r.count} for r in rows], 200

@admin_ns.route('/organizer-performance')
class OrganizerPerformance(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Compare organizer performance (Spec 6.7 / Feature 18)"""
        rows = db.session.query(
            User.id,
            User.name,
            func.count(db.distinct(Event.id)).label('events'),
            func.count(Registration.id).label('registrations'),
            func.sum(Event.price).label('revenue')
        ).join(Event, Event.organizer_id == User.id)\
         .outerjoin(Registration, (Registration.event_id == Event.id) & (Registration.status == 'confirmed'))\
         .filter(User.role == 'organizer')\
         .group_by(User.id, User.name)\
         .order_by(func.count(Registration.id).desc()).all()

        return [{
            'organizer_id': r.id,
            'organizer_name': r.name,
            'total_events': r.events,
            'total_registrations': r.registrations,
            'total_revenue': float(r.revenue or 0)
        } for r in rows], 200

@admin_ns.route('/events')
class AdminEventList(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Get all events (active and inactive) for admin management"""
        events = Event.query.order_by(Event.id.desc()).all()
        return [{
            'id':             e.id,
            'title':          e.title,
            'organizer_id':   e.organizer_id,
            'sport_category': e.sport_category,
            'venue_city':     e.venue_city,
            'venue_address':  e.venue_address,
            'event_date':     e.event_date.isoformat() if e.event_date else None,
            'capacity':       e.capacity,
            'price':          e.price,
            'banner_url':     e.banner_url,
            'description':    e.description,
            'is_active':      e.is_active,
        } for e in events], 200


@admin_ns.route('/escalations')
class EscalationsList(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        """Get list of unresolved escalation tickets."""
        tickets = EscalationTicket.query.filter_by(is_resolved=False).all()
        return [t.to_dict() for t in tickets], 200

@admin_ns.route('/escalations/<int:id>/resolve')
class EscalationResolve(Resource):
    @jwt_required()
    @role_required('admin')
    def put(self, id):
        """Mark an escalation ticket as resolved."""
        ticket = EscalationTicket.query.get(id)
        if not ticket:
            return {'message': 'Ticket not found'}, 404
        ticket.is_resolved = True
        db.session.commit()
        return ticket.to_dict(), 200
