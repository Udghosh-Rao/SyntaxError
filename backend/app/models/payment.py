"""
Payment model — tracks a Razorpay transaction associated with a Registration.
One payment per registration (one-to-one).
"""
from datetime import datetime
from ..extensions import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_id = db.Column(
        db.Integer,
        db.ForeignKey('registrations.id'),
        nullable=False,
        unique=True  # One-to-one with Registration
    )
    razorpay_order_id = db.Column(db.String(100), unique=True, nullable=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)
    razorpay_signature = db.Column(db.String(300), nullable=True)
    amount = db.Column(db.Float, nullable=False)           # Total paid in INR
    platform_fee = db.Column(db.Float, nullable=False)     # 15–20% deduction
    organizer_payout = db.Column(db.Float, nullable=False) # amount - platform_fee
    status = db.Column(db.String(30), nullable=False, default='created')  # created | paid | failed
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    registration = db.relationship('Registration', back_populates='payment')

    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'razorpay_order_id': self.razorpay_order_id,
            'razorpay_payment_id': self.razorpay_payment_id,
            'amount': self.amount,
            'platform_fee': self.platform_fee,
            'organizer_payout': self.organizer_payout,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Payment registration={self.registration_id} status={self.status} amount={self.amount}>'
