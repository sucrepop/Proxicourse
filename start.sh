#!/bin/bash

echo "========================================"
echo " Application Gestion Livraisons Repas"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR : Python 3 n'est pas installé"
    echo "Veuillez installer Python 3"
    exit 1
fi

echo "Python détecté !"
echo ""

# Vérifier si les dépendances sont installées
echo "Vérification des dépendances..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installation des dépendances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERREUR : Impossible d'installer les dépendances"
        exit 1
    fi
else
    echo "Dépendances OK !"
fi

echo ""
echo "========================================"
echo " Démarrage de l'application..."
echo "========================================"
echo ""
echo "L'application sera accessible à l'adresse :"
echo "http://localhost:5000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

# Démarrer l'application
python3 app.py
