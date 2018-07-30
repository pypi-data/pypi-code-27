from .. import utils
from gamechain.play import gc_message


def build_gc_message_chain(messages):
    msg_chain = []
    stt_msg = utils.single(messages, lambda m: m.msg_type == gc_message.MSG_STT)
    msg_chain.append(stt_msg)

    curr_txid = stt_msg.txid
    next_msg = utils.single(messages, lambda m: m.previous_txid == curr_txid, False)

    while next_msg is not None:
        msg_chain.append(next_msg)

        curr_txid = next_msg.txid
        next_msg = utils.single(messages, lambda m: m.previous_txid == curr_txid, False)

    return msg_chain

