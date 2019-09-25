# Bugs imprévus
Tous les objets SudokuGrid contenaient la même grille ...
en fait j'avait initialisé leur liste `grid` en attribut et ça réutilisait le même à chaque fois

> Il faut donc toujours initaliser les attributs (non primitifs) dans une méthode