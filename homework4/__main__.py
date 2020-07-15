from util.Matrix import Matrix
from util.Equation_Resolver import EquationResolver


def read_result_array(file):
    file = open(file, "r")
    result = []
    size = file.readline()[:-1]
    for index in range(0, int(size)):
        element = float(file.readline()[:-1]);
        if element != '':
            result.append(element)
    return result


for index_file in range(1,6):

    coefficients_a = Matrix(f"input_equation/a_{index_file}.txt")
    solution = None

    try:
        equation: EquationResolver = EquationResolver(coefficients_a, read_result_array(f"input_equation/b_{index_file}.txt",))
        solution = equation.resolve()
    except Exception as e:
        print("There was a problem in resolving the eq: ", e)

    print(f"File no. {index_file}")
    print("The solution is: ", solution)
    print("The norm is: ", equation.norm_verify())


coefficients_a = Matrix(f"input_equation/test_a.txt")
solution = None

try:
    equation = EquationResolver(coefficients_a, read_result_array(f"input_equation/test_b.txt",))
    solution = equation.resolve()
except Exception as e:
    print("There was a problem")
    print(e)

print(f"File no. test")
print("The solution is: ", solution)
print("The norm is: ", equation.norm_verify())


