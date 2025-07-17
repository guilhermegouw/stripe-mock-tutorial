# checkout/test_services.py
from unittest.mock import Mock, patch

import pytest

from checkout.services import StripePaymentService


class TestStripePaymentService:
    def test_create_payment_intent_success(self):
        service = StripePaymentService()

        mock_payment_intent = Mock()
        mock_payment_intent.id = "pi_test_12345"
        mock_payment_intent.status = "succeeded"
        mock_payment_intent.amount = 5000  # $50.00 in cents

        with patch(
            "stripe.PaymentIntent.create", return_value=mock_payment_intent
        ) as mock_create:
            result = service.create_payment_intent(
                amount=50.00, currency="usd", order_id="12345"
            )

            mock_create.assert_called_once_with(
                amount=5000,
                currency="usd",
                metadata={"order_id": "12345"},
            )

            assert result["transaction_id"] == "pi_test_12345"
            assert result["status"] == "succeeded"
            assert result["amount"] == 5000
