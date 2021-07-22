from rest_framework import serializers

from .models import Hexes

class HexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hexes
        fields = ('Hex', 'Like', 'Dislike')