class KalahaGame:
    def __init__(self):
        # Initialize board: 6 stones in each pit, 0 in Kalahas
        self.board = [6] * 6 + [0] + [6] * 6 + [0] # Pits 0-5: Player 1, 7-12: Player 2, 6 & 13: Kalahas
        self.current_player = 2 # Player 1 starts
    
    def print_board(self):
        # Print the board state in a user-friendly way
        print("P2: ", self.board[13], "|", *self.board[12:6:-1])
        print("    ", end="")
        print("    ", *self.board[:6], "|", "P1: ", self.board[6])
        print("\n")

    def make_move(self, pit_index):
        stones = self.board[pit_index]
        if stones == 0 or pit_index < 0 or pit_index > 12 or (self.current_player == 1 and pit_index > 5) or (self.current_player == 2 and pit_index < 7):
            print("Invalid move. Try again.")
            return False  # Invalid move
        
        self.board[pit_index] = 0 # Remove all stones from the pit
        while stones > 0: 
            pit_index = (pit_index + 1) % 14
            # Skip opponent's Kalaha
            if (self.current_player == 1 and pit_index == 13) or (self.current_player == 2 and pit_index == 6):
                continue
            self.board[pit_index] += 1
            stones -= 1
        
        # Check for next turn or capture
        self.handle_extra_turns_and_captures(pit_index)

        # Check if the game is over
        if self.is_game_over():
            self.end_game()
            return True

        # Switch player
        if not self.check_for_extra_turn(pit_index):
            self.current_player = 2 if self.current_player == 1 else 1
        return True


    def handle_extra_turns_and_captures(self, last_index):
        # Check if last stone landed on the player's side and in an empty pit
        if self.current_player == 1 and 0 <= last_index <= 5 and self.board[last_index] == 1:
            opposite_index = 12 - last_index
            if self.board[opposite_index] > 0:  # Ensure opposite pit has stones
                # Capture
                self.board[6] += self.board[opposite_index] + 1  # Add stones to player's Kalaha
                self.board[last_index] = 0  # Clear the last pit
                self.board[opposite_index] = 0  # Clear the captured pit
        elif self.current_player == 2 and 7 <= last_index <= 12 and self.board[last_index] == 1:
            opposite_index = 12 - last_index
            if self.board[opposite_index] > 0:  # Ensure opposite pit has stones
                # Capture
                self.board[13] += self.board[opposite_index] + 1  # Add stones to player's Kalaha
                self.board[last_index] = 0  # Clear the last pit
                self.board[opposite_index] = 0  # Clear the captured pit


 
    def check_for_extra_turn(self, last_index):
        # Check if the last stone landed in the player's Kalaha for an extra turn
        return (self.current_player == 1 and last_index == 6) or (self.current_player == 2 and last_index == 13)
    
    def is_game_over(self):
        # Check if all pits on one side are empty
        return all(stone == 0 for stone in self.board[:6]) or all(stone == 0 for stone in self.board[7:13])
    
    def end_game(self):
        # Sum all remaining stones on each player's side and move them to their Kalaha
        if all(stone == 0 for stone in self.board[:6]):  # If Player 1's side is empty
            self.board[13] += sum(self.board[7:13])  # Move Player 2's stones to their Kalaha
            for i in range(7, 13):
                self.board[i] = 0  # Clear Player 2's pits
        elif all(stone == 0 for stone in self.board[7:13]):  # If Player 2's side is empty
            self.board[6] += sum(self.board[:6])  # Move Player 1's stones to their Kalaha
            for i in range(6):
                self.board[i] = 0  # Clear Player 1's pits

        # Determine the winner
        if self.board[6] > self.board[13]:
            print("Game over. Player 1 wins!")
        elif self.board[6] < self.board[13]:
            print("Game over. Player 2 wins!")
        else:
            print("Game over. It's a tie!")

        # Optionally, print the final board state
        self.print_board()

    def play(self):
        while not self.is_game_over():
            self.print_board()
            if self.current_player == 1:
                print("Player 1's turn. Choose a pit (0-5): ", end="")
            else:
                print("Player 2's turn. Choose a pit (7-12): ", end="")
            
            pit_index = int(input())  # Get input from the player
            if self.current_player == 1 and 0 <= pit_index <= 5 or self.current_player == 2 and 7 <= pit_index <= 12:
                self.make_move(pit_index)
            else:
                print("Invalid selection. Please choose a pit on your side of the board.")

# Example of how to use this basic setup
if __name__ == "__main__":
    game = KalahaGame()
    game.play()
