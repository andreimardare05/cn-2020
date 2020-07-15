import numpy as np
import math


class Polynom:
    def __init__(self, coefficients, function, number):
        self.coefficients = coefficients
        self.function = function
        self.size = coefficients.size
        self.number_to_approximate = number
        self.approximation = None

    # Approximate the value of the polynom using Horner's scheme
    def solution(self):
        coefficients = np.flip(self.coefficients)
        if coefficients.size < 2:
            raise Exception('You need to pass an array of coefficients with size > 1')
        result = coefficients[0]
        for index in range(1, self.size):
            result = self.number_to_approximate * result + coefficients[index]
        self.approximation = result
        return result

    def norm(self):
        if self.approximation is None:
            raise Exception("You need to approximate your solution in order to compute the norm")
        return math.fabs(self.function(self.number_to_approximate) - self.approximation)
