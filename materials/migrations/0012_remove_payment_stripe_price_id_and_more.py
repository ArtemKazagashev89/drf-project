# Generated by Django 5.1.6 on 2025-03-11 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0011_payment_stripe_price_id_payment_stripe_product_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="stripe_price_id",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="stripe_product_id",
        ),
        migrations.AddField(
            model_name="course",
            name="stripe_price_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="course",
            name="stripe_product_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
