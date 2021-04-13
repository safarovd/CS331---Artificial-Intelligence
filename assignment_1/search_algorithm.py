import argparse

class SearchAlgorithm():

    def arg_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument("echo", help="echo the string you use here")
        args = parser.parse_args()
        print(args.echo)
                
SearchAlgorithm.arg_parse()