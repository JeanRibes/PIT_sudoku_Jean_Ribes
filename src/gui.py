# importations à faire pour la réalisation d'une interface graphique
import sys
from typing import List

from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableView, QDialog, QTableWidgetItem, QVBoxLayout, \
    QDialogButtonBox, QPushButton, QLabel
from PyQt5 import uic
from grid import Grid2D, SudokuGrid
from qt_ui import Ui_MainWindow
from solver import SudokuSolver


class ErrorDialog(QDialog):
    def __init__(self, text=None, title="Erreur", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(title)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(text))
        self.layout.addWidget(self.ok_button)
        self.setLayout(self.layout)


class SudokuWindow(Ui_MainWindow):
    main_window: QMainWindow
    solver: SudokuSolver
    table_item_grid: List[List[QTableWidgetItem]]

    def __init__(self, main_window: QMainWindow):
        self.setupUi(main_window)
        self.retranslateUi(main_window)

        self.sudokuLoad.clicked.connect(self.load_new_sudoku)
        self.main_window = main_window
        self.main_window.show()

        self.table_item_grid = Grid2D(default=None)  # prépare l'affichage de la grille
        for y, row in enumerate(self.table_item_grid):
            for x, _ in enumerate(row):
                qitem = QTableWidgetItem()
                self.sudokuTableWidget.setItem(y, x, qitem)
                self.table_item_grid[y][x] = qitem
                if y // 3 < 1 or y // 3 > 1:
                    if x // 3 < 1 or x // 3 > 1:
                        qitem.setBackground(QBrush(QColor("lightGray")))
                if y//3 == 1 and x//3 == 1:
                    qitem.setBackground(QBrush(QColor("lightGray")))

        self.solver = SudokuSolver(
            SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376"))
        self.update_data(self.solver.sudokugrid.grid)

        self.solveButton.clicked.connect(self.solve)

    def solve(self):
        self.solver.solve_step()
        self.update_data()

    def update_data(self, list2d: Grid2D = None):
        if list2d is None:
            list2d = self.solver.sudokugrid.grid
        for y, row in enumerate(list2d):
            for x, elem in enumerate(row):
                self.table_item_grid[y][x].setText(str(elem))
                if elem == 0:
                    self.table_item_grid[y][x].setToolTip(
                        str(self.solver.possible_values_grid[y][x])
                    )
        self.sudokuTableWidget.repaint()

    def load_new_sudoku(self):
        sudoku_string = self.sudokuInput.text()
        try:
            self.solver = SudokuSolver(SudokuGrid(sudoku_string))
            self.update_data()
        except ValueError:
            qde = ErrorDialog("Erreur de format !")
            qde.exec()


app = QApplication.instance()
if not app:  # sinon on crée une instance de QApplication
    app = QApplication(sys.argv)
main_window = SudokuWindow(QMainWindow())

# exécution de l'application, l'exécution permet de gérer les événements
app.exec_()
