from django.contrib import admin
from .models import Category, MenuItem

# Admin pour Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # remplit automatiquement le slug
    search_fields = ('name',)

# Admin pour MenuItem
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('available', 'category')
    search_fields = ('name', 'category__name')
