from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'payment_id', 'user', 'order', 'tx_ref', 'amount',
            'status', 'chapa_transaction_id', 'created_at',
            'updated_at'
        ]
