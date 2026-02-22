from app.extensions import db

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
    price_tier = db.Column(db.String(20), nullable=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.Column(db.JSON, nullable=True)
    banner_url = db.Column(db.String(300), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    registrations = db.relationship('Registration', back_populates='event', lazy=True)
    organizer = db.relationship('User', back_populates='events_organized')

    def save(self):
        if self.price is not None:
            if self.price < 500:
                self.price_tier = 'cheap'
            elif self.price <= 2000:
                self.price_tier = 'mid'
            else:
                self.price_tier = 'premium'
        db.session.add(self)
        db.session.commit()

    @property
    def seats_sold(self):
        return len([r for r in self.registrations if r.status == 'confirmed'])

    @property
    def seats_remaining(self):
        return self.capacity - self.seats_sold

    @property
    def fill_rate(self):
        if self.capacity == 0:
            return 0.0
        return round((self.seats_sold / self.capacity) * 100, 1)

    @property
    def performance_label(self):
        fr = self.fill_rate
        if fr < 30:
            return 'LOW'
        elif fr <= 70:
            return 'MEDIUM'
        else:
            return 'HIGH'

    @property
    def revenue(self):
        return self.seats_sold * self.price

    def to_dict(self):
        return {
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
            'tags': self.tags or [],
            'banner_url': self.banner_url,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'seats_sold': self.seats_sold,
            'seats_remaining': self.seats_remaining,
            'fill_rate': self.fill_rate,
            'performance_label': self.performance_label,
            'revenue': self.revenue,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
