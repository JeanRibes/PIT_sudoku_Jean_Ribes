#!/usr/bin/env bash
if [ -e "PIT_sudoku_Jean_Ribes.tar.gz" ]; then
	echo "Archive déjà créee, supprimmez-la ou déplacez-la"
else
	tar cfvz PIT_sudoku_Jean_Ribes.tar.gz --exclude *.txt --exclude *.tar.gz --exclude .git ../
fi
