"""Python Cookbook

Chapter 13, recipe 7
"""
from ch13_r05 import roll_iter
from ch13_r06 import gather_stats
from collections import Counter
import time

def summarize_games(total_games, *, seed=None):
    game_statistics = gather_stats(roll_iter(total_games, seed=seed))
    return game_statistics

def win_loss(stats):
    summary = Counter()
    for outcome, game_length in stats:
        summary[outcome] += stats[(outcome, game_length)]
    return summary

def simple_composite(games=100000):
    start = time.perf_counter()
    stats = summarize_games(games)
    end = time.perf_counter()
    #for outcome in sorted(stats):
    #    print(outcome, stats[outcome])
    games = sum(stats.values())
    print('games', games)
    print(win_loss(stats))
    print("{:.2f} seconds".format(end-start))

import concurrent.futures

def parallel_composite(games=100, rolls=1000):
    start = time.perf_counter()
    total_stats = Counter()
    worker_list = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(games):
            worker_list.append(executor.submit(summarize_games, rolls))
        for worker in worker_list:
            stats = worker.result()
            total_stats.update(stats)
    end = time.perf_counter()
    #for outcome in sorted(total_stats):
    #    print(outcome, total_stats[outcome])
    games = sum(total_stats.values())
    print('games', games)
    print(win_loss(total_stats))
    print("{:.2f} seconds".format(end-start))

import logging, sys

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    simple_composite(100000)
    #parallel_composite()
    logging.shutdown()
