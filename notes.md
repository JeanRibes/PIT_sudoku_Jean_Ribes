# Bugs imprévus
Tous les objets SudokuGrid contenaient la même grille ...
en fait j'avait initialisé leur liste `grid` en attribut et ça réutilisait le même à chaque fois

> Il faut donc toujours initaliser les attributs (non primitifs) dans une méthode

Pour créer des listes 2D vides, il faut utiliser des boucles for et des .append, sinon ça va créer des listes
par référence et elles auront le même contenu

Mettre à jour les définition UI de Python après édition dans QtCreator
```shell script
pyuic5 -o qt_ui.py ../qtcreator-ui/SudokuSolver/mainwindow.ui && python3 gui.py
```