from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.id'), unique=True, nullable=False)
    razorpay_order_id = db.Column(db.String(100), unique=True, nullable=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)
    razorpay_signature = db.Column(db.String(300), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    platform_fee = db.Column(db.Float, nullable=False)
    organizer_payout = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='created')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    registration = db.relationship('Registration', back_populates='payment')

    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'razorpay_order_id': self.razorpay_order_id,
            'amount': self.amount,
            'platform_fee': self.platform_fee,
            'organizer_payout': self.organizer_payout,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
