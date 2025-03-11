import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(amount):
    """Создает цену в Stripe."""
    price = stripe.Price.create(
        currency='rub',
        unit_amount=int(amount * 100),
        product_data={"name": "Оплата курса"}
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
        success_url='https://127.0.0.1:8000/success/',
        cancel_url='https://127.0.0.1:8000/cancel/',
    )
    return session.id, session.url


