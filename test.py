
import numpy as np
import utils

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


def seg_intersect(a, b, c, d):
    e = b-a
    f = d-c
    p = utils.perp(e)
    h = np.dot((a-c), p) / np.dot(f, p)
    return 0 < h < 1

