import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


class TestCheckoutView:
    def test_checkout_view_returns_200(self, api_client):
        payload = {"amount": 50.00, "currency": "usd", "order_id": "12345"}
        response = api_client.post(reverse("checkout"), data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_checkout_requires_amount_field(self, api_client):
        payload = {"currency": "usd", "order_id": "12345"}
        response = api_client.post(reverse("checkout"), data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data["errors"]

    def test_checkout_rejects_amount_below_minimum(self, api_client):
        payload = {
            "amount": 0.49,  # Below $0.50 minimum
            "currency": "usd",
            "order_id": "12345",
        }
        response = api_client.post(reverse("checkout"), data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data["errors"]

    def test_checkout_requires_currency_field(self, api_client):
        payload = {"amount": 50.00, "order_id": "12345"}
        response = api_client.post(reverse("checkout"), data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "currency" in response.data["errors"]

    def test_checkout_rejects_invalid_currency(self, api_client):
        payload = {
            "amount": 50.00,
            "currency": "eur",  # Invalid - we only support USD
            "order_id": "12345",
        }
        response = api_client.post(reverse("checkout"), data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "currency" in response.data["errors"]

    def test_checkout_requires_order_id_field(self, api_client):
        payload = {"amount": 50.00, "currency": "usd"}
        response = api_client.post(reverse("checkout"), data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "order_id" in response.data["errors"]
