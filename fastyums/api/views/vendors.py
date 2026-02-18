from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from vendors.models import Vendor

from api.serializers.accounts import AddressSerializer
from api.serializers.vendors import VendorSerializer

from api.permissions import IsOwner, IsVendor
from api.filters.vendors import VendorFilter


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.select_related(
        'owner'
    ).prefetch_related('addresses')
    serializer_class = VendorSerializer
    lookup_field = 'vendor_id'
    filter_class = VendorFilter
    search_fields = ['name']

    def get_permissions(self):
        if self.request.user.is_staff:
            return [AllowAny()]

        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        if self.action == 'create':
            return [IsVendor()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsVendor(), IsOwner()]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    @action(detail=True, methods=['post'], url_path='addresses')
    def address(self, request, vendor_id=None):
        vendor = self.get_object()

        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type = ContentType.objects.get_for_model(vendor)

        serializer.save(
            content_type=content_type,
            object_id=vendor.vendor_id
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @address.mapping.get
    def list_address(self, request, vendor_id=None):
        vendor = self.get_object()
        addresses = vendor.addresses.all()

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
