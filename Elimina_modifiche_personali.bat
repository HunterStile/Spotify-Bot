@echo off
cd /D "C:\Users\PC\Desktop\Spotify-Bot"

:: Conferma prima di procedere
echo ATTENZIONE: Questo comando rimuoverà tutti i commit non reversibilmente!
echo Sei sicuro di voler continuare? [S/N]
set /p confirm=

if /i "%confirm%" NEQ "S" (
    echo Operazione annullata.
    pause
    exit /b
)

:: Ripristina la repository al primo commit
git checkout --orphan temp-branch
git add -A
git commit -m "Ripristino commit iniziale"
git branch -D main
git branch -m main
git push --force origin main

pause