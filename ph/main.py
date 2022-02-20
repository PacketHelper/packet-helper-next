from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ph.models.info_response import VersionResponse

from ph.routers.api import api

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api, prefix="/api", tags=["api"])

templates = Jinja2Templates(directory="static")


@app.get("/")
def get_root(request: Request, status_code=status.HTTP_200_OK) -> HTMLResponse:
    """Return Vue singlepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hex/{hex_string}")
def get_hex(request: Request, status_code=status.HTTP_200_OK) -> HTMLResponse:
    """Return specific path for Vue singlepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/version", status_code=status.HTTP_200_OK)
def get_version() -> VersionResponse:
    """Return information about version of the Packethelper"""
    return VersionResponse(packethelper="0.1", framework="fastapi")
