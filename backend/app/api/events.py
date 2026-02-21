"""
Events Blueprint
Endpoints:
  GET    /api/events              — List all active events (with recommendation scoring for auth users)
  GET    /api/events/:id          — Get event detail
  GET    /api/events/:id/similar  — Similar events (Feature 5)
  POST   /api/events              — Create event (organizer only)
  PUT    /api/events/:id          — Update event (organizer only, own events)
  DELETE /api/events/:id          — Soft-delete event (organizer only, own events)
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from ..extensions import db
from ..models.event import Event
from ..models.user import User
from ..services.recommendation import score_events
from ..services.algolia_sync import sync_event_to_algolia, remove_event_from_algolia
from ..utils.decorators import role_required

events_bp = Blueprint('events', __name__)


@events_bp.route('/events', methods=['GET'])
def get_events():
    """
    Return all active events.
    If authenticated, apply recommendation scoring (Features 1–4).
    Otherwise, sort by registration count descending.
    """
    events = Event.query.filter_by(is_active=True).all()

    # Try to get JWT identity (optional JWT)
    user = None
    try:
        verify_jwt_in_request(optional=True)
        uid = get_jwt_identity()
        if uid:
            user = User.query.get(int(uid))
    except Exception:
        pass

    if user:
        events = score_events(events, user)
    else:
        events.sort(key=lambda e: e.seats_sold, reverse=True)

    return jsonify([e.to_dict() for e in events]), 200


@events_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Return full details of a single event."""
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict()), 200


@events_bp.route('/events/<int:event_id>/similar', methods=['GET'])
def get_similar_events(event_id):
    """
    Feature 5: Return up to 5 events with the same sport_category and venue_city,
    sorted by confirmed registration count descending, excluding the event itself.
    """
    event = Event.query.get_or_404(event_id)
    similar = (
        Event.query
        .filter(
            Event.id != event_id,
            Event.sport_category == event.sport_category,
            Event.venue_city == event.venue_city,
            Event.is_active == True,
        )
        .all()
    )
    # Sort by seats_sold descending
    similar.sort(key=lambda e: e.seats_sold, reverse=True)
    similar = similar[:5]
    return jsonify([e.to_dict() for e in similar]), 200


@events_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required('organizer')
def create_event():
    """Create a new event. Organizer only. Auto-computes price_tier. Syncs to Algolia."""
    organizer_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required = ['title', 'sport_category', 'event_date', 'capacity', 'price']
    for f in required:
        if data.get(f) is None:
            return jsonify({'error': f'{f} is required'}), 400

    from datetime import datetime
    event = Event(
        title=data['title'],
        sport_category=data['sport_category'],
        description=data.get('description'),
        venue_city=data.get('venue_city'),
        venue_address=data.get('venue_address'),
        event_date=datetime.fromisoformat(data['event_date']),
        capacity=int(data['capacity']),
        price=float(data['price']),
        organizer_id=organizer_id,
        tags=data.get('tags', []),
        banner_url=data.get('banner_url'),
        is_active=True,
    )
    event.assign_price_tier()

    db.session.add(event)
    db.session.commit()

    # Sync to Algolia
    try:
        sync_event_to_algolia(event)
    except Exception as e:
        current_app.logger.warning(f'Algolia sync failed: {e}')

    return jsonify(event.to_dict()), 201


@events_bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
@role_required('organizer')
def update_event(event_id):
    """Update an event. Organizer only, must own the event."""
    organizer_id = int(get_jwt_identity())
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != organizer_id:
        return jsonify({'error': 'Forbidden: you do not own this event'}), 403

    data = request.get_json() or {}
    from datetime import datetime

    if 'title' in data:
        event.title = data['title']
    if 'sport_category' in data:
        event.sport_category = data['sport_category']
    if 'description' in data:
        event.description = data['description']
    if 'venue_city' in data:
        event.venue_city = data['venue_city']
    if 'venue_address' in data:
        event.venue_address = data['venue_address']
    if 'event_date' in data:
        event.event_date = datetime.fromisoformat(data['event_date'])
    if 'capacity' in data:
        event.capacity = int(data['capacity'])
    if 'price' in data:
        event.price = float(data['price'])
        event.assign_price_tier()
    if 'tags' in data:
        event.tags = data['tags']
    if 'banner_url' in data:
        event.banner_url = data['banner_url']

    db.session.commit()

    # Sync to Algolia
    try:
        sync_event_to_algolia(event)
    except Exception as e:
        current_app.logger.warning(f'Algolia sync failed: {e}')

    return jsonify(event.to_dict()), 200


@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
@role_required('organizer')
def delete_event(event_id):
    """Soft-delete (deactivate) an event. Organizer only, must own the event."""
    organizer_id = int(get_jwt_identity())
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != organizer_id:
        return jsonify({'error': 'Forbidden: you do not own this event'}), 403

    event.is_active = False
    db.session.commit()

    # Remove from Algolia
    try:
        remove_event_from_algolia(event.id)
    except Exception as e:
        current_app.logger.warning(f'Algolia delete failed: {e}')

    return jsonify({'message': 'Event deactivated successfully'}), 200
