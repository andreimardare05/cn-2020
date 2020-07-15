from util.Element import Element
import random
import copy
import numpy as np


def compute_machine_precision():
    counter = 0
    u = 1
    while 1 + u != 1:
        counter = counter + 1
        u = 10 ** -counter
    return u


EPS = 10**-7
MAX_POSITIVE_INTEGER = 10 ** 2


class Matrix:
    # rtype=0 Create matrix with no valuess
    # rtype=1 Create matrix from file
    # rtype=2 Create matrix with random values
    def __init__(self, data, rtype=1):
        self.size = None
        self.lines = None
        self.transpose = None
        self.file = None
        if rtype == 1:
            self.init_from_file(data)
        elif rtype == 0:
            self.init_from_data(data)
        elif rtype == 2:
            self.generate_matrix(data)
        else:
            raise Exception("Option that you introduced is not supported")

    def init_from_file(self, file):
        self.file = open(file, "r")
        self.size = int(self.file.readline())
        self.lines = [[]] * self.size

        while True:
            line = self.file.readline().split(', ')

            values = [x.strip(' ') for x in line]

            if len(values) < 3:
                break

            element = Element(values[0], values[2][:-1])

            position = int(values[1])

            if not self.lines[position]:
                self.lines[position] = []
            self.lines[position].append(element)

        self.sort_columns()

    def init_from_data(self, data):
        self.size = len(data)
        self.lines = data

    def generate_matrix(self, size):
        self.size = size
        self.lines = [[]] * self.size

        # Set the main diagonal with values (diagonal matrix)
        for index in range(0, self.size):
            value = random.randint(1, MAX_POSITIVE_INTEGER)
            element = Element(value, index)
            self.lines[index] = []
            self.lines[index].append(element)

        counter = self.size / 3
        tuples = []
        # Set values above the main diagonal
        while True:
            index = random.randint(0, self.size - 1)
            second_index = random.randint(index, self.size - 1)
            value = random.randint(0, MAX_POSITIVE_INTEGER)

            if not (index, second_index) in tuples:
                tuples.append((index, second_index))
                tuples.append((second_index, index))
                element = Element(value, second_index)
                transposed_element = Element(value, index)
                self.lines[index].append(element)
                self.lines[second_index].append(transposed_element)
                counter = counter - 2

            if counter <= 0:
                break

        self.sort_columns()

    def sort_columns(self):
        for index in range(0, self.size):
            self.lines[index].sort(key=lambda x: x.position)

    def add_to_line(self, index, new_element):
        if not self.lines[index]:
            self.lines[index] = []
            self.lines[index].append(new_element)
            return

        for element in self.lines[index]:
            if element.position == new_element.position:
                element.value += new_element.value
                if element.value == 0:
                    self.lines[index].remove(element)
                return

        self.lines[index].append(new_element)

    def make_transpose(self):
        self.transpose = [[]] * self.size
        item = None

        for index in range(0, self.size):
            self.transpose[index] = []

        for index in range(0,self.size):
            for item in self.lines[index]:
                element = Element(item.value, index)
                self.transpose[item.position].append(element)
            self.transpose[item.position].sort(key=lambda x: x.position)

    def symmetric_matrix(self):
        if self.transpose is None:
            raise Exception("You need to compute transpose matrix first")
        for index in range(0, self.size):
            for iter_index in range(0, len(self.lines[index])):
                if self.transpose[index][iter_index].position == self.lines[index][iter_index].position \
                        and abs(self.transpose[index][iter_index].value - self.lines[index][iter_index].value) > EPS:
                    return False
        return True

    def get_el_col(self, index_a, index_b):
        try:
            for element in self.lines[index_a]:
                if element.position == index_b:
                    return element
            return None
        except IndexError:
            return None

    def __add__(self, matrix):
        result = Matrix(self.size, 1)
        for i in range(self.size):
            for element in self.lines[i]:
                result.add_to_line(i, copy.copy(element))
            for element in matrix.lines[i]:
                result.add_to_line(i, copy.copy(element))

        return result

    def __mul__(self, obj):
        if type(object) == Matrix:
            matrix = obj
            result = Matrix(self.size, 1)
            for i in range(self.size):
                for element in matrix.lines[i]:
                    for j in range(matrix.size):
                        col_element = self.get_el_col(j, i)
                        if col_element:
                            new_element = Element(col_element.value, element.position)
                            new_element.value *= element.value
                            result.add_to_line(j, new_element)
            return result
        elif type(obj) == np.ndarray:
            result = []
            for index in range(self.size):
                compute_sum = 0
                for element in self.lines[index]:
                    compute_sum += element.value * obj[element.position]
                result.insert(index, compute_sum)
            return result
        else:
            raise Exception("Operation is not permitted")

    def __eq__(self, another_matrix):
        if not isinstance(another_matrix, Matrix):
            raise Exception("You need to pass an matrix obj in order to check the equality")
        if self.size != another_matrix.size:
            raise Exception("Matrices size is different from one another")
        another_matrix = another_matrix.lines
        for index in range(0, self.size):
            for iter_index in range(0, len(another_matrix[index])):
                item = abs(another_matrix[index][iter_index].value - self.lines[index][iter_index].value)
                if another_matrix[index][iter_index].position != self.lines[index][iter_index].position \
                        and abs(another_matrix[index][iter_index].value - self.lines[index][iter_index].value) > EPS:
                    return False
        return True

    def __copy__(self):
        return Matrix(copy.copy(self.lines), rtype=0)







