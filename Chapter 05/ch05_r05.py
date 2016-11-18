"""Python Cookbook

Chapter 5, recipe 5
"""

import cmd
import random
from collections import Counter

red_bins = (1, 3, 5, 7, 9, 12, 14, 16, 18,
    21, 23, 25, 27, 28, 30, 32, 34, 36)

#black_bins = (2, 4, 6, 8, 10, 11, 13, 15, 17,
#    19, 20, 22, 24, 26, 29, 31, 33, 35)
#
#assert set(red_bins) | set(black_bins) == set(range(1,37))

def roulette_bin(i):
    return str(i), {
        'even' if i%2 == 0 else 'odd',
        'low'  if 1 <= i < 19 else 'high',
        'red'  if i in red_bins else 'black'
    }

def zero_bin():
    return '0', set()

def zerozero_bin():
    return '00', set()

def wheel():
    """
    >>> random.seed(1)
    >>> w = wheel()
    >>> spin = random.choice(w)
    >>> spin == ('7', {'odd', 'red', 'low'})
    True
    >>> spin = random.choice(w)
    >>> spin == ('35', {'black', 'high', 'odd'})
    True
    """
    b0 = [zero_bin()]
    b00 = [zerozero_bin()]
    b1_36 = [
        roulette_bin(i) for i in range(1,37)
    ]
    return b0+b00+b1_36

class Roulette(cmd.Cmd):
    prompt="Roulette> "
    bet_names = set(['even', 'odd', 'high', 'low', 'red', 'black'])
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
    def preloop(self):
        self.stake = 100
        self.wheel = wheel()
        self.bets = {}
        print("Starting with {stake}".format_map(vars(self)))
    def postloop(self):
        print("Ending with {stake}".format_map(vars(self)))
    bet_names = set(['even', 'odd', 'high', 'low', 'red', 'black'])
    def do_bet(self, bet):
        '''Bet <name> <amount>
        Name is one of even, odd, red, black, high, or low
        '''
        try:
            name, text_amount = bet.split()
            name in self.bet_names
            amount= int(text_amount)
        except Exception as ex:
            print(ex)
            return
        self.bets[name]= amount
    def do_spin(self, args):
        if not self.bets:
            print( "No bets placed" )
            return
        self.spin = random.choice(self.wheel)
        print("Spin", self.spin)
        label, winners = self.spin
        for b in self.bets:
            if b in winners:
                self.stake += self.bets[b]
                print("Win", b)
            else:
                self.stake -= self.bets[b]
                print("Lose", b)
        self.bets= {}
    def do_stake(self, args):
        print("stake = {stake}".format_map(vars(self)))
    def do_done(self, args):
        return True

if __name__ == "__main__":
    import doctest, sys
    fail, run = doctest.testmod()
    if fail != 0:
        sys.exit(fail)
    r = Roulette()
    r.cmdloop()
