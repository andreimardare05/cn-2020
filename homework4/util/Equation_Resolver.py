from util.Matrix import Matrix
import numpy as np
import math

EPS = 10 ** -16


def compute_machine_precision():
    counter = 0
    u = 1
    while 1 + u != 1:
        counter = counter + 1
        u = 10 ** -counter
    return u


class EquationResolver:
    value = 0
    position = 0
    max_iterations = 10000

    def __init__(self, coefficients, result, max_iterations=10000):
        self.solution = None
        if type(coefficients) == Matrix:
            self.coefficients = coefficients
            self.result = result
            if self.coefficients.size != len(self.result):
                raise Exception("The coefficients matrix size should be the same with "
                                "the size of the results for every equation")
            self.size = len(result)
            if max_iterations <= 0:
                raise Exception("The maximum number of iterations needs to be greater than 0")
            self.max_iterations = max_iterations
            self.precision = compute_machine_precision()
            print("The EQ_SOLVER was initialized successfully")

    def resolve(self):
        self.solution = None
        if not self.check_determinant():
            raise Exception("The matrix determinant should be > 0 ")
        x_current = np.zeros(self.size)
        k = 0
        difference = self.max_iterations
        while k <= self.max_iterations and EPS <= difference <= 10 ** 16:
            sum_squares = 0
            # Compute the new x_current
            for index in range(0, self.coefficients.size):
                sum_line = 0
                diagonal_value = 0
                for elem in self.coefficients.lines[index]:
                    item = 0
                    if elem.position == index:
                        diagonal_value = elem.value
                    else:
                        item = elem.value * x_current[elem.position]
                    sum_line += item
                value = (self.result[index] - sum_line) / diagonal_value
                # Add the value to the sum_squares in order to be computed in norm afterwards
                sum_squares += (x_current[index] - value)**2
                x_current[index] = value
            # Compute the norm
            difference = self.norm(sum_squares)
            k = k + 1

        if difference - EPS < 0:
            self.solution = x_current
            return self.solution

        return None;

    def check_determinant(self):
        for index_line in range(0, self.coefficients.size):
            exists = False
            for item in self.coefficients.lines[index_line]:
                if item.position == index_line and item.value > 0:
                    exists = True
                    break
            if not exists:
                return False
        return True

    @staticmethod
    def norm(sum_of_squares):
        return math.sqrt(sum_of_squares)

    def norm_verify(self):
        if self.solution is None:
            return None
        dot_array = np.zeros(self.size)
        counter = 0
        for index in range(0, self.coefficients.size):
            for item in self.coefficients.lines[index]:
                dot_array[counter] = dot_array[counter] + item.value * self.solution[item.position]
            counter += 1
        return np.max(np.subtract(dot_array, np.array(self.result)))
