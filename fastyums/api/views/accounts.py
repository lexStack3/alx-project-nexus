from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
from api.serializers.vendors import VendorSerializer
from api.permissions import (
    IsOwner, IsAuthenticatedUser,
    IsVendor, IsCourier, IsAdminOrVendor
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

    @action(detail=True, methods=['post'], url_path='addresses')
    def address(self, request, user_id=None):
        user = self.get_object()

        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type = ContentType.objects.get_for_model(user)

        serializer.save(
            content_type=content_type,
            object_id=user.user_id
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @address.mapping.get
    def list_addresses(self, request, user_id=None):
        user = self.get_object()
        addresses = user.addresses.all()

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='vendors'
    )
    def list_vendors(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminOrVendor],
        url_path='couriers'
    )
    def list_courier(self, request):
        couriers = User.objects.filter(role=User.Roles.COURIER)
        serializer = UserSerializer(couriers, many=True)
        return Response(serializer.data)


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
