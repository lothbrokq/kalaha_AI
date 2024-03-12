import copy

class KalahaAI:
    def __init__(self, game):
        self.game = game

    def choose_move(self, depth=10):  # Added depth parameter with default value
        state = self.game.get_state()
        best_score = float('-inf')
        best_move = None
        for action in self.actions(state):
            print(f"AI is considering move from pit {action}")
            simulated_state = self.result(state, action)
            score = self.min_value(simulated_state, depth - 1)  # Pass depth - 1 to the next level
            print(f"AI evaluated move {action} with score {score}")
            if score > best_score:
                best_score = score
                best_move = action
        print(f"AI chooses pit {best_move} with a score of {best_score}")
        return best_move

    def actions(self, state):
        # Returns all legal moves from the given state
        valid_moves = []
        start, end = (7, 13) if self.game.get_current_player() == 2 else (0, 6)
        for pit_index in range(start, end):
            if state[pit_index] > 0:  # Ensure there are stones to play
                valid_moves.append(pit_index)
        return valid_moves

    def result(self, state, action):
        # Simulates a move and returns the resulting state
        new_state, _ = self.game.make_move(copy.deepcopy(state), action)
        return new_state

    def terminal_test(self, state):
        # Checks if the game is over for the given state
        return self.game.is_game_over_state(state)

    def utility(self, state):
        # Assuming AI is player 2
        if self.game.is_game_over_state(state):
            winner = self.game.get_winner_based_on_state(state)  # Adjust based on your implementation
            if winner == 2:
                #print("AI sees a winning move")
                return 1  # AI win
            elif winner == 1:
                #print("AI sees a losing move")
                return -1  # AI loss
            else:
                #print("AI sees a draw")
                return 0  # Draw
        return 0  # Non-terminal state

    def min_value(self, state, depth):
        if self.terminal_test(state) or depth == 0:  # Check for terminal state or depth limit
            return self.utility(state)
        v = float('inf')
        for a in self.actions(state):
            v = min(v, self.max_value(self.result(state, a), depth - 1))  # Decrease depth by 1
        return v

    def max_value(self, state, depth):
        if self.terminal_test(state) or depth == 0:  # Check for terminal state or depth limit
            return self.utility(state)
        v = float('-inf')
        for a in self.actions(state):
            v = max(v, self.min_value(self.result(state, a), depth - 1))  # Decrease depth by 1
        return v
