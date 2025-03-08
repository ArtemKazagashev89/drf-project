from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModer, IsOwner
from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer
from .stripe_service import create_product, create_price, create_checkout_session


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)

        # Создаем продукт в Stripe
        product = create_product(course.title)

        # Создаем цену для этого продукта
        price_amount = 10000  # Укажите цену в копейках
        price = create_price(product.id, price_amount)

        # Сохраняем идентификаторы Stripe в модели Course
        course.stripe_product_id = product.id
        course.stripe_price_id = price.id
        course.save()

        return Response({'message': 'Курс создан и продукт в Stripe создан!'}, status=201)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        else:
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveApiView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item, created = Subscription.objects.get_or_create(user=user, course=course_item)

        if created:
            subs_item.is_subscribe = True
            subs_item.save()
            message = "Подписка добавлена"
        else:
            subs_item.delete()
            message = "Подписка удалена"

        return Response({"message": message})


class CheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # Отладочное сообщение
        print(f"Course ID: {course.id}, Price ID: {course.stripe_price_id}")

        # Убедитесь, что stripe_price_id существует
        if not course.stripe_price_id:
            return Response({"error": "Цена для курса не найдена."}, status=404)

        session = create_checkout_session(course.stripe_price_id)

        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            session_id=session.id
        )

        return Response({"checkout_url": session.url}, status=200)