"""
User model — represents all three roles: user, organizer, admin.
All roles share a single table, differentiated by the `role` field.
"""
from datetime import datetime
from ..extensions import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # user | organizer | admin
    city = db.Column(db.String(100), nullable=True)
    budget_preference = db.Column(db.String(20), nullable=True, default='mid')  # cheap | mid | premium
    preferred_sports = db.Column(db.JSON, nullable=True)  # e.g. ["football", "tennis"]
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    registrations = db.relationship('Registration', back_populates='user', lazy='dynamic')
    events_organized = db.relationship('Event', back_populates='organizer', lazy='dynamic')

    def set_password(self, plain_text: str):
        """Hash and store password."""
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')

    def check_password(self, plain_text: str) -> bool:
        """Verify password against stored hash."""
        return bcrypt.check_password_hash(self.password_hash, plain_text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'city': self.city,
            'budget_preference': self.budget_preference,
            'preferred_sports': self.preferred_sports or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<User {self.email} [{self.role}]>'
