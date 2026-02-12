import django_filters


class BaseFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='create_at',
        lookup_expr='lte'
    )
