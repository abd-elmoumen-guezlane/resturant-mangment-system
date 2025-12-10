from django.contrib import admin
from .models import Order, OrderItem

# Inline pour voir les OrderItem directement dans Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # nombre de lignes vides supplémentaires
    readonly_fields = ('price',)  # prix calculé automatiquement

# Admin pour Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    inlines = [OrderItemInline]