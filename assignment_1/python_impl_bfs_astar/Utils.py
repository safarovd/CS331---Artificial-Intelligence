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
    path = [state.return_state_as_lists()]
    solution = []
    while state.prev_state:
        path.append(state.prev_state.return_state_as_lists())
        state = state.prev_state
    for s in path[::-1]:
        solution.append(list(reversed(s)))
    return solution