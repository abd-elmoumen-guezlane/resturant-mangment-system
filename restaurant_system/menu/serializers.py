from rest_framework import serializers
from .models import Category, MenuItem

# Serializer pour les catégories
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Serializer pour les plats / menu items
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # inclut les infos de la catégorie

    class Meta:
        model = MenuItem
        fields = '__all__'
