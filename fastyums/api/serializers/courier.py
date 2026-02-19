from rest_framework import serializers

from courier.models import Delivery
from accounts.models import User
from orders.models import Order


class OrderReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'phone', 'email'
        ]
        read_only = True


class CourierUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username']
        read_only = True


class OrderCourierSerializer(serializers.ModelSerializer):
    receiver = OrderReceiverSerializer(source='user', read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'address', 'receiver',
            'created_at', 'updated_at'
        ]

class DeliverySerializer(serializers.ModelSerializer):
    courier = CourierUserSerializer(read_only=True)
    order = OrderCourierSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'delivery_id', 'courier', 'order',
            'status', 'estimated_delivery_time', 'delivered_at'
        ]

class DeliveryCreateSerializer(serializers.ModelSerializer):
    courier = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Roles.COURIER)
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.filter(status=Delivery.DeliveryStatus.PENDING)
    )

    class Meta:
        model = Delivery
        fields = ['delivery_id', 'courier', 'order']


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['status', 'estimated_delivery_time', 'delivered_at']
