# importations à faire pour la réalisation d'une interface graphique
import sys
from code import InteractiveConsole, InteractiveInterpreter
from contextlib import redirect_stdout
from io import StringIO
from threading import Thread
from typing import List

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QCursor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableView, QDialog, QTableWidgetItem, QVBoxLayout, \
    QDialogButtonBox, QPushButton, QLabel, QFileDialog, QListWidgetItem, QAbstractItemView, QTableWidget, QLineEdit, \
    QPlainTextEdit
from PyQt5 import uic

import solver
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

    def __init__(self, table: QTableWidget, solver: SudokuSolver):
        self.table = table
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
        self.sudokugrid_to_view(solver)

    def view_to_sudoku(self) -> Grid2D:
        """
        Écrase les données en les remplaçant par ce qui est affiché à l'écran
        """
        new_grid = Grid2D(default=None)
        for y in range(0, 9):
            for x in range(0, 9):
                item = self.table_item_grid[y][x].text()
                if item == None or item == '':
                    item = 0
                new_grid[y][x] = int(item)
        return new_grid

    def sudokugrid_to_view(self, solver: SudokuSolver):
        """
        Met à jour l'affichage après un changement des données
        """
        for y in range(0, 9):
            for x in range(0, 9):
                if solver.sudokugrid.grid[y][x] == 0:
                    self.table_item_grid[y][x].setText("")
                else:
                    self.table_item_grid[y][x].setText(str(solver.sudokugrid.grid[y][x]))
                self.table_item_grid[y][x].setToolTip(str(solver.possible_values_grid[y][x]))
        self.table.repaint()


class JankyDebugInterpreter(InteractiveInterpreter):
    inbox: QLineEdit
    outbox: QPlainTextEdit
    a: InteractiveConsole
    history: list

    def __init__(self, inputBox: QLineEdit, outputBox: QPlainTextEdit, *args, **kwargs):
        self.inbox = inputBox
        self.outbox = outputBox
        self.inbox.returnPressed.connect(self.read_eval_print)
        self.write("Python %s on %s\n%s\n(%s)\n" %
                   (sys.version, sys.platform, "",
                    self.__class__.__name__))
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
            except SystemExit:
                raise
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


class SudokuWindow(QMainWindow, Ui_MainWindow):
    solver: SudokuSolver
    sudoku_model: SudokuGridView
    jdein: JankyDebugInterpreter

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.debugBox.setLayout(self.debugLayout)
        self.selectBox.setLayout(self.selectLayout)

        self.sudokuLoad.clicked.connect(self.load_new_sudoku)

        self.solver = SudokuSolver(
            SudokuGrid("349287501000000700000509002200095007001000400800720005100402000008000000000000376"))

        self.sudoku_model = SudokuGridView(self.sudokuTableWidget, self.solver)

        self.jdein = JankyDebugInterpreter(self.in_box, self.out_box, locals=locals())
        self.sudokuTableWidget.itemClicked.connect(self.sudoku_clicked)

        self.solveButton.clicked.connect(self.solve)
        self.fileSelectButton.clicked.connect(self.dialog_select_file)
        self.sudokuDbList.addItem("349287501000000700000509002200095007001000400800720005100402000008000000000000376")
        self.sudokuDbList.itemDoubleClicked.connect(self.dblist_select)
        self.gridEditMode.stateChanged.connect(self.toggle_edit_mode)
        self.exportGridButton.clicked.connect(self.export_grid)
        self.big_solve.clicked.connect(self.hard_solve)
        self.nextButton.clicked.connect(self.next_sudoku)
        self.previousButton.clicked.connect(self.previous_sudoku)
        try:
            self.load_file("../sudoku_db.txt")
        except:
            pass
        self.show()

    def next_sudoku(self):
        r = self.sudokuDbList.currentRow()
        if r < self.sudokuDbList.count():
            self.sudokuDbList.setCurrentRow(r + 1)
            self.dblist_select(self.sudokuDbList.selectedItems().pop())
            self.hard_solve()

    def previous_sudoku(self):
        r = self.sudokuDbList.currentRow()
        if r > 0:
            self.sudokuDbList.setCurrentRow(r - 1)
            self.dblist_select(self.sudokuDbList.selectedItems().pop())

    def dialog_select_file(self):
        file, type = QFileDialog.getOpenFileName(caption="Séléctionner un fichier de sudokus",
                                                 filter="Text File (*.txt)")
        if file == '':
            return
        else:
            self.load_file(file)

    def dblist_select(self, a: QListWidgetItem):
        print(a.text())
        self.jdein.write(a.text() + "\n")
        self.solver = SudokuSolver(SudokuGrid(a.text()))
        self.update_view()

    def solve(self):
        self.gridEditMode.setCheckState(0)
        self.toggle_edit_mode(0)
        self.solver.solve_step()
        self.update_view()

    def hard_solve(self):
        self.gridEditMode.setCheckState(0)
        self.toggle_edit_mode(0)
        solver.daemon_runnning = False
        if hasattr(self, 'daemon_sudoku'):
            self.daemon_sudoku.quit()
            self.daemon_sudoku.exit(0)
            self.daemon_sudoku.terminate()

        class DaemonSolver(QThread):
            daemon = True
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self, solver):
                super().__init__()
                self.solver = solver

            def run(self):
                def update(sud):
                    self.signal.emit(SudokuSolver(sud))
                result: SudokuGrid = self.solver.solve(update)
                update(result)

        self.daemon_sudoku = DaemonSolver(self.solver)
        self.daemon_sudoku.signal.connect(self.thread_receive)
        solver.daemon_runnning = True
        self.daemon_sudoku.start()

    def load_new_sudoku(self):
        sudoku_string = self.sudokuInput.text()
        self.sudokuInput.setText("")
        try:
            self.solver = SudokuSolver(SudokuGrid(sudoku_string))
            self.update_view()
        except ValueError:
            qde = ErrorDialog("Erreur de format !")
            qde.exec()

    def sudoku_clicked(self, item: QTableWidgetItem):
        print("y={}, x={}".format(item.row(), item.column()))

    def toggle_edit_mode(self, a):
        if a == 0:
            self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.solver.sudokugrid.grid = self.sudoku_model.view_to_sudoku()
            self.solver.reduce_all_domains(auto_complete=False)
            self.update_view()
        elif a == 2:
            # self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
            self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
            # self.sudokuTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.EditKeyPressed)

    def export_grid(self):
        grid_flat = list()
        for row in self.sudoku_model.view_to_sudoku():
            for item in row:
                grid_flat.append(item.text())
        self.sudokuInput.setText("".join(grid_flat))

    def update_view(self):
        self.sudoku_model.sudokugrid_to_view(self.solver)

    def load_file(self, file: str):
        with open(file, 'r') as sudokudb_file:
            for line in sudokudb_file.readlines():
                self.sudokuDbList.addItem(line.rstrip("\n"))
        self.sudokuDbList.repaint()

    def thread_receive(self, solver: SudokuSolver):
        self.solver = solver
        self.update_view()


app = QApplication.instance()
if not app:  # sinon on crée une instance de QApplication
    app = QApplication(sys.argv)
main_window = SudokuWindow()

# exécution de l'application, l'exécution permet de gérer les événements
sys.exit(app.exec_())
