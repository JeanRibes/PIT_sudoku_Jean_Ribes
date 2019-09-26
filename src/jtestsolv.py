from grid import *
from solver import SudokuSolver

agrid  = SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
s = SudokuSolver(agrid)
print(s.is_solved())
print(s.sudokugrid)
print("reducing domains")
print(s.reduce_all_domains())
print("reduced domains")

rd=s.reduce_all_domains()
g = Grid2D()
g = Grid2D(rd)
print(g.list2d)
print("using Grid2D")
print(g)
