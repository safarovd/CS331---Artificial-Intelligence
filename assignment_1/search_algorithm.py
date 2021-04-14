import argparse
import re
from collections import defaultdict
from copy import deepcopy

class SearchAlgorithm():

    class State():
        prev_state = None
        def __init__(self, chickens, wolves, boat):
            self.left_chickens = chickens
            self.left_wolves = wolves
            self.right_chickens = 0
            self.right_wolves = 0
            self.left_boat = boat
            self.right_boat = 1 if not boat else 0
            self.prev_state = None
        
        def move_chicken_right(self, amount):
            self.left_chickens -= amount
            self.right_chickens += amount
        
        def move_chicken_left(self, amount):
            self.left_chickens += amount
            self.right_chickens -= amount

        def move_wolf_right(self, amount):
            self.left_wolves -= amount
            self.right_wolves += amount
        
        def move_wolf_left(self, amount):
            self.left_wolves += amount
            self.right_wolves -= amount
        
        def move_boat(self):
            temp = self.left_boat
            self.left_boat = self.right_boat
            self.right_boat = temp
        
        def save_parent_state(self, parent):
            self.prev_state = parent

        def return_state_as_tuple(self):
            return (self.right_chickens,self.right_wolves,self.right_boat,self.left_chickens,self.left_wolves,self.left_boat)

        def return_state_as_lists(self):
            return [[self.right_chickens,self.right_wolves,self.right_boat],[self.left_chickens,self.left_wolves,self.left_boat]]

    def __init__(self):
        parser = argparse.ArgumentParser(description='Python search_algorithm.py < initial state file > < goal state file > < mode > < output file >')
        parser.add_argument('arguments', metavar='S', type=str, nargs='+',
                            help='Make sure you follow the format "Python search_algorithm.py < initial state file > < goal state file > < mode > < output file >')
        args = parser.parse_args()
        
        self.start = [[int(float(animal)) for animal in bank] for bank in self.read_files(args.arguments[0])]
        self.goal = [[int(float(animal)) for animal in bank] for bank in self.read_files(args.arguments[1])]
        self.algorithm = args.arguments[2]
        self.output = args.arguments[3]

        print("Your inputs are: ", args.arguments[0], args.arguments[1], self.algorithm, self.output)

    def read_files(self, my_file):
        banks = []
        with open("./test_cases/" + my_file, "r") as f:
            right_bank = [int(number) for number in f.readline().split(',')]
            left_bank = [int(number) for number in f.readline().split(',')]
        banks.append(right_bank)
        banks.append(left_bank)
        f.close()
        print(banks)
        return banks

    def process_algorithms(self):
        if self.algorithm == "bfs":
            print("Executing Breadth-First Serach Algorithm...")
            solution = self.bfs()
        else:
            print("Executing <TBD> Algorithm...")
        if solution:
            f = open(self.output, "w")
            for state in solution:
                f.write(str(state) + "\n")
            f.close()

    def move_animals(self, animal, amount, direction, parent):
        new_state = deepcopy(parent)
        # save link to parent
        new_state.prev_state = parent
        
        if animal == "chicken":
            if direction == "right":
                new_state.move_chicken_right(amount)
            else:
                new_state.move_chicken_left(amount)
        elif animal == "wolf":
            if direction == "right":
                new_state.move_wolf_right(amount)
            else:
                new_state.move_wolf_left(amount)
        else:
            if direction == "right":
                new_state.move_wolf_right(amount)
                new_state.move_chicken_right(amount)
            else:
                new_state.move_wolf_left(amount)
                new_state.move_chicken_left(amount)
        
        new_state.move_boat()
        return new_state


    def generate_successors(self, parent):
        neighbors = []
        
        if parent.right_boat:
            if parent.right_chickens > 0:
                neighbors.append(self.move_animals("chicken", 1, "left", parent))
            # if there are chickens on right bank and # of chickens is greater than # of wolves move 2 chickens
            if parent.right_chickens > 1:
                neighbors.append(self.move_animals("chicken", 2, "left", parent))
            # if there are wolves on right bank, move 1 wolf
            if parent.right_wolves > 0:
                neighbors.append(self.move_animals("wolf", 1, "left", parent))
            
            if (parent.right_chickens == parent.right_wolves) and (parent.right_chickens and parent.right_wolves):
                neighbors.append(self.move_animals("both", 1, "left", parent))
            # if there are wolves on right bank, move 2 wolves
            if parent.right_wolves > 1:
                neighbors.append(self.move_animals("wolf", 2, "left", parent))

        if parent.left_boat:
            if parent.left_chickens > 0:
                neighbors.append(self.move_animals("chicken", 1, "right", parent))
            # if there are chickens on left bank and # of chickens is greater than # of wolves move 2 chickens
            if parent.left_chickens > 1:
                neighbors.append(self.move_animals("chicken", 2, "right", parent))
            # if there are wolves on left bank, move 1 wolf
            if parent.left_wolves > 0:
                neighbors.append(self.move_animals("wolf", 1, "right", parent))
            # Put both animals in the boat
            if (parent.left_chickens == parent.left_wolves) and (parent.left_chickens and parent.left_wolves):
                neighbors.append(self.move_animals("both", 1, "right", parent))
            # if there are wolves on left bank, move 2 wolves
            if parent.left_wolves > 1:
                neighbors.append(self.move_animals("wolf", 2, "right", parent))

        return neighbors

    def unwrap_path(self, state):
        path = [state.return_state_as_lists()]
        while state.prev_state:
            path.append(state.prev_state.return_state_as_lists())
            state = state.prev_state
        print(len(path))
        return path[::-1]
    
    def bfs(self):
        state = self.State(self.start[1][0], self.start[1][1], self.start[1][2])
        path_cost = 0
        
        if state.return_state_as_lists() == self.goal:
            print("BFS: Solution Found!")
            return self.unwrap_path(state)

        frontier = []
        frontier.append(state)
        explored = set()
        
        while frontier:

            if not frontier:
                print("BFS: Failed To Find Solution!")
                return []

            curr = frontier.pop(0)
            if curr.return_state_as_lists() == self.goal:
                print("BFS: Solution Found!")
                return self.unwrap_path(curr)

            if (curr.left_chickens != 0) and curr.left_chickens < curr.left_wolves:
                print("Skip: ", curr.return_state_as_lists())
                continue
            if (curr.right_chickens != 0) and curr.right_chickens < curr.right_wolves:
                print("Skip: ", curr.return_state_as_lists())
                continue

            path_cost += 1
            explored.add(curr.return_state_as_tuple())
            successors = self.generate_successors(curr)
            for child in successors:
                if child.return_state_as_tuple() not in explored:
                    print(child.return_state_as_lists())
                    # if child.return_state_as_lists() == self.goal:
                    #     print("BFS: Solution Found!")
                    #     return self.unwrap_path(child)
                    frontier.append(child)
        print("**EXIT BFS LOOP")


if __name__ == "__main__":
    SearchAlgorithm().process_algorithms()

