"""Python Cookbook

Chapter 7, recipe 2, timing comparison
"""

import timeit

if __name__ == "__main__":

    m1 = timeit.timeit('''repr(card)''', setup='''
    from ch07_r02 import make_card
    card = make_card(10,'S')
    ''' )

    m2 = timeit.timeit('''str(card)''', setup='''
    from ch07_r02 import make_card
    card = make_card(10,'S')
    ''' )

    print( "Card.__repr__ {0:.4f}".format(m1) )
    print( "object.__str__ {0:.4f}".format(m2) )
    print( 100*abs(m1-m2)/m1 )
