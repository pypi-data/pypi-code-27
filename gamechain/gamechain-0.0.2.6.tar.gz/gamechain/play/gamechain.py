from .. import utils
from gamechain.lobby import gamechain_lobby
from ..play import gc_engine, gc_message, gc_state
import json


def initialize_game(initiator_key, JSON_FILE, table_addr, game_id,
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

    gcl_client = gamechain_lobby.GameChainLobbyClient(initiator_key, JSON_FILE)
    txid = gcl_client.send_gc_message(table_addr, init_game_conditions_str_bytes)
    return f"bitcoincash-gc:{txid}"


def get_game_messages(table_addr, player_pubkeys):
    txids = utils.get_transaction_ids_for_address(table_addr)

    game_messages = []
    for txid in txids:
        msg = gc_message.receive_message_by_txid_with_pubkeys(txid, player_pubkeys)
        if msg is not None:
            game_messages.append(msg)

    return game_messages


def start_playing(init_game_msg, player_key, initiator_public_key, json_file, game_processor):
    # find game tx
    bch_init_txid = init_game_msg.split("bitcoincash-gc:")[1]

    # receive game STT message
    stt_message = gc_message.receive_message_by_txid(bch_init_txid, initiator_public_key)

    if stt_message is None or stt_message.msg_type != gc_message.MSG_STT:
        raise Exception(f"Unable to play game based on init_game_msg: {init_game_msg}")

    init_game_msg = stt_message.msg.msg_data

    game_processor.initialize_game(init_game_msg)
    player_pubkeys = game_processor.player_pubkeys
    table_addr = stt_message.receiver_addr

    game_messages = get_game_messages(table_addr, player_pubkeys)
    game_state_to_now = gc_state.build_gc_message_chain(game_messages)
    # game_turns = [msg for msg in game_state_to_now if msg.msg_type == gc_message.MSG_TMT]
    game_turns = [msg for msg in game_state_to_now if msg.msg_type != gc_message.MSG_STT]

    print("GM INIT >> " + game_state_to_now[0].msg.msg_data)
    for gt in game_turns:
        print("GM >> " + gt.msg.msg_data)

    engine = gc_engine.GameEngine(game_processor, player_key, player_pubkeys, table_addr, json_file)
    engine.initialize_game(stt_message, game_turns)
    engine.play()
