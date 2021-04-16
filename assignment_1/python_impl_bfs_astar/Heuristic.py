from Utils import validate, unwrap_path, read_files, unwrap_path_costs, arg_parser
from copy import deepcopy
import time

goal = [[int(float(animal)) for animal in bank] for bank in read_files(arg_parser().arguments[1])]

def heuristic_bfs(state):
    path_cost = 0
    
    if state.return_state_as_lists() == goal:
        print("H_BFS: Solution Found!")
        return state

    queue = []
    frontier = []

    queue.append(state)
    frontier.append(state.return_state_as_tuple())
    explored = set()
    
    while queue:
        if not queue:
            print("H_BFS: Failed To Find Solution!")
            return []
        # # chooses the lowest-cost node in frontier
        curr = queue.pop(0)
        frontier.pop(0)
        explored.add(curr.return_state_as_tuple())

        if not validate(curr):
            continue

        path_cost += 1
        for child in heuristic_generate_successors(curr):
            if child.return_state_as_tuple() not in explored and child.return_state_as_tuple() not in frontier:
                # if we find solution, unwrap path and return cost
                if child.return_state_as_lists() ==  goal:
                    return child
                else:
                    queue.append(child)
                    frontier.append(child.return_state_as_tuple())
    return

# perform actions for out generation of successors
def heuristic_move_animals(animal, amount, direction, parent):
    new_state = deepcopy(parent)
    # save link to parent so we can unwrap path
    new_state.prev_state = parent
    new_state.cost += 1
    # if we want to move chicken
    if animal == "chicken":
        # move chicken to right bank
        if direction == "right":
            new_state.move_chicken_right(amount)
        else:
            new_state.move_chicken_left(amount)
    elif animal == "wolf":
        if direction == "right":
            new_state.move_wolf_right(amount)
        else:
            new_state.move_wolf_left(amount)
    # if we want to move both animals at once
    elif animal == "2 chickens 1 wolf":
        if direction == "right":
            new_state.move_wolf_right(amount - 1)
            new_state.move_chicken_right(amount)
        else:
            new_state.move_wolf_left(amount - 1)
            new_state.move_chicken_left(amount)
    else:
        if direction == "right":
            new_state.move_wolf_right(amount)
            new_state.move_chicken_right(amount - 1)
        else:
            new_state.move_wolf_left(amount)
            new_state.move_chicken_left(amount - 1)
    
    new_state.move_boat()
    return new_state

def heuristic_generate_successors( parent):
    neighbors = []
    if parent.right_boat:
        neighbors.append(heuristic_move_animals("chicken", 1, "left", parent))
        # if there are chickens on right bank and # of chickens is greater than # of wolves move 2 chickens
        neighbors.append(heuristic_move_animals("chicken", 2, "left", parent))
        # if there are wolves on right bank, move 1 wolf
        neighbors.append(heuristic_move_animals("wolf", 1, "left", parent))
        # send both animals on the boat
        neighbors.append(heuristic_move_animals("both", 1, "left", parent))
        # if there are wolves on right bank, move 2 wolves
        neighbors.append(heuristic_move_animals("wolf", 2, "left", parent))
        # move 3 chickens to the left bank
        neighbors.append(heuristic_move_animals("chicken", 3, "left", parent))
        # if there are wolves on right bank, move 1 wolf
        neighbors.append(heuristic_move_animals("wolf", 3, "left", parent))
        # send both animals on the boat
        neighbors.append(heuristic_move_animals("2 chickens", 2, "left", parent))
        # if there are wolves on right bank, move 2 wolves
        neighbors.append(heuristic_move_animals("2 wolves", 2, "left", parent))
    
    if parent.left_boat:
        # move 1 chicken to the right
        neighbors.append(heuristic_move_animals("chicken", 1, "right", parent))
        # if there are chickens on right bank and # of chickens is greater than # of wolves move 2 chickens
        neighbors.append(heuristic_move_animals("chicken", 2, "right", parent))
        # if there are wolves on right bank, move 1 wolf
        neighbors.append(heuristic_move_animals("wolf", 1, "right", parent))
        # send both animals on the boat
        neighbors.append(heuristic_move_animals("both", 1, "right", parent))
        # if there are wolves on right bank, move 2 wolves
        neighbors.append(heuristic_move_animals("wolf", 2, "right", parent))
        # move 3 chickens to the right bank
        neighbors.append(heuristic_move_animals("chicken", 3, "right", parent))
        # if there are wolves on right bank, move 1 wolf
        neighbors.append(heuristic_move_animals("wolf", 3, "right", parent))
        # send both animals on the boat
        neighbors.append(heuristic_move_animals("2 chickens 1 wolf", 2, "right", parent))
        # if there are wolves on right bank, move 2 wolves
        neighbors.append(heuristic_move_animals("2 wolves 1 chicken", 2, "right", parent))
    return neighbors
