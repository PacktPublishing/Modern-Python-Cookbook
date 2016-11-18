"""Python Cookbook
"""
import random
from collections import Counter
from math import log

LO = 1
HI = 12

def hinter(target, summary):
    count= 1
    guess = int(input("Enter an initial guess: "))
    while guess != target:
        count += 1
        if guess < LO or guess > HI:
            print("Keep to the range", LO, "to", HI)
        elif guess < target:
            print("Too low")
        elif guess > target:
            print("Too high")
        else:
            raise Exception("Design Error")
        guess = int(input("Enter your next guess: "))
    print("Correct!")
    print(count, "tries")
    print()
    summary[count] += 1

if __name__ == "__main__":
    frequency = Counter()
    hinter(random.randint(LO, HI), frequency)
    again = input("Again? ").lower()
    while again.startswith('y'):
        hinter(random.randint(LO, HI), frequency)
        again = input("Again? ").lower()

    total = sum(frequency[count]*count for count in frequency)
    count = sum(frequency[count] for count in frequency)
    print("Your performance")
    print(frequency)
    print("avg =", total/count)
    print("ideally", log(HI-LO+1, 2))
