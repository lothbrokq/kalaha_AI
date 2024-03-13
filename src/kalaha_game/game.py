import copy

class KalahaGame:
    def __init__(self):
        # Initialize board: 6 stones in each pit, 0 in Kalahas
        self.board = [6] * 6 + [0] + [6] * 6 + [0]  # Pits 0-5: Player 1, 7-12: Player 2, 6 & 13: Kalahas
        # initial state = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        
        #self.board = [1, 1, 12, 1, 1, 5, 0, # Capture example
        #              0, 0, 1, 0, 5, 4, 0]
        
        #self.board = [1, 1, 1, 1, 1, 5, 0, # Extra turn example
        #              1, 0, 1, 0, 2, 1, 0]
        
        #self.board = [0, 0, 2, 4, 1, 0, 36, # End game example
        #              0, 0, 0, 0, 0, 9, 36]

        self.current_player = 1  # Player 1 starts
    
    def get_winner_based_on_state(self, board):
        # This method assumes that the game is over. It calculates which player has more stones in their Kalaha.
        # Remember, this doesn't declare the winner based on game rules directly (e.g., emptying one side of the board)
        # but rather who has more stones in their Mancala/Kalaha after the game ends.
        if board[6] > board[13]:  # If Player 1 has more stones in their Kalaha
            return 1
        elif board[13] > board[6]:  # If Player 2 has more stones in their Kalaha
            return 2
        else:
            return "Tie"  # A tie if both have the same number of stones
    
    # def print_board(self):
    #     # Print the board state in a user-friendly way
    #     print("P2:  ", self.board[13], " | ", *self.board[12:6:-1])
    #     print("    ", end="")
    #     print("       ", *self.board[:6], " | ", "P1:  ", self.board[6])
    #     print("\n")

    def print_board(self):
        # Print the board state in a user-friendly way
        print("P2:  ", self.board[13], "  |  ", self.board[12], " ", self.board[11], " ", self.board[10], " ", self.board[9], " ", self.board[8], " ", self.board[7])
        print("    ", end="")
        print("         ", self.board[0], " ", self.board[1], " ", self.board[2], " ", self.board[3], " ", self.board[4], " ", self.board[5], "  |  ", "P1:  ", self.board[6])
        print("\n")

    def get_board(self):
        return copy.deepcopy(self.board) # Return the current board states

    def get_current_player(self):
        return self.current_player

    def play_turn(self, pit_index):
        if self.is_valid_move(pit_index):
            extra_turn = self.make_move(self.board, pit_index)[1]
            if self.is_game_over(self.board):
                self.end_game()
                return True
            if not extra_turn:  # Only switch player if no extra turn granted
                self.switch_player()
            return True
        else:
            print("Invalid move. Try again.")
            return False

    def is_valid_move(self, pit_index):
        if 0 <= pit_index <= 5 and self.current_player == 1 and self.board[pit_index] > 0 or \
           7 <= pit_index <= 12 and self.current_player == 2 and self.board[pit_index] > 0:
            return True
        return False

    def make_move(self, board, pit_index):
        stones = board[pit_index]
        board[pit_index] = 0
        last_index = pit_index
        while stones > 0:
            last_index = (last_index + 1) % 14
            if (self.current_player == 1 and last_index == 13) or (self.current_player == 2 and last_index == 6):
                continue
            board[last_index] += 1
            stones -= 1

        return board, self.handle_extra_turns_and_captures(board, last_index)

    def handle_extra_turns_and_captures(self, board, last_index):
        extra_turn = False
        if (self.current_player == 1 and last_index == 6) or (self.current_player == 2 and last_index == 13):
            extra_turn = True

        if 0 <= last_index <= 5 and self.current_player == 1 and board[last_index] == 1 or \
           7 <= last_index <= 12 and self.current_player == 2 and board[last_index] == 1:
            opposite_index = 12 - last_index
            if board[opposite_index] > 0:
                capture_pit = 6 if self.current_player == 1 else 13
                board[capture_pit] += board[opposite_index] + 1
                board[last_index] = 0
                board[opposite_index] = 0

        return extra_turn

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def is_game_over(self, board):
        return all(stone == 0 for stone in board[:6]) or all(stone == 0 for stone in board[7:13])

    def end_game(self):
        if all(stone == 0 for stone in self.board[:6]):
            self.board[13] += sum(self.board[7:13])
            self.board[7:13] = [0]*6
        elif all(stone == 0 for stone in self.board[7:13]):
            self.board[6] += sum(self.board[:6])
            self.board[:6] = [0]*6

        print("Game over. Player 1: {} | Player 2: {}".format(self.board[6], self.board[13]))
        winner = self.get_winner()
        print(f"Winner: Player {winner}")
        self.print_board()

    def get_winner(self):
        if self.board[6] > self.board[13]:
            return 1
        elif self.board[13] > self.board[6]:
            return 2
        else:
            return "Tie"

