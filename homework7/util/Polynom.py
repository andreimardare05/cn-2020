import numpy as np
import random as rd
import math

# Define upper bound for number of iterations
k_max = 10 ** 8
# Machine precision
EPS = 1e-16


def signature_x(x):
    if x >= 0:
        return 1
    return -1


class Polynom:
    def __init__(self, coefficients, function):
        self.coefficients = np.array(coefficients)
        self.size = self.coefficients.size
        self.function = function
        self.number_to_approximate = None
        self.A = abs(max(self.coefficients, key=lambda x: abs(x)))
        self.R = (self.A + abs(self.coefficients[0])) / abs(self.coefficients[0])
        print(f"Interval: [{-self.R}, {self.R}]")
        self.result_roots = None

    # Approximate the value of the polynom using Horner's scheme
    def solution_horner(self, coefficients, x):
        if coefficients.size < 2:
            raise Exception('You need to pass an array of coefficients with size > 1')
        result = coefficients[0]
        for index in range(1, self.size):
            result = x * result + coefficients[index]
        return np.polyval(coefficients, x)
        return result

    def laguerre_method(self, x):
        check = True
        k = 0
        delta_x = 0
        while check:
            delta_x = self.compute_delta_x(x)
            if delta_x is None:
                return None
            x = x - delta_x
            k = k + 1
            check = k < k_max and EPS <= abs(delta_x) <= 10 ** 8
        # Convergent
        if abs(delta_x) < EPS:
            return x
        # Divergent
        else:
            return None

    # Return possible roots using numpy
    def solve_using_numpy(self):
        return np.roots(self.coefficients)

    def compute_first_derivative(self, x):
        p = np.poly1d(self.coefficients)
        p1 = np.polyder(p)
        return p1(x)

    def compute_second_derivative(self, x):
        p = np.poly1d(self.coefficients)
        p2 = np.polyder(p, 2)
        return p2(x)

    def roots(self):
        result = set()

        for counter in range(1, 100):
            x = rd.uniform(-self.R, self.R)

            candidate = self.laguerre_method(x)
            if candidate is not None:
                check = True
                for item in result:
                    # Check machine precision 10 ** - 16 in this case
                    if math.fabs(item - candidate) < EPS:
                        check = False
                        break
                if check:
                    result.add(round(candidate, 14))

        self.result_roots = result

        return result

    def compute_h_x(self, coefficients, x_k, p_first):
        p_second = self.compute_second_derivative(x_k)
        n = self.size - 1

        h_x = (n - 1) ** 2 * p_first ** 2
        h_x = h_x - n * (n - 1) * self.solution_horner(coefficients, x_k) * p_second
        if h_x < 0:
            return None

        return h_x

    def write_in_file(self):
        f = open("out.txt", "a")

        if self.result_roots is None:
            raise Exception("Result could not be written in file. Call roots function"
                            " first in order to have the result.")
        f.write("Solution is: ")

        for item in self.result_roots:
            f.write(str(item) + ' ')
        f.close()

    # \frac{x}{y}
    def compute_delta_x(self, x_k):
        p_first = self.compute_first_derivative(x_k)
        n = self.size - 1

        x = n * self.solution_horner(self.coefficients, x_k)
        y = p_first
        h_x = self.compute_h_x(self.coefficients, x_k, p_first)

        if h_x is None:
            return None
        y = y + signature_x(y) * math.sqrt(h_x)
        if abs(y) <= EPS:
            return None

        return x / y