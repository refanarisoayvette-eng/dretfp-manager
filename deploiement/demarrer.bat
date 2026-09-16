@echo off
chcp 65001 >nul
color 0B
echo ============================================================
echo   DEMARRAGE DE DRETFP MANAGER
echo ============================================================
echo.

call venv\Scripts\activate.bat
set DJANGO_SETTINGS_MODULE=config.settings_production

echo Adresse IP du serveur :
ipconfig | findstr /i "IPv4"
echo.

echo Le serveur va demarrer sur le port 8000.
echo.
echo Pour acceder depuis un autre PC :
echo    http://[VOTRE-IP]:8000
echo.
echo Pour arreter : Ctrl+C
echo.
echo ============================================================
echo.

waitress-serve --host=0.0.0.0 --port=8000 config.wsgi:application

pause