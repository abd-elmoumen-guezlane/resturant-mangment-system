from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('menu/', include('menu_service.urls')),
    path('order/', include('order_service.urls')),
    path('delivery/', include('delivery_service.urls')),
    path('api/', include('api.urls')),
]
