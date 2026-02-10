from rest_framework import viewsets
from accounts.models import User, Address
from api.serializers.accounts import (
    UserSerializer,
    AddressSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('addresses')
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
