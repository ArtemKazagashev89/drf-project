# Generated by Django 5.1.6 on 2025-03-11 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0013_course_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="price",
        ),
        migrations.RemoveField(
            model_name="course",
            name="stripe_price_id",
        ),
        migrations.RemoveField(
            model_name="course",
            name="stripe_product_id",
        ),
    ]
