from app.models.event import Event
from app.models.registration import Registration
from app.extensions import db
from sqlalchemy import func, case
from datetime import datetime, timedelta


class RecommendationService:
    """
    Priority stack (Features 1-4):
      1. Preferred sports match   (+4)
      2. City match               (+3)
      3. Budget tier match        (+2)
      4. Within next 7 days       (+1)
      5. Fallback: popular (registration count)
    """

    @staticmethod
    def get_recommended(user, limit=20):
        # Always calculate registration count for fallback and tie-breakers (F1, F5)
        reg_count = db.session.query(
            Registration.event_id,
            func.count(Registration.id).label('cnt')
        ).group_by(Registration.event_id).subquery()

        q = Event.query.filter(Event.is_active == True).outerjoin(
            reg_count, Event.id == reg_count.c.event_id
        )

        now = datetime.utcnow()

        if user and (user.preferred_sports or user.city or user.budget_preference):
            sports = user.preferred_sports or []
            city = user.city
            budget = user.budget_preference

            # F1: Preferred sports match (+40)
            sport_score = case((Event.sport_category.in_(sports), 40), else_=0) if sports else 0

            # F2: City match (+30)
            city_score = case((Event.venue_city == city, 30), else_=0) if city else 0

            # F4: Budget match (+20)
            budget_score = case((Event.price_tier == budget, 20), else_=0) if budget else 0

            # F3: Within next 7 days (+10)
            week_end = now + timedelta(days=7)
            date_score = case((db.and_(Event.event_date >= now, Event.event_date <= week_end), 10), else_=0)

            total_score = date_score
            if sports:
                total_score = total_score + sport_score
            if city:
                total_score = total_score + city_score
            if budget:
                total_score = total_score + budget_score

            # Sort by total preference score, then fallback to popularity (cnt), then proximity to current date
            q = q.order_by(
                Event.is_featured.desc(),
                total_score.desc(),
                func.coalesce(reg_count.c.cnt, 0).desc(),
                Event.event_date.asc()
            )
        else:
            # F1 Fallback: New/Anonymous users see popular events ranked by registrations
            q = q.order_by(
                Event.is_featured.desc(),
                func.coalesce(reg_count.c.cnt, 0).desc(),
                Event.event_date.asc()
            )

        return q.limit(limit).all()

    @staticmethod
    def get_similar(event, limit=5):
        """Feature 5 – Same sport + city, ranked by registrations."""
        reg_count = db.session.query(
            Registration.event_id,
            func.count(Registration.id).label('cnt')
        ).group_by(Registration.event_id).subquery()

        return Event.query.filter(
            Event.id != event.id,
            Event.is_active == True,
            Event.sport_category == event.sport_category,
            Event.venue_city == event.venue_city
        ).outerjoin(
            reg_count, Event.id == reg_count.c.event_id
        ).order_by(
            func.coalesce(reg_count.c.cnt, 0).desc()
        ).limit(limit).all()
