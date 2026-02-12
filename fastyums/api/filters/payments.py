import django_filters
from payments.models import Payment


class PaymentFilter(django_filters.FilterSet):
    payment_id = django_filters.UUIDFilter(field_name='payment_id')
    username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains'
    )
    user_id = django_filters.UUIDFilter(field_name='user__user_id')
    order_id = django_filters.UUIDFilter(field_name='order__order_id')
    tx_ref = django_filters.CharFilter(
        field_name='tx_ref',
        lookup_expr='iexact'
    )
    chapa_transaction_id = django_filters.CharFilter(
        field_name='chapa_transaction_id',
        lookup_expr='iexact'
    )
    created_from = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )

    class Meta:
        model = Payment
        fields = []
