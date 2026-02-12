from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from vendors.models import Vendor
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

    def perform_create(self, serialzier):
        serializer.save(owner=self.request.user)
