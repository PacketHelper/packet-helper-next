from http.client import OK

from fastapi.testclient import TestClient

from ph.main import app

client = TestClient(app)


def test_version():
    response = client.get("/")
    assert response.status_code == OK
