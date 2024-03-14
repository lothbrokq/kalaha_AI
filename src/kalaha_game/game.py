import copy

class KalahaGame:
    def __init__(self, player1_type='human', player2_type='human'):
        self.board = [6] * 6 + [0] + [6] * 6 + [0]  # Initial board state
        #self.board = [0, 0, 0, 0, 0, 1, 0, 
        #              4, 4, 4, 4, 4, 4, 0]
        self.current_player = 1
        self.player_types = {1: player1_type, 2: player2_type}

    def print_board(self):
        print("P2: ", self.board[13], " | ", *self.board[12:6:-1])
        print("    ", end="")
        print("      ", *self.board[:6], " | ", "P1: ", self.board[6])
        print("\n")

    def get_board(self):
        return copy.deepcopy(self.board)

    def get_current_player(self):
        return self.current_player

    def is_valid_move(self, pit_index):
        if 0 <= pit_index <= 5 and self.current_player == 1 and self.board[pit_index] > 0 or \
           7 <= pit_index <= 12 and self.current_player == 2 and self.board[pit_index] > 0:
            return True
        return False

    def make_move(self, pit_index, simulate=False):
        if not self.is_valid_move(pit_index):
            return self.board, False, "Invalid move. Try again."

        board = copy.deepcopy(self.board) if simulate else self.board
        stones = board[pit_index]
        board[pit_index] = 0
        last_index = pit_index
        while stones > 0:
            last_index = (last_index + 1) % 14
            if (self.current_player == 1 and last_index == 13) or (self.current_player == 2 and last_index == 6):
                continue  # Skip opponent's Kalaha
            board[last_index] += 1
            stones -= 1

        extra_turn = self.handle_extra_turns_and_captures(last_index, board)
        if not extra_turn and not simulate:  # Only switch players if not simulating
            self.switch_player()
        return board, extra_turn, ""

    def handle_extra_turns_and_captures(self, last_index, board):
        extra_turn = False
        if (self.current_player == 1 and last_index == 6) or (self.current_player == 2 and last_index == 13):
            extra_turn = True  # Grant extra turn for landing in own Kalaha

        if 0 <= last_index <= 5 and self.current_player == 1 and board[last_index] == 1 or \
        7 <= last_index <= 12 and self.current_player == 2 and board[last_index] == 1:
            opposite_index = 12 - last_index
            if board[opposite_index] > 0:  # Capture condition
                capture_pit = 6 if self.current_player == 1 else 13
                board[capture_pit] += board[opposite_index] + 1
                board[last_index] = 0
                board[opposite_index] = 0

        return extra_turn


    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def is_game_over(self):
        return all(stone == 0 for stone in self.board[:6]) or all(stone == 0 for stone in self.board[7:13])

    def end_game(self):
        board = self.board
        if all(stone == 0 for stone in board[:6]):
            board[13] += sum(board[7:13])
            board[7:13] = [0]*6
        elif all(stone == 0 for stone in board[7:13]):
            board[6] += sum(board[:6])
            board[:6] = [0]*6

        print("Game over. Player 1: {} | Player 2: {}".format(board[6], board[13]))
        winner = self.get_winner_based_on_state(board)
        print(f"Winner: Player {winner}")
        self.print_board()

    def get_winner_based_on_state(self, board):
        if board[6] > board[13]:
            return 1
        elif board[13] > board[6]:
            return 2
        else:
            return "Tie"
