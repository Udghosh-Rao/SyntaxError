"""
Chatbot Blueprint — Feature 7: AI Chatbot (LangChain + RAG)
Endpoint: POST /api/chatbot
"""
from flask import Blueprint, request, jsonify
from ..services.chatbot_service import get_chatbot_response
from ..models.escalation import EscalationTicket
from ..extensions import db

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot():
    """
    Feature 7:
    Accept JSON with `message` field.
    Pass through LangChain RAG pipeline.
    Return response. If escalated, save EscalationTicket and include escalated: true.
    Public endpoint — accessible to all (auth not required per spec).
    """
    data = request.get_json()
    if not data or not data.get('message'):
        return jsonify({'error': 'message is required'}), 400

    user_message = data['message'].strip()
    session_context = data.get('session_context', '')

    result = get_chatbot_response(user_message, session_context)

    response_data = {
        'response': result['answer'],
        'escalated': result['escalated'],
    }

    # If escalated, save ticket
    if result['escalated']:
        ticket = EscalationTicket(
            user_query=user_message,
            session_context=session_context,
            is_resolved=False,
        )
        db.session.add(ticket)
        db.session.commit()
        response_data['ticket_id'] = ticket.id

    return jsonify(response_data), 200
