# -*-coding: utf8-*-
from grid import SudokuGrid, Grid2D


def list_possible_solutions(liste: list)->set:
    # possible_solutions = list(range(1, 10))
    # for i in range(1, 10):  # il faut bien aller jusqu'à 10 pour inclure 9
    #    if i in liste:
    #        possible_solutions.remove(i)
    # return possible_solutions
    return set(range(1, 10)) - set(liste)  # plus logique quand on utilise des sets


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
        self.possible_values_grid = Grid2D(default={0})
        self.reduce_all_domains()

    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        for row in self.possible_values_grid.list2d:
            for elem in row:
                if elem is not None:
                    if len(elem) < 1:
                        return False
        return True
        # pas nécessaire quand le reste du solveur marche bien, mais utile pour commencer
        # for y, row in enumerate(self.sudokugrid.grid):
        #    for x, elem in enumerate(row):
        #        if elem > 0:
        #            if self.sudokugrid.get_row(y).count(elem) > 1:
        #                print(".", end='')
        #                #            print("Une valeur apparait plus d'une'fois dans sa ligne")
        #                return False
        #            if self.sudokugrid.get_col(x).count(elem) > 1:
        #                print(".", end='')
        #                #           print("Une valeur apparait plus d'une fois dans sa colonne")
        #                return False
        #            if self.sudokugrid.get_region(y // 3, x // 3).count(elem) > 1:
        #                #            print("une valeur apparait plsu d'une fois dans son carré")
        #                print(".", end='')
        #                return False

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """
        return len(list(self.sudokugrid.get_empty_pos())) == 0  # plus rapide

        # plus compréhensible
        # for y in range(0, 3):  # il n'y a pas exactement 9 chiffres uniques dans un carré
        #    for x in range(0, 3):  # carré 3x3
        #        if sum(self.sudokugrid.get_region(y,x)) != 45:  # regarder si faire la somme des 9 éléments est + rapide
        #            return False
        # for y in range(0, 9):  # il n'y a pas exactement 9 chiffre uniques dans une ligne
        #    if sum(self.sudokugrid.get_row(y)) != 45:return False
        # for x in range(0, 9):  # ... dans une colonnes
        #    if sum(self.sudokugrid.get_col(x)) != 45:return False
        # return True

    def reduce_all_domains(self, auto_complete=True):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """
        for y, x in self.sudokugrid.get_empty_pos():
            local_others = self.sudokugrid.get_row(y) \
                           + self.sudokugrid.get_col(x) \
                           + self.sudokugrid.get_region(y // 3, x // 3)  # carré actuel
            possible_values = list_possible_solutions(local_others)
            self.possible_values_grid.list2d[y][x] = possible_values
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
            if last_v in i:
                i.remove(last_v)
                if len(i) == 0:
                    i.add(0)
                # else:
                #    print("bizarre : {} at (y={},x={})".format(i,last_i, last_j))
        for i in self.possible_values_grid.get_col(last_j):
            if last_v in i:
                i.remove(last_v)
                if len(i) == 0:
                    i.add(0)
        for i in self.possible_values_grid.get_region(last_i // 3, last_j // 3):
            if last_v in i:
                i.remove(last_v)
                if len(i) == 0:
                    i.add(0)

    def commit_one_var(self, last_y=0, last_x=0):
        """À COMPLÉTER
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """
        for y, x in self.sudokugrid.get_empty_pos():
            possible_solutions = self.possible_values_grid.list2d[y][x]
            if len(possible_solutions) == 1:
                only_solution = possible_solutions.pop()
                if only_solution != 0:
                    self.sudokugrid.write(y, x, only_solution)
                    possible_solutions.add(0)  # la case devient {0}
                    return y, x, only_solution
            elementsH = set(self.possible_values_grid.get_row_except(y, x))
            elementsV = set(self.possible_values_grid.get_col_except(x, y))
            elementsSquare = set(self.possible_values_grid.get_region_except(y // 3, x // 3, y, x))
            for n in possible_solutions:  # int
                if len(elementsV) > 1:  # pour ne pas utiliser 0 comme élément, car il apparait forcément dans les
                                        # solutions (il représente les cases remplies)
                    if n not in elementsV and n not in self.sudokugrid.get_col(x):
                        #                print("V{} at ({},{})".format(n, y, x))
                        self.sudokugrid.write(y, x, n)
                        self.possible_values_grid.list2d[y][x] = {0}
                        return y, x, n
                if len(elementsH) > 1:
                    if n not in elementsH and n not in self.sudokugrid.get_row(y):
                        #               print("H{} at ({},{})".format(n, y, x))
                        self.sudokugrid.write(y, x, n)
                        self.possible_values_grid.list2d[y][x] = {0}
                        return y, x, n
                if len(elementsSquare) > 1:
                    if n not in elementsSquare and n not in self.sudokugrid.get_row(y):
                        #               print("Sq{} at ({},{})".format(n, y, x))
                        self.sudokugrid.write(y, x, n)
                        self.possible_values_grid.list2d[y][x] = {0}
                        return y, x, n
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
        last_modification = 1
        while last_modification is not None:  # il n'y avait pas de cases avec une seule possibilité
            last_modification = self.commit_one_var()
            if last_modification is not None:
                self.reduce_domains(*last_modification)  # on unpack la position & valeur
            else:
                return  # il n'est plus possible de trouver une unique solution "simple"

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

        solutions = []
        for y, x in self.sudokugrid.get_empty_pos():
            pos_sols = self.possible_values_grid.list2d[y][x]
            if pos_sols != {0}:
                solutions.append((y, x, pos_sols))
        solutions.sort(key=lambda sols: len(sols[2]))  # on trie les tuples par 3e élément (nombre de solutions)

        solvers = []
        y, x, selected_solutions = solutions[0]  # on prend le premier choix dans la liste triée
        for selected_solution in selected_solutions:
            new_grid = self.sudokugrid.copy()
            new_grid[y][x] = selected_solution
            new_solver = SudokuSolver(new_grid)
            solvers.append(new_solver)
        return solvers

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
        # if not daemon_running:
        #    return
        self.solve_step()
        if self.is_solved():
            return self.sudokugrid
        else:
            if self.is_valid():
                for solver in self.branch():
                    result = solver.solve()
                    if result is not None:
                        return result
                return None
            else:
                return None

    def save_solution_entry(self, y, x, v):
        if self.sudokugrid.write(y, x, v):
            self.possible_values_grid.list2d[y][x] = {0}

    def forksolve(this):
        """
        En fait c'est plus lent que sans le multiprocessing, peut-être dû au temps de création
        d'un nouveau processus python
        :return:
        """
        from multiprocessing import Pipe, Process, Value
        from multiprocessing.connection import Connection

        def run(self, tube: Connection, unfinished: Value):
            self.solve_step()
            # if not unfinished.value:
            #    print("fini")
            if self.is_solved():
                # print("solved")
                unfinished.value = False
                tube.send(self.sudokugrid)  # " return "
            else:
                if self.is_valid() and unfinished.value:
                    solvers = self.branch()
                    for solver in solvers:
                        Process(target=run, args=(solver, tube, unfinished)).start()

        # print("start")
        sortie, multi_solvers = Pipe()
        unfinished = Value('b', True)
        run(this, multi_solvers, unfinished)
        return sortie.recv()
