@echo off
echo ========================================
echo  Application Gestion Livraisons Repas
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR : Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b
)

echo Python détecté !
echo.

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR : Impossible d'installer les dépendances
        pause
        exit /b
    )
) else (
    echo Dépendances OK !
)

echo.
echo ========================================
echo  Démarrage de l'application...
echo ========================================
echo.
echo L'application sera accessible à l'adresse :
echo http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arrêter l'application
echo.

REM Démarrer l'application
python app.py

pause
