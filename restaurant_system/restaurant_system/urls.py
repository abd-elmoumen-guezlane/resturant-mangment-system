from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Import des ViewSets
from delivery.views import DeliveryProfileViewSet, DeliveryViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from menu.views import CategoryViewSet, MenuItemViewSet  # <-- import menu

# Router DRF
router = routers.DefaultRouter()

# Delivery
router.register(r'delivery-profiles', DeliveryProfileViewSet)
router.register(r'deliveries', DeliveryViewSet)

# Orders
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

# Menu
router.register(r'categories', CategoryViewSet)       # CRUD catégories
router.register(r'menu-items', MenuItemViewSet)      # CRUD plats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # <-- toutes les routes DRF
]
