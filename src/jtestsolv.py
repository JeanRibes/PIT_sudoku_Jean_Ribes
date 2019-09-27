from grid import *
from solver import SudokuSolver

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
