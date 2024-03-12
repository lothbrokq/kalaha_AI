import random

class KalahaAI:
    def __init__(self, game):
        self.game = game
    
    def current_state(self):
        return self.game.get_board(), self.game.get_current_player()
    
    def player(self, state):
        return state[1]
    
    def board(self, state):
        board = state
        print("We are getting the board", board)
        return state[0]

    #Given a state, returns an integer that corresponds to the pit that makes the best move 
    def choose_move(self):
        print("AI is thinking...")
        state = self.current_state()

        best_move = None
        best_score = float("-inf") if self.player(state) == 2 else float("inf")

        for action in self.actions(state):
            result_state = self.result(state, action)
            print("this is result state", result_state)
            score = self.minimax(result_state)
            if (self.player(state) == 2 and score > best_score) or (self.player(state) == 1 and score < best_score):
                best_score = score
                best_move = action

        return best_move

    #returns a list of integers corresponding to applicable move in the current state
    def actions(self, state):
        # Since we assume AI is always player 2, we check pits 7-12
        board = self.board(state)
        print("this is the board", board)
        return [i for i in range(7, 13) if board[i] > 0]
    

    #returns the resulting state given a state and an action
    def result(self, state, action):
        new_board = self.board(state).copy()
        new_board, extra_turn = self.game.make_move(new_board, action)
        if extra_turn:
            return new_board, self.player(state)
        else:
            player = 1 if self.player(state) == 2 else 2
            return new_board, player
    
    #returns a bool determning whether the game is over given a state
    def terminal_test(self, state):
        return self.game.is_game_over(self.board(state))
    
    #given a terminal state returns the utility of the state
    def utility(self, state):
        return self.translate_winner(self.game.get_winner(state[0]))

    def translate_winner(self, player):
        if player == 1:
            return -1
        elif player == 2:
            return 1 
        else:
            return 0

    def minimax(self, state, max_depth):
        if max_depth == 0:
            return 
        print("minimax is really thinking hard")
        if self.terminal_test(state):
            return self.utility(state)
        elif self.player(state) == 2:
            return max([self.minimax(self.result(state, action)) for action in self.actions(state)])
        elif self.player(state) == 1:
            return min([self.minimax(self.result(state, action)) for action in self.actions(state)])
        else:
            print("ERROR IN MINIMAX")


        