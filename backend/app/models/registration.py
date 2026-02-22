from app.extensions import db

class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status = db.Column(db.String(30), default='pending')
    role = db.Column(db.String(20), default='athlete')
    role_details = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='uq_user_event_registration'),
    )

    user = db.relationship('User', back_populates='registrations')
    event = db.relationship('Event', back_populates='registrations')
    payment = db.relationship('Payment', back_populates='registration', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'status': self.status,
            'role': self.role,
            'role_details': self.role_details or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'payment': self.payment.to_dict() if self.payment else None,
            'event': self.event.to_dict() if self.event else None
        }
