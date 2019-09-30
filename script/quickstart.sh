#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

echo $DIR
if [ -e $DIR/venv ] && [ -d $DIR/venv ]
then
    echo "Pas besoin de créer un virtualenv"
    . $DIR/venv/bin/activate

    echo "vérification que tout est bien installé"
    if python3 -c "import PyQt5; import sys"
    then
      echo "OK"
    else
      echo "dépendances manquantes"
      exit 1
    fi
else
    echo "Recherche d'une implémentation de virtualenv"
    if [ -e /usr/bin/virtualenv ] && [ -x /usr/bin/virtualenv ]
    then
      echo "utilisation de virtualenv"
      virtualenv -p /usr/bin/python3 $DIR/venv
    else
      echo "utilisation de python3-venv"
      python3 -m venv $DIR/venv
    fi
    . $DIR/venv/bin/activate
    pip install -r requirements.txt
    echo "Dépendances installées, lancement de l'interface graphique"
fi
echo " lancement GUI"
python3 $DIR/src/gui.py