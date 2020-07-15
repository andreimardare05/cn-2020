from util.Matrix import Matrix

matrix_a = Matrix("input/a.txt")
matrix_b = Matrix("input/b.txt")

matrix_result = matrix_a + matrix_b
matrix_result2 = matrix_a * matrix_b

matrix_apb = Matrix("input/aplusb.txt")
matrix_aob = Matrix("input/aorib.txt")

print(matrix_result == matrix_apb)
print(matrix_result2 == matrix_aob)