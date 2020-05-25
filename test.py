from pprint import pprint

import numpy as np


def f(x):
    return -x ** 2 + x


def integ(x):
    return x ** 2 / 2.0 - x ** 3 / 3.0


class Foo:

    def __init__(self):
        self.bar = self.Bar()
        self.var = 'foovar'
        self.bar.do()

    class Bar:
        def __init__(self):
            print('bar')

        def do(self):
            print()



f = Foo()
for i in np.arange(0.1, 1.1, 0.1):
    print(i, integ(i), integ(i) - integ(i - 0.1))
