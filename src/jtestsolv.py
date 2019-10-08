from grid import *
from solver import SudokuSolver
import time
start = time.time()
for i in range(1, 245):
    sg1 = SudokuGrid.from_file("sudoku_db.txt", i)
    ss = SudokuSolver(sg1)
    SudokuGrid = ss.solve()
end = time.time()
dt = end-start
print()
print(dt, end=" s\n")
