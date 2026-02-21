"""
Admin Blueprint — Features 13–18 + Escalation Ticket Management
Endpoints:
  GET /api/admin/analytics            — Feature 13: Platform overview stats
  GET /api/admin/popular-sport        — Feature 14: Sport categories ranked
  GET /api/admin/city-distribution    — Feature 15: Users by city
  GET /api/admin/fill-rate            — Feature 16: All events fill rate table
  GET /api/admin/monthly-trend        — Feature 17: 12-month registration trend
  GET /api/admin/organizer-performance — Feature 18: Organizer comparison table
  GET /api/admin/escalations          — Get unresolved chatbot escalation tickets
  PUT /api/admin/escalations/:id/resolve — Resolve a ticket
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ..extensions import db
from ..models.user import User
from ..models.event import Event
from ..models.registration import Registration
from ..models.payment import Payment
from ..models.escalation import EscalationTicket
from ..utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/analytics', methods=['GET'])
@jwt_required()
@role_required('admin')
def platform_analytics():
    """Feature 13: Total users, events, registrations, revenue."""
    total_users = User.query.count()
    total_events = Event.query.filter_by(is_active=True).count()
    total_registrations = Registration.query.filter_by(status='confirmed').count()
    total_revenue = db.session.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).filter(Payment.status == 'paid').scalar()

    return jsonify({
        'total_users': total_users,
        'total_events': total_events,
        'total_registrations': total_registrations,
        'total_revenue': float(total_revenue or 0),
    }), 200


@admin_bp.route('/admin/popular-sport', methods=['GET'])
@jwt_required()
@role_required('admin')
def popular_sport():
    """Feature 14: Sport categories ranked by confirmed registration count."""
    rows = (
        db.session.query(
            Event.sport_category,
            func.count(Registration.id).label('registration_count')
        )
        .join(Registration, Registration.event_id == Event.id)
        .filter(Registration.status == 'confirmed')
        .group_by(Event.sport_category)
        .order_by(func.count(Registration.id).desc())
        .all()
    )
    result = [
        {'sport_category': r.sport_category, 'registration_count': r.registration_count}
        for r in rows
    ]
    return jsonify(result), 200


@admin_bp.route('/admin/city-distribution', methods=['GET'])
@jwt_required()
@role_required('admin')
def city_distribution():
    """Feature 15: User count per city."""
    rows = (
        db.session.query(
            User.city,
            func.count(User.id).label('user_count')
        )
        .filter(User.city.isnot(None))
        .group_by(User.city)
        .order_by(func.count(User.id).desc())
        .all()
    )
    result = [{'city': r.city, 'user_count': r.user_count} for r in rows]
    return jsonify(result), 200


@admin_bp.route('/admin/fill-rate', methods=['GET'])
@jwt_required()
@role_required('admin')
def fill_rate_dashboard():
    """Feature 16: All events with fill rate data."""
    events = Event.query.all()
    result = []
    for event in events:
        result.append({
            'event_id': event.id,
            'title': event.title,
            'organizer_name': event.organizer.name if event.organizer else 'N/A',
            'capacity': event.capacity,
            'seats_filled': event.seats_sold,
            'seats_remaining': event.seats_remaining,
            'fill_rate': event.fill_rate,
            'performance_label': event.performance_label,
            'is_active': event.is_active,
        })
    return jsonify(result), 200


@admin_bp.route('/admin/monthly-trend', methods=['GET'])
@jwt_required()
@role_required('admin')
def monthly_trend():
    """
    Feature 17: Confirmed registrations per calendar month for past 12 months.
    Returns array with month, count, and delta%.
    """
    now = datetime.utcnow()
    months = []
    for i in range(11, -1, -1):
        month_start = (now.replace(day=1) - relativedelta(months=i)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        month_end = (month_start + relativedelta(months=1))
        count = Registration.query.filter(
            Registration.status == 'confirmed',
            Registration.created_at >= month_start,
            Registration.created_at < month_end,
        ).count()
        months.append({'month': month_start.strftime('%Y-%m'), 'count': count})

    # Calculate delta
    result = []
    for i, m in enumerate(months):
        prev = months[i - 1]['count'] if i > 0 else 0
        if prev > 0:
            delta = round(((m['count'] - prev) / prev) * 100, 1)
        else:
            delta = None
        result.append({'month': m['month'], 'count': m['count'], 'delta': delta})

    return jsonify(result), 200


@admin_bp.route('/admin/organizer-performance', methods=['GET'])
@jwt_required()
@role_required('admin')
def organizer_performance():
    """
    Feature 18: Compare all organizers by total events, registrations, revenue.
    """
    organizers = User.query.filter_by(role='organizer').all()
    result = []
    for org in organizers:
        events = org.events_organized.all()
        total_events = len(events)
        total_regs = sum(e.seats_sold for e in events)
        total_revenue = sum(e.revenue for e in events)
        result.append({
            'organizer_id': org.id,
            'organizer_name': org.name,
            'total_events': total_events,
            'total_registrations': total_regs,
            'total_revenue': total_revenue,
        })
    # Sort by total_revenue descending
    result.sort(key=lambda x: x['total_revenue'], reverse=True)
    return jsonify(result), 200


@admin_bp.route('/admin/escalations', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_escalations():
    """Get all unresolved chatbot escalation tickets."""
    tickets = EscalationTicket.query.filter_by(is_resolved=False).order_by(
        EscalationTicket.created_at.desc()
    ).all()
    return jsonify([t.to_dict() for t in tickets]), 200


@admin_bp.route('/admin/escalations/<int:ticket_id>/resolve', methods=['PUT'])
@jwt_required()
@role_required('admin')
def resolve_escalation(ticket_id):
    """Mark an escalation ticket as resolved."""
    ticket = EscalationTicket.query.get_or_404(ticket_id)
    ticket.is_resolved = True
    db.session.commit()
    return jsonify({'message': 'Ticket resolved', 'ticket_id': ticket_id}), 200
