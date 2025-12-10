# delivery/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib import messages
from users.decorators import jwt_required
from .models import DeliveryProfile, Delivery
from .serializers import DeliveryProfileSerializer, DeliverySerializer
from users.models import Livreur

# API Views (pour les API REST)
class DeliveryProfileViewSet(viewsets.ModelViewSet):
    queryset = DeliveryProfile.objects.all()
    serializer_class = DeliveryProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        profile, created = DeliveryProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            profile = DeliveryProfile.objects.get(user=self.request.user)
            return Delivery.objects.filter(delivery_person=profile)
        except DeliveryProfile.DoesNotExist:
            return Delivery.objects.none()

    def perform_create(self, serializer):
        if 'delivery_person_id' not in serializer.validated_data:
            profile, _ = DeliveryProfile.objects.get_or_create(user=self.request.user)
            serializer.save(delivery_person=profile)
        else:
            serializer.save()

# Vue pour afficher le template du profil
@jwt_required
def profile_view(request):
    user_id = request.session.get('user_id')
    user = Livreur.objects.get(id=user_id)
    profile, created = DeliveryProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.vehicle_type = request.POST.get('vehicle_type')
        profile.is_available = request.POST.get('is_available') == 'on'
        profile.save()
        messages.success(request, 'Profil enregistré avec succès!')
        return redirect('delivery-profile')
    
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'delivery/profile.html', context)

# Vue pour afficher les livraisons
@jwt_required
def deliveries_view(request):
    user_id = request.session.get('user_id')
    user = Livreur.objects.get(id=user_id)
    
    try:
        profile = DeliveryProfile.objects.get(user=user)
        deliveries = Delivery.objects.filter(delivery_person=profile)
    except DeliveryProfile.DoesNotExist:
        deliveries = []
    
    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        new_status = request.POST.get('status')
        try:
            delivery = Delivery.objects.get(id=delivery_id, delivery_person=profile)
            delivery.status = new_status
            delivery.save()
            messages.success(request, 'Statut mis à jour avec succès!')
            return redirect('delivery-list')
        except Delivery.DoesNotExist:
            messages.error(request, 'Livraison non trouvée')
    
    context = {
        'deliveries': deliveries
    }
    return render(request, 'delivery/deliveries.html', context)
