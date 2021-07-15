import binascii
from typing import List

from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether, GRE
from scapy.packet import Raw, Packet


def scapy_reader(hex_str: str, packet_to_convert: List[str]) -> List[Packet]:
    hex_str = binascii.unhexlify(hex_str)
    if not isinstance(hex_str, bytes):
        raise Exception("ERR:: hex_str must be in bytes!")
    available_packets = {
        "ETH": Ether,
        "IP": IP,
        "IPv6": IPv6,
        "GRE": GRE,
        "TCP": TCP,
        "UDP": UDP,
        "DNS": DNS,
        "Raw": Raw,
    }

    converted_packets = []

    for packet_ in packet_to_convert:
        packet_obj = available_packets.get(packet_, Raw)
        packet_obj = packet_obj(hex_str)
        if not packet_obj.raw_packet_cache:
            return converted_packets
        hex_str = hex_str.replace(packet_obj.raw_packet_cache, b"")

        converted_packets.append(packet_obj)
    # if something left and we cannot decode it, repr it as Raw()
    if len(hex_str):
        converted_packets.append(Raw(hex_str))
    return converted_packets
