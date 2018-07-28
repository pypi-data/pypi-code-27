from bitcash import format
from gamechain.lobby import gcl_message


def parse_op_push_data(push_data_bytes):
    if push_data_bytes[0] == gcl_message.OP_PUSHDATA:
        size = push_data_bytes[1]
        return push_data_bytes[2:2+size+1]


OP_RETURN_PREFIX_BYTES = 0x6A
def parse_op_return(op_return_bytes, sender_public_key=None):
    # pull out GCL prefix
    if op_return_bytes[0] == OP_RETURN_PREFIX_BYTES and \
       op_return_bytes[1] == 0x04 and \
       op_return_bytes[2] == 0x00 and \
       op_return_bytes[3] == 0x00 and \
       op_return_bytes[4] == 0x13 and \
       op_return_bytes[5] == 0x37:
        op_push_data = parse_op_push_data(op_return_bytes[6:])
        return parse_gcl_message(op_push_data, sender_public_key)

    return None


def parse_lfg(msg_payload):
    public_key_bytes = msg_payload[:33]
    msg_data_size = msg_payload[33]
    signed_msg_data_size = msg_payload[34]
    signed_msg_data_offset = 35 + msg_data_size

    msg_data = msg_payload[35:35 + msg_data_size]
    signed_msg_data = msg_payload[signed_msg_data_offset:signed_msg_data_offset + signed_msg_data_size]

    valid = format.verify_sig(signed_msg_data, msg_data, public_key_bytes)
    if valid:
        msg_data_str = msg_data.decode()
        msg_lfg = gcl_message.MsgLfg(public_key_bytes, msg_data_str)
        return gcl_message.MSG_LFG, msg_lfg

    return None


def parse_wtp(msg_payload):
    lfg_txid_bytes = msg_payload[:32]
    public_key_bytes = msg_payload[32:32+33]
    msg_data_size = msg_payload[32+33]
    signed_txid_size = msg_payload[32+33+1]

    msg_data_offset = 32 + 33 + 1 + 1
    msg_data = msg_payload[msg_data_offset:msg_data_offset + msg_data_size]
    signed_txid = msg_payload[msg_data_offset + msg_data_size:msg_data_offset + msg_data_size + signed_txid_size]

    valid = format.verify_sig(signed_txid, lfg_txid_bytes, public_key_bytes)
    if valid:
        msg_data_str = msg_data.decode()
        msg_wtp = gcl_message.MsgWtp(public_key_bytes, lfg_txid_bytes, msg_data_str)
        return gcl_message.MSG_WTP, msg_wtp

    return None


def parse_acc(msg_payload, sender_public_key_bytes):
    wtp_txid_bytes = msg_payload[:32]
    msg_data_size = msg_payload[32]
    signed_txid_size = msg_payload[33]

    msg_data_offset = 34
    msg_data = msg_payload[msg_data_offset:msg_data_offset + msg_data_size]
    signed_txid = msg_payload[msg_data_offset + msg_data_size:msg_data_offset + msg_data_size + signed_txid_size]

    valid = format.verify_sig(signed_txid, wtp_txid_bytes, sender_public_key_bytes)
    if valid:
        msg_data_str = msg_data.decode()
        msg_acc = gcl_message.MsgAcc(wtp_txid_bytes, msg_data_str)
        return gcl_message.MSG_ACC, msg_acc

    return None


def parse_rej(msg_payload, sender_public_key_bytes):
    wtp_txid_bytes = msg_payload[:32]
    msg_data_size = msg_payload[32]
    signed_txid_size = msg_payload[33]

    msg_data_offset = 34
    msg_data = msg_payload[msg_data_offset:msg_data_offset + msg_data_size]
    signed_txid = msg_payload[msg_data_offset + msg_data_size:msg_data_offset + msg_data_size + signed_txid_size]

    valid = format.verify_sig(signed_txid, wtp_txid_bytes, sender_public_key_bytes)
    if valid:
        msg_data_str = msg_data.decode()
        msg_rej = gcl_message.MsgRej(wtp_txid_bytes, msg_data_str)
        return gcl_message.MSG_REJ, msg_rej

    return None


def parse_can(msg_payload, sender_public_key_bytes):
    txid_bytes = msg_payload[:32]
    msg_data_size = msg_payload[32]
    signed_txid_size = msg_payload[33]

    msg_data_offset = 34
    msg_data = msg_payload[msg_data_offset:msg_data_offset + msg_data_size]
    signed_txid = msg_payload[msg_data_offset + msg_data_size:msg_data_offset + msg_data_size + signed_txid_size]

    valid = format.verify_sig(signed_txid, txid_bytes, sender_public_key_bytes)
    if valid:
        msg_data_str = msg_data.decode()
        msg_can = gcl_message.MsgCan(msg_data_str)
        return gcl_message.MSG_CAN, msg_can

    return None


def parse_gcl_message(gcl_bytes, sender_public_key):
    if gcl_bytes[0] != 0x01:
        return None

    msg_type = gcl_bytes[1]
    msg_payload = gcl_bytes[2:]

    if msg_type == gcl_message.MSG_LFG:
        return parse_lfg(msg_payload)

    if msg_type == gcl_message.MSG_WTP:
        return parse_wtp(msg_payload)

    if msg_type == gcl_message.MSG_ACC:
        return parse_acc(msg_payload, sender_public_key)

    if msg_type == gcl_message.MSG_REJ:
        return parse_rej(msg_payload, sender_public_key)

    if msg_type == gcl_message.MSG_CAN:
        return parse_can(msg_payload, sender_public_key)

    return None