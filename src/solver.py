import numpy as np

from grid import SudokuGrid


class SudokuSolver:
    """Cette classe permet d'explorer les solutions d'une grille de Sudoku pour la résoudre.
    Elle fait intervenir des notions de programmation par contraintes
    que vous n'avez pas à maîtriser pour ce projet."""

    def __init__(self, grid):
        """À COMPLÉTER
        Ce constructeur initialise une nouvelle instance de solver à partir d'une grille initiale.
        Il construit les ensembles de valeurs possibles pour chaque case vide de la grille,
        en respectant les contraintes définissant un Sudoku valide.
        :param grid: Une grille de Sudoku
        :type grid: SudokuGrid
        """
        self.grilleSudoku = grid
        self.grillePossibles = np.zeros(729, dtype=np.uint8).reshape(9, 9, 9)
        self.reduce_all_domains()

    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        self.reduce_all_domains()  # MaJ des solutions possibles
        for i, j in self.grilleSudoku.get_empty_pos():
            if self.grillePossibles[i][j].sum() == 0:
                return False
        for i, row in enumerate(self.grilleSudoku.sudoku):
            for j, case in enumerate(row):
                if case > 0:
                    if np.count_nonzero(self.grilleSudoku.get_row(i) == case)>1:
                        return False
                    if np.count_nonzero(self.grilleSudoku.get_col(j) == case)>1:
                        return False
                    if np.count_nonzero(self.grilleSudoku.get_region(i // 3, j // 3) == case)>1:
                        return False
        return True

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """
        for i in range(0, 3):
            for j in range(0, 3):
                if sum(self.grilleSudoku.get_region(i,j))!=45:
                    return False
        for i in range(0, 9):
            if sum(self.grilleSudoku.get_row(i))!=45:
                return False
        for j in range(0, 9):
            if sum(self.grilleSudoku.get_col(j)) != 45:
                return False
        return True

    def reduce_all_domains(self):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """
        for i, j in self.grilleSudoku.get_empty_pos():
            valeursUniquesCase = np.unique(np.setdiff1d(np.arange(1, 10), np.concatenate((self.grilleSudoku.get_row(i), self.grilleSudoku.get_col(j), self.grilleSudoku.get_region(i // 3, j // 3)))))
            np.copyto(self.grillePossibles[i][j][:len(valeursUniquesCase)],valeursUniquesCase.astype(np.uint8))
        return self.grillePossibles

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
        self.grillePossibles[last_i][np.where(self.grillePossibles[last_i] == last_v)]=0
        self.grillePossibles[:,last_j][np.where(self.grillePossibles[:, last_j] ==last_v)] =0
        self.grillePossibles[3 * (last_i // 3):3 *((last_i // 3) + 1),3 * (last_j // 3):3* ((last_j // 3) + 1)][np.where(self.grillePossibles[3 * (last_i//3):3*((last_i//3)+1),3 * (last_j // 3):3*((last_j//3)+1)]==last_v)]=0

    def commit_one_var(self):
        """À compléter
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """
        for i, j in self.grilleSudoku.get_empty_pos():
            solutionsCase = np.unique(self.grillePossibles[i][j])
            if solutionsCase.shape == (2,):
                solUnique=solutionsCase[1]
                if solUnique != 0:
                    if self.grilleSudoku.write(i, j, solUnique) == True:
                        self.grillePossibles[i][j] = np.zeros(9, dtype=np.uint8)
                    return i, j, solUnique
            autrerowsCase = np.delete(self.grillePossibles, j, axis=1)[i].flatten()
            autreColsCase = np.delete(self.grillePossibles, i, axis=0)[:, j].flatten()
            autresRegionCase = np.delete(self.grillePossibles[3 * (i//3):3 * (i//3 + 1), 3 * (j//3):3 * (j//3 + 1)].flatten(), 3 * i + j)
            for sol in solutionsCase:
                if sol != 0:
                    if len(autreColsCase) > 1:
                        if sol not in autreColsCase and sol not in self.grilleSudoku.get_col(j):
                            if self.grilleSudoku.write(i,j,sol) == True:
                                self.grillePossibles[i][j] = np.zeros(9, dtype=np.uint8)
                            return i, j,sol
                    if len(autrerowsCase) > 1:
                        if sol not in autrerowsCase and sol not in self.grilleSudoku.get_row(i):
                            if self.grilleSudoku.write(i,j,sol)==True:
                                self.grillePossibles[i][j] = np.zeros(9, dtype=np.uint8)
                            return i,j, sol
                    if len(autresRegionCase) > 1:
                        if sol not in autresRegionCase and sol not in self.grilleSudoku.get_row(i):
                            if self.grilleSudoku.write(i,j,sol)==True:
                                self.grillePossibles[i][j]=np.zeros(9, dtype=np.uint8)
                            return i,j,sol
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
        commitReussi = True
        while commitReussi==True:  # il n'y avait pas de cases avec une seule possibilité
            last_modification = self.commit_one_var()  # *last_pos)
            if last_modification is not None:
                commitReussi=True
            else:
                commitReussi=False
            if commitReussi==True:
                i,j,v=last_modification
                self.reduce_domains(i,j,v)  # on unpack la position & valeur

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
        for i, j in self.grilleSudoku.get_empty_pos():
            pos_sols = np.unique(self.grillePossibles[i][j])
            if len(pos_sols) != 1:
                solutions.append((i,j,pos_sols))

        sudokuSolvers = []
        i, j, solutionsUtilisees = solutions[0]
        for solutionCase in solutionsUtilisees:
            if solutionCase != 0:
                nouvelleGrille = self.grilleSudoku.copy()
                nouvelleGrille.sudoku[i][j] = solutionCase
                nouveauSolver = SudokuSolver(nouvelleGrille)
                sudokuSolvers.append(nouveauSolver)
        return sudokuSolvers

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
        self.solve_step()
        if self.is_solved():
            return self.grilleSudoku
        elif self.is_valid():
            for brancheSolveur in self.branch():
                return brancheSolveur.solve()
        else:
            return None


