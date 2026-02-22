import os
from typing import List, Dict, Optional

class SearchService:
    """
    Service for Algolia search integration.
    Handles indexing and searching of events.
    """
    
    def __init__(self):
        # Initialize Algolia client
        self.app_id = os.getenv('ALGOLIA_APP_ID')
        self.api_key = os.getenv('ALGOLIA_API_KEY')
        self.index_name = 'events'
        
        # Placeholder for actual Algolia client initialization
        # from algoliasearch.search_client import SearchClient
        # self.client = SearchClient.create(self.app_id, self.api_key)
        # self.index = self.client.init_index(self.index_name)
    
    def index_event(self, event_id: int, event_data: Dict) -> bool:
        """
        Index an event in Algolia.
        
        Args:
            event_id: Event ID
            event_data: Event data dictionary
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare event data for indexing
            doc = {
                'objectID': str(event_id),
                'title': event_data.get('title'),
                'description': event_data.get('description'),
                'category': event_data.get('category'),
                'location': event_data.get('location'),
                'date': event_data.get('date'),
                'max_participants': event_data.get('max_participants'),
                'current_participants': event_data.get('current_participants', 0),
                'organizer_id': event_data.get('organizer_id')
            }
            
            # In production, save to Algolia
            # self.index.save_object(doc)
            
            return True
        except Exception as e:
            print(f'Error indexing event: {str(e)}')
            return False
    
    def search_events(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search events using Algolia.
        
        Args:
            query: Search query string
            filters: Optional filter criteria (category, location, etc.)
        
        Returns:
            List of matching events
        """
        try:
            # Build search parameters
            search_params = {
                'query': query,
                'hitsPerPage': 20
            }
            
            # Add filters if provided
            if filters:
                filter_conditions = []
                if 'category' in filters:
                    filter_conditions.append(f"category:'{filters['category']}'")
                if 'location' in filters:
                    filter_conditions.append(f"location:'{filters['location']}'")
                if 'min_date' in filters:
                    filter_conditions.append(f"date >= {filters['min_date']}")
                
                if filter_conditions:
                    search_params['filters'] = ' AND '.join(filter_conditions)
            
            # In production, perform actual Algolia search
            # results = self.index.search(query, search_params)
            
            # For MVP, return mock results
            return [
                {
                    'objectID': '1',
                    'title': 'Sample Event',
                    'category': 'Football',
                    'location': 'Stadium A',
                    'date': '2024-12-15'
                }
            ]
        except Exception as e:
            print(f'Error searching events: {str(e)}')
            return []
    
    def delete_event(self, event_id: int) -> bool:
        """
        Remove an event from Algolia index.
        
        Args:
            event_id: Event ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # In production, delete from Algolia
            # self.index.delete_object(str(event_id))
            
            return True
        except Exception as e:
            print(f'Error deleting event: {str(e)}')
            return False
    
    def get_facets(self, facet_name: str) -> List[str]:
        """
        Get available facet values for filtering.
        
        Args:
            facet_name: Name of facet (e.g., 'category', 'location')
        
        Returns:
            List of available facet values
        """
        try:
            # In production, get facets from Algolia
            if facet_name == 'category':
                return ['Football', 'Cricket', 'Tennis', 'Basketball', 'Badminton', 'Running']
            elif facet_name == 'location':
                return ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai']
            
            return []
        except Exception as e:
            print(f'Error getting facets: {str(e)}')
            return []
