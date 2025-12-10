from django.urls import path
from .views import profile_view, deliveries_view

urlpatterns = [
    path('profile/', profile_view, name='delivery-profile'),
    path('deliveries/', deliveries_view, name='delivery-list'),
]
