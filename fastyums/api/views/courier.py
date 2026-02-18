from rest_framework import viewsets
from rest_framework.permissions import (
    IsAdminUser, AllowAny, SAFE_METHODS
)

from courier.models import Delivery
from accounts.models import User
from api.serializers.courier import (
    DeliverySerializer, DeliveryUpdateSerializer,
    DeliveryCreateSerializer
)
from api.permissions import (
    IsCourier, IsOwner, IsAuthenticatedUser
)
from api.filters.courier import DeliveryFilter


class DeliveryViewSet(viewsets.ModelViewSet):
    filter_class = DeliveryFilter
    search_fields = [
        'courier__full_name', 'courier__username', 'user__username'
    ]
    lookup_field = 'delivery_id'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Delivery.objects.all()
        elif user.role == User.Roles.COURIER:
            return Delivery.objects.filter(courier=user)
        elif user.role == User.Roles.CUSTOMER:
            return Delivery.objects.filter(order__user=user)
        elif user.role == User.Roles.VENDOR:
            return Delivery.objects.filter(
                order__items__product__vendor__owner=user
            ).distinct()

        return Delivery.objects.none()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return DeliveryUpdateSerializer
        elif self.action == 'create':
            return DeliveryCreateSerializer
        return DeliverySerializer


    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [AllowAny()]

        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedUser()]

        if self.action in ['update', 'partial_update']:
            return [IsCourier(), IsOwner()]

        if self.action in ['destroy']:
            return [IsAdminUser()]

        return super().get_permissions()
