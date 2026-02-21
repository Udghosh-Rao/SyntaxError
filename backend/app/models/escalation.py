"""
EscalationTicket model — chatbot fallback escalation record.
Created when the AI chatbot cannot answer a user query with sufficient confidence.
Admin can view and resolve these tickets through the Admin Dashboard.
"""
from datetime import datetime
from ..extensions import db


class EscalationTicket(db.Model):
    __tablename__ = 'escalation_tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_query = db.Column(db.Text, nullable=False)           # User's original message
    session_context = db.Column(db.Text, nullable=True)       # Recent conversation history
    is_resolved = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_query': self.user_query,
            'session_context': self.session_context,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<EscalationTicket id={self.id} resolved={self.is_resolved}>'
