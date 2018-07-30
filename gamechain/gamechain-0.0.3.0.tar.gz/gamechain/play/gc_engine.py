import time
from gamechain.comm import gc_comm
from gamechain.play import gc_message, gc_message_builder, gc_state, gamechain


class GameEngine:

    def __init__(self, game_processor, player_key, player_pubkeys, table_addr, json_file):
        self.game_processor = game_processor
        self.player_key = player_key
        self.player_pubkeys = player_pubkeys
        self.table_addr = table_addr
        self.json_file = json_file
        self._processed_txids = []

    def initialize_game(self, stt_msg, game_turns):
        self.game_processor.initialize_game(stt_msg.msg.msg_data)
        self._processed_txids.append(stt_msg.txid)
        for gt in game_turns:
            turn_msg = gt.msg.msg_data
            player_addr = gt.sender_addr
            self.game_processor.process_player_turn(player_addr, gt.msg_type, turn_msg)
            self._processed_txids.append(gt.txid)

    def play(self):
        gcc = gc_comm.GcCommClient(self.player_key, self.json_file)
        while not self.game_processor.is_game_complete():
            if self.game_processor.is_player_turn(self.player_key.address):
                prev_turn_txid = self._processed_txids[-1]
                turn_msg_type, turn_msg = self.game_processor.wait_for_player_move(self.player_key.address)
                turn_msg_bytes = turn_msg.encode()
                if turn_msg_type == gc_message.MSG_TMT:
                    to_send = gc_message_builder.create_taking_my_turn_message(self.player_key, prev_turn_txid, turn_msg_bytes)
                elif turn_msg_type == gc_message.MSG_WIN:
                    to_send = gc_message_builder.create_i_win_message(self.player_key, prev_turn_txid, turn_msg_bytes)
                elif turn_msg_type == gc_message.MSG_DRW:
                    to_send = gc_message_builder.create_draw_message(self.player_key, prev_turn_txid, turn_msg_bytes)
                else:
                    raise Exception("Invalid turn_msg_type: %s" % turn_msg_type)
                turn_txid = gcc.send_message(self.table_addr, to_send)
                self._processed_txids.append(turn_txid)
            else:
                # check for and process new messages
                print("Checking for new game messages")
                game_messages = gamechain.get_game_messages(self.table_addr, self.player_pubkeys)
                gc_message_chain = gc_state.build_gc_message_chain(game_messages)
                new_messages = [msg for msg in gc_message_chain if msg.txid not in self._processed_txids]
                if len(new_messages) == 0:
                    time.sleep(2)
                else:
                    for next_msg in new_messages:
                        self.game_processor.process_player_turn(next_msg.sender_addr, next_msg.msg_type, next_msg.msg.msg_data)
                        self._processed_txids.append(next_msg.txid)

        gcc.stop()
        print("Game over! Winner is %s" % self.game_processor.game_winner)
