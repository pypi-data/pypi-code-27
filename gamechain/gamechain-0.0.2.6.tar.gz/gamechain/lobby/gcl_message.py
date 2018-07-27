
import time
from bitcash import transaction, network
import cashaddress
from .. import utils
from . import gcl_parser
from gamechain.comm import gc_comm

GCL_PREFIX = 1337
GC_PREFIX = 31337

MSG_LFG = 0x01
MSG_WTP = 0x02
MSG_ACC = 0x03
MSG_REJ = 0x04
MSG_CAN = 0x05

FEE_AMOUNT = 250
MESSAGE_AMOUNT = 0
AMOUNT_UNITS ='satoshi'
MESSAGE_LIMIT = 220  # 100

OP_PUSHDATA = 0x4C


class GclMessage:
    def __init__(self, txid, sender_addr, receiver_addr, msg_type, msg):
        self.txid = txid
        self.sender_addr = utils.ensure_prefixed_address(sender_addr)
        self.receiver_addr = utils.ensure_prefixed_address(receiver_addr)
        self.msg_type = msg_type
        self.msg = msg

    @property
    def txid_bytes(self):
        return bytes.fromhex(self.txid)


class MsgLfg:
    def __init__(self, public_key_bytes, msg_data):
        self.public_key_bytes = public_key_bytes
        self.msg_data = msg_data


class MsgWtp:
    def __init__(self, public_key_bytes, lfg_txid_bytes, msg_data):
        self.public_key_bytes = public_key_bytes
        self.lfg_txid_bytes = lfg_txid_bytes
        self.msg_data = msg_data


class MsgAcc:
    def __init__(self, wtp_txid_bytes, msg_data):
        self.wtp_txid_bytes = wtp_txid_bytes
        self.msg_data = msg_data


class MsgCan:
    def __init__(self, wtp_txid_bytes, msg_data):
        self.wtp_txid_bytes = wtp_txid_bytes
        self.msg_data = msg_data


class MsgRej:
    def __init__(self, msg_data):
        self.msg_data = msg_data


def get_fee_amount(op_return_data, msg_count=0):
    op_return_fee_multiplier = 1
    if msg_count > 1:
        op_return_fee_multiplier = 3

    return FEE_AMOUNT + (op_return_fee_multiplier * len(op_return_data))


def get_unspent_by_txid(sender_key, next_to_spend_txid):
    next_tx_found = False
    while not next_tx_found:
        unspents = sender_key.get_unspents()
        # unspents.sort(key=lambda x: x.amount, reverse=True)
        for unspent in unspents:
            if unspent.txid == next_to_spend_txid:
                return unspent

        if not next_tx_found:
            time.sleep(1)


def send_message(sender_key, spend_from_txid, receiver_addr, op_ret_data):
    # if len(op_ret_data) > MESSAGE_LIMIT:
    #     print(op_ret_data)
    #     raise Exception("Message is too long")

    unspent = get_unspent_by_txid(sender_key, spend_from_txid)
    print(unspent)

    def chunk_data(data, size):
        return (data[i:i + size] for i in range(0, len(data), size))

    messages = []

    if op_ret_data:
        # message_chunks = chunk_data(op_ret_data.encode('utf-8'), MESSAGE_LIMIT)
        message_chunks = chunk_data(op_ret_data, MESSAGE_LIMIT)

        for message in message_chunks:
            messages.append((message, None))

    fee_amount = get_fee_amount(op_ret_data, len(messages))
    amount_back_to_sender = unspent.amount - fee_amount - MESSAGE_AMOUNT
    outputs = [
        (sender_key.address, amount_back_to_sender),
        (receiver_addr, MESSAGE_AMOUNT),
    ]

    outputs.extend(messages)

    tx_hex = transaction.create_p2pkh_transaction(sender_key, [unspent], outputs)
    tx_id = transaction.calc_txid(tx_hex)

    network.NetworkAPI.broadcast_tx_testnet(tx_hex)

    return tx_id


def _parse_message_from_op_return_msg(op_return_msg):
    msg_bytes = bytes.fromhex(op_return_msg)

    return msg_bytes


# #OP_RETURN_PREFIX = "OP_RETURN "
# OP_RETURN_PREFIX = "6a"
# # OP_RETURN_AND_SIZE_BYTES_COUNT = 4
# def receive_message_by_txid(txid, sender_public_key=None) -> GclMessage:
#     tx = utils.get_tx_testnet(txid)
#     vouts = tx["vout"]
#     addr_vouts = [vout for vout in vouts if "addresses" in vout["scriptPubKey"].keys()]
#     sender_addr = addr_vouts[0]["scriptPubKey"]["addresses"][0]
#     receiver_addr = addr_vouts[1]["scriptPubKey"]["addresses"][0]
#     # op_return_msg = next(vout["scriptPubKey"]["hex"][OP_RETURN_AND_SIZE_BYTES_COUNT:] for vout in vouts if vout["scriptPubKey"]["asm"].startswith(OP_RETURN_PREFIX))
#     # op_return_asm = next(vout["scriptPubKey"]["asm"][2:] for vout in vouts if
#     #                      vout["scriptPubKey"]["asm"].startswith(OP_RETURN_PREFIX))
#     op_return_asms = [vout["scriptPubKey"]["hex"][2:] for vout in vouts if
#                       vout["scriptPubKey"]["hex"].startswith(OP_RETURN_PREFIX)]
#     op_return_asm = op_return_asms[0]
#     msg_bytes = bytes.fromhex(op_return_asm)
#
#     # msg_bytes = _parse_message_from_op_return_msg(op_return_msg)
#     print(f"TX_ID: {txid}")
#     print(f"MSG_ASM: {op_return_asm}")
#     msg_type, msg_contents = gcl_parser.parse_op_return(msg_bytes, sender_public_key)
#
#     return GclMessage(txid, sender_addr, receiver_addr, msg_type, msg_contents)

# TURN_PREFIX = "OP_RETURN "
# OP_RETURN_PREFIX = "6a"
# OP_RETURN_AND_SIZE_BYTES_COUNT = 4
def receive_message_by_txid(txid, sender_public_key=None) -> GclMessage:
    sender_addr, receiver_addr, op_return_asms = gc_comm.get_sender_receiver_op_returns_by_txid(txid)
    op_return_asm_bytes = op_return_asms[0]

    print(f"TX_ID: {txid}")
    print(f"MSG_ASM: {op_return_asm_bytes}")
    msg_type, msg_contents = gcl_parser.parse_op_return(op_return_asm_bytes, sender_public_key)

    return GclMessage(txid, sender_addr, receiver_addr, msg_type, msg_contents)


def check_if_message_is_for_addr(tx, addr):
    vouts = tx["vout"]
    if len(vouts) < 2:
        return False

    receiver_addr = next(iter(vouts[1].keys()))
    receiver_addr = cashaddress.convert.to_cash_address(receiver_addr)
    receiver_addr = utils.ensure_prefixed_address(receiver_addr)

    return receiver_addr == addr


if __name__ == "__main__":
    print("MSG")
    msg, sender, receiver = receive_message_by_txid("a90285a9270c980b860f6f0921ec887395778a400e1e3c850dc0fac8dabba23d")
    # h = int("0x" + msg, 16)
    print(msg)
    # h = bytes.fromhex(msg)
    # print(h)




#
# const transaction = new bch.Transaction()
#         .from(utxo)
#         .to(toAddr, 0)
#         .change(fromAddr)
#         .fee(FEE)
#         .addData(message)
#         .sign(fromPk);
