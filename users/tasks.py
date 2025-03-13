from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


@shared_task
def deactivate_inactive_users():
    """Проверяет пользователей и блокирует тех, кто не заходил более месяца."""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.username} был заблокирован из-за неактивности.")