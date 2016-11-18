"""Python Cookbook

Chapter 13, recipe 11
"""

import subprocess

def command_iter(files):
    for n in range(files):
        filename = 'game_{n}.yaml'.format_map(vars())
        command = ['python3', 'ch13_r05.py',
            '--samples', '10', '--output', filename]
        yield command

def command_output_iter(iterable):
    for command in iterable:
        process = subprocess.run(command, stdout=subprocess.PIPE, check=True)
        output_bytes = process.stdout
        output_text = output_bytes.decode('utf-8')
        output_lines = list(l.strip() for l in output_text.splitlines())
        yield output_lines

from collections import Counter

def process_batches():
    command_sequence = command_iter(2)
    output_lines_sequence = command_output_iter(command_sequence)
    for batch in output_lines_sequence:
        for line in batch:
            if line.startswith('Counter'):
                batch_counter = eval(line)
                yield batch_counter

if __name__ == "__main__":
    total_counter = Counter()
    for batch_counter in process_batches():
        print(batch_counter)
        total_counter.update(batch_counter)
    print("Total")
    print(total_counter)
