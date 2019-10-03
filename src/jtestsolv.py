from grid import *
from solver import SudokuSolver

sg = SudokuGrid("175600000009002005000080040006020000008506400000030800050010000700200410000003967")
b= Grid2D(sg.grid.copy())
print(sg.grid)
print(b.get_region_except(2,2,1,1))
sys.exit(0)
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
