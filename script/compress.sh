#!/usr/bin/env bash
if [[ $(pwd) == *script ]]; then
  echo "up a dir"
  cd ..
fi
echo "$(pwd)"
if [ -e "PIT_sudoku_Jean_Ribes.tar.gz" ]; then
  echo "Archive déjà créee, supprimmez-la ou déplacez-la"
else
  tar --gzip --create --file PIT_sudoku_Jean_Ribes.tar.gz --exclude .git --exclude venv --exclude sudoku_db.txt src script
  #tar --gzip --create --file PIT_sudoku_Jean_Ribes.tar.gz --exclude *.txt --exclude *.tar.gz --exclude .git --exclude venv --verbose src script
fi
