#!/usr/bin/env python3
from grid import SudokuGrid
from sys import argv

from solver import SudokuSolver

if __name__ == '__main__':
    ifile, iline = None, None
    if len(argv) == 3:
        ifile = str(argv[1])
        iline = int(argv[2])
    else:
        ifile = input("Nom du fichier contenant les sudokus :")
        iline = input("Numéro de ligne contenant le sudoku voulu: ")
    sudoku = SudokuGrid.from_file(ifile, int(iline))
    solver = SudokuSolver(sudoku)
    cheat = False
    while (not solver.is_solved()) or cheat:
        print(solver.grilleSudoku)
        x = input("Position x [0-8]: ")
        y = input("Position y [0-8]: ")
        n = input("Valeur [1-9]: ")
        if x == "cheat":
            solver.grilleSudoku = solver.solve()
            cheat = True
            print("Cheating...")
            continue
        try:
            cheat = False
            if not sudoku.write(int(y), int(x), int(n)):
                print("erreur !")
        except UserWarning as e:
            print(" * Erreur ! *")
            print(e.args[0])
    print("Bravo !")
    print(solver.grilleSudoku)
