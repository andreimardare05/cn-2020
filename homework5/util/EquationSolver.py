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


class EquationSolver:
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

        return None

    def check_determinant(self):
        for index_line in range(0, self.lines.size):
            exists = False
            for item in self.lines[index_line]:
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

    # The Moore-Penrose pseudo-inverse of matrix A
    @staticmethod
    def moore_penrose(u, s, v):
        s_i = np.zeros((len(v), len(u)))
        for index in range(0, len(s)):
            s_i[index, index] = 1.0 / s[index]
        result = np.dot(v, s_i)
        result = np.dot(result, u.T)
        return result

    def svd_decomposition_method(self, eps=10 ** -9):
        solution_equation = self.result

        coefficients = np.zeros((self.size, self.size))

        for index in range(0, self.coefficients.size):
            for item in self.coefficients.lines[index]:
                coefficients[index, item.position] = item.value

        u, s, v = np.linalg.svd(coefficients)

        rank = sum([1 for value in s if value > eps])
        # rank = np.linalg.matrix_rank()

        list_values = [value for value in s if value > eps]
        sigma_max = max(list_values)
        sigma_min = min(list_values)
        conditioning_number = sigma_max / sigma_min
        # conditioning_number = np.linalg.cond()

        pseudo_inverse = np.linalg.pinv(coefficients)
        # pseudo_inverse = self.moore_penrose(u,s,v)
        pseudo_x = np.dot(pseudo_inverse, solution_equation)
        norm = self.compute_euclidean_norm(solution_equation - np.dot(coefficients, pseudo_x))
        second_norm = np.sum(np.abs(pseudo_inverse-np.sum(np.linalg.inv(np.transpose(coefficients) * coefficients)
                                                          * np.transpose(coefficients))))

        return {
            "singular_values": s,
            "rank": rank,
            "conditioning_number": conditioning_number,
            "pseudo-inverse": pseudo_inverse,
            "pseudo-x": pseudo_x,
            "first_norm": norm,
            "second_norm": second_norm
        }

    @staticmethod
    def compute_euclidean_norm(v):
        return math.sqrt(np.sum(np.dot(v, v)))

