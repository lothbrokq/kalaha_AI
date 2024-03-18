import copy

class KalahaAI:
    def __init__(self, game):
        self.game = game

    def get_state(self):
        return self.game.get_board(), self.game.get_current_player()

    def choose_move(self, depth=12): 
        state = self.get_state()
        best_score = float('-inf')
        best_move = None
        for action in self.actions(state):
            simulated_state = self.result(state, action)
            score = self.minimax_value(simulated_state, depth - 1, float('-inf'), float('inf'))  
            print(f"AI evaluated move {action} with score {score}")
            if score > best_score:
                best_score = score
                best_move = action
        print(f"AI chooses pit {best_move} with a score of {best_score}")
        return best_move

    def actions(self, state):
        valid_moves = []
        board = state[0]
        start, end = (7, 13) if self.game.get_current_player() == 2 else (0, 6)
        for pit_index in range(start, end):
            if board[pit_index] > 0:  # A move is legal if there is stones in the pit
                valid_moves.append(pit_index)
        return valid_moves

    def result(self, state, action):
        board = state[0]
        new_board, extra_turn = self.game.make_move(copy.deepcopy(board), action)
        if extra_turn:
            new_state = new_board, state[1]
        else:
            next_player = 1 if state[1] == 2 else 2
            new_state = new_board, next_player
        return new_state

    def terminal_test(self, state):
        board  = state[0]
        return self.game.is_game_over(board)

    def utility(self, state):
        board = state[0]
        # Assuming AI is player 2
        if self.game.is_game_over(board):
            winner = self.game.get_winner(board)
            if winner == 2:
                return 1  # AI win
            elif winner == 1:
                return -1  # AI loss
            else:
                return 0  # Draw
        return 0  # Non-terminal state, should not be called
    
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
        kalaha_weight = 5
        pit_weight = 2
        extra_turn_weight = 10
        capture_weight = 3 

        player_kalaha_index = 6 if player_turn == 0 else 13
        opponent_kalaha_index = 13 if player_turn == 0 else 6
        player_score = 0
        opponent_score = 0

        player_score += board[player_kalaha_index] * kalaha_weight
        opponent_score += board[opponent_kalaha_index] * kalaha_weight

        player_side = range(0, 6) if player_turn == 0 else range(7, 13)
        opponent_side = range(7, 13) if player_turn == 0 else range(0, 6)

        #Evaluate captures
        for pit in player_side:
            seeds = board[pit]
            inactive_stones = 50
            if board[6] + board[13] > inactive_stones:
                player_score += board[pit] * pit_weight
            final_pit = calculate_final_pit_index(pit, seeds, player_turn)
            can_capture = final_pit in player_side and board[final_pit] == 0 and board[12 - final_pit] > 0

            if can_capture:
                player_score += (board[12 - final_pit] + 1) * capture_weight

        for pit in opponent_side:
            seeds = board[pit]
            inactive_stones = 50
            if board[6] + board[13] > inactive_stones:
                opponent_score += board[pit] * pit_weight

            opponent_turn = 1 if player_turn == 0 else 0
            final_pit_opponent = calculate_final_pit_index(pit, seeds, opponent_turn)
            can_capture = final_pit_opponent in opponent_side and board[final_pit_opponent] == 0 and board[12 - final_pit_opponent] > 0

            if can_capture:
                opponent_score += (board[12 - final_pit_opponent] + 1) * capture_weight

        #Evaluate extra turns
        for pit in player_side:
            seeds = board[pit]
            if seeds == (player_kalaha_index - pit) % 14:
                player_score += extra_turn_weight 

        for pit in opponent_side:
            seeds = board[pit]
            if seeds == (opponent_kalaha_index - pit) % 14:
                opponent_score += extra_turn_weight

        return player_score - opponent_score

