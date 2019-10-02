from grid import *
from solver import SudokuSolver

agrid  = SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
s = SudokuSolver(agrid)
print(s.is_solved())
print(s.sudokugrid)
s.solve_step()
print(s.is_solved())


