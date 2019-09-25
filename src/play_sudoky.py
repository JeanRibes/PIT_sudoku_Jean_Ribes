#!/usr/bin/env python3
from grid import SudokuGrid
from sys import argv
if __name__ == '__main__':
    print(argv)
    ifile,iline=None,None
    if len(argv) == 3:
        ifile = str(argv[1])
        iline = int(argv[2])
    else:
        ifile=input("Nom du fichier contenant les sudokus :")
        iline=intpu("Numéro de ligne contenant le sudoku voulu: ")
    sudoku = SudokuGrid.from_file(ifile, iline)




