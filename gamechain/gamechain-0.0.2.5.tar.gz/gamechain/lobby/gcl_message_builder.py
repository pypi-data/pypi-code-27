from . import gcl_message


def _get_prefix_bytes():
    return 0x0400001337.to_bytes(5, 'big')


def _get_op_pushdata_bytes(message_body_len):
    return gcl_message.OP_PUSHDATA.to_bytes(1, 'big') + message_body_len.to_bytes(1, 'big')


def _get_version_bytes():
    return 0x01.to_bytes(1, 'big')


def create_looking_for_game_message(sender_key, setup_info):
    lfg_msg_bytes = gcl_message.MSG_LFG.to_bytes(1, 'big')
    if len(sender_key.public_key) != 33:
        raise Exception("public_key_bytes must be 33 bytes long")

    msg_bytes = setup_info.encode()
    signed_msg_bytes = sender_key.sign(msg_bytes)

    msg_size = len(msg_bytes).to_bytes(1, 'big')
    signed_msg_size = len(signed_msg_bytes).to_bytes(1, 'big')

    message_body = [
        lfg_msg_bytes,
        sender_key.public_key,
        msg_size,
        signed_msg_size,
        msg_bytes,
        signed_msg_bytes
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
    print("MSG: %s" % message)
    return message


def create_willing_to_play_message(sender_key, lfg_txid_bytes, setup_response):
    wtp_msg_bytes = gcl_message.MSG_WTP.to_bytes(1, 'big')
    if len(lfg_txid_bytes) != 32:
        raise Exception("lfg_txid must be 32 bytes long")
    if len(sender_key.public_key) != 33:
        raise Exception("public_key_bytes must be 33 bytes long")

    setup_response_bytes = setup_response.encode()
    signed_lfg_txid = sender_key.sign(lfg_txid_bytes)

    ac_size = len(setup_response_bytes).to_bytes(1, 'big')
    signed_txid_size = len(signed_lfg_txid).to_bytes(1, 'big')

    message_body = [
        wtp_msg_bytes,
        lfg_txid_bytes,
        sender_key.public_key,
        ac_size,
        signed_txid_size,
        setup_response_bytes,
        signed_lfg_txid
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


def create_accept_wtp_message(sender_key, wtp_txid_bytes, final_setup_info):
    acc_msg_bytes = gcl_message.MSG_ACC.to_bytes(1, 'big')
    if len(wtp_txid_bytes) != 32:
        raise Exception("wtp_txid must be 32 bytes long")
    if len(sender_key.public_key) != 33:
        raise Exception("public_key_bytes must be 33 bytes long")

    setup_info_bytes = final_setup_info.encode()
    signed_wtp_txid = sender_key.sign(wtp_txid_bytes)

    msg_size = len(setup_info_bytes).to_bytes(1, 'big')
    signed_txid_size = len(signed_wtp_txid).to_bytes(1, 'big')

    message_body = [
        acc_msg_bytes,
        wtp_txid_bytes,
        msg_size,
        signed_txid_size,
        setup_info_bytes,
        signed_wtp_txid
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


def create_reject_wtp_message(sender_key, wtp_txid_bytes, rejection_msg):
    rej_msg_bytes = gcl_message.MSG_REJ.to_bytes(1, 'big')
    if len(wtp_txid_bytes) != 32:
        raise Exception("wtp_txid must be 32 bytes long")
    if len(sender_key.public_key) != 33:
        raise Exception("public_key_bytes must be 33 bytes long")

    rejection_msg_bytes = rejection_msg.encode()
    signed_wtp_txid = sender_key.sign(wtp_txid_bytes)

    msg_size = len(rejection_msg_bytes).to_bytes(1, 'big')
    signed_txid_size = len(signed_wtp_txid).to_bytes(1, 'big')

    message_body = [
        rej_msg_bytes,
        wtp_txid_bytes,
        msg_size,
        signed_txid_size,
        rejection_msg_bytes,
        signed_wtp_txid
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


def create_cancel_lfg_message(sender_key, lfg_txid_bytes, cancel_msg):
    can_msg_bytes = gcl_message.MSG_CAN.to_bytes(1, 'big')
    if len(lfg_txid_bytes) != 32:
        raise Exception("lfg_txid must be 32 bytes long")
    if len(sender_key.public_key) != 33:
        raise Exception("public_key_bytes must be 33 bytes long")

    cancel_msg_bytes = cancel_msg.encode()
    signed_lfg_txid = sender_key.sign(lfg_txid_bytes)

    msg_size = len(cancel_msg_bytes).to_bytes(1, 'big')
    signed_txid_size = len(signed_lfg_txid).to_bytes(1, 'big')

    message_body = [
        can_msg_bytes,
        lfg_txid_bytes,
        msg_size,
        signed_txid_size,
        cancel_msg_bytes,
        signed_lfg_txid
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

