"""
Algolia Sync Service
Syncs event records to Algolia index on create/update.
Removes events from Algolia on soft-delete.
"""
from flask import current_app


def _get_client():
    """Get Algolia search client."""
    from algoliasearch.search_client import SearchClient
    app_id = current_app.config.get('ALGOLIA_APP_ID', '')
    api_key = current_app.config.get('ALGOLIA_API_KEY', '')
    if not app_id or not api_key:
        raise ValueError('Algolia credentials not configured')
    return SearchClient.create(app_id, api_key)


def _get_index():
    """Get the Algolia events index."""
    client = _get_client()
    index_name = current_app.config.get('ALGOLIA_INDEX', 'events')
    return client.init_index(index_name)


def sync_event_to_algolia(event):
    """
    Sync an event record to Algolia.
    Called on event create and update.
    Algolia objectID = str(event.id)
    """
    index = _get_index()
    record = {
        'objectID': str(event.id),
        'title': event.title,
        'sport_category': event.sport_category,
        'venue_city': event.venue_city,
        'event_date': event.event_date.isoformat() if event.event_date else None,
        'price': event.price,
        'price_tier': event.price_tier,
        'tags': event.tags or [],
        'banner_url': event.banner_url,
        'is_active': event.is_active,
    }
    index.save_object(record)


def remove_event_from_algolia(event_id: int):
    """
    Remove an event from the Algolia index.
    Called on soft-delete (is_active = False).
    """
    index = _get_index()
    index.delete_object(str(event_id))


def bulk_sync_all_events():
    """Bulk sync all active events to Algolia. Called during deployment seeding."""
    from ..models.event import Event
    from flask import current_app
    events = Event.query.filter_by(is_active=True).all()
    index = _get_index()
    records = []
    for event in events:
        records.append({
            'objectID': str(event.id),
            'title': event.title,
            'sport_category': event.sport_category,
            'venue_city': event.venue_city,
            'event_date': event.event_date.isoformat() if event.event_date else None,
            'price': event.price,
            'price_tier': event.price_tier,
            'tags': event.tags or [],
        })
    index.save_objects(records)
    return len(records)
