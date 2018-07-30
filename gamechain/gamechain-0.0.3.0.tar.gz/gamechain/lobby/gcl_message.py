
import time
from bitcash import transaction, network
import cashaddress
from .. import utils
from . import gcl_parser
from gamechain.comm import gc_comm
from gamechain import which_net

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

GCL_LOKAD_PREFIX = [0x00, 0x00, 0x13, 0x37]


class GclMessage:
    def __init__(self, txid, sender_addr, receiver_addr, msg_type, msg):
        self.txid = txid
        self.sender_addr = which_net.ensure_prefixed_address_str(sender_addr)
        self.receiver_addr = which_net.ensure_prefixed_address_str(receiver_addr)
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
    def __init__(self, wtp_txid_bytes, msg_data):
        self.wtp_txid_bytes = wtp_txid_bytes
        self.msg_data = msg_data


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


def receive_message_by_txid(txid, sender_public_key=None) -> GclMessage:
    sender_addr, receiver_addr, op_return_asms = gc_comm.get_sender_receiver_op_returns_by_txid(txid)
    op_return_gcl_asm_bytes = gc_comm.rx_join_op_returns(op_return_asms, GCL_LOKAD_PREFIX)
    if op_return_gcl_asm_bytes is None:
        print(f"NO GC MESSAGE TO RECEIVE IN TX {txid}")
        return None

    # op_return_asm_bytes = op_return_asms[0]

    print(f"TX_ID: {txid}")
    print(f"MSG_ASM: {op_return_gcl_asm_bytes}")
    # msg_type, msg_contents = gcl_parser.parse_op_return(op_return_gc_asm_bytes, sender_public_key)
    msg_type, msg_contents = gcl_parser.parse_gcl_message(op_return_gcl_asm_bytes, sender_public_key)

    return GclMessage(txid, sender_addr, receiver_addr, msg_type, msg_contents)


def check_if_message_is_for_addr(tx, addr):
    vouts = tx["vout"]
    if len(vouts) < 2:
        return False

    receiver_addr = next(iter(vouts[1].keys()))
    receiver_addr = cashaddress.convert.to_cash_address(receiver_addr)
    receiver_addr = which_net.ensure_prefixed_address_str(receiver_addr)

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
