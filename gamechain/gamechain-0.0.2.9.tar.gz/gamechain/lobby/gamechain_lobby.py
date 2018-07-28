import os
import json
from gamechain.lobby import gcl_message, gcl_message_builder, gcl_parser
from gamechain.comm import gamechain_monitor, message_monitors, gc_comm
from .. import utils, which_net

NEXT_TO_SPEND_TXID = "next_txid"


class GameChainLobbyClient:

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

    def look_for_game(self, gameshelf_id, label, initial_conditions):
        setup_info = f"{initial_conditions},{label}"
        lfg_message = gcl_message_builder.create_looking_for_game_message(self._private_key, setup_info)
        tx_id = gc_comm.send_message(self._private_key, self._data[NEXT_TO_SPEND_TXID],
                                     gameshelf_id, lfg_message)

        self._data[NEXT_TO_SPEND_TXID] = tx_id
        self._save_state()

        return tx_id

    def wait_for_lfg(self, gameshelf_id):
        cm = message_monitors.LfgMonitor(self._gamechain_monitor, gameshelf_id)
        challenge_gcl_msg = cm.wait_for_challenge()
        return challenge_gcl_msg

    def offer_willing_to_play(self, lfg_addr, lfg_txid_bytes, alternative_conditions):
        wtp_message = gcl_message_builder.create_willing_to_play_message(self._private_key, lfg_txid_bytes, alternative_conditions)

        p_lfg_addr = which_net.ensure_prefixed_address(lfg_addr)

        tx_id = gc_comm.send_message(self._private_key, self._data[NEXT_TO_SPEND_TXID],
                                     p_lfg_addr, wtp_message)

        self._data[NEXT_TO_SPEND_TXID] = tx_id
        self._save_state()

        return tx_id

    def wait_for_challenge_response(self, wtp_tx_id, public_key_bytes):
        cm = message_monitors.ChallengeResponseMonitor(self._gamechain_monitor, self._private_key.address,
                                                       wtp_tx_id, public_key_bytes)
        cr_gcl_msg = cm.wait_for_challenge_reponse()
        return cr_gcl_msg

    def stop(self):
        self._gamechain_monitor.stop()

    def wait_for_wtp(self, lfg_txid):
        my_addr = self._private_key.address
        mon = message_monitors.WtpMonitor(self._gamechain_monitor, my_addr, lfg_txid)
        wtp_gcl_msg = mon.wait_for_wtp()
        return wtp_gcl_msg

    def accept_wtp(self, sender_addr, wtp_txid_bytes, init_game_msg):
        accept_wtp_message_bytes = gcl_message_builder.create_accept_wtp_message(self._private_key, wtp_txid_bytes,
                                                                                 init_game_msg)

        p_sender_addr = which_net.ensure_prefixed_address(sender_addr)

        tx_id = gc_comm.send_message(self._private_key, self._data[NEXT_TO_SPEND_TXID],
                                     p_sender_addr, accept_wtp_message_bytes)

        self._data[NEXT_TO_SPEND_TXID] = tx_id
        self._save_state()

        return tx_id

    def reject_wtp(self, sender_addr, reject_msg):
        reject_wtp_msg_bytes = reject_msg.encode()
        p_sender_addr = which_net.ensure_prefixed_address(sender_addr)

        tx_id = gc_comm.send_message(self._private_key, self._data[NEXT_TO_SPEND_TXID],
                                     p_sender_addr, reject_wtp_msg_bytes)

        self._data[NEXT_TO_SPEND_TXID] = tx_id
        self._save_state()

        return tx_id

    def send_gc_message(self, receiver_addr, msg_body):
        p_receiver_addr = which_net.ensure_prefixed_address(receiver_addr)

        tx_id = gc_comm.send_message(self._private_key, self._data[NEXT_TO_SPEND_TXID],
                                     p_receiver_addr, msg_body)

        self._data[NEXT_TO_SPEND_TXID] = tx_id
        self._save_state()

        return tx_id
