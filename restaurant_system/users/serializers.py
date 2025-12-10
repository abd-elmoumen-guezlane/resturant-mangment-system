from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Livreur


class LivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livreur
        fields = ["id", "email", "nom", "prenom", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        # Passer le password explicitement à create_livreur
        livreur = Livreur.objects.create_livreur(
            email=validated_data.pop("email"), password=password, **validated_data
        )
        return livreur


# Serializer JWT personnalisé pour Livreur
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"  # Utiliser email au lieu de username

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter des claims personnalisés
        token["email"] = user.email
        token["nom"] = user.nom
        token["prenom"] = user.prenom
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Ajouter des données utilisateur dans la réponse
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "nom": self.user.nom,
            "prenom": self.user.prenom,
        }
        return data
