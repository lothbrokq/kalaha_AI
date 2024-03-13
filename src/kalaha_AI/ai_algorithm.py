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
            score = self.minimax_value(simulated_state, depth - 1, float('-inf'), float('inf'))  # Pass depth - 1 to the next level
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
        return self.game.is_game_over(board)

    def utility(self, state):
        board = state[0]
        # Assuming AI is player 2
        if self.game.is_game_over(board):
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

    # def minimax_value(self, state, depth):
    #     if self.terminal_test(state) or depth == 0:
    #         return self.evaluate(state)

    #     if state[1] == 2: # If player is AI then maximising player
    #         best_value = float('-inf')
    #         for action in self.actions(state):
    #             value = self.minimax_value(self.result(state, action), depth - 1)
    #             best_value = max(best_value, value)
    #     else:
    #         best_value = float('inf')
    #         for action in self.actions(state):
    #             value = self.minimax_value(self.result(state, action), depth - 1)
    #             best_value = min(best_value, value)

    #     return best_value
    
    def minimax_value(self, state, depth, alpha=float('-inf'), beta=float('inf')):
        if self.terminal_test(state) or depth == 0:
            return self.evaluate(state)

        if state[1] == 2:  # Maximizing for AI
            value = float('-inf')
            for action in self.actions(state):
                value = max(value, self.minimax_value(self.result(state, action), depth - 1, alpha, beta))
                if value >= beta:  # Prune the branch
                    return value
                alpha = max(alpha, value)
        else:  # Minimizing for opponent
            value = float('inf')
            for action in self.actions(state):
                value = min(value, self.minimax_value(self.result(state, action), depth - 1, alpha, beta))
                if value <= alpha:  # Prune the branch
                    return value
                beta = min(beta, value)

        return value


    
    def evaluate(self, state):
        def calculate_final_pit_index(start_pit, seeds, player_turn):
            final_pit = start_pit
            while seeds > 0:
                final_pit += 1
                # Skip opponent's Kalaha
                if (player_turn == 0 and final_pit == 13) or (player_turn == 1 and final_pit == 6):
                    continue
                if final_pit > 13:
                    final_pit = 0  # Loop back to the beginning of the board
                seeds -= 1
            return final_pit
        
        board, player_turn = state
        player_turn -= 1  # Adjusting player_turn to be 0-indexed for consistency

        # Weight factors for evaluation
        kalaha_weight = 5 #gpt siger 2.5 - 5
        pit_weight = 2 #gpt siger 1-2
        extra_turn_weight = 10 #gpt siger 5-10
        capture_weight = 3 #gpt siger 1-3

        # Initialize scores
        player_kalaha_index = 6 if player_turn == 0 else 13
        opponent_kalaha_index = 13 if player_turn == 0 else 6
        player_score = 0
        opponent_score = 0

        # Calculate store scores with weighted value
        player_score += board[player_kalaha_index] * kalaha_weight
        opponent_score += board[opponent_kalaha_index] * kalaha_weight

        # Evaluate seeds on the player's and opponent's sides (excluding stores)
        player_side = range(0, 6) if player_turn == 0 else range(7, 13)
        opponent_side = range(7, 13) if player_turn == 0 else range(0, 6)

        for pit in player_side:
            seeds = board[pit]
            magic_number = 36
            if board[6] + board[13] > magic_number:
                player_score += board[pit] * pit_weight
            # Capture logic
            # Determine the pit where the last stone would land
            final_pit = calculate_final_pit_index(pit, seeds, player_turn)
            can_capture = final_pit in player_side and board[final_pit] == 0 and board[12 - final_pit] > 0
            # Check if final pit is on player's side and would result in a capture
            if can_capture:
                # Add score for potential capture
                player_score += (board[12 - final_pit] + 1) * capture_weight

        # Adding opponent capture logic
        for pit in opponent_side:
            seeds = board[pit]
            magic_number = 50 # Adjust this value based on AI behaviour
            if board[6] + board[13] > magic_number:
                opponent_score += board[pit] * pit_weight
            # Determine the pit where the last stone would land for the opponent
            final_pit_opponent = (pit + board[pit]) % 14
            can_capture = final_pit_opponent in opponent_side and board[final_pit_opponent] == 0 and board[12 - final_pit_opponent] > 0
            # Check if final pit is on opponent's side and would result in a capture
            if can_capture:
                # Subtract score for potential opponent capture from player's perspective
                opponent_score += (board[12 - final_pit_opponent] + 1) * capture_weight

        # Extra turn logic
        for pit in player_side:
            seeds = board[pit]
            if seeds == (player_kalaha_index - pit) % 14:  # Exact count to land in the store
                player_score += extra_turn_weight  # Extra turn possibility

        for pit in opponent_side:
            seeds = board[pit]
            if seeds == (opponent_kalaha_index - pit) % 14:
                opponent_score += extra_turn_weight

        # The final score is the difference between the player's and opponent's scores
        # Positive values favor the player, negative values favor the opponent.
        return player_score - opponent_score

