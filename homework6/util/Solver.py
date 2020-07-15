import numpy as np
import math
from util.Polynom import Polynom
from util.Trigonometric import Trigonometric
import matplotlib.pyplot as plt


def read_file(file):
    file = open(file, "r")
    result = []
    size = file.readline()[:-1]
    for index in range(0, int(size)):
        element = float(file.readline()[:-1])
        if element != '':
            result.append(element)
    return result


class Solver:
    def __init__(self, input_array, output_array, function, type=0, method_solve=0):
        self.method_solve = method_solve
        self.function = function
        self.type = type
        try:
            if not type:
                self.input_values = np.array(read_file(input_array))
                self.size = self.input_values.size
                if self.input_values[0] >= self.input_values[self.input_values.size - 1]:
                    raise Exception("Condition a < b is not satisfied. Values need to be < from one another")
                self.output_values = np.array(read_file(output_array))
            else:
                self.input_values = np.array(input_array)
                self.size = self.input_values.size
                if self.input_values[0] >= self.input_values[self.input_values.size - 1]:
                    raise Exception("Condition a < b is not satisfied. Values need to be < from one another")
                self.output_values = np.array(output_array)
        except Exception as e:
            print("An exception has occurred in initializing solver: ", e)

    def compute_vandermonde_matrix(self):
        matrix = np.zeros((self.size, self.size))

        for i in range(0, self.size):
            for j in range(0, self.size):
                if j == 0:
                    matrix[i, j] = 1
                else:
                    matrix[i, j] = self.input_values[i] ** j

        return matrix

    def compute_matrix_trigonometric(self):
        matrix = np.zeros((self.size, self.size))
        fi = 1
        for i in range(0, self.size):
            for j in range(0, self.size):
                if j == 0:
                    matrix[i, j] = fi
                else:
                    k = int((j + 1) / 2)
                    if j % 2 == 1:
                        fi = math.sin(k * self.input_values[i])
                    else:
                        fi = math.cos(k * self.input_values[i])
                    matrix[i, j] = fi
        return matrix

    def solve(self, number):
        if not self.method_solve:
            vandermonde_matrix = self.compute_vandermonde_matrix()
            coefficients = np.linalg.solve(vandermonde_matrix, self.output_values)
            points = []
            x = 1.0
            while x <= 5.0:
                p = Polynom(coefficients, self.function, x)
                points.append((x, p.solution()))
                x += 0.1
            self.plot(coefficients, points)
            p = Polynom(coefficients, self.function, number)
            return p.solution(), p.norm()
        else:
            matrix = self.compute_matrix_trigonometric()
            coefficients = np.linalg.solve(matrix, self.output_values)
            points = []
            x = -15
            while x < 15:
                t = Trigonometric(coefficients, self.function, x)
                points.append((x, t.solution()))
                x += 0.35
            self.plot(coefficients, points)
            t = Trigonometric(coefficients, self.function, number)
            return t.solution(), t.norm()

    def plot(self, coefficients, points):
        x = self.input_values
        y = self.output_values

        fig = plt.figure()

        x_i = [x[0] for x in points]
        y_i = [x[1] for x in points]
        if not self.type:
            ax1 = fig.add_subplot(211)
            poly = np.poly1d(np.flip(coefficients))

            new_x = np.linspace(x[0], x[-1])
            new_y = poly(new_x)

            ax1.plot(x, y, "o", new_x, new_y)
            plt.xlim([x[0] - 1, x[-1] + 1])

            ax2 = fig.add_subplot(212)
            ax2.plot(x_i, y_i, color="red",)

        else:
            ax1 = fig.add_subplot(211)
            ax1.plot(x, y)

            ax2 = fig.add_subplot(212)
            ax2.plot(x_i, y_i, color="red",)

        plt.show()
