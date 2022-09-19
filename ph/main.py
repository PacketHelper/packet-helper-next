from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from ph.models.info_response import VersionResponse
from ph.routers.api import api

app = FastAPI(
    title="Packet Helper Next",
    description="Packet Helper API helps you to decode hex into packets with description 🚀",
    version="0.1",
    license_info={
        "name": "GPL v2.0",
        "url": "https://github.com/PacketHelper/packet-helper-next/blob/main/LICENSE",
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api, prefix="/api", tags=["api"])

templates = Jinja2Templates(directory="static")


@app.get("/", include_in_schema=False, status_code=status.HTTP_200_OK)
def get_root(request: Request) -> _TemplateResponse:
    """Return Vue single page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hex/{hex_string}", include_in_schema=False, status_code=status.HTTP_200_OK)
def get_hex(request: Request) -> _TemplateResponse:
    """Return specific path for Vue singlepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(
    "/version", status_code=status.HTTP_200_OK, include_in_schema=False, deprecated=True
)
def get_version() -> VersionResponse:
    """Return information about version of the Packethelper"""
    return VersionResponse(packethelper="0.1", framework="fastapi")
