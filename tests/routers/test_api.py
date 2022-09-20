from fastapi import status
from fastapi.testclient import TestClient

from ph.main import app
from ph.models.creator_packets import (
    CreatorPacketsObjectsRequest,
    CreatorPacketsObjectsResponse,
    CreatorPacketsRequest,
    CreatorPacketsResponse,
)
from ph.models.decoded_hex import DecodedHex

client = TestClient(app)


class TestAPIPackets:
    @staticmethod
    def test_post_api_packets__success():
        response = client.post(
            "/api/packets",
            json=CreatorPacketsRequest(packets=["Ether"]).dict(),
        )
        assert response.status_code == status.HTTP_201_CREATED
        json_response = CreatorPacketsResponse(**response.json())
        assert len(json_response.packets) == 1
        assert json_response.packets[0]["Ethernet"]
        assert len(json_response.packets[0]["Ethernet"]) == 3

    @staticmethod
    def test_post_api_packets__negative__packet_not_exists_in_scapy():
        response = client.post(
            "/api/packets",
            json=CreatorPacketsRequest(packets=["NonExistingPacket"]).dict(),
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert (
            response.json()["detail"]["error"]
            == "Layer is not supported 'NonExistingPacket'"
        )

    @staticmethod
    def test_get_packet():
        response = client.get(
            "api/hex/ffffffaaa9ff00000000001208004500003c0001000040047cbb7f0000017f000001450000280001000040067ccd7f0000017f00000100140050000000000000000050022000917c0000"
        )
        assert response.status_code == status.HTTP_200_OK
        assert DecodedHex.parse_obj(
            response.json()
        ), "Response should be parsed to the 'DecodedHex' without problems"


class TestAPICreate:
    @staticmethod
    def test_post_api__success():
        response = client.post(
            "/api/create",
            json=CreatorPacketsObjectsRequest(
                packets=[
                    {
                        "Ethernet": {
                            "src": "ff:ff:ff:ff:ff:ff",
                            "dst": "ff:ff:ff:ff:ff:ff",
                            "type": 0,
                        }
                    },
                ]
            ).dict(),
        )
        assert response.status_code == status.HTTP_201_CREATED
        creator_packets_response = CreatorPacketsObjectsResponse.parse_obj(
            response.json()
        )
        assert (
            creator_packets_response.builtpacket.get("hex", "")
            == "ff ff ff ff ff ff ff ff ff ff ff ff 00 00"
        )

    @staticmethod
    def test_post_api_create__negative__packet_not_exists_in_scapy():
        response = client.post(
            "/api/create",
            json=CreatorPacketsObjectsRequest(
                packets=[
                    {
                        "NonExistingLayer": {
                            "src": "ff:ff:ff:ff:ff:ff",
                            "dst": "ff:ff:ff:ff:ff:ff",
                            "type": 0,
                        }
                    },
                ]
            ).dict(),
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert (
            response.json()["detail"]["error"]
            == "Layer is not supported 'NonExistingLayer'"
        )
