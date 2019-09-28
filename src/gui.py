# importations à faire pour la réalisation d'une interface graphique
import sys
from code import InteractiveConsole, InteractiveInterpreter
from contextlib import redirect_stdout
from io import StringIO
from typing import List

from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QCursor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableView, QDialog, QTableWidgetItem, QVBoxLayout, \
    QDialogButtonBox, QPushButton, QLabel, QFileDialog, QListWidgetItem, QAbstractItemView, QTableWidget, QLineEdit, \
    QPlainTextEdit
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


class SudokuGridView:
    table: QTableWidget
    table_item_grid: List[List[QTableWidgetItem]]  # garde une liste des monQitems affichés
    sudoku_list2d: Grid2D  # référence vers la liste des entiers du SudokuSolver
    solutions_list2d: Grid2D

    def __init__(self, table: QTableWidget, solver: SudokuSolver):
        self.table = table
        self.sudoku_list2d = solver.sudokugrid.grid
        self.solutions_list2d = solver.possible_values_grid
        self.table_item_grid = Grid2D(default=None)

        for y, row in enumerate(self.table_item_grid):
            for x, _ in enumerate(row):
                qitem = QTableWidgetItem()
                self.table.setItem(y, x, qitem)
                self.table_item_grid[y][x] = qitem
                if y // 3 < 1 or y // 3 > 1:
                    if x // 3 < 1 or x // 3 > 1:
                        qitem.setBackground(QBrush(QColor("lightGray")))
                if y // 3 == 1 and x // 3 == 1:
                    qitem.setBackground(QBrush(QColor("lightGray")))
                qitem.setToolTip(str(self.solutions_list2d[y][x]))

    def view_to_sudoku(self):
        """
        Écrase les données en les remplaçant par ce qui est affiché à l'écran
        """
        for y in range(0, 9):
            for x in range(0, 9):
                item = self.table_item_grid[y][x].text()
                if item == None or item == '':
                    item = 0
                self.sudoku_list2d[y][x] = int(item)

    def sudokugrid_to_view(self):
        """
        Met à jour l'affichage après un changement des données
        """
        for y in range(0, 9):
            for x in range(0, 9):
                self.table_item_grid[y][x].setText(str(self.sudoku_list2d[y][x]))
                self.table_item_grid[y][x].setToolTip(str(self.solutions_list2d[y][x]))
        self.table.repaint()

    def change_data(self, list2d: List[List[int]]):
        """
        Remplace les données du solver par celles données en paramètre.
        Ne met pas à jour l'affichage tout seul
        :param list2d: la liste 2D des nouvelles données
        """
        for y in range(0, 9):
            for x in range(0, 9):
                self.table_item_grid[y][x].setText(str(list2d[y][x]))
                self.sudoku_list2d[y][x] = list2d[y][x]


class JankyDebugInterpreter(InteractiveInterpreter):
    inbox: QLineEdit
    outbox: QPlainTextEdit
    a: InteractiveConsole
    history: list

    def __init__(self, inputBox: QLineEdit, outputBox: QPlainTextEdit, *args, **kwargs):
        self.inbox = inputBox
        self.outbox = outputBox
        self.inbox.returnPressed.connect(self.read_eval_print)
        self.outbox.appendPlainText("salut")
        super().__init__(*args, **kwargs)
        self.history = list()

    def read_eval_print(self):
        # self.outbox.scroll(0, 100)
        code = self.inbox.text()
        if code == "up":
            self.inbox.setText(self.history.pop())
            return
        with redirect_stdout(self):
            try:
                 t = exec(code, self.locals)
                 if t is not None:
                     self.write(t)
            except:
                self.showtraceback()
        self.inbox.setText("")
        self.history.append(code)

    def write(self, data):
        texte = str(data)
        self.outbox.insertPlainText(texte)
        self.outbox.ensureCursorVisible()
        # self.outbox.centerCursor()
        # self.outbox.setCursor(QCursor())


class SudokuWindow(Ui_MainWindow):
    main_window: QMainWindow
    solver: SudokuSolver
    sudoku_model: SudokuGridView
    jid: JankyDebugInterpreter

    def __init__(self, main_window: QMainWindow):
        self.setupUi(main_window)
        self.retranslateUi(main_window)

        self.sudokuLoad.clicked.connect(self.load_new_sudoku)
        self.main_window = main_window
        self.main_window.show()

        self.solver = SudokuSolver(
            SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376"))

        self.sudoku_model = SudokuGridView(self.sudokuTableWidget, self.solver)
        self.sudoku_model.sudokugrid_to_view()

        self.jid = JankyDebugInterpreter(self.in_box, self.out_box, locals=locals())
        self.sudokuTableWidget.itemClicked.connect(self.sudoku_clicked)

        self.solveButton.clicked.connect(self.solve)
        self.fileSelectButton.clicked.connect(self.dialog_select_file)
        self.sudokuDbList.addItem("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
        self.sudokuDbList.itemDoubleClicked.connect(self.dblist_select)
        self.gridEditMode.stateChanged.connect(self.toggle_edit_mode)
        self.exportGridButton.clicked.connect(self.export_grid)

    def dialog_select_file(self):
        file, type = QFileDialog.getOpenFileName(caption="Séléctionner un fichier de sudokus",
                                                 filter="Text File (*.txt)")
        if file == '':
            return
        with open(file, 'r') as sudokudb_file:
            for line in sudokudb_file.readlines():
                self.sudokuDbList.addItem(line.rstrip("\n"))
        self.sudokuDbList.repaint()

    def dblist_select(self, a: QListWidgetItem):
        print(a.text())
        self.sudokuInput.setText(a.text())

    def solve(self):
        self.gridEditMode.setCheckState(0)
        self.toggle_edit_mode(0)
        self.solver.solve_step()
        self.sudoku_model.sudokugrid_to_view()

    def load_new_sudoku(self):
        sudoku_string = self.sudokuInput.text()
        self.sudokuInput.setText("")
        try:
            self.sudoku_model.change_data(SudokuGrid(sudoku_string).grid)
            self.sudoku_model.sudokugrid_to_view()
        except ValueError:
            qde = ErrorDialog("Erreur de format !")
            qde.exec()

    def sudoku_clicked(self, item: QTableWidgetItem):
        print("y={}, x={}".format(item.row(), item.column()))

    def toggle_edit_mode(self, a):
        if a == 0:
            self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.sudoku_model.view_to_sudoku()
            self.solver.reduce_all_domains(auto_complete=False)
            self.sudoku_model.sudokugrid_to_view()
        elif a == 2:
            # self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
            self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
            # self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.EditKeyPressed)

    def export_grid(self):
        grid_flat = list()
        for row in self.sudoku_model.table_item_grid:
            for item in row:
                grid_flat.append(item.text())
        self.sudokuInput.setText("".join(grid_flat))


app = QApplication.instance()
if not app:  # sinon on crée une instance de QApplication
    app = QApplication(sys.argv)
main_window = SudokuWindow(QMainWindow())

# exécution de l'application, l'exécution permet de gérer les événements
app.exec_()
