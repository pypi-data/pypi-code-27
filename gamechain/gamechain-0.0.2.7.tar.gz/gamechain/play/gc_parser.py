from bitcash import format
from . import gc_message


def parse_stt(msg_payload):
    initiator_key_bytes = msg_payload[:33]
    game_id_bytes = msg_payload[33:33+32]

    sizes_offset = 33 + 32
    signed_game_id_size = msg_payload[sizes_offset]
    msg_bytes_size_bytes = msg_payload[sizes_offset + 1:sizes_offset + 1 + 2]
    msg_size = int.from_bytes(msg_bytes_size_bytes, byteorder='big')

    messages_offset = sizes_offset + 3
    signed_game_id = msg_payload[messages_offset:messages_offset + signed_game_id_size]
    msg_data = msg_payload[messages_offset + signed_game_id_size: messages_offset + signed_game_id_size + msg_size]

    valid = format.verify_sig(signed_game_id, game_id_bytes, initiator_key_bytes)
    if valid:
        msg_data_str = msg_data.decode()
        msg_stt = gc_message.MsgStt(initiator_key_bytes, msg_data_str)
        return gc_message.MSG_STT, msg_stt, None

    return None


def parse_tmt(msg_payload, sender_public_key):
    previous_txid_bytes = msg_payload[:32]

    sizes_offset = 32
    msg_bytes_size_bytes = msg_payload[sizes_offset:sizes_offset + 2]
    msg_size = int.from_bytes(msg_bytes_size_bytes, byteorder='big')
    signed_previous_txid_size = msg_payload[sizes_offset + 2]

    after_sizes_offset = 32 + 3
    game_turn_ops = msg_payload[after_sizes_offset:after_sizes_offset + msg_size]

    after_game_turn_ops_offset = after_sizes_offset + msg_size
    signed_previous_txid = msg_payload[after_game_turn_ops_offset:after_game_turn_ops_offset + signed_previous_txid_size + 1]

    valid = format.verify_sig(signed_previous_txid, previous_txid_bytes, sender_public_key)
    if valid:
        game_turn_ops_str = game_turn_ops.decode()
        msg_tmt = gc_message.MsgTmt(game_turn_ops_str)
        previous_txid = previous_txid_bytes.hex()
        return gc_message.MSG_TMT, msg_tmt, previous_txid

    return None


def parse_win(msg_payload, sender_public_key):
    previous_txid_bytes = msg_payload[:32]

    sizes_offset = 32
    msg_bytes_size_bytes = msg_payload[sizes_offset:sizes_offset + 2]
    msg_size = int.from_bytes(msg_bytes_size_bytes, byteorder='big')
    signed_previous_txid_size = msg_payload[sizes_offset + 2]

    after_sizes_offset = 32 + 3
    game_turn_ops = msg_payload[after_sizes_offset:after_sizes_offset + msg_size]

    after_game_turn_ops_offset = after_sizes_offset + msg_size
    signed_previous_txid = msg_payload[after_game_turn_ops_offset:after_game_turn_ops_offset + signed_previous_txid_size + 1]

    valid = format.verify_sig(signed_previous_txid, previous_txid_bytes, sender_public_key)
    if valid:
        game_turn_ops_str = game_turn_ops.decode()
        msg_win = gc_message.MsgTmt(game_turn_ops_str)
        previous_txid = previous_txid_bytes.hex()
        return gc_message.MSG_WIN, msg_win, previous_txid

    return None


def parse_draw(msg_payload, sender_public_key):
    previous_txid_bytes = msg_payload[:32]

    sizes_offset = 32
    msg_bytes_size_bytes = msg_payload[sizes_offset:sizes_offset + 2]
    msg_size = int.from_bytes(msg_bytes_size_bytes, byteorder='big')
    signed_previous_txid_size = msg_payload[sizes_offset + 2]

    after_sizes_offset = 32 + 3
    game_turn_ops = msg_payload[after_sizes_offset:after_sizes_offset + msg_size]

    after_game_turn_ops_offset = after_sizes_offset + msg_size
    signed_previous_txid = msg_payload[after_game_turn_ops_offset:after_game_turn_ops_offset + signed_previous_txid_size + 1]

    valid = format.verify_sig(signed_previous_txid, previous_txid_bytes, sender_public_key)
    if valid:
        game_turn_ops_str = game_turn_ops.decode()
        msg_draw = gc_message.MsgTmt(game_turn_ops_str)
        previous_txid = previous_txid_bytes.hex()
        return gc_message.MSG_DRW, msg_draw, previous_txid

    return None


def parse_gc_message(gc_bytes, sender_public_key):
    if gc_bytes[0] != 0x01:
        return None

    msg_type = gc_bytes[1]
    msg_payload = gc_bytes[2:]

    if msg_type == gc_message.MSG_STT:
        return parse_stt(msg_payload)

    if msg_type == gc_message.MSG_TMT:
        return parse_tmt(msg_payload, sender_public_key)

    if msg_type == gc_message.MSG_WIN:
        return parse_win(msg_payload, sender_public_key)

    if msg_type == gc_message.MSG_DRW:
        return parse_draw(msg_payload, sender_public_key)

    return None
