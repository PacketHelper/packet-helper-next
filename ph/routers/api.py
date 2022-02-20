from fastapi import APIRouter, status
import importlib
from os import getenv

from fastapi import HTTPException
from packet_helper_core import PacketData, PacketDataScapy
from packet_helper_core.utils.conversion import from_sh_list
from packet_helper_core.utils.utils import decode_hex
from scapy_helper import get_hex as scapy_helper_get_hex
from scapy_helper import hexdump, to_list

from ph.models.creator_packets import (
    CreatorPacketsObjectsRequest,
    CreatorPacketsObjectsResponse,
    CreatorPacketsRequest,
    CreatorPacketsResponse,
)
from ph.models.decoded_hex import DecodedHex
from ph.models.info_response import InfoResponse


api = APIRouter()


@api.get(
    "/info",
    description="Get information about packet helper version and revision",
    status_code=status.HTTP_200_OK,
    tags=["api"],
)
def get_info() -> InfoResponse:
    ph_version = getenv("PH_VERSION", "v1.0.0:00000000").split(":")
    return InfoResponse(version=ph_version[0], revision=ph_version[1])


@api.get("/hex/{hex_string}", status_code=status.HTTP_200_OK, tags=["api"])
def get_api_hex(hex_string: str) -> DecodedHex:
    def prepare_api_response(hex_string):
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
    response = None
    try:
        response = DecodedHex(
            hex=hex_string,
            summary={
                "length": len(h.split()),
                "length_unit": "B",
                "hexdump": hexdump(h, dump=True),
            },
            structure=prepare_api_response(hex_string),
        )
    except IndexError as ie:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "error": f"Hex <{hex_string}> is incorrect. Is packet length is correct?"
            },
        )

    return response


@api.post("/api/packets", status_code=status.HTTP_201_CREATED, tags=["api"])
def post_api_packets(request: CreatorPacketsRequest) -> CreatorPacketsResponse:
    imported_all = importlib.import_module("scapy.all")
    packet = None
    try:
        for protocol in request.packets:
            new_layer = imported_all.__getattribute__(protocol)
            if packet is None:
                packet = new_layer()
                continue
            packet /= new_layer()
    except AttributeError as error:
        raise HTTPException(
            status_code=500,
            detail={"error": f"Layer is not supported {str(error).split()[-1]}"},
        )

    return CreatorPacketsResponse(packets=to_list(packet))


@api.post("/api/create", status_code=status.HTTP_201_CREATED, tags=["api"])
def post_api_create(
    request: CreatorPacketsObjectsRequest,
) -> CreatorPacketsObjectsResponse:
    _hex = scapy_helper_get_hex(from_sh_list(request.packets))
    return CreatorPacketsObjectsResponse(builtpacket={"hex": _hex})
