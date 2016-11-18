"""Python Cookbook

Chapter 13, recipe 12
"""

import subprocess
class Command:
    def execute(self, options):
        self.command = self.create_command(options)
        results = subprocess.run(self.command,
            check=True, stdout=subprocess.PIPE)
        self.output = results.stdout
        return self.output
    def create_command(self, options):
        return ['echo', self.__class__.__name__, repr(self.options)]

import ch13_r05

class Simulate(Command):
    def __init__(self, seed=None):
        self.seed = seed
    def execute(self, options):
        if self.seed:
            os.environ['RANDOMSEED'] = str(self.seed)
        super().execute(options)
    def create_command(self, options):
        return ['python3', 'ch13_r05.py',
            '--samples', str(options.samples),
            '-o', options.game_file]

import ch13_r06

class Summarize(Command):
    def create_command(self, options):
        return ['python3', 'ch13_r06.py',
            '-o', options.summary_file,
            ] + options.game_files

from argparse import Namespace
import yaml

def demo():
    options = Namespace(samples=100,
        game_file='x12.yaml', game_files=['x12.yaml'],
        summary_file='y12.yaml')
    step1 = Simulate()
    step2 = Summarize()
    output1 = step1.execute(options)
    print(step1.command, output1)
    output2 = step2.execute(options)
    print(step2.command, output2)

    with open('y12.yaml') as report_file:
        report_document = yaml.load(report_file)
    print(report_document)

def process_i(options):
    step1 = Simulate()
    options.game_files = []
    for i in range(options.simulations):
        options.game_file = 'game_{i}.yaml'.format_map(vars())
        options.game_files.append(options.game_file)
        step1.execute(options)
    step2 = Summarize()
    step2.execute(options)

def process_c(options):
    step1 = Simulate()
    step1.execute(options)
    if 'summary_file' in options:
        step2 = Summarize()
        step2.execute(options)


if __name__ == "__main__":
    demo()
    options_i = Namespace(simulations=2, samples=100,
        summary_file='y12.yaml')
    process_i(options_i)
    options_c = Namespace(simulations=2, samples=100, game_file='x.yaml')
    process_c(options_c)
