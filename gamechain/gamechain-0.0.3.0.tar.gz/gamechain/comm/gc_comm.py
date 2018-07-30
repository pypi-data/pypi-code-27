import os, time, json
from bitcash import transaction, network
from gamechain.gc_types import GcPrivateKey
import cashaddress
from .. import utils, which_net
from . import gamechain_monitor

GCL_PREFIX = 1337
GC_PREFIX = 31337

OP_RETURN_PREFIX_BYTES = 0x6A
OP_RETURN_PREFIX = "6a"

OP_PUSHDATA = 0x4C
OP_PUSHDATA2 = 0x4D

FEE_AMOUNT = 250
MESSAGE_AMOUNT = 0
AMOUNT_UNITS = 'satoshi'
MESSAGE_LIMIT = 220  # 100

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


def rx_join_op_returns(op_return_asms, lokad_prefix):
    def process_first_op_return(op_return_bytes):
        # pull out GC prefix
        if op_return_bytes[0] == OP_RETURN_PREFIX_BYTES and \
                op_return_bytes[1] == 0x04 and \
                op_return_bytes[2] == lokad_prefix[0] and \
                op_return_bytes[3] == lokad_prefix[1] and \
                op_return_bytes[4] == lokad_prefix[2] and \
                op_return_bytes[5] == lokad_prefix[3]:
            return op_return_bytes[6:]

        return None

    def process_subsequent_op_return(op_return_bytes):
        if op_return_bytes[0] == OP_RETURN_PREFIX_BYTES:
            return op_return_bytes[1:]

        return None

    def process_length_prefix(op_return_bytes):
        if op_return_bytes[0] == OP_PUSHDATA:
            size = op_return_bytes[1]
            return op_return_bytes[2:2 + size + 1]
        elif op_return_bytes[0] == OP_PUSHDATA2:
            size_bytes = op_return_bytes[1:3]
            size = int.from_bytes(size_bytes, byteorder='big')
            return op_return_bytes[3:3 + size + 1]

        return None

    op_return_asm_bytes = process_first_op_return(op_return_asms[0])
    if op_return_asm_bytes is None:
        return None

    if len(op_return_asms) > 1:
        for subsequent_op_return_asm_bytes in op_return_asms[1:]:
            processed_bytes = process_subsequent_op_return(subsequent_op_return_asm_bytes)
            if processed_bytes is None:
                return None
            op_return_asm_bytes += processed_bytes

    op_return_asm_bytes = process_length_prefix(op_return_asm_bytes)
    return op_return_asm_bytes


def get_fee_amount(op_return_data, msg_count=0):
    op_return_fee_multiplier = 1
    if msg_count > 1:
        op_return_fee_multiplier = 3

    return FEE_AMOUNT + (op_return_fee_multiplier * len(op_return_data))


def get_unspent_by_txid(sender_key, next_to_spend_txid):
    next_tx_found = False
    while not next_tx_found:
        unspents = sender_key.get_unspents()
        for unspent in unspents:
            if unspent.txid == next_to_spend_txid:
                return unspent

        if not next_tx_found:
            time.sleep(1)


def send_message(sender_key: GcPrivateKey, spend_from_txid, receiver_addr, op_ret_data):
    unspent = get_unspent_by_txid(sender_key, spend_from_txid)
    print(unspent)

    def chunk_data(data, size):
        return (data[i:i + size] for i in range(0, len(data), size))

    messages = []

    if op_ret_data:
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

    tx_hex = transaction.create_p2pkh_transaction(sender_key.bitcash_key, [unspent], outputs)
    tx_id = transaction.calc_txid(tx_hex)

    if which_net.is_testnet():
        network.NetworkAPI.broadcast_tx_testnet(tx_hex)
    else:
        raise Exception("TX broadcasting only tested with testnet")

    return tx_id


def get_sender_receiver_op_returns_by_txid(txid):
    tx = utils.get_tx(txid)
    vouts = tx["vout"]
    addr_vouts = [vout for vout in vouts if "addresses" in vout["scriptPubKey"].keys()]
    sender_addr = which_net.ensure_prefixed_address_str(addr_vouts[0]["scriptPubKey"]["addresses"][0])
    receiver_addr = which_net.ensure_prefixed_address_str(addr_vouts[1]["scriptPubKey"]["addresses"][0])
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
    receiver_addr = which_net.ensure_prefixed_address_str(receiver_addr)

    return receiver_addr == addr

