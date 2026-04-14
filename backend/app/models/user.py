import uuid
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


def generate_referral_code():
    """Generate a unique 8-char uppercase referral code e.g. LS-A3FX92K1"""
    return 'LS-' + uuid.uuid4().hex[:8].upper()


class User(db.Model):
    __tablename__ = 'users'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name              = db.Column(db.String(100), nullable=False)
    email             = db.Column(db.String(150), unique=True, nullable=False)
    password_hash     = db.Column(db.String(256), nullable=False)
    role              = db.Column(db.String(20), default='user')
    city              = db.Column(db.String(100), nullable=True)
    budget_preference = db.Column(db.String(20), default='mid')
    preferred_sports  = db.Column(db.JSON, nullable=True)
    avatar_url        = db.Column(db.String(500), nullable=True)
    created_at        = db.Column(db.DateTime, server_default=db.func.now())

    # ── Referral system ──────────────────────────────────────────────────────
    # Every user gets a unique referral code on creation
    referral_code     = db.Column(db.String(20), unique=True, nullable=True)

    # The user who referred this user (null if no referral was used)
    referred_by_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    referred_by       = db.relationship('User', remote_side=[id], backref='referrals', foreign_keys=[referred_by_id])

    registrations     = db.relationship('Registration', back_populates='user', lazy=True)
    events_organized  = db.relationship('Event', back_populates='organizer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id':                self.id,
            'name':              self.name,
            'email':             self.email,
            'role':              self.role,
            'city':              self.city,
            'budget_preference': self.budget_preference,
            'preferred_sports':  self.preferred_sports or [],
            'avatar_url':        self.avatar_url,
            'referral_code':     self.referral_code,
            'referred_by_id':    self.referred_by_id,
            'referral_count':    len(self.referrals),
            'created_at':        self.created_at.isoformat() if self.created_at else None,
        }