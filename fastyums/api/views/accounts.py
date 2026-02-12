from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny, IsAdminUser
)

from accounts.models import User, Address
from vendors.models import Vendor
from api.serializers.accounts import (
    UserSerializer,
    AdminUserSerializer,
    AddressSerializer
)
from api.permissions import (
    IsOwner, IsAuthenticatedUser,
    IsVendor, IsCourier
)

from api.filters.accounts import UserFilter, AddressFilter


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'user_id'
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'role']

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return User.objects.all().prefetch_related('addresses')

        return User.objects.filter(
            user_id=user.user_id
        ).prefetch_related('addresses')

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [AllowAny()]

        if self.action == 'create':
            return [AllowAny()]

        if self.action == 'list':
            return [IsOwner()]

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedUser(), IsOwner()]

        return super().get_permissions()


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsVendor | IsOwner | IsCourier | IsAdminUser]
    filterset_class = AddressFilter
    search_fields = ['name', 'street', 'city', 'state', 'country']
    lookup_field = 'address_id'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Address.objects.all()

        # If vendor
        if user.role == User.Roles.VENDOR and hasattr(user, 'vendor'):
            vendor_content_type = ContentType.objects.get_for_model(Vendor)
            return Address.objects.filter(
                content_type=vendor_content_type,
                object_id=user.vendors.pk
            )

        # If customer
        user_content_type = ContentType.objects.get_for_model(User)
        return Address.objects.filter(
            content_type=user_content_type,
            object_id=user.pk
        )

        return Address.objects.none()

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [AllowAny()]

        if self.action in ['create']:
            return [IsAuthenticatedUser()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]

        return super().get_permissions()


    def perform_create(self, serializer):
        user = self.request.user

        if user.role == User.Roles.VENDOR and hasattr(user, 'vendor'):
            owner = user.vendor
        else:
            owner = user

        content_type = ContentType.objects.get_for_model(owner)

        if serializer.validated_data.get('is_default', False):
            Address.objects.filter(
                content_type=content_type,
                object_id=owner.pk,
                is_default=True
            ).update(is_default=False)

        serializer.save(
            content_type=content_type,
            object_id=owner.pk
        )
