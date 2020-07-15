import math
import numpy as np


# Class to approximate functions of T period
class Trigonometric:
    def __init__(self, coefficients, function, number):
        self.coefficients = coefficients
        self.function = function
        self.size = coefficients.size
        self.number_to_approximate = number
        self.approximation = None

    # Approximate the value of the function using a linear combination of sin and cos function
    def solution(self):
        result = 0
        result += self.coefficients[0] * 1
        if self.coefficients.size < 2:
            raise Exception('You need to pass an array of coefficients with size > 1')
        for index in range(1, self.coefficients.size):
            k = int((index + 1) / 2)
            if index % 2 == 1:
                fi = math.sin(k * self.number_to_approximate)
            else:
                fi = math.cos(k * self.number_to_approximate)
            result += self.coefficients[index] * fi
        self.approximation = result
        return result

    def norm(self):
        if self.approximation is None:
            raise Exception("You need to approximate your solution in order to compute the norm")
        return math.fabs(self.function(self.number_to_approximate) - self.approximation)