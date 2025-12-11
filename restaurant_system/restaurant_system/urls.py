from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Import des ViewSets
from delivery.views import DeliveryProfileViewSet, DeliveryViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from menu.views import CategoryViewSet, MenuItemViewSet

# Router DRF
router = routers.DefaultRouter()
router.register(r"delivery-profiles", DeliveryProfileViewSet)
router.register(r"deliveries", DeliveryViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"order-items", OrderItemViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"menu-items", MenuItemViewSet)

# URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # toutes les routes DRF
    path("", include("users.urls")),  # URLs pour users (auth)
    path("", include("delivery.urls")),  # URLs pour les templates de livraison
    path("", include("menu.urls")),  # URLs pour les templates de menu client
]