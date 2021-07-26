import json

from rest_framework.test import APITestCase
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy_helper import to_list, get_hex


class TestApi(APITestCase):
    def test_check_api_redirection(self):
        url = self.client.get("/api/hex")
        assert url.status_code == 302, "Request should be redirected"

    def test_check_api_response(self):
        url = self.client.get(
            "/api/hex/00001Cffffff0000000000000800450000340001000040047cc37f0000017f0000014500002000010000402f7cac7f0000017f000001000000000035003500080000"
        )
        assert url.data["summary"]["length"] == 66, "Decoded packet should be 66B"
        assert (
            len(url.data["structure"]) == 4
        ), "Structure should contain 4 elements (Ether, IP, IP, GRE)"
        assert url.status_code == 200

    def test_create(self):
        packet = Ether() / IP() / TCP()
        url = self.client.post(
            "/api/create",
            data=json.dumps({"json": to_list(packet)}),
            content_type="application/json",
        )

        assert url.status_code == 201, "Endpoint should return 201 Created"
        assert url.data["hex"] == get_hex(packet), (
            f"Endpoint should return hex: " f"{get_hex(packet)}"
        )
