import django_filters
from categories.models import Category, Product


class CategoryFilter(django_filters.FilterSet):
    category_id = django_filters.UUIDFilter(field_name='category_id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Category
        fields = []


class ProductFilter(django_filters.FilterSet):
    product_id = django_filters.UUIDFilter(field_name='product_id')
    vendor_name = django_filters.CharFilter(
        field_name='vendor__name', lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__name', lookup_expr='icontains'
    )
    available = django_filters.BooleanFilter(field_name='available')

    class Meta:
        model = Product
        fields = []
