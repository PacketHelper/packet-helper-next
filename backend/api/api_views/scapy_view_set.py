from rest_framework.response import Response
from rest_framework.views import APIView
from scapy_helper import to_list
import importlib


class ScapyViewSet(APIView):
    def post(self, request, format=None):
        imported_all = importlib.import_module("scapy.all")
        packet = None
        for protocol in request.data:
            new_layer = imported_all.__getattribute__(protocol)
            if packet is None:
                packet = new_layer()
                continue
            packet /= new_layer()
        return Response(to_list(packet))
