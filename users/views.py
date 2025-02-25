from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from users.serializers import PaymentSerializer

from .models import Payment


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_set_fields = {
        "payment_date": ["exact", "lt", "gt"],
        "paid_course": ["exact"],
        "paid_lesson": ["exact"],
        "payment_method": ["exact"],
    }
