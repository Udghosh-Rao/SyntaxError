"""
Recommendation Service — Features 1–4
Scores events for authenticated users based on:
  +4  sport preference match   (Feature 1)
  +3  city (nearby) match      (Feature 2)
  +2  budget tier match        (Feature 4)
  +1  within next 7 days       (Feature 3)
"""
from datetime import datetime, timedelta
from typing import List


def score_events(events: list, user) -> list:
    """
    Apply recommendation scoring to a list of Event objects for a given User.
    Returns the events sorted by score descending.
    """
    now = datetime.utcnow()
    week_later = now + timedelta(days=7)

    preferred_sports = [s.lower() for s in (user.preferred_sports or [])]
    user_city = (user.city or '').strip().lower()
    budget = (user.budget_preference or 'mid').lower()

    scored = []
    for event in events:
        score = 0

        # Feature 1: Preferred sports match (+4)
        if preferred_sports and event.sport_category.lower() in preferred_sports:
            score += 4

        # Feature 2: Nearby city match (+3)
        if user_city and event.venue_city and event.venue_city.lower() == user_city:
            score += 3

        # Feature 4: Budget tier match (+2)
        if event.price_tier and event.price_tier.lower() == budget:
            score += 2

        # Feature 3: Within next 7 days (+1)
        if event.event_date and now <= event.event_date <= week_later:
            score += 1

        scored.append((score, event))

    # Sort by score descending, then by event_date ascending as tiebreaker
    scored.sort(key=lambda x: (-x[0], x[1].event_date or datetime.max))
    return [event for _, event in scored]


def get_this_week_events(events: list) -> list:
    """Filter events happening within the next 7 days (Feature 3)."""
    now = datetime.utcnow()
    week_later = now + timedelta(days=7)
    return [e for e in events if e.event_date and now <= e.event_date <= week_later]
