from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.id'), nullable=False)
    razorpay_order_id = db.Column(db.String(100))
    razorpay_payment_id = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    platform_fee = db.Column(db.Float)
    organizer_payout = db.Column(db.Float)
    status = db.Column(db.String(30), default='created')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
