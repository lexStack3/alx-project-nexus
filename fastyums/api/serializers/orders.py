from rest_framework import serializers

from orders.models import Order, OrderItem
from accounts.models import User


class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'phone'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderItem
        fields = [
            'item_id', 'order', 'product', 'quantity',
            'price_at_purchase'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    user = OrderUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'user', 'address', 'items', 'total_price', 'status'
        ]
