from grid import *
from solver import SudokuSolver

sg1 = SudokuGrid("200000060000075030048090100000300000300010009000008000001020570080730000090000004")
ssg01 = SudokuSolver(sg1)

def solve(solver: SudokuSolver):
    solver.solve_step()
    if solver.is_solved():
        return solver
    elif solver.is_valid():
        for child_solver in solver.branch():
            child_solver.reduce_all_domains()
            c_s = solve(child_solver)
            if c_s is not None:
                return c_s
    else:
        print(".", end='')
        return None
solved = solve(ssg01)
print(solved.sudokugrid)

sys.exit(0)
s01 = ssg01.branch()
v_s=list()
for solver in s01:
    solver.solve_step()
    if solver.is_valid():
        print(solver.is_solved())
        for s2 in solver.branch():
            v_s.append(s2)
for solver in v_s:
    solver.solve_step()
    if solver.is_valid():
        if solver.is_solved():
            print(solver.sudokugrid)