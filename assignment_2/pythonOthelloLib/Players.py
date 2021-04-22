'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import math
import copy
import sys

sys.setrecursionlimit(100000)

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
    
    # calls decisions and passes into it intial state
    def get_move(self, board):
        return self.minimax_decision(board)
    
    # which way we want to go
    def minimax_decision(self, board_state):
        if self.symbol == board_state.p2_symbol:
            _, action = self.minimax_max_value(board_state)
        else:
            _, action = self.minimax_min_value(board_state)
        return action.move

    def minimax_max_value(self, board_state):
        if (self.terminal_test(board_state)):
            print("terminal")
            return self.utility(board_state), board_state
        value = -999999
        best_value = -999999
        best_action = board_state
        successors = self.generate_successors(board_state)
        for successor in successors:
            value, action = self.minimax_min_value(successor)
            if best_value <= value:
                best_value = value
                best_action = action
        # print("max best: ", best_action.move)
        # print("max best value: ", best_value)
        # print("max invalid: ", best_action.invalid_moves)
        # self.p_successors(successors)
        return best_value, best_action 

    def minimax_min_value(self, board_state):
        if (self.terminal_test(board_state)):
            print("terminal")
            return self.utility(board_state), board_state
        value = 999999
        best_value = 999999
        best_action = board_state
        successors = self.generate_successors(board_state)
        for successor in successors:
            value, action = self.minimax_max_value(successor)
            if best_value >= value:
                best_value = value
                best_action = action
        # print("min best: ", best_action.move)
        # print("min invalid: ", best_action.invalid_moves)
        # self.p_successors(successors)
        return best_value, best_action

    # terminal state has been found when neither players can make any further moves
    def terminal_test(self, board):
        if (not board.has_legal_moves_remaining(self.symbol)) and (not board.has_legal_moves_remaining(self.oppSym)):
            return True #leaf node
        else:
            return False #not a leaf node

    # return the weight of every move minimax can make
    # positive weight: more player two pieces on the board 
    # negative weight: more player onme pieces on the board 
    def utility(self, board):
        # weights = [[1000, -10, -10, 1000],
        #            [-10, -5, -5, -10],
        #            [-10, -5, -5, -10],
        #            [1000, -10, -10, 1000]]
        # board.val = weights[board.move[1]][board.move[0]]
        # weight = weights[board.move[1]][board.move[0]]
        # print("weight: ", weight)
        weight = board.count_score(self.symbol) - board.count_score(self.oppSym)
        board.val = weight
        return weight

    def generate_successors(self, current_board_state):
        successors = []
        for col in range(0, 4):
            for row in range(0, 4):
                # print("set: ", current_board_state.invalid_moves)
                if (current_board_state.is_legal_move(col, row, self.symbol) and (col, row) not in current_board_state.invalid_moves):
                # if current_board_state.is_legal_move(col, row, self.symbol):
                    # print(current_board_state.display())
                    # print("current player: ", current_player)
                    # print("1 move: ", (col, row))
                    successor = copy.deepcopy(current_board_state)
                    successors.append(successor)
                    successors[-1].play_move(col, row, self.symbol)
                    successors[-1].move = (col, row)
        return successors

    def p_successors(self, s):
        for a in s:
            print(a.move)

        