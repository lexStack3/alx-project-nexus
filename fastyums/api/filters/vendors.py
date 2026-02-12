import django_filters
from vendors.models import Vendor


class VendorFilter(django_filters.FilterSet):
    vendor_id = django_filters.UUIDFilter(field_name='vendor_id')
    owner_id = django_filters.UUIDFilter(field_name='owner.user_id')
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontain'
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_epxr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Vendor
        fields = []
