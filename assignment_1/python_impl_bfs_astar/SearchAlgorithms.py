##############################################
# Collaborators: Daniel Safarov and Caden Burke
# Date: 4/13/2021
# Assignment 1
# Algorithms: Breadth First Search, Deapth First Search
################################################

import argparse
from copy import deepcopy
import sys
from State import State
from Utils import validate, unwrap_path, read_files, unwrap_path_costs, arg_parser, print_outputs
from heapq import heapify, heapreplace, heappop, heappush
import heapq
from collections import defaultdict
import Heuristic
import time

sys.setrecursionlimit(100000)

class SearchAlgorithm():
    # defualt constructer for SearchAlgorithms class. Defines and initializes our start and goal states and determines the algorithm we want and output file
    def __init__(self):
        args = arg_parser()
        self.start = [[int(float(animal)) for animal in bank] for bank in read_files(args.arguments[0])]
        self.goal = [[int(float(animal)) for animal in bank] for bank in read_files(args.arguments[1])]
        self.algorithm = args.arguments[2]
        self.output = args.arguments[3]
        print("Your inputs are: ", args.arguments[0], args.arguments[1], self.algorithm, self.output)

    # call correct algorithms
    def process_algorithms(self):
        solution = None
        # run BFS algorithm
        if self.algorithm == "bfs":
            solution, path = self.bfs()
            print("The solution using BFS is: ")
            print_outputs(solution)
            print("The number of expantions performed using BFS are: ", path)
            print("The path cost using BFS is: ", len(solution)-1)
        # run A* algorithm
        elif self.algorithm == "astar":
            solution, path = self.a_star()
            print("The solution using A* is: ")
            print_outputs(solution)
            print("The number of expantions performed using A* are: ", path)
            print("The path cost using A* is: ", len(solution)-1)
        # run heuristic algorithm for fun
        elif self.algorithm == "heuristic":
            s = Heuristic.heuristic_bfs(State(self.start[1][0], self.start[1][1], self.start[1][2]))
            print("The solution using the Heuristic BFS is: ")
            print("The optimistic path cost by moving up to 3 animals at a time is: ", s.cost)
        # write the solution to output.txt file
        if solution:
            f = open(self.output, "w")
            for state in solution:
                f.write(str(state) + "\n")
            f.close()

    # perform actions for out generation of successors
    def move_animals(self, animal, amount, direction, parent):
        # make sure to deep copy the parent so we don't overwrite the members within the parent and create a successor
        new_state = deepcopy(parent)
        # save link to parent so we can unwrap path at goal discovery
        new_state.prev_state = parent
        new_state.cost += 1
        
        # if we want to move chicken
        if animal == "chicken":
            # move chicken to right bank or left
            if direction == "right":
                new_state.move_chicken_right(amount)
            else:
                new_state.move_chicken_left(amount)
        elif animal == "wolf":
            # move wolf to right bank or left
            if direction == "right":
                new_state.move_wolf_right(amount)
            else:
                new_state.move_wolf_left(amount)
        # if we want to move both animals at once
        else:
            if direction == "right":
                new_state.move_wolf_right(amount)
                new_state.move_chicken_right(amount)
            else:
                new_state.move_wolf_left(amount)
                new_state.move_chicken_left(amount)
        # return successor
        new_state.move_boat()
        return new_state

    # generate all possible successors (specify every scenario)
    def generate_successors(self, parent):
        neighbors = []
        if parent.right_boat:
            neighbors.append(self.move_animals("chicken", 1, "left", parent))
        # if there are chickens on right bank and # of chickens is greater than # of wolves move 2 chickens
            neighbors.append(self.move_animals("chicken", 2, "left", parent))
        # if there are wolves on right bank, move 1 wolf
            neighbors.append(self.move_animals("wolf", 1, "left", parent))
        # send both animals on the boat
            neighbors.append(self.move_animals("both", 1, "left", parent))
        # if there are wolves on right bank, move 2 wolves
            neighbors.append(self.move_animals("wolf", 2, "left", parent))
        
        if parent.left_boat:
            neighbors.append(self.move_animals("chicken", 1, "right", parent))
            # if there are chickens on left bank and # of chickens is greater than # of wolves move 2 chickens
            neighbors.append(self.move_animals("chicken", 2, "right", parent))
            # if there are wolves on left bank, move 1 wolf
            neighbors.append(self.move_animals("wolf", 1, "right", parent))
            # Put both animals in the boat
            neighbors.append(self.move_animals("both", 1, "right", parent))
            # if there are wolves on left bank, move 2 wolves
            neighbors.append(self.move_animals("wolf", 2, "right", parent))
        return neighbors

    def bfs(self):
        state = State(self.start[1][0], self.start[1][1], self.start[1][2])
        path_cost = 0
        queue = []
        frontier = []

        if state.return_state_as_lists() == self.goal:
            print("BFS: Solution Found!")
            return unwrap_path(state), path_cost

        queue.append(state)
        frontier.append(state.return_state_as_tuple())
        explored = set()
        while queue:
            if not queue:
                print("BFS: Failed To Find Solution!")
                return [[],[]], path_cost
            # chooses the lowest-cost node in frontier
            curr = queue.pop(0)
            frontier.pop(0)
            explored.add(curr.return_state_as_tuple())
            # make sure none of the rules are being broken, if so, skip current state
            if not validate(curr):
                continue

            path_cost += 1
            for child in self.generate_successors(curr):
                if child.return_state_as_tuple() not in explored and child.return_state_as_tuple() not in frontier:
                    # if we find solution, unwrap path and return cost
                    if child.return_state_as_lists() == self.goal:
                        print("BFS: Solution Found!")
                        return unwrap_path(child), path_cost
                    else:
                        queue.append(child)
                        frontier.append(child.return_state_as_tuple())
        print("BFS: Exit loop")

    def a_star(self):
        state = State(self.start[1][0], self.start[1][1], self.start[1][2])
        path_cost = 0
        
        if state.return_state_as_lists() == self.goal:
            print("A*: Solution Found!")
            return unwrap_path(state), path_cost
        
        # my heap for prioritizing states using priority cost
        heap = [(state.cost + state.heuristic(), state)]
        heapify(heap)
        # create a frontier dictionary for keeping track of the states we have stored in heap. 
        # We can track this by using the state tuples as a key for (used in later conditionals - line: 200) 
        frontier = {}
        frontier[state.return_state_as_tuple()] = (state.cost + state.heuristic_cost, state)
        # explored set so we don't revisit already explanded nodes
        explored = set()
        while heap:
            if not heap:
                print("A*: Failed To Find Solution!")
                return [[],[]], path_cost
            # chooses the lowest-cost node in frontier
            curr = heappop(heap)
            # pop off the state. Remeber we push onto the heap a tuple (0:path_cost, 1:state, 2:state_values_as_tuple).
            frontier.pop(curr[1].return_state_as_tuple(), None)
            # if we find solution, unwrap path and return cost
            if curr[1].return_state_as_lists() == self.goal:
                print("A*: Solution Found!")
                return unwrap_path(curr[1]), path_cost

            explored.add(curr[1].return_state_as_tuple())

            if not validate(curr[1]):
                continue

            path_cost += 1
            for child in self.generate_successors(curr[1]):
                if child.return_state_as_tuple() not in explored and child.return_state_as_tuple() not in frontier:
                    child.heuristic()          
                    heappush(heap, (child.cost + child.heuristic_cost, child))
                    frontier[child.return_state_as_tuple()] = (child.cost + child.heuristic_cost, child)
                # remember we store the value for the frontier as a tuple as well {state_values: (0:path_cost, 1:state)}
                elif child.return_state_as_tuple() in frontier and frontier[child.return_state_as_tuple()][0] > child.cost + child.heuristic_cost:
                    # remove the old state from heap. This procedure turns heap back into standard list
                    heap.remove(frontier[child.return_state_as_tuple()])
                    # remove the state from the frontier tracker too
                    frontier.pop(child.return_state_as_tuple(), None)
                    # turn heap list back into a heap
                    heapify(heap)
                    heappush(heap, (child.cost + child.heuristic_cost, child))
        print("A*: Exit loop")
        return
# pretend this is int main()
if __name__ == "__main__":
    SearchAlgorithm().process_algorithms()
