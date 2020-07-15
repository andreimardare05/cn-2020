from util.Polynom import Polynom


def f(x):
    return (x - 1) * (x - 2) * (x - 3)


p = Polynom([1, -6, 11, -6], f)
print(p.solve_using_numpy())
print(p.roots())
# Call in order to write in file the result
p.write_in_file()
