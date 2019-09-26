from grid import *
from solver import SudokuSolver

agrid  = SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
agrid  = SudokuGrid("002000079008130000000000840200017000070000030000590002069000000000063100520000400")
s = SudokuSolver(agrid)
print(s.is_solved())
print(s.sudokugrid)
print("reducing domains")
s.reduce_all_domains()
print(s.possible_values_grid)
print("reduced domains")

#rd=s.reduce_all_domains()
#g = Grid2D()
#g = Grid2D(rd)
#print(g.list2d)
#print("using Grid2D")
#print(g)

#g2=Grid2D(list2d=[[1,2],[3,4]], length=2)
#print(g2)
#print(g2[1][1])
#g2[0][1]=0
#print(g2)
#print(list(g2.get_row(0)))
#print(list(g2.get_col(1)))
