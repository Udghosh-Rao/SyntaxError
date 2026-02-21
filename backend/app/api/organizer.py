"""
Organizer Blueprint — Features 8–12
Endpoints:
  GET /api/organizer/dashboard         — Feature 8 & 9: Events list with performance labels
  GET /api/organizer/trend/:event_id   — Feature 10: Daily registration trend
  GET /api/organizer/ticket-summary    — Feature 11: Ticket sales summary
  GET /api/organizer/category-insight  — Feature 12: Popular sport category
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
from ..extensions import db
from ..models.event import Event
from ..models.registration import Registration
from ..utils.decorators import role_required

organizer_bp = Blueprint('organizer', __name__)


@organizer_bp.route('/organizer/dashboard', methods=['GET'])
@jwt_required()
@role_required('organizer')
def organizer_dashboard():
    """
    Feature 8 & 9: Return all events owned by this organizer.
    Each event includes: event_id, title, event_date, venue_city, registrations (confirmed count),
    seats_remaining, revenue, fill_rate, performance_label.
    """
    organizer_id = int(get_jwt_identity())
    events = Event.query.filter_by(organizer_id=organizer_id).all()

    result = []
    for event in events:
        result.append({
            'event_id': event.id,
            'title': event.title,
            'sport_category': event.sport_category,
            'event_date': event.event_date.isoformat() if event.event_date else None,
            'venue_city': event.venue_city,
            'capacity': event.capacity,
            'registrations': event.seats_sold,
            'seats_remaining': event.seats_remaining,
            'revenue': event.revenue,
            'fill_rate': event.fill_rate,
            'performance_label': event.performance_label,
            'is_active': event.is_active,
            'price': event.price,
        })

    return jsonify(result), 200


@organizer_bp.route('/organizer/trend/<int:event_id>', methods=['GET'])
@jwt_required()
@role_required('organizer')
def registration_trend(event_id):
    """
    Feature 10: Return daily registration counts for the specified event.
    Only the owning organizer may access this.
    """
    organizer_id = int(get_jwt_identity())
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != organizer_id:
        return jsonify({'error': 'Forbidden: not your event'}), 403

    # Group registrations by date
    rows = (
        db.session.query(
            func.date(Registration.created_at).label('day'),
            func.count(Registration.id).label('count')
        )
        .filter(Registration.event_id == event_id)
        .group_by(func.date(Registration.created_at))
        .order_by(func.date(Registration.created_at))
        .all()
    )

    trend = [{'day': str(row.day), 'count': row.count} for row in rows]
    return jsonify(trend), 200


@organizer_bp.route('/organizer/ticket-summary', methods=['GET'])
@jwt_required()
@role_required('organizer')
def ticket_summary():
    """
    Feature 11: For each event, return tickets sold, capacity, percentage filled, revenue.
    """
    organizer_id = int(get_jwt_identity())
    events = Event.query.filter_by(organizer_id=organizer_id).all()

    result = []
    for event in events:
        sold = event.seats_sold
        pct = round((sold / event.capacity * 100), 1) if event.capacity > 0 else 0
        result.append({
            'event_id': event.id,
            'title': event.title,
            'capacity': event.capacity,
            'seats_sold': sold,
            'percentage_filled': pct,
            'revenue': event.revenue,
        })

    return jsonify(result), 200


@organizer_bp.route('/organizer/category-insight', methods=['GET'])
@jwt_required()
@role_required('organizer')
def category_insight():
    """
    Feature 12: Return sport categories with total registrations for this organizer's events.
    """
    organizer_id = int(get_jwt_identity())

    rows = (
        db.session.query(
            Event.sport_category,
            func.count(Registration.id).label('registration_count')
        )
        .join(Registration, Registration.event_id == Event.id)
        .filter(
            Event.organizer_id == organizer_id,
            Registration.status == 'confirmed'
        )
        .group_by(Event.sport_category)
        .order_by(func.count(Registration.id).desc())
        .all()
    )

    result = [
        {'sport_category': row.sport_category, 'registration_count': row.registration_count}
        for row in rows
    ]
    return jsonify(result), 200
