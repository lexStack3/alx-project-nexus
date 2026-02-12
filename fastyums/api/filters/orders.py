import django_filters
from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    order_id = django_filters.UUIDFilter(field_name='order_id')
    user_id = django_filters.UUIDFilter(field_name='user__user_id')
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Order.Status.choices
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Order
        fields = []
