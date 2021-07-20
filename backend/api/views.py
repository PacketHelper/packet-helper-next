from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from scapy_helper import hexdump
from backend.api.models import Hexes

from packet_helper_core.packet_data import PacketData
from packet_helper_core.packet_data_scapy import PacketDataScapy
from packet_helper_core.utils.utils import decode_hex

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))


def handler404_redirect(request, exception, template_name="404.html"):
    if request.path[:5] == "/hex/":
        return redirect(f"/?redirect={request.path[5:]}")
    return redirect("/")


class Hex2ViewSet(APIView):
    def get(self, request, format=None, hex_string: str = None):
        h = " ".join(
            [
                "".join([hex_string[e - 1], hex_string[e]])
                for e, x in enumerate(hex_string)
                if e % 2
            ]
        )
        return Response(
            {
                "hex": hex_string,
                "summary": {
                    "length": len(h.split()),
                    "length_unit": "B",
                    "hexdump": hexdump(h, dump=True),
                },
                "structure": Hex2ViewSet.prepare_api_response(hex_string),
            }
        )

    @staticmethod
    def prepare_api_response(hex_string, request=None):
        packet = decode_hex(hex_string)
        packet_data = PacketData(raw=str(packet))

        scapy_data = PacketDataScapy(hex_string, packet_data)

        return scapy_data.structure


class InfoViewSet(APIView):
    def get(self, request, format=None):
        with open("VERSION") as version_file:
            version = version_file.read()

        from os import getenv

        revision = getenv("PH_REVISION", "dev")

        return Response({"version": version, "revision": revision})


def add_hex(request, hex_string):
    if not Hexes.objects.filter(hex=hex_string):
        newHex = Hexes(hex=hex_string)
        newHex.save()


def like(request, hex_string):
    hex = Hexes.objects.get(hex=hex_string)
    hex.likes += 1
    hex.save()


def dislike(request, hex_string):
    hex = Hexes.objects.get(hex=hex_string)
    hex.dislikes += 1
    hex.save()
