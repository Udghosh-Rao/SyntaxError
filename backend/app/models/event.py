from app.extensions import db
from sqlalchemy import func

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    sport_category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    venue_city = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_tier = db.Column(db.String(20))  # cheap, mid, premium
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.Column(db.JSON)  # outdoor, team, night
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    registrations = db.relationship('Registration', backref='event', lazy=True)
    organizer = db.relationship('User', foreign keys=[organizer_id])
    
    @property
    def seats_remaining(self):
        sold = len([r for r in self.registrations if r.status == 'confirmed'])
        return self.capacity - sold
    
    @property
    def fill_rate(self):
        sold = self.capacity - self.seats_remaining
        return round(sold / self.capacity * 100, 1)
    
    @property
    def performance_label(self):
        fr = self.fill_rate
        if fr < 30:
            return 'LOW'
        elif fr < 70:
            return 'MEDIUM'
        return 'HIGH'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'sport_category': self.sport_category,
            'venue_city': self.venue_city,
            'event_date': self.event_date.isoformat(),
            'price': self.price,
            'seats_remaining': self.seats_remaining,
            'fill_rate': self.fill_rate
        }
