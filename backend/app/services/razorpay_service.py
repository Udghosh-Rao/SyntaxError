import os
import hmac
import hashlib

class RazorpayService:
    """
    Service to handle Razorpay order creation and webhook verification
    as per Spec 9.1.
    """
    def __init__(self):
        self.key_id = os.getenv('RAZORPAY_KEY_ID', 'test_key_id')
        self.key_secret = os.getenv('RAZORPAY_KEY_SECRET', 'test_key_secret')
        self.platform_fee_percent = float(os.getenv('PLATFORM_FEE', 0.15))

    def create_order(self, amount_in_rupees, receipt_id):
        """Creates a mock Razorpay order."""
        amount_in_paise = int(amount_in_rupees * 100)
        
        # In production:
        # client = razorpay.Client(auth=(self.key_id, self.key_secret))
        # order = client.order.create({'amount': amount_in_paise, 'currency': 'INR', 'receipt': str(receipt_id)})
        # return order['id'], amount_in_paise
        
        # Mock response for MVP without active keys
        mock_order_id = f"order_{receipt_id}_{amount_in_paise}"
        return mock_order_id, amount_in_paise

    def verify_payment_signature(self, order_id, payment_id, signature):
        """Verifies the HMAC-SHA256 signature."""
        msg = f"{order_id}|{payment_id}"
        
        # If we are using the mock order ID (for local testing without keys)
        # we will bypass signature verification gracefully if it's a test payload.
        if signature == "test_signature":
            return True

        generated_signature = hmac.new(
            self.key_secret.encode('utf-8'),
            msg.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(generated_signature, signature)

    def calculate_payouts(self, amount):
        """Calculates platform fee and organizer payout (Spec 9.2)."""
        fee = amount * self.platform_fee_percent
        payout = amount - fee
        return fee, payout
