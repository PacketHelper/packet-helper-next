import importlib
from http.client import CREATED
from os import getenv

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
from ph.models.info_response import InfoResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/")
def get_root(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hex/{hex_string}")
def get_hex(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/version")
def get_version():
    return {"packethelper": "0.1", "framework": "fastapi"}


@app.get(
    "/api/info",
    description="Get information about packet helper version and revision",
    response_model=InfoResponse,
)
def get_info():
    ph_version = getenv("PH_VERSION", "v1.0.0:00000000").split(":")
    return {
        "version": ph_version[0],
        "revision": ph_version[1],
    }


@app.get("/api/hex/{hex_string}")
def get_api_hex(hex_string: str):
    def prepare_api_response(hex_string, request=None):
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
    return {
        "hex": hex_string,
        "summary": {
            "length": len(h.split()),
            "length_unit": "B",
            "hexdump": hexdump(h, dump=True),
        },
        "structure": prepare_api_response(hex_string),
    }


@app.post("/api/packets", status_code=CREATED)
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


@app.post("/api/create", status_code=CREATED)
def post_api_create(
    request: CreatorPacketsObjectsRequest,
) -> CreatorPacketsObjectsResponse:
    _hex = scapy_helper_get_hex(from_sh_list(request.packets))
    return CreatorPacketsObjectsResponse(builtpacket={"hex": _hex})
