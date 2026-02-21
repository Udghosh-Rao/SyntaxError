"""
Chatbot Service — Feature 7: LangChain RAG Pipeline
Uses FAISS vector store + OpenAI GPT-4o-mini via LangChain.
The vector store is initialised ONCE at first use and cached in memory.
"""
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Cached vector store (initialised once at startup)
_vector_store = None
_qa_chain = None

# ── FAQ Knowledge Base ──────────────────────────────────────────────────────
FAQ_DOCUMENTS = [
    "How do I register for an event? Navigate to the event detail page and click Register & Pay. Complete the Razorpay checkout to confirm your spot.",
    "What payment methods are accepted? You can pay via credit card, debit card, UPI, mobile wallets, and net banking through Razorpay.",
    "How do I cancel my registration? Go to My Registrations and click Cancel on the event. Refund policies depend on the organizer.",
    "How do I get a refund? Submit a refund request within 48 hours of cancellation. Refunds are processed within 5–7 business days.",
    "Where can I see my registered events? After logging in, go to My Registrations from your profile menu.",
    "How do I contact support? Use this chatbot for instant answers. For unresolved issues, our team will follow up within 24 hours.",
    "Can I register multiple people for one event? Currently each account registers one participant. Create separate accounts for multiple participants.",
    "What happens if an event is cancelled? You will receive a full refund and an email notification.",
    "How do organizers receive payouts? Razorpay processes organizer payouts automatically after the platform fee is deducted.",
    "How do I become an organizer? Select the Organizer role during registration.",
    "What sports events are available? Browse the homepage for football, cricket, tennis, basketball, running, badminton, swimming, and cycling events.",
    "How are events recommended to me? Events are ranked by your preferred sports, your city, your budget preference, and events happening soon.",
    "Is my payment secure? Yes, all payments are processed through Razorpay, a PCI-DSS compliant payment gateway.",
    "How do I create an event as an organizer? Log in as an organizer and go to your dashboard. Use the Create Event tab to fill in event details.",
    "What is the platform fee? The platform retains 15% of each ticket sale. Organizers receive the remaining 85% as payout.",
]

ESCALATION_FALLBACK_MESSAGE = (
    "I'm sorry, I couldn't find a confident answer to your question. "
    "Your query has been escalated to our support team, who will follow up within 24 hours."
)


def _initialize_vector_store():
    """
    Build FAISS vector store from FAQ documents using OpenAI embeddings.
    Called once and result is cached in _vector_store.
    """
    global _vector_store

    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document
    from flask import current_app

    openai_key = current_app.config.get('OPENAI_API_KEY', '')
    if not openai_key:
        logger.warning('OPENAI_API_KEY not set — chatbot will use fallback mode')
        return None

    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    docs = [Document(page_content=faq) for faq in FAQ_DOCUMENTS]
    _vector_store = FAISS.from_documents(docs, embeddings)
    logger.info('FAISS vector store initialised with %d FAQ documents', len(FAQ_DOCUMENTS))
    return _vector_store


def _get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = _initialize_vector_store()
    return _vector_store


def get_chatbot_response(user_message: str, session_context: str = '') -> Dict:
    """
    Main chatbot entry point.
    Runs the LangChain RAG pipeline:
      1. Embed user query
      2. Retrieve top 3 similar FAQ chunks from FAISS
      3. Inject chunks as context into LLM prompt
      4. Generate answer with GPT-4o-mini
    Returns: {'answer': str, 'escalated': bool}
    """
    try:
        vector_store = _get_vector_store()
        if vector_store is None:
            return {'answer': ESCALATION_FALLBACK_MESSAGE, 'escalated': True}

        from langchain_openai import ChatOpenAI
        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        from flask import current_app

        openai_key = current_app.config.get('OPENAI_API_KEY', '')

        # Retrieve top 3 matching FAQ chunks
        retriever = vector_store.as_retriever(search_kwargs={'k': 3})
        docs = retriever.get_relevant_documents(user_message)

        if not docs:
            return {'answer': ESCALATION_FALLBACK_MESSAGE, 'escalated': True}

        # Build context from retrieved docs
        context = '\n\n'.join([d.page_content for d in docs])

        # Prompt template
        prompt_template = """You are a helpful support assistant for a sports event management platform.
Use the following FAQ context to answer the user's question accurately and concisely.
If the answer is not in the context, say you don't know and suggest contacting support.

Context:
{context}

User Question: {question}

Answer:"""

        llm = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.2,
            openai_api_key=openai_key,
        )

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=['context', 'question']
        )

        formatted_prompt = prompt.format(context=context, question=user_message)
        response = llm.invoke(formatted_prompt)
        answer = response.content.strip()

        # Escalate if answer is uncertain
        uncertain_phrases = ["i don't know", "i cannot", "contact support", "not sure", "unclear"]
        escalated = any(phrase in answer.lower() for phrase in uncertain_phrases)

        return {'answer': answer, 'escalated': escalated}

    except Exception as e:
        logger.error(f'Chatbot error: {e}')
        return {'answer': ESCALATION_FALLBACK_MESSAGE, 'escalated': True}
