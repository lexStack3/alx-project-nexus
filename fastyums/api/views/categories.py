from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied

from categories.models import Category, Product

from api.serializers.categories import CategorySerializer, ProductSerializer
from api.permissions import IsVendor, IsOwner
from api.filters.categories import CategoryFilter, ProductFilter

from api.filters.categories import CategoryFilter, ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    search_fields = ['name']
    lookup_field = 'category_id'

    def get_queryset(self):
        return Category.objects.prefetch_related(
            'products__vendor__owner'
        )

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return [AllowAny()]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['vendor__name', 'name', 'available']
    lookup_field = 'product_id'

    def get_queryset(self):
        return Product.objects.select_related(
            'vendor',
            'vendor__owner',
            'category'
        )

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'vendor'):
            raise PermissionDenied("You do not have a vendor profile.")

        serializer.save(vendor=user.vendor)

    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [AllowAny()]

        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        if self.action == 'create':
            return [IsVendor()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsVendor(), IsOwner()]

        return super().get_permissions()
