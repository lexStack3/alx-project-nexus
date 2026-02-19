from rest_framework_nested import routers
from rest_framework import permissions
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views.accounts import UserViewSet, AddressViewSet
from .views.categories import CategoryViewSet, ProductViewSet
from .views.courier import DeliveryViewSet
from .views.orders import OrderViewSet
from .views.payments import PaymentViewSet
from .views.vendors import VendorViewSet

router = routers.DefaultRouter()

router.register('accounts', UserViewSet, basename='account')
user_router = routers.NestedDefaultRouter(router, r'accounts', lookup='account')
user_router.register(r'addresses', AddressViewSet, basename='user-address')
user_router.register(r'vendors', VendorViewSet, basename='vendors')

router.register('vendors', VendorViewSet, basename='vendors')
vendor_router = routers.NestedDefaultRouter(
    router, r'vendors', lookup='vendors'
)
vendor_router.register(r'addresses', AddressViewSet, basename='vendor-address')

router.register('categories', CategoryViewSet, basename='categories')
category_router = routers.NestedDefaultRouter(
    router, r'categories', lookup='categories'
)
category_router.register(
    r'products', ProductViewSet, basename='category-product'
)

router.register('couriers', DeliveryViewSet, basename='couriers')
courier_router = routers.NestedDefaultRouter(
    router, r'couriers', lookup='couriers'
)
courier_router.register(r'orders', OrderViewSet, basename='courier-orders')

router.register('orders', OrderViewSet, basename='orders')
router.register('products', ProductViewSet, basename='products')
router.register('payments', PaymentViewSet, basename='payments')

schema_view = get_schema_view(
    openapi.Info(
        title='FastYums App API',
        default_version='v1',
        description='API documentation for FastYums API',
        terms_of_service='https://www.localhost.com/terms/',
        contact=openapi.Contact(email='alexanderedim80@gmail.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_router.urls)),
    path('', include(vendor_router.urls)),
    path('', include(category_router.urls)),
    path('', include(courier_router.urls)),

    # Swagger Endpoints
    path('swagger.json', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # JWT Auth endpoints
    path('auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token-refresh')
]
