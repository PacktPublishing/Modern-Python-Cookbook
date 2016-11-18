"""Python Cookbook

Chapter 13, recipe 6
"""
import argparse
import sys
from pathlib import Path
from collections import Counter
import yaml

import logging

detail_log = logging.getLogger("overview_stats.detail")
write_log = logging.getLogger("overview_stats.write")

def get_options(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='*')
    parser.add_argument('-o', '--output')
    options = parser.parse_args(argv)
    detail_log.debug("options: {}".format(options))
    return options

def main():
    options = get_options(sys.argv[1:])
    if options.output is not None:
        report_path = Path(options.output)
        with report_path.open('w') as result_file:
            process_all_files(result_file, options.file)
        write_log.info("wrote {}".format(report_path))
    else:
        process_all_files(sys.stdout, options.file)

def process_all_files(result_file, file_names):
    for source_path in (Path(n) for n in file_names):
        detail_log.info("read {}".format(source_path))
        with source_path.open() as source_file:
            game_iter = yaml.load_all(source_file)
            statistics = gather_stats(game_iter)
            result_file.write(
                yaml.dump(dict(statistics), explicit_start=True)
            )

def gather_stats(game_iter):
    counts = Counter()
    for game in game_iter:
        if len(game) == 1 and sum(game[0]) in (2, 3, 12):
            outcome = "loss"
        elif len(game) == 1 and sum(game[0]) in (7, 11):
            outcome = "win"
        elif len(game) > 1 and sum(game[-1]) == 7:
            outcome = "loss"
        elif len(game) > 1 and sum(game[0]) == sum(game[-1]):
            outcome = "win"
        else:
            detail_log.error("problem with {}".format(game))
            raise Exception("Wait, What?")
        event = (outcome, len(game))
        detail_log.debug("game {} -> event {}".format(game, event))
        counts[event] += 1
    return counts

import logging.config
if __name__ == "__main__":
    config_yaml = '''
version: 1
formatters:
    default:
        style: "{"
        format: "{levelname}:{name}:{message}"
        #   Example: INFO:overview_stats.detail:read x.yaml
    timestamp:
        style: "{"
        format: "{asctime}//{levelname}//{name}//{message}"

handlers:
    console:
        class: logging.StreamHandler
        stream: ext://sys.stderr
        formatter: default
    file:
        class: logging.FileHandler
        filename: write.log
        formatter: timestamp

loggers:
    overview_stats.detail:
        handlers:
        -   console
    overview_stats.write:
        handlers:
        -   file
        -   console

root:
    level: INFO
'''
    # logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    logging.config.dictConfig(yaml.load(config_yaml))
    main()
    logging.shutdown()
