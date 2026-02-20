from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

chatbot_ns = Namespace('chatbot', description='AI Chatbot operations')

message_model = chatbot_ns.model('Message', {
    'user_message': fields.String(required=True),
    'context': fields.String()
})

response_model = chatbot_ns.model('Response', {
    'bot_message': fields.String(),
    'suggestions': fields.List(fields.String())
})

# Placeholder for LangChain integration
class ChatbotService:
    """Service for AI-powered chatbot using LangChain"""
    
    def __init__(self):
        # In production, initialize with OpenAI or Gemini API
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = 'gpt-3.5-turbo'
    
    def get_response(self, user_message, context=None):
        """
        Get AI response for user message.
        In production, integrate with LangChain + OpenAI/Gemini
        """
        try:
            # Placeholder logic - replace with actual LangChain integration
            if 'event' in user_message.lower():
                return {
                    'bot_message': 'I can help you find and register for events! What type of sports event are you interested in?',
                    'suggestions': ['Browse all events', 'Search by category', 'My registrations']
                }
            elif 'registration' in user_message.lower():
                return {
                    'bot_message': 'You can register for events through our platform. Would you like help finding an event?',
                    'suggestions': ['View my registrations', 'Browse events', 'Cancel registration']
                }
            elif 'payment' in user_message.lower():
                return {
                    'bot_message': 'We accept payments via Razorpay. You can also view your payment history.',
                    'suggestions': ['Payment methods', 'View payments', 'Refund policy']
                }
            else:
                return {
                    'bot_message': 'How can I help you with sports events today?',
                    'suggestions': ['Browse events', 'My account', 'Contact support']
                }
        except Exception as e:
            return {
                'bot_message': 'Sorry, I encountered an error. Please try again.',
                'suggestions': ['Start over', 'Contact support']
            }

# Initialize chatbot service
chatbot_service = ChatbotService()

@chatbot_ns.route('/chat')
class Chat(Resource):
    @jwt_required()
    @chatbot_ns.expect(message_model)
    @chatbot_ns.response(200, 'Response generated')
    def post(self):
        """Get AI chatbot response"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        user_message = data.get('user_message')
        context = data.get('context')
        
        if not user_message:
            return {'message': 'User message is required'}, 400
        
        try:
            response = chatbot_service.get_response(user_message, context)
            return response, 200
        except Exception as e:
            return {'message': f'Error processing message: {str(e)}'}, 500

@chatbot_ns.route('/suggestions')
class Suggestions(Resource):
    @jwt_required()
    @chatbot_ns.response(200, 'Suggestions retrieved')
    def get(self):
        """Get suggested chatbot responses"""
        user_id = get_jwt_identity()
        
        suggestions = {
            'quick_replies': [
                'Help me find an event',
                'Show my registrations',
                'Check payment status',
                'How to cancel registration?',
                'What events are trending?',
                'Contact support'
            ],
            'common_questions': [
                'What sports events are available?',
                'How do I register for an event?',
                'What is the refund policy?',
                'How do I make a payment?',
                'Can I modify my registration?',
                'How do I contact event organizers?'
            ]
        }
        
        return suggestions, 200

@chatbot_ns.route('/faq')
class FAQ(Resource):
    @chatbot_ns.response(200, 'FAQs retrieved')
    def get(self):
        """Get frequently asked questions"""
        faqs = {
            'faqs': [
                {
                    'question': 'How do I search for events?',
                    'answer': 'Use the search bar on the homepage or browse by category to find sports events near you.'
                },
                {
                    'question': 'Can I cancel my registration?',
                    'answer': 'Yes, you can cancel your registration up to 48 hours before the event for a full refund.'
                },
                {
                    'question': 'What payment methods are accepted?',
                    'answer': 'We accept all major credit/debit cards and UPI through Razorpay.'
                },
                {
                    'question': 'How do I contact an event organizer?',
                    'answer': 'You can message event organizers through our platform messaging feature.'
                },
                {
                    'question': 'Is there a platform fee?',
                    'answer': 'A small service fee is added to each registration to maintain our platform.'
                }
            ]
        }
        
        return faqs, 200
