from resources.solver import LinearEq


my_third_eq = LinearEq(7,[[2.5, 2, 2],
     [5, 6, 5],
     [5, 6, 6.5]], [2,2,2])

my_third_eq = LinearEq(6, [[1.0, 2.0, 1.0, 1.0],
     [1.0, 4.0, -1.0, 7.0],
     [4.0, 9.0, 5.0, 11.0],
     [1.0, 0.0, 6.0, 4.0]],  [0.0, 20.0, 18.0, 1.0])

my_third_eq = LinearEq(6, [[1.0, 1.0, -1.0], [1.0, -2.0, 3.0], [2.0, 3.0, 1.0]], [4.0, -6.0, 7.0])


print("Coef. linear eq:")
print(my_third_eq.matrix)

print("Result. eq:")
print(my_third_eq.result)

print("LOWER(l): ")
print(my_third_eq.lower)

print("UPPER(u): ")
print(my_third_eq.lower)

print("Solution for linear eq.:")
print(my_third_eq.resolve_with_LU_decomposition())

print("1st. norm: ", my_third_eq.norm())
print("Other norms: \n", my_third_eq.additional_norms())

print("Inv. norm: ")
print(my_third_eq.compute_inv_norm())

print("Inv. coef. matrix: ")
print(my_third_eq.compute_inv_with_LU_decomposition())



