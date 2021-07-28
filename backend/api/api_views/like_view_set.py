from rest_framework.response import Response
from rest_framework.views import APIView
from backend.api.models import Hexes


class LikeViewSet(APIView):
    def get(self, request, hex_string, format=None):
        url = self.client.get(f"/api/hex/{hex_string}")
        hex_str = hex_string.lower()
        if not Hexes.objects.filter(Hex=hex_str) and not url.data["warning"]:
            newHex = Hexes(Hex=hex_str)
            newHex.save()
        hex = Hexes.objects.get(Hex=hex_str)
        hex.Likes += 1
        hex.save()
        return Response(status=200)
