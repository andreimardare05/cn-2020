from sympy import *

from util.Poly import Poly


def __main__():
    p = Poly([1, -4, 3])
    p.get_roots()
    print(p.result)

    x = Symbol('x')

    f = x*x + exp(x)

    p.set_func(f, x)
    p.get_min()
    print(p.min)
    print(p.get_fd())
    print(p.get_sd())


__main__()