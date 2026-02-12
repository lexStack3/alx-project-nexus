from rest_framework import viewsets

from orders.models import Order, OrderItem
from api.permissions import IsAuthenticatedUser
from api.serializers.orders import (
    OrderSerializer, OrderCreateSerializer
)

from api.filters.orders import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    lookup_field = 'order_id'
    filter_class = OrderFilter
    search_fields = ['user.username', 'status']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        if user.role == 'CUS':
            return Order.objects.filter(user=user)

        if user.role == 'VEN':
            return Order.objects.filter(
                items__product__vendor__owner=user
            ).distinct()

        return Order.objects.none()

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [AllowAny()]

        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticatedUser()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticatedUser(), IsOwner()]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, validated_data):
        request = self.context['request']
        items_data = validated_data.pop('items')
        address = validated_data.pop('address_is')

        total_price = 0

        order = Order.objects.create(
            user=request.user,
            address=address.to_dict,
            total_price=0
        )

        for item in items_data:
            product = Product.objects.get(product_id=item['product'])
            quantity = item['quantity']
            price = product.price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price
            )

            total_price += price * quantity

        order.total_price = total_price
        order.save()

        return order
