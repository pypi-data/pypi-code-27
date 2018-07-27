import json
from itertools import cycle
from gamechain.play import gc_message


class TicTacToeProcessor:

    def initialize_game(self, init_game_msg):
        game_data = json.loads(init_game_msg)
        all_player_data = game_data["players"]
        players = [(pd["addr"], bytes.fromhex(pd["key"])) for pd in all_player_data]
        self.players = players
        self.player_cycle = cycle(players)
        self.next_to_act_addr = self.get_next_to_act()

        self.game_state = "---|---|---"
        self.x_addr = players[0][0]
        self.o_addr = players[1][0]

        self.game_over = False
        self.game_winner = None

    @property
    def player_pubkeys(self):
        return dict(self.players)

    @property
    def player_order(self):
        return [p[0] for p in self.players]

    def process_player_turn(self, player_addr, msg_type, turn_msg):
        if player_addr != self.next_to_act_addr:
            raise Exception("Invalid next to act addr: " + player_addr)

        if not self.check_valid(turn_msg):
            raise Exception("Invalid move! " + turn_msg)

        if msg_type == gc_message.MSG_TMT:
            self.game_state = turn_msg
            self.next_to_act_addr = self.get_next_to_act()

        if msg_type == gc_message.MSG_DRW:
            if self._is_game_complete(turn_msg):
                self.report_to_player("Game is a draw")
                self.game_over = True
            else:
                self.report_to_player("Draw declared but game is not complete!")

        if msg_type == gc_message.MSG_WIN:
            check_to_win_symbol = self.get_player_symbol(player_addr)
            if self.is_symbol_winner(turn_msg, check_to_win_symbol):
                self.report_to_player("Winner is %s" % check_to_win_symbol)
                self.game_winner = player_addr
                self.game_over = True
            else:
                self.report_to_player("Win declared by %s but game is not complete!" % check_to_win_symbol)

    def check_valid(self, turn_msg):
        if turn_msg is None:
            return False
        if len(turn_msg) != len("---|---|---"):
            return False
        if turn_msg[3] != "|" or turn_msg[7] != "|":
            return False
        return True

    def get_player_symbol(self, player_addr):
        player_symbol = "?"
        if player_addr == self.x_addr:
            player_symbol = "X"
        if player_addr == self.o_addr:
            player_symbol = "O"
        return player_symbol

    def create_input_message(self, game_state, player_addr):
        player_symbol = self.get_player_symbol(player_addr)
        msg_strs = ["\n", "You are " + player_symbol, "\n"]

        rows = game_state.split("|")
        for r in rows:
            msg_strs.append(r)
            msg_strs.append("\n")

        msg_strs.append("Choose grid location for " + player_symbol + " >> ")
        return "".join(msg_strs)

    def wait_for_player_move(self, player_addr):
        valid = False
        while not valid:
            input_message = self.create_input_message(self.game_state, player_addr)
            next_move = input(input_message)
            updated_game_state = self.process_move(next_move, player_addr)
            valid = self.check_valid(updated_game_state)

        self.game_state = updated_game_state
        self.next_to_act_addr = self.get_next_to_act()
        player_gc_message_type = self.get_player_gc_message_type(updated_game_state, player_addr)

        if player_gc_message_type == gc_message.MSG_WIN:
            self.game_over = True
            self.game_winner = player_addr

        return player_gc_message_type, updated_game_state

    def process_move(self, move, player_addr):
        player_symbol = self.get_player_symbol(player_addr)
        updated_game_state = self.game_state
        move_index = self.get_index_for_move(move)
        if move_index is None:
            return None
        if updated_game_state[move_index] != "-":
            return None
        updated_game_state = updated_game_state[:move_index] + player_symbol + updated_game_state[move_index+1:]
        return updated_game_state

    def get_index_for_move(self, move):
        if len(move) != 2:
            return None

        if move.startswith("A"):
            col_move_index = 0
        elif move.startswith("B"):
            col_move_index = 1
        elif move.startswith("C"):
            col_move_index = 2
        else:
            return None

        if move.endswith("1"):
            row_move_index = 0
        elif move.endswith("2"):
            row_move_index = 1
        elif move.endswith("3"):
            row_move_index = 2
        else:
            return None

        total_index = (4 * row_move_index) + col_move_index
        return total_index

    def report_to_player(self, info):
        input("REPORT >> " + info)

    def _is_game_complete(self, game_state):
        any_moves_left = "-" in game_state
        if not any_moves_left:
            return True
        return False

    def is_game_complete(self):
        return self._is_game_complete(self.game_state) or self.game_over

    def is_symbol_winner(self, game_state, symbol):
        if self._is_top_row_winner(game_state, symbol) or \
            self._is_middle_row_winner(game_state, symbol) or \
            self._is_bottom_row_winner(game_state, symbol) or \
            self._is_left_column_winner(game_state, symbol) or \
            self._is_center_column_winner(game_state, symbol) or \
            self._is_right_column_winner(game_state, symbol) or \
            self._is_top_left_diagonal_winner(game_state, symbol) or \
            self._is_top_right_diagonal_winner(game_state, symbol):
                return True
        return False

    def get_player_gc_message_type(self, game_state, player_addr):
        player_symbol = self.get_player_symbol(player_addr)
        if self.is_symbol_winner(game_state, player_symbol):
            return gc_message.MSG_WIN

        if self._is_game_complete(game_state):
            return gc_message.MSG_DRW

        return gc_message.MSG_TMT

    def _get_row(self, row_index, game_state):
        return game_state.split("|")[row_index]

    def _get_column(self, col_index, game_state):
        row1 = self._get_row(0, game_state)
        row2 = self._get_row(1, game_state)
        row3 = self._get_row(2, game_state)

        col = row1[col_index] + row2[col_index] + row3[col_index]
        return col

    def _get_top_left_diagonal(self, game_state):
        top_left = self._get_row(0, game_state)[0]
        middle = self._get_row(1, game_state)[1]
        bottom_right = self._get_row(2, game_state)[2]

        diagonal = top_left + middle + bottom_right
        return diagonal

    def _is_top_left_diagonal_winner(self, game_state, symbol):
        diag_sequence = self._get_top_left_diagonal(game_state)
        symbol_sequence = symbol * 3
        if diag_sequence == symbol_sequence:
            return True
        return False

    def _is_top_right_diagonal_winner(self, game_state, symbol):
        diag_sequence = self._get_top_right_diagonal(game_state)
        symbol_sequence = symbol * 3
        if diag_sequence == symbol_sequence:
            return True
        return False

    def _get_top_right_diagonal(self, game_state):
        top_right = self._get_row(0, game_state)[2]
        middle = self._get_row(1, game_state)[1]
        bottom_left = self._get_row(2, game_state)[0]

        diagonal = bottom_left + middle + top_right
        return diagonal

    def _check_row_winner(self, game_state, symbol, row_index):
        row_sequence = self._get_row(row_index, game_state)
        symbol_sequence = symbol * 3
        if row_sequence == symbol_sequence:
            return True
        return False

    def _is_top_row_winner(self, game_state, symbol):
        return self._check_row_winner(game_state, symbol, 0)

    def _is_middle_row_winner(self, game_state, symbol):
        return self._check_row_winner(game_state, symbol, 1)

    def _is_bottom_row_winner(self, game_state, symbol):
        return self._check_row_winner(game_state, symbol, 2)

    def _check_column_winner(self, game_state, symbol, col_index):
        col_sequence = self._get_column(col_index, game_state)
        symbol_sequence = symbol * 3
        if col_sequence == symbol_sequence:
            return True
        return False

    def _is_left_column_winner(self, game_state, symbol):
        return self._check_column_winner(game_state, symbol, 0)

    def _is_center_column_winner(self, game_state, symbol):
        return self._check_column_winner(game_state, symbol, 1)

    def _is_right_column_winner(self, game_state, symbol):
        return self._check_column_winner(game_state, symbol, 2)

    def is_player_turn(self, player_addr):
        return self.next_to_act_addr == player_addr

    def get_next_to_act(self):
        return next(self.player_cycle)[0]

