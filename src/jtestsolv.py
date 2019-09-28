from grid import *
from solver import SudokuSolver

s = SudokuSolver(SudokuGrid("200000060000070030048090100000300000300010009000008000001020570080730000090000004"))
s = SudokuSolver(SudokuGrid("504000000100300000000006480006002007900107006400600900057800000000001009000000603"))
a:SudokuSolver=s.solve()
print(a.sudokugrid)
print(a.is_solved())
print(a.is_valid())

sys.exit(0)

agrid  = SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
#agrid  = SudokuGrid("002000079008130000000000840200017000070000030000590002069000000000063100520000400")
s = SudokuSolver(agrid)
print(s.is_solved())
print(s.sudokugrid)
print("reducing domains")
print(s.possible_values_grid)
s.solve_step()
print(s.possible_values_grid)
s.reduce_all_domains()
s.reduce_all_domains()
print(s.possible_values_grid)
print(s.sudokugrid)


