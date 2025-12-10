from django.contrib import admin
from .models import DeliveryProfile, Delivery

# Admin pour DeliveryProfile (Livreurs)
@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'vehicle_type', 'is_available')
    list_filter = ('is_available', 'vehicle_type')
    search_fields = ('user__username', 'phone', 'vehicle_type')

# Admin pour Delivery (Livraisons)
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'delivery_person', 'status', 'created_at')
    list_filter = ('status', 'delivery_person')
    search_fields = ('order__customer_name', 'delivery_person__user__username')
