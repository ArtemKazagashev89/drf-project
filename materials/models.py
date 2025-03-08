from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/previews", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=1000)

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/previews", blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE, blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    paid_lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    session_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    is_subscribe = models.BooleanField(default=False, verbose_name="Подписка")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")
