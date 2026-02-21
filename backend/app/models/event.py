"""
Event model — represents a sports event created by an organizer.
Includes computed properties: seats_sold, seats_remaining, fill_rate, performance_label, revenue.
Price tier is automatically assigned on save.
"""
from datetime import datetime
from flask import current_app
from ..extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    sport_category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    venue_city = db.Column(db.String(100), nullable=True)
    venue_address = db.Column(db.String(300), nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_tier = db.Column(db.String(20), nullable=True)  # cheap | mid | premium (auto-assigned)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.Column(db.JSON, nullable=True)  # e.g. ["outdoor", "team"]
    banner_url = db.Column(db.String(300), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    organizer = db.relationship('User', back_populates='events_organized')
    registrations = db.relationship('Registration', back_populates='event', lazy='dynamic')

    # ── Computed properties (not stored in DB) ──────────────────────────────

    @property
    def seats_sold(self) -> int:
        """Count of confirmed registrations."""
        return self.registrations.filter_by(status='confirmed').count()

    @property
    def seats_remaining(self) -> int:
        return max(0, self.capacity - self.seats_sold)

    @property
    def fill_rate(self) -> float:
        """Fill rate percentage rounded to 1 decimal."""
        if self.capacity == 0:
            return 0.0
        return round((self.seats_sold / self.capacity) * 100, 1)

    @property
    def performance_label(self) -> str:
        """LOW < 30% | MEDIUM 30–70% | HIGH > 70%."""
        rate = self.fill_rate
        if rate < 30:
            return 'LOW'
        elif rate <= 70:
            return 'MEDIUM'
        return 'HIGH'

    @property
    def revenue(self) -> float:
        return round(self.seats_sold * self.price, 2)

    # ── Price tier logic ────────────────────────────────────────────────────

    @staticmethod
    def compute_price_tier(price: float) -> str:
        """
        Assign price_tier based on price.
        Thresholds from config: PRICE_TIER_CHEAP_MAX (default 500) and PRICE_TIER_MID_MAX (default 2000).
        """
        try:
            cheap_max = current_app.config.get('PRICE_TIER_CHEAP_MAX', 500)
            mid_max = current_app.config.get('PRICE_TIER_MID_MAX', 2000)
        except RuntimeError:
            cheap_max, mid_max = 500, 2000

        if price < cheap_max:
            return 'cheap'
        elif price <= mid_max:
            return 'mid'
        return 'premium'

    def assign_price_tier(self):
        """Auto-assign price_tier when saving."""
        self.price_tier = Event.compute_price_tier(self.price)

    def to_dict(self, include_computed=True):
        data = {
            'id': self.id,
            'title': self.title,
            'sport_category': self.sport_category,
            'description': self.description,
            'venue_city': self.venue_city,
            'venue_address': self.venue_address,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'capacity': self.capacity,
            'price': self.price,
            'price_tier': self.price_tier,
            'organizer_id': self.organizer_id,
            'organizer_name': self.organizer.name if self.organizer else None,
            'tags': self.tags or [],
            'banner_url': self.banner_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_computed:
            data.update({
                'seats_sold': self.seats_sold,
                'seats_remaining': self.seats_remaining,
                'fill_rate': self.fill_rate,
                'performance_label': self.performance_label,
                'revenue': self.revenue,
            })
        return data

    def __repr__(self):
        return f'<Event {self.title} [{self.sport_category}]>'
