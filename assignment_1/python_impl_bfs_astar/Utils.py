import argparse
import time

# collect the arguments from the command line and return them
def arg_parser():
        parser = argparse.ArgumentParser(description='Python search_algorithm.py < initial state file > < goal state file > < mode > < output file >')
        parser.add_argument('arguments', metavar='S', type=str, nargs='+',
                            help='Make sure you follow the format "Python search_algorithm.py < initial state file > < goal state file > < mode > < output file >')
        args = parser.parse_args()
        return args

# read start and goal files
def read_files(my_file):
    banks = []
    with open("./test_cases/" + my_file, "r") as f:
        right_bank = [int(number) for number in f.readline().split(',')]
        left_bank = [int(number) for number in f.readline().split(',')]
    banks.append(right_bank)
    banks.append(left_bank)
    f.close()
    return banks

# validate every successor
def validate(state):
    if state.left_chickens < 0 or state.left_wolves < 0 or state.right_chickens < 0 or state.right_wolves < 0:
        return False
    if (state.left_chickens != 0) and state.left_chickens < state.left_wolves:
        return False
    if (state.right_chickens != 0) and state.right_chickens < state.right_wolves:
        return False
    return True

# unwrap paths from goal state
def unwrap_path(state):
    path = []
    if state:
        path = [state.return_state_as_lists()]
        while state.prev_state:
            path.insert(0, state.prev_state.return_state_as_lists())
            state = state.prev_state
    return path[::-1]

# unwrap paths from goal state
def unwrap_path_costs(state):
    path = []
    if state: 
        while state.prev_state != None:
            path.insert(0, state.cost)
            state = state.prev_state
    return path[::-1]

def print_outputs(solution):
    for state in solution:
        print(state)
