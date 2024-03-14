from src.kalaha_game.game import KalahaGame
from src.kalaha_AI.ai_algorithm import KalahaAI

class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number

    def choose_move(self, game):
        if self.player_number == 1:
            pit_range = "(0-5)"
        else:
            pit_range = "(7-12)"
        
        pit_index = int(input(f"Player {self.player_number}'s turn. Choose a pit {pit_range}: "))
        
        # Ensure the pit index is valid for the current player
        while not game.is_valid_move(pit_index):
            print("Invalid move. Try again.")
            pit_index = int(input(f"Player {self.player_number}'s turn. Choose a pit {pit_range}: "))
        
        return pit_index

class AIPlayer:
    def __init__(self, ai_logic, player_number):
        self.ai_logic = ai_logic
        self.player_number = player_number

    def choose_move(self, game):
        pit_index = self.ai_logic.choose_move()
        print(f"AI (Player {self.player_number}) chose pit {pit_index}")
        return pit_index

def play_game(player1, player2, game):
    players = {1: player1, 2: player2}

    game_ended = False
    while not game_ended:
        game.print_board()
        current_player = game.get_current_player()
        pit_index = players[current_player].choose_move(game)
        game.make_move(pit_index)
        
        if game.is_game_over():
            game.end_game()  # Finalize game state and print the winner
            game_ended = True

def select_game_mode(game):
    mode = input("Select game mode - Player vs Player (1), Player vs AI (2), AI vs AI (3): ")
    if mode == '1':
        return HumanPlayer(1), HumanPlayer(2)
    elif mode == '2':
        # Pass the game instance and player number to KalahaAI
        return HumanPlayer(1), AIPlayer(KalahaAI(game, 2), 2)
    elif mode == '3':
        # Pass the game instance and player number to KalahaAI for both AI players
        return AIPlayer(KalahaAI(game, 1), 1), AIPlayer(KalahaAI(game, 2), 2)
    else:
        print("Invalid selection, defaulting to Player vs Player.")
        return HumanPlayer(1), HumanPlayer(2)

if __name__ == "__main__":
    game = KalahaGame()
    player1, player2 = select_game_mode(game)  # Pass the game instance to select_game_mode
    play_game(player1, player2, game)

