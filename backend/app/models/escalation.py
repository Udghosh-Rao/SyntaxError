from app.extensions import db

class EscalationTicket(db.Model):
    __tablename__ = 'escalation_tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_query = db.Column(db.Text, nullable=False)
    session_context = db.Column(db.Text, nullable=True)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_query': self.user_query,
            'session_context': self.session_context,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
