from app.extensions import db


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
                           unique=True, nullable=False)
    balance    = db.Column(db.Float, default=0.0, nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())

    user = db.relationship('User', backref=db.backref('wallet', uselist=False))

    def to_dict(self):
        return {
            'user_id':    self.user_id,
            'balance':    round(self.balance, 2),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id   = db.Column(db.Integer, db.ForeignKey('wallets.id', ondelete='CASCADE'),
                            nullable=False)
    amount      = db.Column(db.Float, nullable=False)          # positive = credit, negative = debit
    type        = db.Column(db.String(30), nullable=False)     # 'credit' | 'debit' | 'referral_bonus'
    description = db.Column(db.String(200), nullable=True)
    created_at  = db.Column(db.DateTime, server_default=db.func.now())

    wallet = db.relationship('Wallet', backref=db.backref('transactions', lazy=True))

    def to_dict(self):
        return {
            'id':          self.id,
            'amount':      round(self.amount, 2),
            'type':        self.type,
            'description': self.description,
            'created_at':  self.created_at.isoformat() if self.created_at else None,
        }