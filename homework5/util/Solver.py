from util.Matrix import Matrix
from util.EquationSolver import EquationSolver

import numpy as np
import math


def compute_machine_precision():
    counter = 0
    u = 1
    while 1 + u != 1:
        counter = counter + 1
        u = 10 ** -counter
    return u


def read_result_array(file):
    file = open(file, "r")
    result = []
    size = file.readline()[:-1]
    for index in range(0, int(size)):
        element = float(file.readline()[:-1])
        if element != '':
            result.append(element)
    return result


EPS = compute_machine_precision()


class Solver:
    def __init__(self, file_name, parameter):
        self.parameter = parameter
        if self.parameter <= 0 and type(self.parameter) == int:
            raise Exception("Parameter needs to be an natural non-zero number")
        self.matrix_file: Matrix = Matrix(file_name)
        self.file_name = file_name
        self.matrix_random: Matrix

    def solve(self):
        # Display the eigenvalues computed with
        # the power method both for the randomly generated matrix and the one
        # stored in the file.
        if self.parameter == self.matrix_file.size and self.parameter > 500:
            # Generate an symmetric NXN matrix
            self.matrix_random = Matrix(self.parameter, 2)
            self.matrix_random.make_transpose()
            if self.matrix_random.symmetric_matrix():
                print("Random generated matrix")
                eigenvalue, eigenvalues = self.power_method(self.matrix_random)
                print("Largest eigenvalue of matrix: ", eigenvalue)
                print("Associated eigenvector: ", eigenvalues)
            else:
                raise Exception("In order to display the eigenvalues computed "
                                "with the power method, matrix needs to be symmetric")

            # Check if the matrix from the file is symmetric
            self.matrix_file.make_transpose()
            if self.matrix_file.symmetric_matrix():
                print("Matrix from file with size")
                eigenvalue, eigenvalues = self.power_method(self.matrix_file)
                print("Largest eigenvalue matrix: ", eigenvalue)
                print("Associated eigenvector: ", eigenvalues)
            else:
                raise Exception("In order to display the eigenvalues computed "
                                "with the power method, matrix needs to be symmetric")
        elif self.parameter == self.matrix_file.size and self.parameter <= 500:
            self.matrix_file.make_transpose()
            if self.matrix_file.symmetric_matrix():
                print("Matrix from file with size")
                eigenvalue, eigenvalues = self.power_method(self.matrix_file)
                print("Largest eigenvalue of matrix: ", eigenvalue)
                print("Associated eigenvector: ", eigenvalues)
            else:
                raise Exception("In order to display the eigenvalues computed "
                                "with the power method, matrix needs to be symmetric")
        elif self.parameter > self.matrix_file.size and self.file_name.startswith("input/test"):
            equation_solver = EquationSolver(self.matrix_file, read_result_array("input/result_a.txt"))
            for item in equation_solver.svd_decomposition_method().items():
                print(f"Property {item[0]} has value: {item[1]}")
        else:
            raise Exception("There was a problem with your input or the option is not available.")

    def power_method(self, matrix_a: Matrix, iterations=10**6, eps=10**-9):
        # Generate random vector of values v(0)) with norm = 1
        v = np.random.randn(matrix_a.size)
        v = np.divide(v, self.compute_euclidean_norm(v))
        v = np.abs(v)

        w = matrix_a * v
        value_lambda = np.dot(w, v)
        k = 0

        while k <= iterations and np.linalg.norm(np.subtract(w, np.multiply(value_lambda, v)),2) > matrix_a.size * eps:
            # K + 1 iteration
            v = np.divide(w,  np.linalg.norm(w,2))
            w = matrix_a * v
            value_lambda = np.dot(w, v)
            k += 1

        # Alg. did not compute try to give another epsilon
        if k > iterations:
            return None, None

        return value_lambda, np.array(v)

    @staticmethod
    def compute_euclidean_norm(v):
        return math.sqrt(np.sum(np.dot(v, v)))