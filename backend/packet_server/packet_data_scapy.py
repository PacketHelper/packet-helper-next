from dataclasses import dataclass

from scapy_helper import get_hex, hexdump

from backend.packet_server.packet_data import PacketData
from backend.packet_server.utils.scapy_reader import scapy_reader


@dataclass
class PacketDataScapy:
    raw: str
    packet_data: PacketData

    def __post_init__(self):
        self.header = [x.replace("\r", "") for x in self.packet_data.header]
        self.headers_scapy = scapy_reader(self.raw, self.header)

        self.headers_full = [repr(x) for x in self.headers_scapy]
        self.headers_single = [f"{x.split(' |')[0]}>" for x in self.headers_full]

        self.structure = self.__make_structure()

    def __make_structure(self):
        temp_structure = []

        for e, h in enumerate(self.headers_scapy):
            _dict = {
                "id": e,
                "name": h.name,
                "bytes": str(h),
                "hex": get_hex(h),
                "partial_hexdump": hexdump(h, dump=True),
                "length": len(h.raw_packet_cache),
                "length_unit": "B",
                "repr": f"{repr(h).split(' |')[0]}>",
                "repr_full": repr(h),
            }

            # RAW elements on the end are added to the last package as data!
            try:
                _dict["tshark_name"] = self.packet_data.body2[e][0]
                _dict["tshark_raw_summary"] = self.packet_data.body2[e][1:]
            except IndexError:
                break

            temp_structure.append(_dict)
        return temp_structure