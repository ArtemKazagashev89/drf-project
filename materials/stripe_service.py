import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_price(amount):
    """Создает цену в Stripe."""
    price = stripe.Price.create(
        currency='rub',
        unit_amount=int(amount * 100),
        product_data={"name": "Payment"}
    )
    return price


def create_stripe_session(price_id):
    """Создание сессии для оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://127.0.0.1:8000/',
    )
    return session.get("id"), session.get("url")


def retrieve_session(session_id):
    """Получение статуса сессии платежа в Stripe."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session