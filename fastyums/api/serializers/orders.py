from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from orders.models import Order, OrderItem
from accounts.models import User, Address
from categories.models import Product

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


class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['address_id', 'items']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_content_type = ContentType.objects.get_for_model(User)

            self.fields['address_id'].queryset = Address.objects.filter(
                content_type=user_content_type,
                object_id=request.user.user_id
            )

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        items_data = validated_data.pop('items')
        address = validated_data.pop('address_id')

        order = Order.objects.create(
            user=user,
            address=address.to_dict,
            total_price=0
        )

        total = 0

        for item in items_data:
            product = Product.objects.get(product_id=item['product'])

            quantity = item['quantity']
            price = product.price
            
            if product.quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}"
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price
            )

            total += price * quantity

        order.total_price += total
        order.save()

        return order
