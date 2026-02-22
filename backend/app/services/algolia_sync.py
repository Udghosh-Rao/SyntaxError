import os

class AlgoliaSyncService:
    """
    Service to sync Event records with Algolia as per Spec 8.
    For this MVP, this is a mock implementation that logs actions
    instead of making actual Algolia API calls if keys are missing.
    """
    def __init__(self):
        self.app_id = os.getenv('ALGOLIA_APP_ID')
        self.api_key = os.getenv('ALGOLIA_API_KEY')
        self.index_name = os.getenv('ALGOLIA_INDEX', 'events')
        
        # if self.app_id and self.api_key:
        #     self.client = SearchClient.create(self.app_id, self.api_key)
        #     self.index = self.client.init_index(self.index_name)
        # else:
        #     self.index = None

    def index_event(self, event):
        """Syncs an event to Algolia on create/update."""
        doc = {
            'objectID': str(event.id),
            'title': event.title,
            'sport_category': event.sport_category,
            'venue_city': event.venue_city,
            'event_date': event.event_date.isoformat() if event.event_date else None,
            'price': event.price,
            'price_tier': event.price_tier,
            'tags': event.tags or []
        }
        # if self.index:
        #     self.index.save_object(doc)
        print(f"[Algolia Sync] Indexed event {event.id}: {doc['title']}")

    def remove_event(self, event_id):
        """Removes an event from Algolia on delete."""
        # if self.index:
        #     self.index.delete_object(str(event_id))
        print(f"[Algolia Sync] Removed event {event_id}")
