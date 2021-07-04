from rest_framework.test import APIRequestFactory, APITestCase


class TestApi(APITestCase):
    def test_check_api_redirection(self):
        url = self.client.get("/api/hex")
        assert url.status_code == 302, "Request should be redirected"

    def test_check_api_response(self):
        url = self.client.get("/api/hex/00001Cffffff0000000000000800450000340001000040047cc37f0000017f0000014500002000010000402f7cac7f0000017f000001000000000035003500080000")
        assert url.status_code == 200