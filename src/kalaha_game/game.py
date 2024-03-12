class KalahaGame:
    def __init__(self):
        # Initialize board: 6 stones in each pit, 0 in Kalahas
        self.board = [6] * 6 + [0] + [6] * 6 + [0]  # Pits 0-5: Player 1, 7-12: Player 2, 6 & 13: Kalahas
        # initial state = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        self.current_player = 1  # Player 1 starts
    
    def print_board(self):
        # Print the board state in a user-friendly way
        print("P2:  ", self.board[13], " | ", *self.board[12:6:-1])
        print("    ", end="")
        print("       ", *self.board[:6], " | ", "P1:  ", self.board[6])
        print("\n")

    def get_board(self):
        return self.board # Return the current board states

    def play_turn(self, pit_index):
        if self.is_valid_move(pit_index):
            extra_turn = self.make_move(self.board, pit_index)
            if self.is_game_over():
                self.end_game()
                return True
            if not extra_turn:  # Only switch player if no extra turn granted
                self.switch_player()
            return True
        else:
            print("Invalid move. Try again.")
            return False

    def is_valid_move(self, pit_index):
        if (self.current_player == 1 and 0 <= pit_index <= 5 and self.board[pit_index] > 0) or \
           (self.current_player == 2 and 7 <= pit_index <= 12 and self.board[pit_index] > 0):
            return True
        return False

    def make_move(self, board, pit_index):
        stones = board[pit_index]
        board[pit_index] = 0  # Remove all stones from the pit
        last_index = pit_index
        while stones > 0:
            last_index = (last_index + 1) % 14
            if (self.current_player == 1 and last_index == 13) or (self.current_player == 2 and last_index == 6):
                continue
            board[last_index] += 1
            stones -= 1

        return board, self.handle_extra_turns_and_captures(last_index)

    def handle_extra_turns_and_captures(self, last_index):
        # Check if last stone landed in the player's Kalaha for an extra turn
        extra_turn = False
        if (self.current_player == 1 and last_index == 6) or (self.current_player == 2 and last_index == 13):
            extra_turn = True
        
        # Handle captures
        if self.current_player == 1 and 0 <= last_index <= 5 and self.board[last_index] == 1:
            opposite_index = 12 - last_index
            if self.board[opposite_index] > 0:
                self.board[6] += self.board[opposite_index] + 1  # Add captured stones
                self.board[last_index] = 0
                self.board[opposite_index] = 0
        elif self.current_player == 2 and 7 <= last_index <= 12 and self.board[last_index] == 1:
            opposite_index = 12 - last_index
            if self.board[opposite_index] > 0:
                self.board[13] += self.board[opposite_index] + 1  # Add captured stones
                self.board[last_index] = 0
                self.board[opposite_index] = 0

        return extra_turn

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def is_game_over(self):
        return all(stone == 0 for stone in self.board[:6]) or all(stone == 0 for stone in self.board[7:13])

    def end_game(self):
        if all(stone == 0 for stone in self.board[:6]):
            self.board[13] += sum(self.board[7:13])
            for i in range(7, 13):
                self.board[i] = 0
        elif all(stone == 0 for stone in self.board[7:13]):
            self.board[6] += sum(self.board[:6])
            for i in range(6):
                self.board[i] = 0

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

    def play(self):
        while not self.is_game_over():
            self.print_board()
            if self.current_player == 1:
                print("Player 1's turn. Choose a pit (0-5): ", end="")
            else:
                print("Player 2's turn. Choose a pit (7-12): ", end="")

            pit_index = int(input())
            self.play_turn(pit_index)

if __name__ == "__main__":
    game = KalahaGame()
    game.play()
