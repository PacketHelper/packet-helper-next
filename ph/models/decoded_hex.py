from typing import Literal

from pydantic import BaseModel


class HexSummary(BaseModel):
    length: int
    length_unit: Literal["B", "b"]
    hexdump: str


class HexDecodedHexChksumStatus(BaseModel):
    chksum: str
    chksum_calculated: str
    status: bool | None


class HexStructure(BaseModel):
    name: str
    bytes: str
    hex: str
    hex_one: str
    length: int
    length_unit: Literal["B", "b"]
    repr: str
    repr_full: str
    tshark_name: str
    tshark_raw_summary: list[str]
    chksum_status: HexDecodedHexChksumStatus


class DecodedHexResponse(BaseModel):
    hex: str
    summary: HexSummary
    structure: list[HexStructure]
