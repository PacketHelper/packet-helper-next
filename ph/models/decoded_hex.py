from typing import Any, Dict, Literal

from pydantic import BaseModel


class HexSummary(BaseModel):
    length: int
    length_unit: Literal["B", "b"]
    hexdump: str


class DecodedHex(BaseModel):
    hex: str
    summary: HexSummary
    structure: Dict[str, Any]
