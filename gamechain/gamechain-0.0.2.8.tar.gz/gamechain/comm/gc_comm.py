import os, time, json
from bitcash import transaction, network
import cashaddress
from .. import utils
from . import gamechain_monitor

GCL_PREFIX = 1337
GC_PREFIX = 31337

FEE_AMOUNT = 250
MESSAGE_AMOUNT = 0
AMOUNT_UNITS ='satoshi'
MESSAGE_LIMIT = 220  # 100

OP_PUSHDATA = 0x4C

NEXT_TO_SPEND_TXID = "next_txid"


class GcCommClient:

    def __init__(self, private_key, save_file):
        self._private_key = private_key
        self._save_file = save_file

        if not os.path.exists(save_file):
            init_data = self._create_init_data()
            self._data = init_data
            self._save_state()

        self._load_state()

        self._gamechain_monitor = gamechain_monitor.GameChainMonitor(60)

    def _create_init_data(self):
        unspents = self._private_key.get_unspents()
        unspents.sort(key=lambda u: u.amount, reverse=True)
        next_to_use_tx = unspents[0]
        init_data = {
            NEXT_TO_SPEND_TXID: next_to_use_tx.txid
        }
        return init_data

    def _load_state(self):
        with open(self._save_file) as json_file:
            self._data = json.load(json_file)

    def _save_state(self):
        print("Saving state: %s" % self._data)
        with open(self._save_file, 'w') as outfile:
            json.dump(self._data, outfile)

    def send_message(self, to_addr, msg):
        tx_id = send_message(self._private_key, self._data[NEXT_TO_SPEND_TXID], to_addr, msg)

        self._data[NEXT_TO_SPEND_TXID] = tx_id
        self._save_state()

        return tx_id

    def stop(self):
        self._gamechain_monitor.stop()


def get_fee_amount(op_return_data):
    return FEE_AMOUNT + len(op_return_data)


def get_unspent_by_txid(sender_key, next_to_spend_txid):
    next_tx_found = False
    while not next_tx_found:
        unspents = sender_key.get_unspents()
        for unspent in unspents:
            if unspent.txid == next_to_spend_txid:
                return unspent

        if not next_tx_found:
            time.sleep(1)


def send_message(sender_key, spend_from_txid, receiver_addr, op_ret_data):
    unspent = get_unspent_by_txid(sender_key, spend_from_txid)
    print(unspent)

    fee_amount = get_fee_amount(op_ret_data)
    amount_back_to_sender = unspent.amount - fee_amount - MESSAGE_AMOUNT
    outputs = [
        (sender_key.address, amount_back_to_sender),
        (receiver_addr, MESSAGE_AMOUNT),
    ]

    def chunk_data(data, size):
        return (data[i:i + size] for i in range(0, len(data), size))

    messages = []

    if op_ret_data:
        message_chunks = chunk_data(op_ret_data, MESSAGE_LIMIT)

        for message in message_chunks:
            messages.append((message, None))

    outputs.extend(messages)

    tx_hex = transaction.create_p2pkh_transaction(sender_key, [unspent], outputs)
    tx_id = transaction.calc_txid(tx_hex)

    network.NetworkAPI.broadcast_tx_testnet(tx_hex)

    return tx_id


def _parse_message_from_op_return_msg(op_return_msg):
    msg_bytes = bytes.fromhex(op_return_msg)
    return msg_bytes


OP_RETURN_PREFIX = "6a"
def get_sender_receiver_op_returns_by_txid(txid):
    tx = utils.get_tx_testnet(txid)
    vouts = tx["vout"]
    addr_vouts = [vout for vout in vouts if "addresses" in vout["scriptPubKey"].keys()]
    sender_addr = utils.ensure_prefixed_address(addr_vouts[0]["scriptPubKey"]["addresses"][0])
    receiver_addr = utils.ensure_prefixed_address(addr_vouts[1]["scriptPubKey"]["addresses"][0])
    op_return_hexes = [vout["scriptPubKey"]["hex"] for vout in vouts if
                      vout["scriptPubKey"]["hex"].startswith(OP_RETURN_PREFIX)]

    op_return_asms_bytes = [bytes.fromhex(op_return_asm) for op_return_asm in op_return_hexes]
    return sender_addr, receiver_addr, op_return_asms_bytes


def check_if_message_is_for_addr(tx, addr):
    vouts = tx["vout"]
    if len(vouts) < 2:
        return False

    receiver_addr = next(iter(vouts[1].keys()))
    receiver_addr = cashaddress.convert.to_cash_address(receiver_addr)
    receiver_addr = utils.ensure_prefixed_address(receiver_addr)

    return receiver_addr == addr

