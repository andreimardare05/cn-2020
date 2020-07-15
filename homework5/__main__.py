from util.Solver import Solver

files = ['a_300.txt', 'a_500.txt', 'a_1000.txt', 'a_1500.txt', 'a_2020.txt', 'test_a.txt']
print("Files available are: ", files)

index = int(input("Enter the index of the file (from 1-6): "))
parameter = int(input("Enter the parameter value: "))

solver = Solver(f"input/{files[index-1]}", parameter)
solver.solve()
