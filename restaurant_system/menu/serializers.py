from rest_framework import serializers
from .models import Category, MenuItem

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# MenuItem Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    # Nested read-only pour affichage
    category = CategorySerializer(read_only=True)
    # Pour création/modification
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'available', 'category', 'category_id']
        read_only_fields = ['id', 'category']
