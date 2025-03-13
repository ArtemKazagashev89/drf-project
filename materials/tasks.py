from celery import shared_task
from django.core.mail import send_mail
from materials.models import Subscription, Course


@shared_task
def send_course_update_email(course_id):
    """Отправка уведомлений подписчикам о обновлении курса."""
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        user = subscription.user
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Курс '{course.title}' был обновлен. Проверьте новые материалы!",
            from_email='EMAIL_HOST_USER',
            recipient_list=[user.email]
        )




