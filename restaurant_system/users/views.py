from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Livreur
from .serializers import LivreurSerializer, CustomTokenObtainPairSerializer

# Vue pour afficher le template de registration
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        password = request.POST.get('password')
        
        try:
            livreur = Livreur.objects.create_livreur(
                email=email,
                password=password,
                nom=nom,
                prenom=prenom
            )
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('login-page')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'inscription: {str(e)}')
    
    return render(request, 'authentification/register.html')

# Vue pour afficher le template de login avec JWT
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Stocker les tokens dans la session
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            request.session['user_nom'] = user.nom
            request.session['user_prenom'] = user.prenom
            
            messages.success(request, 'Connexion réussie !')
            return redirect('delivery-profile')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')
    
    return render(request, 'authentification/login.html')

# Vue pour déconnexion
def logout_view(request):
    # Supprimer les tokens de la session
    request.session.flush()
    messages.success(request, 'Déconnexion réussie !')
    return redirect('login-page')

# API Views (pour les API REST si nécessaire)
class LivreurRegisterView(generics.CreateAPIView):
    queryset = Livreur.objects.all()
    serializer_class = LivreurSerializer
    permission_classes = [AllowAny]

class LivreurTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
