"""
Razorpay Service — Feature 6
Handles order creation and payment signature verification.
"""
import hmac
import hashlib
from flask import current_app


def _get_razorpay_client():
    """Return a configured Razorpay client instance."""
    import razorpay
    key_id = current_app.config.get('RAZORPAY_KEY_ID', '')
    key_secret = current_app.config.get('RAZORPAY_KEY_SECRET', '')
    if not key_id or not key_secret:
        raise ValueError('Razorpay credentials not configured. Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env')
    return razorpay.Client(auth=(key_id, key_secret))


def create_razorpay_order(amount_inr: float) -> dict:
    """
    Create a Razorpay order.
    amount_inr: price in INR (will be converted to paise = × 100)
    Returns the Razorpay order dict with id, amount, currency.
    """
    client = _get_razorpay_client()
    amount_paise = int(amount_inr * 100)  # Razorpay requires paise (integer)
    order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1,  # Auto-capture upon payment
    })
    return order


def verify_razorpay_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verify HMAC-SHA256 signature from Razorpay webhook/callback.
    The expected signature = HMAC-SHA256(order_id + '|' + payment_id, key_secret)
    Returns True if valid, False otherwise.
    """
    key_secret = current_app.config.get('RAZORPAY_KEY_SECRET', '')
    if not key_secret:
        raise ValueError('RAZORPAY_KEY_SECRET not configured')

    msg = f'{order_id}|{payment_id}'
    expected = hmac.new(
        key_secret.encode('utf-8'),
        msg.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
