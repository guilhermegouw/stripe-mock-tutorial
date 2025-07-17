from decimal import Decimal

from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True, min_value=Decimal(0.50)
    )
    currency = serializers.CharField(max_length=3, required=True)
    order_id = serializers.CharField(max_length=100, required=True)

    def validate_currency(self, value):
        if value.lower() != "usd":
            raise serializers.ValidationError("Only 'usd' currency is supported.")
        return value.lower()  # Normalize to lowercase
