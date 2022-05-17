from typing import Any, Dict, List, Literal

from pydantic import BaseModel


class HexSummary(BaseModel):
    length: int
    length_unit: Literal["B", "b"]
    hexdump: str


class DecodedHex(BaseModel):
    hex: str
    summary: HexSummary
    structure: List[Dict[str, Any]]
