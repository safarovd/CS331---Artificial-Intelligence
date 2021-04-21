'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import math
import copy

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)

class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
    # calls decisions and passes into it potential moves
    def get_move():
        return
    
    # which way we want to go
    def minimax_decision(self, board_state):
        return max()

    def minimax_max_value(self, board_state, depth):
        if (self.terminal_test(board_state, depth)):
            utility(board_state)
        value = -math.inf
        # make max player one
        player = board_state.p1_symbol
        for action in generate_successors(state, player):
            value = max(value, self.minimax_min_value(action, depth-1))
        return value

    def minimax_min_value(self, board_state, depth):
        if (self.terminal_test(board_state, depth)):
            utility(board_state)
        value = math.inf
        # make min player player two
        player = board_state.p2_symbol
        for action in generate_successors(state, player):
            value = min(value, self.minimax_max_value(action, depth-1))
        return value

    # terminal state has been found when neither players can make any further moves
    def terminal_test(self, board, depth):
        if (!board.has_legal_moves_remaining(board.p1_symbol) and board.has_legal_moves_remaining(board.p2_symbol)) or (depth >= 5):
            return True #leaf node
        else:
            return False #not a leaf node

    # return the weight of every move minimax can make
    # positive weight: more player one pieces on the board 
    # negative weight: more player two pieces on the board 
    def utility(self, board):
        int weight = board.count_score(board.p1_symbol) - board.count_score(board.p2_symbol)
        return weight

    def generate_successors(self, current_board_state, current_player):
        successors = []
        row, col = 0, 0

        for row in range(0, 4):
            for col in range(0, 4):
                if (current_board_state.is_legal_move(row, col, current_player)):
                    successor = copy.deepcopy(current_board_state)
                    successors.append(successor)
                    successors[-1].play_move(col, row, current_player)
        return successors

        