import numpy as np

from grid import SudokuGrid


class SudokuSolver:
    def __init__(self, grid):
        self.grilleSudoku=grid
        self.grillePossibilitees=np.zeros(729, dtype=np.uint8).reshape(9, 9, 9)
        self.reduce_all_domains()

    def is_valid(self):
        for i, row in enumerate(self.grilleSudoku.sudoku):
            for j, case in enumerate(row):
                if case > 0:
                    if np.count_nonzero(self.grilleSudoku.get_row(i)==case)>1:
                        return False
                    if np.count_nonzero(self.grilleSudoku.get_col(j)==case)>1:
                        return False
                    if np.count_nonzero(self.grilleSudoku.get_region(i//3,j//3)==case)>1:
                        return False
        for i, j in self.grilleSudoku.get_empty_pos():
            if self.grillePossibilitees[i][j].sum()==0:
                return False
        return True

    def is_solved(self):
        for i in range(0,9):
            if sum(self.grilleSudoku.get_row(i))!=45:
                return False
        for j in range(0,9):
            if sum(self.grilleSudoku.get_col(j))!=45:
                return False
        for i in range(0,3):
            for j in range(0,3):
                if sum(self.grilleSudoku.get_region(i,j))!=45:
                    return False
        return True

    def reduce_all_domains(self):
        for i, j in self.grilleSudoku.get_empty_pos():
            valeursUniquesCase = np.unique(np.setdiff1d(np.arange(1,10), np.concatenate((self.grilleSudoku.get_row(i),self.grilleSudoku.get_col(j),self.grilleSudoku.get_region(i // 3, j // 3)))))
            np.copyto(self.grillePossibilitees[i][j][:len(valeursUniquesCase)], valeursUniquesCase.astype(np.uint8))
        return self.grillePossibilitees

    def reduce_domains(self, last_i, last_j, last_v):
        self.grillePossibilitees[last_i][np.where(self.grillePossibilitees[last_i] == last_v)]=0
        self.grillePossibilitees[:, last_j][np.where(self.grillePossibilitees[:, last_j] == last_v)]=0
        self.grillePossibilitees[3 * (last_i // 3):3 * ((last_i // 3) + 1), 3 * (last_j // 3):3 * ((last_j // 3) + 1)][np.where(self.grillePossibilitees[3 * (last_i // 3):3 * ((last_i // 3) + 1), 3 * (last_j // 3):3 * ((last_j // 3) + 1)] == last_v)]=0

    def commit_one_var(self):
        for i, j in self.grilleSudoku.get_empty_pos():
            solutionsCase=np.unique(self.grillePossibilitees[i][j])
            if solutionsCase.shape==(2,):
                solUnique=solutionsCase[1]
                if solUnique!=0:
                    if self.grilleSudoku.write(i, j, solUnique)==True:
                        self.grillePossibilitees[i][j] = np.zeros(9, dtype=np.uint8)
                    return i,j,solUnique
            autrerowsCase=np.delete(self.grillePossibilitees,j,axis=1)[i].flatten()
            autreColsCase= np.delete(self.grillePossibilitees,i,axis=0)[:, j].flatten()
            autresRegionCase=np.delete(self.grillePossibilitees[3*(i//3):3*(i//3+1),3*(j//3):3*(j//3+1)].flatten(),3*i+j)
            for sol in solutionsCase:
                if sol!=0:
                    if len(autreColsCase)>1:
                        if sol not in autreColsCase and sol not in self.grilleSudoku.get_col(j):
                            if self.grilleSudoku.write(i,j,sol)==True:
                                self.grillePossibilitees[i][j] = np.zeros(9, dtype=np.uint8)
                            return i, j,sol
                    if len(autrerowsCase) > 1:
                        if sol not in autrerowsCase and sol not in self.grilleSudoku.get_row(i):
                            if self.grilleSudoku.write(i,j,sol)==True:
                                self.grillePossibilitees[i][j]=np.zeros(9, dtype=np.uint8)
                            return i,j,sol
                    if len(autresRegionCase)>1:
                        if sol not in autresRegionCase and sol not in self.grilleSudoku.get_row(i):
                            if self.grilleSudoku.write(i,j,sol)==True:
                                self.grillePossibilitees[i][j]=np.zeros(9, dtype=np.uint8)
                            return i,j,sol
        return None

    def solve_step(self):
        commitReussi = True
        while commitReussi==True:
            last_modification = self.commit_one_var()
            if last_modification is not None:
                commitReussi=True
            else:
                commitReussi=False
            if commitReussi==True:
                i,j,v=last_modification
                self.reduce_domains(i,j,v)

    def branch(self):
        solutions = []
        for i,j in self.grilleSudoku.get_empty_pos():
            pos_sols=np.unique(self.grillePossibilitees[i][j])
            if len(pos_sols)!=1:
                solutions.append((i,j,pos_sols))

        sudokuSolvers=[]
        i,j,solutionsUtilisees=solutions[0]
        for solutionCase in solutionsUtilisees:
            if solutionCase!=0:
                nouvelleGrille=self.grilleSudoku.copy()
                nouvelleGrille.sudoku[i][j]=solutionCase
                nouveauSolver=SudokuSolver(nouvelleGrille)
                sudokuSolvers.append(nouveauSolver)
        return sudokuSolvers

    def solve(self):
        self.solve_step()
        if self.is_solved():
            return self.grilleSudoku
        elif self.is_valid():
            for brancheSolveur in self.branch():
                s=brancheSolveur.solve()
                if s is not None:
                    return s
        else:
            return None
