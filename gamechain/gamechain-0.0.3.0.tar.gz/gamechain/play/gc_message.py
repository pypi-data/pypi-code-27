from ..comm import gc_comm
from . import gc_parser

MSG_STT = 0x01
MSG_TMT = 0x03
MSG_WIN = 0x04
MSG_LUZ = 0x05
MSG_DRW = 0x06

# OP_PUSHDATA = 0x4C
# OP_PUSHDATA2 = 0x4D

GC_LOKAD_PREFIX = [0x00, 0x03, 0x13, 0x37]


class GcMessage:
    def __init__(self, txid, sender_addr, receiver_addr, msg_type, msg, previous_txid):
        self.txid = txid
        self.sender_addr = sender_addr
        self.receiver_addr = receiver_addr
        self.msg_type = msg_type
        self.msg = msg
        self.previous_txid = previous_txid

    @property
    def txid_bytes(self):
        return bytes.fromhex(self.txid)


class MsgStt:
    def __init__(self, public_key_bytes, msg_data):
        self.public_key_bytes = public_key_bytes
        self.msg_data = msg_data


class MsgTmt:
    def __init__(self, msg_data):
        self.msg_data = msg_data

#
# OP_RETURN_PREFIX_BYTES = 0x6A
# OP_RETURN_PREFIX = "6a"


# def join_gc_op_returns(op_return_asms):
#     def process_first_op_return(op_return_bytes):
#         # pull out GC prefix
#         if op_return_bytes[0] == OP_RETURN_PREFIX_BYTES and \
#                 op_return_bytes[1] == 0x04 and \
#                 op_return_bytes[2] == 0x00 and \
#                 op_return_bytes[3] == 0x03 and \
#                 op_return_bytes[4] == 0x13 and \
#                 op_return_bytes[5] == 0x37:
#             return op_return_bytes[6:]
#
#         return None
#
#     def process_subsequent_op_return(op_return_bytes):
#         if op_return_bytes[0] == OP_RETURN_PREFIX_BYTES:
#             return op_return_bytes[1:]
#
#         return None
#
#     def process_length_prefix(op_return_bytes):
#         if op_return_bytes[0] == OP_PUSHDATA:
#             size = op_return_bytes[1]
#             return op_return_bytes[2:2 + size + 1]
#         elif op_return_bytes[0] == OP_PUSHDATA2:
#             size_bytes = op_return_bytes[1:3]
#             size = int.from_bytes(size_bytes, byteorder='big')
#             return op_return_bytes[3:3 + size + 1]
#
#         return None
#
#     op_return_asm_bytes = process_first_op_return(op_return_asms[0])
#     if op_return_asm_bytes is None:
#         return None
#
#     if len(op_return_asms) > 1:
#         for subsequent_op_return_asm_bytes in op_return_asms[1:]:
#             processed_bytes = process_subsequent_op_return(subsequent_op_return_asm_bytes)
#             if processed_bytes is None:
#                 return None
#             op_return_asm_bytes += processed_bytes
#
#     op_return_asm_bytes = process_length_prefix(op_return_asm_bytes)
#     return op_return_asm_bytes


def receive_message_by_txid(txid, sender_public_key=None) -> GcMessage:
    sender_addr, receiver_addr, op_return_asms = gc_comm.get_sender_receiver_op_returns_by_txid(txid)
    op_return_gc_asm_bytes = gc_comm.rx_join_op_returns(op_return_asms, GC_LOKAD_PREFIX)
    if op_return_gc_asm_bytes is None:
        print(f"NO GC MESSAGE TO RECEIVE IN TX {txid}")
        return None

    # print(f"TX_ID: {txid}")
    # print(f"MSG_ASM: {op_return_gc_asm_bytes}")

    msg_type, msg_contents, previous_txid = gc_parser.parse_gc_message(op_return_gc_asm_bytes, sender_public_key)

    return GcMessage(txid, sender_addr, receiver_addr, msg_type, msg_contents, previous_txid)


def receive_message_by_txid_with_pubkeys(txid, public_keys={}) -> GcMessage:
    sender_addr, receiver_addr, op_return_asms = gc_comm.get_sender_receiver_op_returns_by_txid(txid)
    op_return_gc_asm_bytes = gc_comm.rx_join_op_returns(op_return_asms, GC_LOKAD_PREFIX)
    if op_return_gc_asm_bytes is None:
        print(f"NO GC MESSAGE TO RECEIVE IN TX {txid}")
        return None

    # print(f"TX_ID: {txid}")
    # print(f"MSG_ASM: {op_return_gc_asm_bytes}")

    sender_public_key = public_keys[sender_addr]
    msg_type, msg_contents, previous_txid = gc_parser.parse_gc_message(op_return_gc_asm_bytes, sender_public_key)

    return GcMessage(txid, sender_addr, receiver_addr, msg_type, msg_contents, previous_txid)


def get_str_for_msg_type(msg_type):
    if msg_type == MSG_STT:
        return "STT"
    elif msg_type == MSG_TMT:
        return "TMT"
    elif msg_type == MSG_WIN:
        return "WIN"
    elif msg_type == MSG_LUZ:
        return "LUZ"
    elif msg_type == MSG_DRW:
        return "DRW"

    return "???"
