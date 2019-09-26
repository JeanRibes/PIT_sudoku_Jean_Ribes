from grid import *
from solver import SudokuSolver

agrid  = SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
#agrid  = SudokuGrid("002000079008130000000000840200017000070000030000590002069000000000063100520000400")
s = SudokuSolver(agrid)
print(s.is_solved())
print(s.sudokugrid)
print("reducing domains")
s.reduce_all_domains()
print(s.possible_values_grid)
print("commiting")
##for n in s.possible_values_grid[7][6]:
#a=list(s.possible_values_grid.get_col_except(6,7))
#print(list(itertools.chain(*a)))
#for n in s.possible_values_grid[7][6]:
#    if n not in itertools.chain(*a):
#        print(n)
print(s.possible_values_grid)
s.reduce_all_domains()
s.find_lone_occurences()
s.reduce_all_domains()
s.find_lone_occurences()
print(s.sudokugrid)
#print(s.sudokugrid)
#print(s.possible_values_grid)
#print(s.is_solved())