import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(name=name)
    return product


def create_price(product_id, amount):
    """Создание цены для продукта в Stripe."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency='usd',
    )
    return price


def create_checkout_session(price_id):
    """Создание сессии для оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://your-site.com/success/',
        cancel_url='https://your-site.com/cancel/',
    )
    return session