from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/previews", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/previews")
    video_link = models.URLField()
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
