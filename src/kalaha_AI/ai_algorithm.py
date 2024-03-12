import random

class KalahaAI:
    def __init__(self, game):
        self.game = game
    
    def current_state(self):
        """
        current_state[0] = board
        current_state[1] = current player
        """
        return self.game.get_board(), self.game.current_player()

    # def choose_move(self):
    #     board = self.game.get_board()
    #     valid_moves = self.actions(board)
    #     return random.choice(valid_moves) if valid_moves else -1

    def choose_move(self):
        print("AI is thinking...")
        board = self.game.get_board()
        valid_moves = self.actions(board)
        best_move = valid_moves[0]
        best_value = float('-inf')
        for move in valid_moves:
            print("I am thinking... hmm")
            result = self.result(board, move)
            value = self.minimax(result)
            if value > best_value:
                best_value = value
                best_move = move
        print("Hah! I choose pit", best_move)
        return best_move

    def actions(self, board):
        # Since we assume AI is always player 2, we check pits 7-12
        return [i for i in range(7, 13) if board[i] > 0]
    
    def result(self, board, action):
        new_board = board.copy()
        new_board, extra_turn = self.game.make_move(new_board, action)
        if extra_turn:
            return new_board, 2
        else:
            return new_board, 1
    
    def terminal_test(self, board):
        return self.game.is_game_over(board)
    
    def utility(self, state):
        return self.translate_winner(self.game.get_winner(state[0]))

    def translate_winner(self, player):
        if player == 1:
            return -1
        elif player == 2:
            return 1 
        else:
            return 0
        
    def minimax(self, state):
        if self.terminal_test(state):
            return self.utility(state)
        elif state[1] == 2:
            return max(self.minimax(self.result(state[0], action) for action in self.actions(state[0])))
        else:
            return min(self.minimax(self.result(state[0], action) for action in self.actions(state[0])))
        