"""Python Cookbook

Chapter 9, recipe 10.
"""
import logging
import sys
from logging import Formatter
from pathlib import Path

def create_log():
    PROD_LOG_FORMAT = ('[{asctime}]'
        ' {levelname} in {module}: {message}'
        )

    with Path('sample.log').open('w') as sample_log_file:
        logging.basicConfig( stream=sample_log_file, level=logging.DEBUG )

        logger = logging.getLogger()
        for handler in logger.handlers:
            handler.setFormatter(Formatter(PROD_LOG_FORMAT, style='{'))

        logger.info("Sample Message One")
        logger.debug("Debugging")
        logger.warn("Something might have gone wrong")

import re
from pathlib import Path
import csv

log_pattern = re.compile(
    r"\[(?P<timestamp>.*?)\]"
    r"\s(?P<levelname>\w+)"
    r"\sin\s(?P<module>[\w\._]+):"
    r"\s(?P<message>.*)")

def extract_row_iter(source_log_file):
    for line in source_log_file:
        match = log_pattern.match(line)
        if match is None: continue
        yield match.groupdict()

def parse_log():
    summary_path = Path('summary_log.csv')
    with summary_path.open('w') as summary_file:

        writer = csv.DictWriter(summary_file,
            ['timestamp', 'levelname', 'module', 'message'])
        writer.writeheader()

        source_log_dir = Path('.')
        for source_log_path in source_log_dir.glob('*.log'):
            with source_log_path.open() as source_log_file:
                writer.writerows(
                    extract_row_iter(source_log_file)
                    )

            print('Converted', source_log_path, 'to', summary_path)

def counting_extract_row_iter(counts, source_log_file):
    for line in source_log_file:
        match = log_pattern.match(line)
        if match is None:
            counts['non-match'] += 1
            continue
        counts['valid'] += 1
        yield match.groupdict()

from collections import Counter
def parse_log2():
    summary_path = Path('summary_log.csv')
    with summary_path.open('w') as summary_file:

        writer = csv.DictWriter(summary_file,
            ['timestamp', 'levelname', 'module', 'message'])
        writer.writeheader()

        source_log_dir = Path('.')
        for source_log_path in source_log_dir.glob('*.log'):
            counts = Counter()
            with source_log_path.open() as source_log_file:
                writer.writerows(
                    counting_extract_row_iter(counts, source_log_file)
                    )

            print('Converted', source_log_path, 'to', summary_path)
            print(counts)

if __name__ == "__main__":
    create_log()
    parse_log2()
