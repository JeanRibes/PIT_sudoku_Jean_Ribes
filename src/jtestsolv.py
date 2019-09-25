from grid import SudokuGrid
from solver import SudokuSolver

agrid  = SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
s = SudokuSolver(agrid)
print(s.is_solved())
print(s.sudokugrid)
print("reducing domains")
print(s.reduce_all_domains())
print("reduced domains")

