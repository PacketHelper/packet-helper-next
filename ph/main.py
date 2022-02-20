from os import getenv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from packet_helper_core import PacketData, PacketDataScapy
from packet_helper_core.utils.utils import decode_hex
from scapy_helper import hexdump

from ph.models.info_response import InfoResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


@app.get("/")
def get_root(request: Request, response_class=HTMLResponse):
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
def get_hex(hex_string: str):
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
