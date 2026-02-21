"""
Registration model — created each time a user registers for an event.
Enforces unique (user_id, event_id) constraint to prevent double-registration.
"""
from datetime import datetime
from ..extensions import db


class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='pending')  # pending | confirmed | cancelled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Unique constraint: one registration per (user, event)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='uq_user_event_registration'),
    )

    # Relationships
    user = db.relationship('User', back_populates='registrations')
    event = db.relationship('Event', back_populates='registrations')
    payment = db.relationship('Payment', back_populates='registration', uselist=False)

    def to_dict(self, include_event=True, include_payment=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_event and self.event:
            data['event'] = {
                'id': self.event.id,
                'title': self.event.title,
                'sport_category': self.event.sport_category,
                'venue_city': self.event.venue_city,
                'event_date': self.event.event_date.isoformat() if self.event.event_date else None,
                'price': self.event.price,
                'banner_url': self.event.banner_url,
            }
        if include_payment and self.payment:
            data['payment'] = {
                'status': self.payment.status,
                'amount': self.payment.amount,
                'razorpay_payment_id': self.payment.razorpay_payment_id,
            }
        return data

    def __repr__(self):
        return f'<Registration user={self.user_id} event={self.event_id} status={self.status}>'
