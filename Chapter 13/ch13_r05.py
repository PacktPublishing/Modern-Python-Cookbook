"""Python Cookbook

Chapter 13, recipe 5
"""
import random
import yaml
from collections import namedtuple, Counter
from pathlib import Path
import argparse
import os
import sys

def write_rolls(output_path, roll_iterator):
    face_count = Counter()
    with output_path.open('w') as output_file:
        for roll in roll_iterator:
            output_file.write(
                yaml.dump(
                    roll,
                    default_flow_style=True,
                    explicit_start=True))
            for dice in roll:
                face_count[sum(dice)] += 1
    return face_count

def summarize(configuration, counts):
    print(configuration)
    print(counts)

Roll = namedtuple('Roll', ('faces', 'total'))
def roll(n=2):
    faces = list(random.randint(1, 6) for _ in range(n))
    total = sum(faces)
    return Roll(faces, total)

def craps_game():
    come_out = roll()
    if come_out.total in [2, 3, 12]:
        return [come_out.faces]
    elif come_out.total in [7, 11]:
        return [come_out.faces]
    elif come_out.total in [4, 5, 6, 8, 9, 10]:
        sequence = [come_out.faces]
        next = roll()
        while next.total not in [7, come_out.total]:
            sequence.append(next.faces)
            next = roll()
        sequence.append(next.faces)
        return sequence
    else:
        raise Exception("Horrifying Logic Bug")

def roll_iter(total_games, seed=None):
    random.seed(seed)
    for i in range(total_games):
        sequence = craps_game()
        yield sequence

def get_options(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--samples', type=int)
    parser.add_argument('-o', '--output')
    options = parser.parse_args(argv)

    if options.output is None:
        sys.exit("No output file specified")

    options.output_path = Path(options.output)

    if "RANDOMSEED" in os.environ:
        seed_text = os.environ["RANDOMSEED"]
        try:
            options.seed = int(seed_text)
        except ValueError:
            sys.exit("RANDOMSEED={0!r} isn't a valid seed value".format(seed_text))
    else:
        options.seed = None
    return options

def main():
    options = get_options(sys.argv[1:])
    face_count = write_rolls(options.output_path, roll_iter(options.samples, options.seed))
    summarize(options, face_count)

import unittest

class GIVEN_ch13_r05_WHEN_run_app_THEN_output(unittest.TestCase):
    def setUp(self):
        self.data_path = Path("ch13_r05_test.yaml")
        if self.data_path.exists():
            self.data_path.unlink()
    def runTest(self):
        os.environ['RANDOMSEED'] = '2'
        options = get_options(['--samples', '10', '--output', 'ch13_r05_test.yaml'])
        face_count = write_rolls(options.output_path, roll_iter(options.samples, options.seed))
        self.assertDictEqual(
            {8: 8, 7: 6, 10: 5, 4: 3, 6: 3, 9: 3, 2: 2, 3: 1, 5: 1, 11: 1, 12: 1},
            face_count)
        results = list(yaml.load_all(self.data_path.read_text()))
        self.assertListEqual(
            [[[1, 1]],
            [[1, 3], [2, 6], [6, 3], [3, 5], [2, 5]],
            [[1, 5], [6, 2], [4, 6], [4, 6], [5, 3], [5, 4], [5, 3], [1, 1], [3, 4]],
            [[3, 4]],
            [[4, 5], [2, 5]],
            [[2, 2], [2, 1], [2, 3], [2, 2]],
            [[5, 5], [3, 5], [6, 5], [2, 4], [4, 6]],
            [[5, 3], [5, 3]],
            [[3, 4]],
            [[2, 4], [6, 6], [4, 6], [5, 2]]],
            results)

if __name__ == "__main__":
    unittest.main(exit=False)
    # main()
