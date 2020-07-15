import numpy as np
import math


class LinearEq:
    def __init__(self, precision, matrix, result):
        self.matrix = np.array(matrix, dtype=float)
        if self.matrix.shape[0] != self.matrix.shape[1]:
            raise Exception("Your coef. matrix needs to be NxN!")
        self.lower, self.upper = self.set_lower_upper_decomposition(np.copy(matrix))
        self.result = np.array(result, dtype=float)
        self.precision = 10 ** (-precision)
        self.solution = None

    def check_equal_zero(self, number):
        if abs(number) < self.precision:
            return True
        else:
            return False

    def set_lower_upper_decomposition(self, clone_matrix):
        lower = np.zeros_like(clone_matrix)
        upper = np.zeros_like(clone_matrix)

        for p in range(clone_matrix.shape[0]):
            lower[p, p] = 1.0
            upper[p, p] = clone_matrix[p, p] - np.dot(lower[p, :p], upper[:p, p])
            for i in range(p + 1, clone_matrix.shape[0]):
                upper[p, i] = clone_matrix[p, i] - np.dot(lower[p, :p], upper[:p, i])
            for i in range(p + 1, clone_matrix.shape[0]):
                if upper[p, p]:
                    lower[i, p] = (clone_matrix[i, p] - np.dot(lower[i, :p], upper[:p, p])) / upper[p, p]
                else:
                    raise Exception("Matrix has a null minor det(A_of_p) = 0. Lower-upper(LU) "
                                    "decomposition could not be computed in this case!")
        return lower, upper

    def get_determinant_matrix(self):
        # print('Determinant: ', np.linalg.det(self.lower) * np.linalg.det(self.upper))
        return np.linalg.det(self.lower) * np.linalg.det(self.upper)

    # lower * Y = result
    # upper * X = Y
    @staticmethod
    def get_solution_by_applying_LU_decompositon(upper, lower, result):
        y = np.zeros_like(result)
        x = np.zeros_like(result)

        # lower * Y = result
        for index, element_result in enumerate(result):
            y[index] = element_result
            if index:
                for p in range(0, index):
                    y[index] = y[index] - lower[index, p] * y[p]
            y[index] = y[index] / lower[index, index]

        # upper * X = Y
        for iterator_index in range(0, x.size):
            index = x.size - 1 - iterator_index
            x[index] = y[index]
            if iterator_index:
                for num in range(0, iterator_index):
                    p = x.size - 1 - num
                    x[index] = x[index] - upper[index, p] * x[p]
            x[index] = x[index] / upper[index, index]
        return x

    def resolve_with_LU_decomposition(self):
        if self.check_equal_zero(self.get_determinant_matrix()):
            raise Exception("Determinant is 0. The LU decomposition could not be computed!")
        self.solution = self.get_solution_by_applying_LU_decompositon(self.upper, self.lower, self.result)
        return self.solution

    def resolve_with_numpy(self):
        # print("Solution with numpy: ", np.linalg.solve(self.matrix, self.result))
        return np.linalg.solve(self.matrix, self.result)

    def compute_inv_with_numpy(self):
        return np.linalg.solve(self.matrix, self.result)

    def norm(self):
        result = np.dot(self.matrix, np.array(self.solution).reshape(self.solution.size, 1)) - self.result.reshape(
            self.solution.size, 1)
        # print(result, sep='\n')
        return math.sqrt(sum(map(lambda x: math.pow(x[0], 2), result)))

    def additional_norms(self):
        matrix_inv = np.linalg.inv(self.matrix)
        if self.solution.size:
            return {
                "difference-solution": math.sqrt(sum(map(lambda x: math.pow(x[0], 2),
                                                         np.array(self.solution - self.resolve_with_numpy()).reshape(
                                                             self.solution.size, 1)))),
                "difference-solution-inverse": math.sqrt(sum(map(lambda x: math.pow(x[0], 2), np.array(
                    self.solution - np.dot(matrix_inv, self.result).reshape(self.solution.size, 1)))))
            }
        else:
            return None

    def compute_inv_norm(self):
        inv_lu = self.compute_inv_with_LU_decomposition()
        inv_lib = self.compute_inv_with_numpy()
        difference = inv_lu - inv_lib
        result = []
        for index in range(0, inv_lu.shape[0]):
            result.append(sum(np.abs(difference[:, index])))
        return max(result)

    def compute_inv_with_LU_decomposition(self):
        result = []
        identity_matrix = np.identity(self.matrix.shape[0])
        for i in range(0, self.matrix.shape[0]):
            result.append(self.get_solution_by_applying_LU_decompositon(self.upper, self.lower, identity_matrix[:, i]))
        return np.array(result).reshape(self.matrix.shape[0], self.matrix.shape[1])
