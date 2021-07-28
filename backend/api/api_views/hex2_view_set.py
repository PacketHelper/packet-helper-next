from rest_framework.response import Response
from rest_framework.views import APIView
from scapy_helper import hexdump

from packet_helper_core import PacketData, PacketDataScapy
from packet_helper_core.utils.utils import decode_hex


class Hex2ViewSet(APIView):
    def get(self, request, format=None, hex_string: str = None):
        url = self.client.get(f"/api/hex/{hex_string}")
        hex_str = hex_string.lower()
        if not Hexes.objects.filter(Hex=hex_str) and not url.data["warning"]:
            newHex = Hexes(Hex=hex_str)
            newHex.save()
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
