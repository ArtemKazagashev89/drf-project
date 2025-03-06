from rest_framework.serializers import ValidationError


class ValidatorYouTubeLink:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_link = value.get(self.field)
        if video_link and not video_link.startswith("https://www.youtube.com/"):
            raise ValidationError("Ссылки на сторонние ресурсы, кроме youtube.com, недопустимы.")
