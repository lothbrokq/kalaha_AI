import copy

class KalahaAI:
    def __init__(self, game, player_number):
        self.game = game
        self.player_number = player_number  # Player number to make AI adaptable for both players

    def get_state(self):
        # Fetch the current game state and the AI's player number
        return self.game.get_board(), self.player_number

    def choose_move(self, depth=12):
        state = self.get_state()
        best_score = float('-inf')
        best_move = None
        for action in self.actions(state):
            simulated_state = self.result(state, action)
            score = self.minimax_value(simulated_state, depth - 1, float('-inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    def actions(self, state):
        # Return legal moves for the current player from the state
        valid_moves = []
        board, player = state
        start, end = (7, 13) if player == 2 else (0, 6)
        for pit_index in range(start, end):
            if board[pit_index] > 0:
                valid_moves.append(pit_index)
        return valid_moves

    def result(self, state, action):
        # Simulate the move and return the new state
        board, player = copy.deepcopy(state[0]), state[1]
        new_board, extra_turn, _ = self.game.make_move(action, simulate=True)
        if not extra_turn:
            player = 1 if state[1] == 2 else 2  # Logic to potentially switch players based on simulation result
        else:
            player = state[1]  # Maintain the same player if extra turn is granted
        return (new_board, player)
    
    def terminal_test(self, state):
        # Check if the game is over for the given state
        board = state[0]
        return self.game.is_game_over()

    def utility(self, state):
        board, player = state
        if self.game.is_game_over(board):
            winner = self.game.get_winner_based_on_state(board)
            if winner == player:
                return 1  # AI win
            elif winner != 'Tie' and winner != player:
                return -1  # AI loss
            else:
                return 0  # Draw
        return 0  # Non-terminal state

    def minimax_value(self, state, depth, alpha, beta):
        if self.terminal_test(state) or depth == 0:
            return self.evaluate(state)

        if state[1] == self.player_number:  # Maximizing for AI
            value = float('-inf')
            for action in self.actions(state):
                value = max(value, self.minimax_value(self.result(state, action), depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut-off
            return value
        else:  # Minimizing for the opponent
            value = float('inf')
            for action in self.actions(state):
                value = min(value, self.minimax_value(self.result(state, action), depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
            return value

    def evaluate(self, state):
        board, player_turn = state

        # Define player and opponent Kalaha indexes based on player_turn
        player_kalaha_index = 6 if player_turn == 1 else 13
        opponent_kalaha_index = 13 if player_turn == 1 else 6

        # Initialize evaluation scores
        player_score = 0
        opponent_score = 0

        # Apply weight factors
        kalaha_weight = 5
        pit_weight = 2
        extra_turn_weight = 10
        capture_weight = 3

        # Kalaha scores
        player_score += board[player_kalaha_index] * kalaha_weight
        opponent_score += board[opponent_kalaha_index] * kalaha_weight

        # Define player and opponent sides of the board
        if player_turn == 1:
            player_side = range(0, 6)
            opponent_side = range(7, 13)
        else:
            player_side = range(7, 13)
            opponent_side = range(0, 6)

        for pit in player_side:
            seeds = board[pit]
            player_score += seeds * pit_weight  # Evaluate seeds in pits

            final_pit = self.calculate_final_pit_index(pit, seeds, player_turn)
            can_capture = final_pit in player_side and board[final_pit] == 1 and board[12 - final_pit] > 0
            if can_capture:
                player_score += (board[12 - final_pit] + 1) * capture_weight

        for pit in opponent_side:
            seeds = board[pit]
            opponent_score += seeds * pit_weight  # Optionally evaluate opponent seeds

        # Extra turn logic for player
        for pit in player_side:
            if board[pit] == (player_kalaha_index - pit) % 14 or board[pit] == 14 + (player_kalaha_index - pit) % 14:
                player_score += extra_turn_weight

        # Subtract opponent potential score from player's perspective
        return player_score - opponent_score

    def calculate_final_pit_index(self, start_pit, seeds, player_turn):
        final_pit = start_pit
        while seeds > 0:
            final_pit += 1
            if final_pit == 14:
                final_pit = 0
            if player_turn == 1 and final_pit == 13:
                continue
            elif player_turn == 2 and final_pit == 6:
                continue
            seeds -= 1
        return final_pit

