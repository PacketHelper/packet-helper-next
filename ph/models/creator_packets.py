from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class CreatorPacketsRequest(BaseModel):
    packets: List[Any]


class CreatorPacketsResponse(BaseModel):
    packets: Optional[List[Dict[str, Any]]]


class CreatorPacketsObjectsRequest(BaseModel):
    packets: List[Dict[str, Any]]


class CreatorPacketsObjectsResponse(BaseModel):
    builtpacket: Dict[str, str]
