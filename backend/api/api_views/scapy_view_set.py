from rest_framework.response import Response
from rest_framework.views import APIView
from scapy.all import *
from scapy_helper import to_list


class ScapyViewSet(APIView):
    def post(self, request, format=None):
        packet = None
        print(request.data)
        for protocol in request.data:
            if packet == None:
                packet = globals()[protocol]()
            else:
                packet /= globals()[protocol]()
        return Response(to_list(packet))
