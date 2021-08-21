from http.client import CREATED

from packet_helper_core.utils.conversion import from_sh_list
from rest_framework.response import Response
from rest_framework.views import APIView
from scapy_helper import get_hex


class CreateViewSet(APIView):
    def post(self, request, format=None):
        return Response({"hex": get_hex(from_sh_list(request.data))}, status=CREATED)
