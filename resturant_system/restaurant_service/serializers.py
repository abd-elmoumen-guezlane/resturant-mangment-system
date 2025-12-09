
from rest_framework import serializers
from .models import RestaurantInfo

class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "opening_time",
            "closing_time"
        ]
