from util.Element import Element


class Matrix:
    file = None
    size = None
    lines = None

    def __init__(self, data, rtype=0):
        if rtype == 0:
            self.init_from_file(data)
        else:
            self.init_empty(data)

    def init_from_file(self, file):
        self.file = open(file, "r")
        self.size = int(self.file.readline())
        self.lines = [[]] * self.size

        while 1:
            element = self.file.readline().split()

            if len(element) == 0:
                break

            new_element = Element(element[0][:-1], element[2])

            position = int(element[1][:-1])

            if not self.lines[position]:
                self.lines[position] = []
            self.lines[position].append(new_element)

    def init_empty(self, size):
        self.size = size
        self.lines = [[]] * self.size

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

    def __add__(self, matrix):
        result = Matrix(self.size, 1)
        for i in range(self.size):
            for element in self.lines[i]:
                result.add_to_line(i, element.copy())
            for element in matrix.lines[i]:
                result.add_to_line(i, element.copy())

        return result

    def __eq__(self, matrix):
        if self.size != matrix.size:
            return False

        for i in range(self.size):
            for element in self.lines[i]:
                if element not in matrix.lines[i]:
                    return False

            for element in matrix.lines[i]:
                if element not in self.lines[i]:
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

    def __mul__(self, matrix):
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

    def print(self):
        for line in self.lines:
            print(line)
