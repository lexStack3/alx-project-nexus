from rest_framework import serializers
from vendors.models import Vendor
from accounts.models import User

from api.serializers.accounts import AddressSerializer


class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'email',
        ]


class VendorSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(
        many=True, read_only=True
    )
    owner = VendorUserSerializer(read_only=True)

    class Meta:
        model = Vendor 
        fields = [
            'vendor_id', 'owner', 'name',
            'description', 'addresses'
        ]
