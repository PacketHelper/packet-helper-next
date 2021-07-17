# from fastapi import APIRouter
# from fastapi import Request
# from fastapi.templating import Jinja2Templates
# from scapy_helper import diff as scapy_diff
# from scapy_helper import hexdump
#
# from packet_helper_core.packet_data import PacketData
# from packet_helper_core.utils.utils import decode_hex, hex_str_operation
#
# templates = Jinja2Templates(directory="templates")
#
# router = APIRouter(
#     prefix="/diff",
#     tags=["diff"]
# )
#
#
# @router.get('/')
# def diff(request: Request):
#     return templates.TemplateResponse(
#         "index_diff.html", context={"request": request}
#     )
#
#
# @router.get('/{first_hex}/{second_hex}')
# def get_diff(request: Request, first_hex: str, second_hex: str):
#     first_packet = PacketData(raw=str(decode_hex(first_hex)))
#     second_packet = PacketData(raw=str(decode_hex(second_hex)))
#
#     def separete_bytes(hex_str: str):
#         return ' '.join([''.join([hex_str[e - 1], hex_str[e]]) for e, x in enumerate(hex_str) if e % 2])
#
#     diff_first, diff_second, diff_status = scapy_diff(separete_bytes(first_hex), separete_bytes(second_hex))
#
#     return templates.TemplateResponse(
#         "diff.html",
#         context={
#             "diff_first": diff_first,
#             "diff_second": diff_second,
#             "diff_status": diff_status,
#             "request": request,
#             "length": first_packet.length,
#             "header": " / ".join(first_packet.header),
#             "array": first_packet.array,
#             "body": first_packet.body2,
#             "raw_hex": hex_str_operation(first_hex, with_new_line=True),
#             "pd": first_packet,
#             "hexdump": hexdump(hex_str_operation(first_hex), dump=True),
#             "length2": second_packet.length,
#             "header2": " / ".join(second_packet.header),
#             "array2": second_packet.array,
#             "body2": second_packet.body2,
#             "raw_hex2": hex_str_operation(second_hex, with_new_line=True),
#             "pd2": second_packet,
#             "hexdump2": hexdump(hex_str_operation(second_hex), dump=True)
#         }
#     )
