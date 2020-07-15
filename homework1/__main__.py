import math
import tkinter


def graphic(c_matrix):
    window = tkinter.Tk()

    for i in range(0, len(c_matrix)):
        for j in range(0, len(c_matrix)):
            block = tkinter.Label(window, text=c_matrix[i][j])
            block.grid(row=i, column=j)

    # block = tkinter.Label(window, text="Salut")
    # block.grid(row = 1, column = 1)

    # for i, block_row in enumerate(maze):
    #     for j, block in enumerate(block_row):
    #         block.grid(row=i, column=j)

    window.mainloop()


def first():
    pw = 0
    pc = 1
    while 1 + pc != 1:
        pw = pw + 1
        pc = 10 ** (-1 * pw)

    return pc


print(first())


def second1():
    x = 1.0
    y = first()
    z = y

    return ((x + y) + z) == (x + (y + z))


def second2():
    x = 1.0
    y = first()
    z = y

    while ((x * y) * z == x * (y * z)):
        x += 1.0

    print(y, z)
    return x


print(second2())


def NUM(v):
    number = 0
    i = 0
    for b in v:
        number = number + b * (2 ** (len(v) - i - 1))
        i += 1
    return number


def divide_matrix(matrix, m, p):
    array_of_matrix = []
    n = len(matrix)

    for i in range(0, p):
        new_matrix = []
        first_frontier = m * i + 1
        second_frontier = m * (i + 1)
        for j in range(0, n):
            new_matrix.append([matrix[j][first_frontier - 1:second_frontier]])

        # fill empty
        new_matrix_len = len(new_matrix)
        for line in range(0, new_matrix_len):
            while len(new_matrix[line]) < m:
                new_matrix[line].append(0)

        array_of_matrix.append(new_matrix)
        # new_matrix = []
        # for col in range(m * (i - 1) + 1, (m * i) + 1):
        #     new_matrix.append(matrix[col])
        # array_of_matrix.append(new_matrix)

    return array_of_matrix


def c_init(n):
    c_i = []
    for i in range(n):
        c_i_row = []
        for j in range(n):
            c_i_row.append(0)
        c_i.append(c_i_row)
    return c_i


def append_line(first_line, second_line):
    new_line = []
    for i, j in zip(first_line, second_line):
        new_line.append(int(i or j))
    return new_line


def third():
    A = [[0, 1, 0],
         [1, 0, 1],
         [1, 1, 1]]

    B = [[0, 0, 1],
         [1, 0, 1],
         [0, 1, 1]]

    n: int = len(A)

    m: int = math.floor(math.log(n, 2))
    p: int = math.ceil(n / m)

    sub_matrix_a = []
    for i in range(0, p):
        a: list = list()
        first_frontier: int = m * i + 1
        second_frontier: int = m * (i + 1)

        for j in range(0, n):
            a.append(list(A[j][first_frontier - 1:second_frontier]))

        for line in range(0, len(a)):
            while len(a[line]) < m:
                a[line].append(0)
        sub_matrix_a.append(a)

    sub_matrix_b = []

    for i in range(0, p):
        first_frontier = m * i + 1
        second_frontier = m * (i + 1)
        sub_matrix_b.append(B[first_frontier - 1:second_frontier])
        for line in range(0, len(sub_matrix_b[0])):
            while len(sub_matrix_b[-1]) < m:
                sub_matrix_b[-1].append([0] * n)

    # creating c_i
    c_i = c_init(n)

    for i in range(0, p):
        sum_linii_b = [[0] * n]

        for j in range(0, 2 ** m):
            k = 0
            if j == 0:
                k = 0
            else:
                while 2 ** k <= j:
                    k = k + 1
                k = k - 1
            sum_linii_b.append(append_line(sum_linii_b[j - (2 ** k)], sub_matrix_b[i][k]))

            C_af = list()
            for x in range(0, n):
                C_af.append(sum_linii_b[NUM(sub_matrix_a[i][x]) - 1])

            z = 0
            for q, r in zip(c_i, C_af):
                c_i[z] = append_line(q, r)
                z = z + 1

    print(c_i)
    graphic(c_i)


third()
