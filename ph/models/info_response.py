from typing import Optional

from pydantic import BaseModel


class InfoResponse(BaseModel):
    version: str
    revision: Optional[str]


class VersionResponse(BaseModel):
    packethelper: str
    framework: str
