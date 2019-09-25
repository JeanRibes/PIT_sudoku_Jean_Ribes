# -*-coding: utf8-*-
import sys
from copy import deepcopy


class SudokuGrid:
    """Cette classe représente une grille de Sudoku.
    Toutes ces méthodes sont à compléter en vous basant sur la documentation fournie en docstring.
    """
    grid: list = None

    @classmethod
    def from_file(cls, filename, line):
        """À COMPLÉTER!
        Cette méthode de classe crée une nouvelle instance de grille
        à partir d'une ligne contenue dans un fichier.
        Pour retourner une nouvelle instance de la classe, utilisez le premier argument ``cls`` ainsi::
            return cls(arguments du constructeur)

        :param filename: Chemin d'accès vers le fichier à lire
        :param line: Numéro de la ligne à lire
        :type filename: str
        :type line: int
        :return: La grille de Sudoku correspondant à la ligne donnée dans le fichier donné
        :rtype: SudokuGrid
        """
        # with open(filename, 'r') as f:
        #    line_str = list(f.readlines()[line].rstrip("\n"))
        # f.close() #pas utilisé ici
        line_f = None
        with open(filename, 'r') as f:
            l_n = 0
            while l_n < line:
                f.readline()
                l_n += 1
            line_f = f.readline().rstrip()
        return cls(line_f)

    @classmethod
    def from_stdin(cls):
        """À COMPLÉTER!
        Cette méthode de classe crée une nouvelle instance de grille
        à partir d'une ligne lu depuis l'entrée standard (saisi utilisateur).
        *Variante avancée: Permettez aussi de «piper» une ligne décrivant un Sudoku.*
        :return: La grille de Sudoku correspondant à la ligne donnée par l'utilisateur
        :rtype: SudokuGrid
        """
        return cls(input())
        raise NotImplementedError()

    def __init__(self, initial_values_str):
        """
        Ce constructeur initialise une nouvelle instance de la classe SudokuGrid.
        Il doit effectuer la conversation de chaque caractère de la chaîne en nombre entier,
        et lever une exception si elle ne peut pas être interprétée comme une grille de Sudoku.
        :param initial_values_str: Une chaîne de caractères contenant **exactement 81 chiffres allant de 0 à 9**,
            où ``0`` indique une case vide
        :type initial_values_str: str
        """
        try:
            assert len(initial_values_str) == 81, "Entrée non valide (!=81)"
        except AssertionError:
            raise ValueError("entrée doit être de longueur 81")
        initial_values_list = list(initial_values_str)
        self.grid = [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],

            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],

            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        ]
        initial_values_list.reverse()
        for y in range(0, 9):
            for x in range(0, 9):
                self.grid[y][x] = int(initial_values_list.pop())

    def __str__(self):
        """À COMPLÉTER!
        Cette méthode convertit une grille de Sudoku vers un format texte pour être affichée.
        :return: Une chaîne de caractère (sur plusieurs lignes...) représentant la grille
        :rtype: str
        """
        s = []
        for l in range(0, 9):
            s.append("─" * 37)
            s.append("\n║ ")
            for c in range(0, 8):
                s.append(str(self.grid[l][c]))
                if (c + 1) % 3 == 0:
                    s.append(" ║ ")
                else:
                    s.append(" │ ")
            s.append(str(self.grid[l][8]) + " ║\n")
        s.append("─" * 37)
        return "".join(s)

    def get_row(self, i):
        """À COMPLÉTER!
        Cette méthode extrait une ligne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param i: Numéro de la ligne à extraire, entre 0 et 8
        :type i: int
        :return: La liste des valeurs présentes à la ligne donnée
        :rtype: list of int
        """
        return self.grid[i]

    def get_col(self, j):
        """À COMPLÉTER!
        Cette méthode extrait une colonne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param j: Numéro de la colonne à extraire, entre 0 et 8
        :type j: int
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of int
        """
        return (self.grid[i][j] for i in range(0, 9))  # range ne va pas à 9

    def get_region(self, reg_row, reg_col):
        """À COMPLÉTER!
        Cette méthode extrait les valeurs présentes dans une région donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param reg_row: Position verticale de la région à extraire, **entre 0 et 2**
        :param reg_col: Position horizontale de la région à extraire, **entre 0 et 2**
        :type reg_row: int
        :type reg_col: int
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of int
        """
        c = [[None, None, None], [None, None, None], [None, None, None]]
        # for y in range(0, 9):
        #    for x in range(0, 9):
        #        sl = y // 3
        #        sc = x // 3
        for i in range(0, 3):
            for j in range(0, 3):
                c[i][j] = self.grid[3 * reg_row + i][3 * reg_col + j]
        region_tc = list()
        for e in c:
            region_tc.extend(e)
        return region_tc

    def get_empty_pos(self):
        """À COMPLÉTER!
        Cette méthode renvoit la position des cases vides dans la grille de Sudoku,
        sous la forme de tuples ``(i,j)`` où ``i`` est le numéro de ligne et ``j`` le numéro de colonne.
        *Variante avancée: Renvoyez un générateur sur les tuples de positions ``(i,j)`` au lieu d'une liste*
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of tuple of int
        """
        empty_poss = list()
        for y in range(0, 9):
            for x in range(0, 9):
                if self.grid[y][x] == 0:
                    empty_poss.append((y, x))
        return empty_poss

    def write(self, i, j, v):
        """À COMPLÉTER!
        Cette méthode écrit la valeur ``v`` dans la case ``(i,j)`` de la grille de Sudoku.
        *Variante avancée: Levez une exception si ``i``, ``j`` ou ``v``
        ne sont pas dans les bonnes plages de valeurs*
        *Variante avancée: Ajoutez un argument booléen optionnel ``force``
        qui empêche d'écrire sur une case non vide*
        :param i: Numéro de ligne de la case à mettre à jour, entre 0 et 8
        :param j: Numéro de colonne de la case à mettre à jour, entre 0 et 8
        :param v: Valeur à écrire dans la case ``(i,j)``, entre 1 et 9
        """
        try:
            assert 0 < i < 8
            assert 0 < j < 8
            assert 1 < v < 9
        except:
            pass
        #            raise UserWarning("Valeurs sortant de la plage")
        self.grid[i][j] = v

    def copy(self):
        """À COMPLÉTER!
        Cette méthode renvoie une nouvelle instance de la classe SudokuGrid,
        copie **indépendante** de la grille de Sudoku.
        Vous pouvez utiliser ``self.__class__(argument du constructeur)``.
        *Variante avancée: vous pouvez aussi utiliser ``self.__new__(self.__class__)``
        et manuellement initialiser les attributs de la copie.*
        """
        s = self.__new__(self.__class__)
        s.grid = deepcopy(self.grid)  # oui autant ne pas tout copier à la main
        return s

    def __getitem__(self, item):
        return self.grid.__getitem__(item)

    def get_item(self, row, col):
        return self.grid[row][col]
