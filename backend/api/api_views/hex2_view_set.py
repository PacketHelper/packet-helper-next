from packet_helper_core import PacketData, PacketDataScapy
from packet_helper_core.utils.utils import decode_hex
from rest_framework.response import Response
from rest_framework.views import APIView
from scapy_helper import hexdump


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
