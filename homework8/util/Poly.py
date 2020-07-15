import math
import random
from sympy import *

from util.horner import horner


class Poly:

    def __init__(self, coef):
        self.coef = coef
        self.result = None
        self.tries = 10000
        self.eps = 0.01
        self.f = None
        self.min = None
        self.f_g = None
        self.s_f_g = None

    def get_roots(self):
        while self.result is None:
            x = [
                self.give_me_random(),
                self.give_me_random(),
                self.give_me_random()
            ]

            self.result = self.calcul_x(x)

    def calcul_x(self, x):
        values = [
            horner(x[0], self.coef),
            horner(x[1], self.coef),
            horner(x[2], self.coef)
        ]

        k = 0
        dlt = x[2] - x[1]

        while k < self.tries and abs(dlt) >= self.eps:
            z = [
                x[1] - x[0],
                x[2] - x[1]
            ]

            d = [
                (values[1] - values[0]) / z[0],
                (values[2] - values[1]) / z[1]
            ]

            y = [None] * 3
            y[0] = (d[1] - d[0]) / (z[0] + z[1])
            y[1] = y[0] * z[1] + d[1]
            y[2] = values[2]

            ss = (y[1] ** 2) - (4 * y[0] * y[2])
            if ss < 0:
                return None

            s = math.sqrt(ss)
            qt = max(y[1] + s, y[1] - s)

            if abs(qt) < self.eps:
                return None

            dlt = 2 * y[2] / qt

            x = [
                x[1],
                x[2],
                x[2] - dlt
            ]

            values = [
                values[1],
                values[2],
                horner(x[2], self.coef)
            ]

            k += 1

        if abs(dlt) < self.eps:
            return x[2]
        return None

    def set_func(self, f, x):
        self.f = lambdify(x, f)
        self.f_g = lambdify(x, f.diff(x))
        self.s_f_g = lambdify(x, f.diff(x, 2))

    def get_min(self):
        while self.min is None:
            x = [
                self.give_me_random(),
                self.give_me_random()
            ]
            self.min = self.compute_x(x)

    def compute_x(self, x):
        i = 0
        g_result = [
            self.f_g(x[0]),
            self.f_g(x[1])
        ]

        delta = x[1] - x[0]

        while self.eps <= abs(delta) < 10000 and i < self.tries:
            if g_result[0] == g_result[1]:
                delta = 0.0001
            else:
                delta = ((x[1] - x[0]) * g_result[1]) / (g_result[1] - g_result[0])

            x = [
                x[1],
                x[1] - delta
            ]

            g_result = [
                g_result[1],
                self.f_g(x[1])
            ]

            i = i + 1

        if abs(delta) < self.eps:
            return x[1]

        return None

    def give_me_random(self):
        return random.random()

    def get_fd(self):
        return self.f_g(self.min)

    def get_sd(self):
        return self.s_f_g(self.min)

