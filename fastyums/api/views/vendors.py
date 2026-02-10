from rest_framework import viewsets
from vendors.models import Vendor
from api.serializers.vendors import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
