from http.client import CREATED, OK

from fastapi.testclient import TestClient

from ph.main import app
from ph.models.creator_packets import (
    CreatorPacketsObjectsRequest,
    CreatorPacketsObjectsResponse,
    CreatorPacketsRequest,
    CreatorPacketsResponse,
)

client = TestClient(app)


def test_version():
    response = client.get("/")
    assert response.status_code == OK


def test_post_api_packets__success():
    response = client.post(
        "/api/packets",
        json=CreatorPacketsRequest(packets=["Ether"]).dict(),
    )
    assert response.status_code == CREATED
    json_response = CreatorPacketsResponse(**response.json())
    assert len(json_response.packets) == 1
    assert json_response.packets[0]["Ethernet"]
    assert len(json_response.packets[0]["Ethernet"]) == 3


def test_post_api_packets__negative__packet_not_exists_in_scapy():
    response = client.post(
        "/api/packets", json=CreatorPacketsRequest(packets=["NonExistingPacket"]).dict()
    )
    assert response.status_code == 500
    assert (
        response.json()["detail"]["error"]
        == "Layer is not supported 'NonExistingPacket'"
    )


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
    assert response.status_code == CREATED
    creator_packets_response = CreatorPacketsObjectsResponse.parse_obj(response.json())
    assert (
        creator_packets_response.builtpacket.get("hex", "")
        == "ff ff ff ff ff ff ff ff ff ff ff ff 00 00"
    )
