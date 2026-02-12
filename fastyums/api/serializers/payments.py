import uuid

from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    tx_ref = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'payment_id', 'user', 'order', 'tx_ref', 'amount',
            'status', 'chapa_transaction_id', 'created_at',
            'updated_at'
        ]

    def validate(self, attrs):
        order = attrs.get('order')
        if Payment.objects.filter(order=order).exists():
            raise serializers.ValidationError(
                "A payment for this order already exists."
            )

    def create(self, validated_data):
        user = self.context['request'].user
        order = validated_data['order']

        tx_ref = f"PAY-{uuid.uuid4().hex[:12]}"

        payment = Payment.objects.create(
            user=user,
            order=order,
            tx_ref=tx_ref,
            amount=order.total_price,
            status=Payment.PaymentStatus.PENDING
        )

        return payment
