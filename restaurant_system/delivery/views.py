# delivery/views.py
from rest_framework import viewsets
from .models import DeliveryProfile, Delivery
from .serializers import DeliveryProfileSerializer, DeliverySerializer

# DeliveryProfile ViewSet
class DeliveryProfileViewSet(viewsets.ModelViewSet):
    queryset = DeliveryProfile.objects.all()
    serializer_class = DeliveryProfileSerializer

# Delivery ViewSet
class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
