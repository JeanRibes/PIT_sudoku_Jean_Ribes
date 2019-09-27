# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qtcreator-ui/SudokuSolver/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(561, 552)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 301, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sudokuInput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.sudokuInput.setObjectName("sudokuInput")
        self.horizontalLayout.addWidget(self.sudokuInput)
        self.sudokuLoad = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.sudokuLoad.setObjectName("sudokuLoad")
        self.horizontalLayout.addWidget(self.sudokuLoad)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.solveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.solveButton.setObjectName("solveButton")
        self.verticalLayout.addWidget(self.solveButton)
        self.sudokuTableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.sudokuTableWidget.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sudokuTableWidget.sizePolicy().hasHeightForWidth())
        self.sudokuTableWidget.setSizePolicy(sizePolicy)
        self.sudokuTableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sudokuTableWidget.setLineWidth(1)
        self.sudokuTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sudokuTableWidget.setTabKeyNavigation(False)
        self.sudokuTableWidget.setRowCount(9)
        self.sudokuTableWidget.setColumnCount(9)
        self.sudokuTableWidget.setObjectName("sudokuTableWidget")
        self.sudokuTableWidget.horizontalHeader().setVisible(False)
        self.sudokuTableWidget.horizontalHeader().setDefaultSectionSize(30)
        self.sudokuTableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.sudokuTableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 561, 22))
        self.menubar.setObjectName("menubar")
        self.menuSolveur_de_Sudoku_de_Jean_Ribes = QtWidgets.QMenu(self.menubar)
        self.menuSolveur_de_Sudoku_de_Jean_Ribes.setObjectName("menuSolveur_de_Sudoku_de_Jean_Ribes")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuSolveur_de_Sudoku_de_Jean_Ribes.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Solveur de sudoku de Jean Ribes"))
        self.sudokuLoad.setText(_translate("MainWindow", "Charger ce sudoku"))
        self.solveButton.setText(_translate("MainWindow", "Résoudre"))
        self.menuSolveur_de_Sudoku_de_Jean_Ribes.setTitle(_translate("MainWindow", "Solveur de Sudoku de Jean Ribes"))
