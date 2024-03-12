from src.kalaha_game.game import KalahaGame  
from src.kalaha_AI.ai_algorithm import KalahaAI

def play_game(game):
    ai_player = KalahaAI(game)  # Initialize AI for interacting with the game

    while not game.is_game_over(game.board):
        game.print_board()
        if game.current_player == 1:
            pit_index = int(input("Player 1's turn. Choose a pit (0-5): "))
            game.play_turn(pit_index)
        else:
            print("Now its AI")
            pit_index = ai_player.choose_move()
            print(f"AI (Player 2) chose pit {pit_index}")
            game.play_turn(pit_index)

if __name__ == "__main__":
    game = KalahaGame()
    inital_board = game.board
    play_game(game)
