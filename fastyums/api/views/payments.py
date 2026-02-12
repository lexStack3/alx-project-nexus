from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from payments.models import Payment
from api.serializers.payments import PaymentSerializer
from api.permissions import IsOwner, IsAuthenticatedUser
from api.filters.payments import PaymentFilter


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    lookup_field = 'payment_id'
    filter_class = PaymentFilter
    search_fields = ['user__username', 'tx_ref']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Payment.objects.all()

        if user.role == 'CUS':
            return Payment.objects.filter(user=user)

        if user.role == 'VEN':
            return Payment.objects.filter(
                order__items__product__vendor__owner=user
            ).distinct()

        return Payment.objects.none()

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [AllowAny()]

        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticatedUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()
