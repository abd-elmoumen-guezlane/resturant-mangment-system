from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

def jwt_required(view_func):
    """Décorateur pour vérifier que l'utilisateur a un JWT valide dans sa session"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.session.get('access_token')
        
        if not access_token:
            messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
            return redirect('login-page')
        
        try:
            # Vérifier que le token est valide
            token = AccessToken(access_token)
            # Si le token est valide, on peut continuer
            return view_func(request, *args, **kwargs)
        except TokenError:
            # Token invalide ou expiré
            messages.error(request, 'Votre session a expiré. Veuillez vous reconnecter.')
            request.session.flush()
            return redirect('login-page')
    
    return wrapper
