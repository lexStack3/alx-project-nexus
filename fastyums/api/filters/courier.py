import django_filters
from courier.models import Delivery


class DeliveryFilter(django_filters.FilterSet):
    delivery_id = django_filters.UUIDFilter(field_name='delivery_id')
    courier_id = django_filters.UUIDFilter(field_name='courier__user_id')
    order_id = django_filters.UUIDFilter(field_name='order__order_id')
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Delivery.DeliveryStatus.choices
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    delivered_after = django_filters.DateTimeFilter(
        field_name='delivered_at',
        lookup_expr='gte'
    )
    delivered_before = django_filters.DateTimeFilter(
        field_name='delivered_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Delivery
        fields = []
