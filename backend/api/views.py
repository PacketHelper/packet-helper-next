from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
<<<<<<< HEAD
=======
from rest_framework.response import Response
from rest_framework.views import APIView
from scapy_helper import hexdump
from backend.api.models import Hexes

from packet_helper_core.packet_data import PacketData
from packet_helper_core.packet_data_scapy import PacketDataScapy
from packet_helper_core.utils.utils import decode_hex
>>>>>>> Add django db model & add new hexes to it

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))


def handler404_redirect(request, exception, template_name="404.html"):
    if request.path[:5] == "/hex/":
        return redirect(f"/?redirect={request.path[5:]}")
    return redirect("/")
