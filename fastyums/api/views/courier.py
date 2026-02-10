from rest_framework import viewsets
from courier.models import Delivery
from api.serializers.courier import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
