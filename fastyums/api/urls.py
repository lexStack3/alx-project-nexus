from rest_framework_nested import routers
from django.urls import path, include

from .views.accounts import UserViewSet, AddressViewSet
from .views.categories import CategoryViewSet, ProductViewSet
from .views.courier import DeliveryViewSet
from .views.orders import OrderViewSet, OrderItemViewSet
from .views.payments import PaymentViewSet
from .views.vendors import VendorViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='user')
user_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
user_router.register(r'addresses', AddressViewSet, basename='user-address')
user_router.register(r'vendors', VendorViewSet, basename='vendors')

router.register('vendors', VendorViewSet, basename='vendors')
vendor_router = routers.NestedDefaultRouter(router, r'vendors', lookup='vendors')
vendor_router.register(r'addresses', AddressViewSet, basename='vendor-address')

router.register('categories', CategoryViewSet, basename='categories')
category_router = routers.NestedDefaultRouter(
    router, r'categories', lookup='categories'
)
category_router.register(r'products', ProductViewSet, basename='category-product')

router.register('couriers', DeliveryViewSet, basename='couriers')
courier_router = routers.NestedDefaultRouter(
    router, r'couriers', lookup='couriers'
)
courier_router.register(r'orders', OrderViewSet, basename='courier-orders')

router.register('orders', OrderViewSet, basename='orders')
order_router = routers.NestedDefaultRouter(
    router, r'orders', lookup='orders'
)
order_router.register(r'order-items', OrderItemViewSet, basename='order-items')

router.register('products', ProductViewSet, basename='products')
router.register('order-items', OrderItemViewSet, basename='order_items')
router.register('payments', PaymentViewSet, basename='payments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_router.urls)),
    path('', include(vendor_router.urls)),
    path('', include(category_router.urls)),
    path('', include(courier_router.urls)),
    path('', include(order_router.urls)),
]
