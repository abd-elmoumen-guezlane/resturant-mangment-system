from rest_framework import viewsets, permissions
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

# ==============================
# ViewSet pour Category
# ==============================
class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les catégories de plats
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Seuls les admins peuvent modifier


# ==============================
# ViewSet pour MenuItem
# ==============================
class MenuItemViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les plats / menu items
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        """
        Admin: peut tout faire
        Client: peut juste voir les plats disponibles
        """
        if self.request.method in ['GET']:
            return [permissions.AllowAny()]  # tout le monde peut voir
        return [permissions.IsAdminUser()]  # modifications réservées aux admins
