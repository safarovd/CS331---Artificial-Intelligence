import argparse

class SearchAlgorithm():

    def __init__(self):
        parser = argparse.ArgumentParser(description='Python search_algorithm.py < initial state file > < goal state file > < mode > < output file >')
        parser.add_argument('arguments', metavar='S', type=str, nargs='+',
                            help='Make sure you follow the format "Python search_algorithm.py < initial state file > < goal state file > < mode > < output file >')
        args = parser.parse_args()

        self.start = args.arguments[0]
        self.goal = args.arguments[1]
        self.algorithm = args.arguments[2]
        self.output = args.arguments[3]

        print("Your inputs are: ", self.start, self.goal, self.algorithm, self.output)

    def process_arguments(self):
        if self.algorithm == "bfs":
            print("Executing Breadth-First Serach Algorithm...")
            solution = self.bfs()
        else:
            print("Executing <TBD> Algorithm...")
        
        f = open(self.output, "w")
        f.write(solution)
        f.close()
    
    def bfs(self):
        return "Hello World"


if __name__ == "__main__":
    SearchAlgorithm().process_arguments()

