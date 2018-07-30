import json
from gamechain.comm import gc_comm
from gamechain.play import gc_message


def _get_prefix_bytes():
    return 0x0400031337.to_bytes(5, 'big')


def _get_op_pushdata_bytes(message_body_len):
    return gc_comm.OP_PUSHDATA2.to_bytes(1, 'big') + message_body_len.to_bytes(2, 'big')


def _get_version_bytes():
    return 0x01.to_bytes(1, 'big')


def pad_gameid_to32(game_id):
    padded = game_id
    while len(padded) < 32:
        padded += " "
    return padded


def create_init_game_str_bytes(game_id,
                               p1_addr, p1_public_key,
                               p2_addr, p2_public_key,
                               challenger_game_conditions) -> str:
    init_game_conditions = {
        "gameAddr": game_id,
        "players": [
            {
                "addr": p1_addr,
                "key": p1_public_key.hex()
            },
            {
                "addr": p2_addr,
                "key": p2_public_key.hex()
            }
        ],
        "setup": challenger_game_conditions
    }
    init_game_conditions_str_bytes = json.dumps(init_game_conditions).encode()
    return init_game_conditions_str_bytes


def create_set_the_table_message(initiator_key, game_id, init_msg_bytes):
    stt_msg_bytes = gc_message.MSG_STT.to_bytes(1, 'big')
    if len(game_id) != 32:
        raise Exception(f"game_id must be 32 bytes long '{game_id}'")

    game_id_bytes = game_id.encode()
    signed_game_id_bytes = initiator_key.sign(game_id_bytes)
    signed_game_id_size_bytes = len(signed_game_id_bytes).to_bytes(1, 'big')

    msg_size = len(init_msg_bytes).to_bytes(2, 'big')

    message_body = [
        stt_msg_bytes,
        initiator_key.public_key,
        game_id_bytes,
        signed_game_id_size_bytes,
        msg_size,
        signed_game_id_bytes,
        init_msg_bytes
    ]
    message_body_bytes = b''.join(message_body)
    message_body_len = len(message_body_bytes)

    message_parts = [
        _get_prefix_bytes(),
        _get_op_pushdata_bytes(message_body_len),
        _get_version_bytes(),
        message_body_bytes
    ]

    message = b''.join(message_parts)
    return message


def create_taking_my_turn_message(player_key, prev_txid, turn_msg_bytes):
    tmt_msgtype_bytes = gc_message.MSG_TMT.to_bytes(1, 'big')

    prev_txid_bytes = bytes.fromhex(prev_txid)
    signed_prev_txid_bytes = player_key.sign(prev_txid_bytes)
    signed_prev_txid_size_bytes = len(signed_prev_txid_bytes).to_bytes(1, 'big')

    msg_size = len(turn_msg_bytes).to_bytes(2, 'big')

    message_body = [
        tmt_msgtype_bytes,
        prev_txid_bytes,
        msg_size,
        signed_prev_txid_size_bytes,
        turn_msg_bytes,
        signed_prev_txid_bytes
    ]
    message_body_bytes = b''.join(message_body)
    message_body_len = len(message_body_bytes)

    message_parts = [
        _get_prefix_bytes(),
        _get_op_pushdata_bytes(message_body_len),
        _get_version_bytes(),
        message_body_bytes
    ]

    message = b''.join(message_parts)
    return message


def create_i_win_message(player_key, prev_txid, turn_msg_bytes):
    iwin_msgtype_bytes = gc_message.MSG_WIN.to_bytes(1, 'big')

    prev_txid_bytes = bytes.fromhex(prev_txid)
    signed_prev_txid_bytes = player_key.sign(prev_txid_bytes)
    signed_prev_txid_size_bytes = len(signed_prev_txid_bytes).to_bytes(1, 'big')

    msg_size = len(turn_msg_bytes).to_bytes(2, 'big')

    message_body = [
        iwin_msgtype_bytes,
        prev_txid_bytes,
        msg_size,
        signed_prev_txid_size_bytes,
        turn_msg_bytes,
        signed_prev_txid_bytes
    ]
    message_body_bytes = b''.join(message_body)
    message_body_len = len(message_body_bytes)

    message_parts = [
        _get_prefix_bytes(),
        _get_op_pushdata_bytes(message_body_len),
        _get_version_bytes(),
        message_body_bytes
    ]

    message = b''.join(message_parts)
    return message


def create_draw_message(player_key, prev_txid, turn_msg_bytes):
    draw_msgtype_bytes = gc_message.MSG_DRW.to_bytes(1, 'big')

    prev_txid_bytes = bytes.fromhex(prev_txid)
    signed_prev_txid_bytes = player_key.sign(prev_txid_bytes)
    signed_prev_txid_size_bytes = len(signed_prev_txid_bytes).to_bytes(1, 'big')

    msg_size = len(turn_msg_bytes).to_bytes(2, 'big')

    message_body = [
        draw_msgtype_bytes,
        prev_txid_bytes,
        msg_size,
        signed_prev_txid_size_bytes,
        turn_msg_bytes,
        signed_prev_txid_bytes
    ]
    message_body_bytes = b''.join(message_body)
    message_body_len = len(message_body_bytes)

    message_parts = [
        _get_prefix_bytes(),
        _get_op_pushdata_bytes(message_body_len),
        _get_version_bytes(),
        message_body_bytes
    ]

    message = b''.join(message_parts)
    return message