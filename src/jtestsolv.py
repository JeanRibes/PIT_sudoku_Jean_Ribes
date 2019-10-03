from grid import *
from solver import SudokuSolver
import time
start = time.time()
for i in range(0, 244):
    sg1 = SudokuGrid.from_file("sudoku_db.txt", i)
    ss = SudokuSolver(sg1)
    ssg01: SudokuGrid = ss.solve()
    if ssg01 is None:
        print('AAAAAAh')
        raise UserWarning("sudoku non résolu")
end = time.time()
dt = end-start
print()
print(dt, end=" s\n")
