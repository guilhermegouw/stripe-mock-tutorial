import stripe


class StripePaymentService:
    def create_payment_intent(self, amount, currency, order_id):
        amount_in_cents = int(amount * 100)
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            metadata={"order_id": order_id},
        )
        return {
            "transaction_id": payment_intent.id,
            "status": payment_intent.status,
            "amount": payment_intent.amount,
        }
