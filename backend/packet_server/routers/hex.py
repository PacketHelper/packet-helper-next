# from fastapi import APIRouter
# from fastapi import Request
# from fastapi.templating import Jinja2Templates
# from scapy_helper import hexdump
#
# from packet_server.packet_data import PacketData
# from packet_server.utils.scapy_reader import scapy_reader
# from packet_server.utils.utils import decode_hex, hex_str_operation, better_scapy_summary
#
# templates = Jinja2Templates(directory="templates")
#
# router = APIRouter()
#
#
# @router.get("/hex/{hex_str}")
# def read_hex(request: Request, hex_str: str):
#     packet = decode_hex(hex_str)
#     packet_data = PacketData(raw=str(packet))
#
#     scapy_code = [repr(x) for x in scapy_reader(hex_str,
#                                                 [x.replace("\r", "") for x in packet_data.header])]
#     scapy_code_summary = [
#         f"{x.split(' |')[0]}>" for x in scapy_code
#     ]
#     return templates.TemplateResponse("hex.html",
#                                       context={"request": request,
#                                                "length": packet_data.length,
#                                                "header": " / ".join(packet_data.header),
#                                                "array": packet_data.array,
#                                                "body": packet_data.body2,
#                                                "raw_hex": hex_str_operation(hex_str, with_new_line=True),
#                                                "pd": packet_data,
#                                                "hexdump": hexdump(hex_str_operation(hex_str), dump=True),
#                                                "scapy_code": scapy_code,
#                                                "scapy_code_summary": scapy_code_summary,
#                                                "better_scapy_code_summary": better_scapy_summary(scapy_reader(hex_str,
#                                                                                                               [
#                                                                                                                   x.replace(
#                                                                                                                       "\r",
#                                                                                                                       "")
#                                                                                                                   for x
#                                                                                                                   in
#                                                                                                                   packet_data.header]))
#                                                }
#                                       )
