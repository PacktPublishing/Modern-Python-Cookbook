"""Python Cookbook

Chapter 13, recipe 9
"""
from pathlib import Path
import sys

class Command:
    def execute(self, options):
        pass

import ch13_r05
class Simulate(Command):
    def __init__(self, seed=None):
        self.seed = seed
    def execute(self, options):
        self.game_path = Path(options.game_file)
        data = ch13_r05.roll_iter(options.games, self.seed)
        ch13_r05.write_rolls(self.game_path, data)

import ch13_r06
class Summarize(Command):
    def execute(self, options):
        self.summary_path = Path(options.summary_file)
        with self.summary_path.open('w') as result_file:
            ch13_r06.process_all_files(result_file, options.game_files)

import ch13_r07
class SimSum(Command):
    def __init__(self, seed=None):
        self.seed = seed
    def execute(self, options):
        data = ch13_r05.roll_iter(self.games, self.seed)
        game_statistics = ch13_r06.gather_stats(data)
        print(game_statistics)


import argparse
def get_options(argv):
    parser = argparse.ArgumentParser(prog='craps')
    subparsers = parser.add_subparsers()
    simulate_parser = subparsers.add_parser('simulate')
    simulate_parser.add_argument('-g', '--games', type=int, default=100000)
    simulate_parser.add_argument('-o', '--output', dest='game_file')
    simulate_parser.set_defaults(command=Simulate)

    summarize_parser = subparsers.add_parser('summarize')
    summarize_parser.add_argument('-o', '--output', dest='summary_file')
    summarize_parser.add_argument('game_files', nargs='*')
    summarize_parser.set_defaults(command=Summarize)

    simsum_parser = subparsers.add_parser('simsum')
    simsum_parser.add_argument('-g', '--games', type=int, default=100000)
    simsum_parser.add_argument('-o', '--output', dest='summary_file')
    simsum_parser.set_defaults(command=SimSum)

    options = parser.parse_args(argv)
    if 'command' not in options:
        parser.print_help()
        sys.exit(2)
    return options

def main():
    options = get_options(sys.argv[1:])
    if options.command is None:
        print("")
    command = options.command(options)
    command.execute()

def demo():
    ex1 = get_options(['simulate', '-g', '100', '-o', 'x.yaml'])
    print(ex1)
    command = ex1.command()
    command.execute(ex1)

    ex2 = get_options(['summarize', '-o', 'y.yaml', 'x.yaml'])
    print(ex2)
    command = ex2.command()
    command.execute(ex2)

    ex3 = get_options(['simsum', '-g', '100', '-o', 'y.yaml'])
    print(ex3)
    command = ex3.command()
    command.execute(ex3)

if __name__ == "__main__":
    main()
