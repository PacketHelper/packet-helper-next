from os import getenv

from rest_framework.response import Response
from rest_framework.views import APIView


class InfoViewSet(APIView):
    def get(self, request, format=None):
        ph_version = getenv("PH_VERSION", "v1.0.0:00000000").split(":")
        return Response({"version": ph_version[0], "revision": ph_version[1]})
