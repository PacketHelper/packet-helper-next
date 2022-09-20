from fastapi import status
from fastapi.testclient import TestClient

from ph.main import app
from ph.models.decoded_hex import DecodedHexResponse

client = TestClient(app)


class TestHex:
    @staticmethod
    def test_get_packet():
        response = client.get(
            "api/hex/ffffffaaa9ff00000000001208004500003c0001000040047cbb7f0000017f000001450000280001000040067ccd7f0000017f00000100140050000000000000000050022000917c0000"
        )
        assert response.status_code == status.HTTP_200_OK
        assert DecodedHexResponse.parse_obj(
            response.json()
        ), "Response should be parsed to the 'DecodedHexResponse' without problems"
