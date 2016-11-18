"""Python Cookbook

Chapter 13, recipe 8
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
        print("Created", self.game_path)

import ch13_r06

class Summarize(Command):
    def execute(self, options):
        self.summary_path = Path(options.summary_file)
        with self.summary_path.open('w') as result_file:
            ch13_r06.process_all_files(result_file, options.game_files)

class Sequence(Command):
    def __init__(self, *commands):
        self.commands = [command() for command in commands]
    def execute(self, options):
        for command in self.commands:
            command.execute(options)

class SimSum(Sequence):
    def __init__(self):
        super().__init__(Simulate, Summarize)
    def execute(self, options):
        new_namespace = Namespace(
            game_file='x.yaml',
            game_files=['x.yaml'],
            **vars(options)
        )
        super().execute(new_namespace)

from argparse import Namespace
def main():
    options_1 = Namespace(games=100, game_file='x.yaml')
    command1 = Simulate()
    command1.execute(options_1)

    options_2 = Namespace(summary_file='y.yaml', game_files=['x.yaml'])
    command2 = Summarize()
    command2.execute(options_2)

    options = Namespace(games=100, game_file='x.yaml',
        summary_file='y.yaml', game_files=['x.yaml']
    )
    both_command = Sequence(Simulate, Summarize)
    both_command.execute(options)

    better_options = Namespace(games=100, summary_file='y.yaml')
    sim_sum_command = SimSum()
    sim_sum_command.execute(better_options)

if __name__ == "__main__":
    main()
