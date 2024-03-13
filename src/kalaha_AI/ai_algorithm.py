import copy

class KalahaAI:
    def __init__(self, game):
        self.game = game

    def get_state(self):
        return self.game.get_board(), self.game.get_current_player()

    def choose_move(self, depth=12):  # Added depth parameter with default value
        state = self.get_state()
        best_score = float('-inf')
        best_move = None
        for action in self.actions(state):
            #print(f"AI is considering move from pit {action}")
            simulated_state = self.result(state, action)
            score = self.minimax_value(simulated_state, depth - 1)  # Pass depth - 1 to the next level
            print(f"AI evaluated move {action} with score {score}")
            if score > best_score:
                best_score = score
                best_move = action
        print(f"AI chooses pit {best_move} with a score of {best_score}")
        return best_move

    def actions(self, state):
        # Returns all legal moves from the given state
        valid_moves = []
        board = state[0]
        start, end = (7, 13) if self.game.get_current_player() == 2 else (0, 6)
        for pit_index in range(start, end):
            if board[pit_index] > 0:  # Ensure there are stones to play
                valid_moves.append(pit_index)
        return valid_moves

    def result(self, state, action):
        # Simulates a move and returns the resulting state
        board = state[0]
        new_board, extra_turn = self.game.make_move(copy.deepcopy(board), action)
        if extra_turn:
            #print(f"Extra turn for the current player {state[1]}")
            new_state = new_board, state[1]
        else:
            next_player = 1 if state[1] == 2 else 2
            new_state = new_board, next_player
        return new_state

    def terminal_test(self, state):
        # Checks if the game is over for the given state
        board  = state[0]
        return self.game.is_game_over_state(board)

    def utility(self, state):
        board = state[0]
        # Assuming AI is player 2
        if self.game.is_game_over_state(board):
            winner = self.game.get_winner_based_on_state(board)  # Adjust based on your implementation
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

    def minimax_value(self, state, depth):
        if self.terminal_test(state) or depth == 0:
            return self.evaluate(state)

        if state[1] == 2: # If player is AI then maximising player
            best_value = float('-inf')
            for action in self.actions(state):
                value = self.minimax_value(self.result(state, action), depth - 1)
                best_value = max(best_value, value)
        else:
            best_value = float('inf')
            for action in self.actions(state):
                value = self.minimax_value(self.result(state, action), depth - 1)
                best_value = min(best_value, value)

        return best_value
    

    def evaluate(self, state):
        board = state[0]
        player = state[1] - 1

        # Weight factors
        store_weight = 1.5
        seed_weight = 1
        mobility_weight = 1.5
        capture_weight = 3
        frontier_weight = 0.5

        # Initialize scores for both players
        player_score = 0
        opponent_score = 0

        # Calculate scores for each player
        for pit in range(len(board)):
            if board[pit] > 0:
                # Player's pit
                if pit // 7 == player:
                    player_score += board[pit]
                    # Additional weight for seeds in the player's store
                    if pit == 6 * player:
                        player_score += store_weight * board[pit]
                # Opponent's pit
                else:
                    opponent_score += board[pit]

        # Calculate mobility
        player_mobility = sum(1 for pit in range(player * 7, player * 7 + 6) if board[pit] > 0)
        opponent_mobility = sum(1 for pit in range(1 - player * 7, 7 - player * 7) if board[pit] > 0)

        # Calculate captures
        player_captures = sum(board[pit] for pit in range(player * 7, player * 7 + 6) if (pit + board[pit]) % 14 == 6)
        opponent_captures = sum(board[pit] for pit in range(1 - player * 7, 7 - player * 7) if (pit + board[pit]) % 14 == 0)

        # Calculate frontier seeds
        player_frontier = sum(1 for pit in range(player * 7, player * 7 + 6) if board[pit] == 1)
        opponent_frontier = sum(1 for pit in range(1 - player * 7, 7 - player * 7) if board[pit] == 1)

        # Calculate final evaluation scores
        player_score += seed_weight * player_score + mobility_weight * (player_mobility - opponent_mobility) + capture_weight * (player_captures - opponent_captures) + frontier_weight * (player_frontier - opponent_frontier)
        opponent_score += seed_weight * opponent_score + mobility_weight * (opponent_mobility - player_mobility) + capture_weight * (opponent_captures - player_captures) + frontier_weight * (opponent_frontier - player_frontier)

        # Return the difference in scores (positive if player is winning, negative if opponent is winning)
        return player_score - opponent_score


    # def player_utility(self):
    #     pass

    # def alpha_beta_cutoff(self):
    #     pass
