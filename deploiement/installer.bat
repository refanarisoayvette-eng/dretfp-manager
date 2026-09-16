@echo off
chcp 65001 >nul
color 0A
echo ============================================================
echo   INSTALLATION DE DRETFP MANAGER
echo   Serveur DRETFP Amoron'i Mania
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe !
    echo Telechargez-le sur https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python detecte

echo.
echo [1/5] Creation de l'environnement virtuel...
python -m venv venv
call venv\Scripts\activate.bat

echo.
echo [2/5] Installation des bibliotheques...
pip install --upgrade pip
pip install -r deploiement\requirements.txt

echo.
echo [3/5] Creation de la base de donnees...
echo Verifiez que la base 'dretfp_db' existe dans PostgreSQL.
pause
python manage.py migrate

echo.
echo [4/5] Collecte des fichiers statiques...
python manage.py collectstatic --noinput

echo.
echo [5/5] Creation du super utilisateur...
python manage.py createsuperuser

echo.
echo ============================================================
echo   INSTALLATION TERMINEE !
echo ============================================================
echo.
echo Pour demarrer le serveur, executez : demarrer.bat
echo.
pause