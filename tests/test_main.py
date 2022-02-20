from http.client import OK

from fastapi.testclient import TestClient

from ph.main import app
from ph.models.packets import CreatorPacketsRequest, CreatorPacketsResponse

client = TestClient(app)


def test_version():
    response = client.get("/")
    assert response.status_code == OK


def test_post_api_packets__success():
    response = client.post(
        "/api/packets",
        json=CreatorPacketsRequest(packets=["Ether"]).dict(),
    )
    assert response.status_code == OK
    json_response = CreatorPacketsResponse(**response.json())
    assert len(json_response.packets) == 1
    assert json_response.packets[0]["Ethernet"]
    assert len(json_response.packets[0]["Ethernet"]) == 3


def test_post_api_packets__negative__packet_not_exists_in_scapy():
    response = client.post(
        "/api/packets", json=CreatorPacketsRequest(packets=["NonExistingPacket"]).dict()
    )
    print(response.json())
    assert response.status_code == 500
    assert (
        response.json()["detail"]["error"]
        == "Layer is not supported 'NonExistingPacket'"
    )
