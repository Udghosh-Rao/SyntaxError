from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.services.chatbot_service import ChatbotService
 
chatbot_ns = Namespace('chatbot', description='AI Chatbot')
chatbot_service = ChatbotService()
 
@chatbot_ns.route('')
class Chat(Resource):
    def post(self):
        data        = request.get_json()
        message     = (data.get('message') or '').strip()
        chat_history = data.get('chat_history') or data.get('history', [])
 
        if not message:
            return {'message': 'Query cannot be empty'}, 400
 
        # Build context string with user ID + role so tools know who's asking
        context = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = User.query.get(int(user_id))
                if user:
                    context = f"user_id:{user.id},role:{user.role},name:{user.name}"
        except Exception:
            pass
 
        result = chatbot_service.get_response(
            message,
            context=context,
            chat_history=chat_history,
        )
        return result, 200