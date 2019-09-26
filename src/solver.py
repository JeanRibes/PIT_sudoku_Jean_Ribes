# -*-coding: utf8-*-
from grid import SudokuGrid, Grid2D


def list_possible_solutions(liste: list):
    possible_solutions = list(range(1, 10))
    for i in range(1, 9):
        if i in liste:
            possible_solutions.remove(i)
    # for i in liste:
    #    try:
    #        possible_solutions.remove(i)
    #    except ValueError:
    #        pass
    return possible_solutions


class SudokuSolver:
    """Cette classe permet d'explorer les solutions d'une grille de Sudoku pour la résoudre.
    Elle fait intervenir des notions de programmation par contraintes
    que vous n'avez pas à maîtriser pour ce projet."""

    sudokugrid: SudokuGrid = None  # contient le sudoku avec des 0 aux endroits non résolus
    possible_values_grid: Grid2D = None  # contient des {sets} de solutions possibles

    def __init__(self, grid):
        """À COMPLÉTER
        Ce constructeur initialise une nouvelle instance de solver à partir d'une grille initiale.
        Il construit les ensembles de valeurs possibles pour chaque case vide de la grille,
        en respectant les contraintes définissant un Sudoku valide.
        :param grid: Une grille de Sudoku
        :type grid: SudokuGrid
        """
        self.sudokugrid = grid
        self.possible_values_grid = Grid2D(default=-1)
        self.reduce_all_domains()
    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        self.reduce_all_domains() # MaJ des solutions possibles
        for row in self.possible_values_grid:
            for elem in row:
                if len(elem) < 1:
                    return False
        return True

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """
        for y in range(0, 3):  # il n'y a pas exactement 9 chiffres uniques dans un carré
            for x in range(0, 3):  # carré 3x3
                if len(set(self.sudokugrid.get_region(y,
                                                      x))) != 9:  # regarder si faire la somme des 9 éléments est + rapide
                    return False
        for y in range(0, 9):  # il n'y a pas exactement 9 chiffre uniques dans une ligne
            if len(set(self.sudokugrid.get_row(y))) != 9:
                return False
        for x in range(0, 9):  # ... dans une colonnes
            if len(set(self.sudokugrid.get_col(x))) != 9:
                return False
        return True

    def reduce_all_domains(self):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """
        for y in range(0, 9):
            for x in range(0, 9):
                if self.sudokugrid.grid[y][x] == 0:
                    local_others = list(self.sudokugrid.get_row(y)) \
                                   + list(self.sudokugrid.get_col(x)) \
                                   + self.sudokugrid.get_region(y // 3, x // 3)  # carré actuel
                    possible_values = list_possible_solutions(
                        local_others
                    )
                    self.possible_values_grid.list2d[y][x] = set(possible_values)  # set pour avoir des valeurs uniques
                else:
                    self.possible_values_grid.list2d[y][x] = {self.sudokugrid[y][x]}
        return self.possible_values_grid

    def reduce_domains(self, last_i, last_j, last_v):
        """À COMPLÉTER
        Cette méthode devrait être appelée à chaque mise à jour de la grille,
        et élimine la dernière valeur affectée à une case
        pour toutes les autres cases concernées par cette mise à jour (même ligne, même colonne ou même région).
        :param last_i: Numéro de ligne de la dernière case modifiée, entre 0 et 8
        :param last_j: Numéro de colonne de la dernière case modifiée, entre 0 et 8
        :param last_v: Valeur affecté à la dernière case modifiée, entre 1 et 9
        :type last_i: int
        :type last_j: int
        :type last_v: int
        """
        for i in self.possible_values_grid.get_row(last_i):
            try:
                i.remove(last_v)  # en fait c'est des sets
            except KeyError:
                pass

    def commit_one_var(self):
        """À COMPLÉTER
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """
        for y, row in enumerate(self.possible_values_grid):
            for x, elem in enumerate(row):
                if self.sudokugrid[y][x] == 0:
                    if len(elem) == 1:  # pas de 'and' pour optimiser
    #                    print("{} at {},{}".format(elem, y, x))
                        self.possible_values_grid[y][x] = elem
                        self.sudokugrid.write(y, x, elem.pop())
                    return (y, x, elem)
        return None

    def solve_step(self):
        """À COMPLÉTER
        Cette méthode alterne entre l'affectation de case pour lesquelles il n'y a plus qu'une possibilité
        et l'élimination des nouvelles valeurs impossibles pour les autres cases concernées.
        Elle répète cette alternance tant qu'il reste des cases à remplir,
        et correspond à la résolution de Sudokus dits «simple».
        *Variante avancée: en plus de vérifier s'il ne reste plus qu'une seule possibilité pour une case,
        il est aussi possible de vérifier s'il ne reste plus qu'une seule position valide pour une certaine valeur
        sur chaque ligne, chaque colonne et dans chaque région*
        """
        if not self.commit_one_var(): # il n'y avait pas de cases avec une seule possibilité
            self.reduce_all_domains()


    def branch(self):
        """À COMPLÉTER
        Cette méthode sélectionne une variable libre dans la solution partielle actuelle,
        et crée autant de sous-problèmes que d'affectation possible pour cette variable.
        Ces sous-problèmes seront sous la forme de nouvelles instances de solver
        initialisées avec une grille partiellement remplie.
        *Variante avancée: Renvoyez un générateur au lieu d'une liste.*
        *Variante avancée: Un choix judicieux de variable libre,
        ainsi que l'ordre dans lequel les affectations sont testées
        peut fortement améliorer les performances de votre solver.*
        :return: Une liste de sous-problèmes ayant chacun une valeur différente pour la variable choisie
        :rtype: list of SudokuSolver
        """
        raise NotImplementedError()

    def solve(self):
        """
        Cette méthode implémente la fonction principale de la programmation par contrainte.
        Elle cherche d'abord à affiner au mieux la solution partielle actuelle par un appel à ``solve_step``.
        Si la solution est complète, elle la retourne.
        Si elle est invalide, elle renvoie ``None`` pour indiquer un cul-de-sac dans la recherche de solution
        et déclencher un retour vers la précédente solution valide.
        Sinon, elle crée plusieurs sous-problèmes pour explorer différentes possibilités
        en appelant récursivement ``solve`` sur ces sous-problèmes.
        :return: Une solution pour la grille de Sudoku donnée à l'initialisation du solver
        (ou None si pas de solution)
        :rtype: SudokuGrid or None
        """
        raise NotImplementedError()
