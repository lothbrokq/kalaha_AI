import random
import json
from src.kalaha_game.game import KalahaGame
from src.kalaha_AI.ai_algorithm import KalahaAI

class SimplifiedLearningManager:
    def __init__(self, num_games=10):
        self.num_games = num_games

    def generate_random_config(self):
        return {
            'kalaha_weight': int(random.uniform(0, 100)),
            'pit_weight': int(random.uniform(0, 100)),
            'extra_turn_weight': int(random.uniform(0, 100)),
            'capture_weight': int(random.uniform(0, 100)),
        }

    def play_game(self, config1, config2):
        game = KalahaGame()
        ai1 = KalahaAI(game, 1, config1)
        ai2 = KalahaAI(game, 2, config2)
        winner = None

        print(f"AI1 Config: {config1}")
        print(f"AI2 Config: {config2}")

        while not game.is_game_over():
            if game.current_player == 1:
                move = ai1.choose_move()
                print(f"AI 1 chooses pit {move}")
            else:
                move = ai2.choose_move()
                print(f"AI 2 chooses pit {move}")
            game.make_move(move)
            game.print_board()

        # Finalize the game state, determine the winner, and print results
        game.print_board()
        game.end_game()
        winner_based_on_state = game.get_winner_based_on_state(game.get_board())

        if winner_based_on_state == 1:
            winner = 'AI1'
        elif winner_based_on_state == 2:
            winner = 'AI2'
        else:
            winner = 'Tie'

        return winner

    def run(self):
        results = []
        config1 = self.generate_random_config()
        config2 = self.generate_random_config()

        for game_number in range(1, self.num_games + 1):
            winner = self.play_game(config1, config2)
            print(f"Game {game_number}: Winner is {winner}")
            results.append({'game': game_number, 'winner': winner, 'config1': config1, 'config2': config2})

            # Adjust loser's configuration
            if winner == 'AI2':
                config1 = self.generate_random_config()
            elif winner == 'AI1':
                config2 = self.generate_random_config()

        # Print results to JSON
        with open('ai_battle_results.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)

if __name__ == "__main__":
    manager = SimplifiedLearningManager()
    manager.run()
