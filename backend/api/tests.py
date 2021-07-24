from django.test import TestCase
from backend.api.views import Hex2ViewSet


class TestAPI(TestCase):
    HEX_STRING = (
        "00001Cffffff0000000000000800450000340001000040047cc"
        "37f0000017f0000014500002000010000402f7cac7f0000017f"
        "000001000000000035003500080000ddd"
    )

    def test_prepare_api_response(self):
        assert Hex2ViewSet.prepare_api_response(TestAPI.HEX_STRING, None)
