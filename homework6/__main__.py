from util.Solver import Solver
import math
import numpy as np


def f(x):
    return x**4 - 12 * (x**3) + 30 + (x**2) + 12


solver = Solver("input/input_a.txt", "input/output_a.txt", f,  0, 0)
number = 3
result, norm = solver.solve(number)
print(f"Approximation for x = {number} is f(x = {number}) ~= {result}")
print(f"Norm is {norm}")


def f1(x):
    return math.sin(x) - math.cos(x)


def f2(x):
    return math.sin(2 * x) + math.sin(x) + math.cos(3 * x)


def f3(x):
    return math.sin(x) ** 2 - math.cos(x) ** 2


def generate_interpolation_points(a, b, func, desired_size=1501):
    input_function = []
    if desired_size % 2 == 0:
        desired_size = desired_size + 1
    input_function.append(a)
    for index in range(1, desired_size - 1):
        candidate = np.random.normal(a, b)
        input_function.append(candidate)
    input_function.append(b)
    input_function = sorted(input_function)
    output_function = [f1(x) for x in input_function]
    return input_function, output_function


input, output = generate_interpolation_points(0, (31 * math.pi) / 16, f1)
solver = Solver(input, output, f1, 1, 1)
number = math.pi
result, norm = solver.solve(number)
print(f"Approximation for x = {number} is f(x = {number}) ~= {result}")
print(f"Norm is {norm}")
