@echo off
cd /D "C:\Users\PC\Desktop\Spotify-Bot"

:: Scarta le modifiche locali non commesse
git checkout -- .

:: Esegui il pull della repository
git pull

pause
