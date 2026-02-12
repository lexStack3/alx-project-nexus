import django_filters
from accounts.models import User, Address

from .basefilters import BaseFilter


class UserFilter(django_filters.FilterSet):
    user_id = django_filters.UUIDFilter(field_name='user_id')
    username = django_filters.CharFilter(
        field_name='username', lookup_expr='icontains'
    )
    email = django_filters.CharFilter(
        field_name='email', lookup_expr='icontains'
    )
    role = django_filters.ChoiceFilter(
        field_name='role', choices=User.Roles.choices
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='creatd_at',
        lookup_expr='lte'
    )

    class Meta:
        model = User
        fields = []


class AddressFilter(django_filters.FilterSet):
    address_id = django_filters.UUIDFilter(field_name='address_id')
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    street = django_filters.CharFilter(
        field_name='street',
        lookup_expr='icontains'
    )
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains'
    )
    state = django_filters.CharFilter(
        field_name='state',
        lookup_expr='icontains'
    )
    country = django_filters.CharFilter(
        field_name='country',
        lookup_expr='icontains'
    )
    is_default = django_filters.BooleanFilter(field_name='is_default')
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='creatd_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Address
        fields = []
