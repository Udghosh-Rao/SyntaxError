import os
from app.extensions import db
from app.models.escalation import EscalationTicket

# In a real app we'd use OpenAI embeddings via LangChain.
# For this MVP, we will use a basic keyword overlap heuristic
# wrapped in a service class to represent the "RAG Pipeline".

FAQ_KNOWLEDGE_BASE = [
    {
        "text": "How do I register for an event? Navigate to the event detail page and click Register & Pay. Complete the Razorpay checkout to confirm your spot.",
        "keywords": ["register", "sign up", "join", "how to register"]
    },
    {
        "text": "What payment methods are accepted? You can pay via credit card, debit card, UPI, mobile wallets, and net banking through Razorpay.",
        "keywords": ["payment", "pay", "methods", "credit card", "upi", "razorpay"]
    },
    {
        "text": "How do I cancel my registration? Go to My Registrations and click Cancel on the event. Refund policies depend on the organizer.",
        "keywords": ["cancel", "unregister", "withdraw"]
    },
    {
        "text": "How do I get a refund? Submit a refund request within 48 hours of cancellation. Refunds are processed within 5-7 business days.",
        "keywords": ["refund", "money back"]
    },
    {
        "text": "Where can I see my registered events? After logging in, go to My Registrations from your profile menu.",
        "keywords": ["registered events", "my registrations", "ticket", "booking"]
    },
    {
        "text": "How do I contact support? Use this chatbot for instant answers. For unresolved issues, our team will follow up within 24 hours.",
        "keywords": ["support", "help", "contact"]
    },
    {
        "text": "Can I register multiple people for one event? Currently each account registers one participant. Create separate accounts for multiple participants.",
        "keywords": ["multiple people", "friends", "team"]
    },
    {
        "text": "What happens if an event is cancelled? You will receive a full refund and an email notification.",
        "keywords": ["event cancelled"]
    },
    {
        "text": "How do organizers receive payouts? Razorpay processes organizer payouts automatically after the platform fee is deducted.",
        "keywords": ["organizer payout", "receive money"]
    },
    {
        "text": "How do I become an organizer? Select the Organizer role during registration.",
        "keywords": ["become organizer", "host event"]
    }
]

class ChatbotService:
    def __init__(self):
        # Placeholder for LangChain / FAISS initialization
        # self.embeddings = OpenAIEmbeddings()
        # self.vectorstore = FAISS.from_texts(...)
        self.kb = FAQ_KNOWLEDGE_BASE

    def _retrieve_context(self, question):
        """Simulate RAG retrieval using keyword overlap."""
        q_lower = question.lower()
        best_match = None
        best_score = 0

        for doc in self.kb:
            score = sum(1 for kw in doc['keywords'] if kw in q_lower)
            if score > best_score:
                best_score = score
                best_match = doc['text']

        return best_match

    def get_response(self, user_message, context=None):
        retrieved_text = self._retrieve_context(user_message)

        if retrieved_text:
            return {
                'response': f"Here is what I found: {retrieved_text}",
                'escalated': False
            }
        else:
            # Fallback path (Spec 10.1, Step 7)
            # Log escalation ticket
            ticket = EscalationTicket(
                user_query=user_message,
                session_context=context
            )
            try:
                db.session.add(ticket)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

            return {
                'response': "I'm not sure about that. I have escalated this query to our human support team, who will get back to you shortly.",
                'escalated': True
            }
