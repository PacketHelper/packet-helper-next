import json

from rest_framework.test import APITestCase
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy_helper import to_list, get_hex
from backend.api.models import Hexes


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
    
    def test_add_hex(self):
        Hex = "00E01CCCCCC2001F33D9736108004500008000004000401124550A0A01010A0A01040035DB66006C2D2D795681800001000200020000046D61696C0870617472696F747302696E0000010001C00C0005000100002A4B0002C011C0110001000100002A4C00044A358C99C011000200010001438C0006036E7332C011C011000200010001438C0006036E7331C011" 
        url = self.client.get(
            f"/api/hex/{Hex}" 
        )
        assert Hexes.objects.filter(Hex=Hex.lower()), "Hex should be added to database"

    def test_like_hex(self):
        Hex = "00E01CCCCCC2001F33D9736108004500008000004000401124550A0A01010A0A01040035DB66006C2D2D795681800001000200020000046D61696C0870617472696F747302696E0000010001C00C0005000100002A4B0002C011C0110001000100002A4C00044A358C99C011000200010001438C0006036E7332C011C011000200010001438C0006036E7331C011"
        likes = Hexes.objects.get(Hex=Hex.lower()).Likes
        url = self.client.get(
            f"/api/hex/{Hex}/like" 
        )
        assert Hexes.objects.filter(Hex=Hex.lower()), "Hex should be added to database"
        assert Hexes.objects.get(Hex=Hex.lower()).Likes == likes + 1, "Like should be added to hex"
    
    def test_dislike_hex(self):
        Hex = "00E01CCCCCC2001F33D9736108004500008000004000401124550A0A01010A0A01040035DB66006C2D2D795681800001000200020000046D61696C0870617472696F747302696E0000010001C00C0005000100002A4B0002C011C0110001000100002A4C00044A358C99C011000200010001438C0006036E7332C011C011000200010001438C0006036E7331C011"
        dislikes = Hexes.objects.get(Hex=Hex.lower()).Dislikes
        url = self.client.get(
            f"/api/hex/{Hex}/like" 
        )
        assert Hexes.objects.filter(Hex=Hex.lower()), "Hex should be added to database"
        assert Hexes.objects.get(Hex=Hex.lower()).Dislikes == dislikes + 1, "Dislike should be added to hex"
    
    def test_dislike_nonexistent_hex(self):
        Hex = "00000000000000109400120208004500003d000e00000a112f4ac0550102c000000104000ec800297231204405210000000100000000000f4240000f424000000000010902736563726574fa7b791c"
        assert not Hexes.objects.filter(Hex=Hex.lower()), "Tested hex shouldn't be in the database, this one is"
        
        dislikes = Hexes.objects.get(Hex=Hex.lower()).Dislikes
        url = self.client.get(
            f"/api/hex/{Hex}/like" 
        )
        assert Hexes.objects.filter(Hex=Hex.lower()), "Hex should be added to database"
        assert Hexes.objects.get(Hex=Hex.lower()).Dislikes == dislikes + 1, "Dislike should be added to hex"