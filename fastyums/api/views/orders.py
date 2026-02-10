from rest_framework import viewsets

from orders.models import Order, OrderItem
from api.serializers.orders import (
    OrderSerializer,
    OrderItemSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
