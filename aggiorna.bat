@echo off
cd /D "C:\Users\PC\Desktop\Spotify-Bot"

:: Controlla se ci sono modifiche locali non commesse
git diff --quiet
if %ERRORLEVEL% NEQ 0 (
    echo Ci sono modifiche locali non commesse. Le modifiche verranno scartate.
    pause
    git checkout -- .
)

:: Esegui il pull della repository
git pull

pause
