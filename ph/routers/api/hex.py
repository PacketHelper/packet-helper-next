import pydantic
from fastapi import APIRouter, HTTPException, status
from packet_helper_core import PacketData, PacketDataScapy
from packet_helper_core.utils.utils import decode_hex
from scapy_helper import hexdump

from ph.models.decoded_hex import DecodedHexResponse, HexStructure

api = APIRouter()


@api.get("/hex/{hex_string}", status_code=status.HTTP_200_OK, tags=["api"])
def get_api_hex(hex_string: str) -> DecodedHexResponse:
    def prepare_api_response(hex_string: str) -> list[HexStructure]:
        packet = decode_hex(hex_string)
        packet_data = PacketData(raw=str(packet))
        scapy_data = PacketDataScapy(hex_string, packet_data)

        return scapy_data.structure

    h = " ".join(
        [
            "".join([hex_string[e - 1], hex_string[e]])
            for e, _ in enumerate(hex_string)
            if e % 2
        ]
    )

    try:
        response = DecodedHexResponse(
            hex=hex_string,
            summary={
                "length": len(h.split()),
                "length_unit": "B",
                "hexdump": hexdump(h, dump=True),
            },
            structure=prepare_api_response(hex_string),
        )
    except IndexError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "error": f"Hex <{hex_string}> is incorrect. Is packet length is correct?"
            },
        )
    except pydantic.error_wrappers.ValidationError as ve:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Incorrect response from engine: <{ve}>"},
        )
    return response
