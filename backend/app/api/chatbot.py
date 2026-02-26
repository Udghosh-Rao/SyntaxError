from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.services.chatbot_service import ChatbotService

chatbot_ns = Namespace('chatbot', description='AI Chatbot operations')
chatbot_service = ChatbotService()

@chatbot_ns.route('')
class Chat(Resource):
    def post(self):
        """Pass query through RAG pipeline, fallback if low confidence (Spec 6.5)"""
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return {'message': 'Query cannot be empty'}, 400
            
        context = None
        try:
            # Optionally extract user ID for context if logged in
            verify_jwt_in_request(optional=True)
            user_id = int(get_jwt_identity())
            if user_id:
                context = f"Internal User ID: {user_id}"
        except Exception:
            pass
            
        result = chatbot_service.get_response(message, context=context)
        return result, 200
