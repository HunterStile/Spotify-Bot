@echo off
echo ===============================================
echo    SPOTIFY BOT - BUILD AUTOMATION
echo ===============================================
echo.

:menu
echo Scegli un'opzione:
echo.
echo 1. Avvia GUI in modalità sviluppo (Python)
echo 2. Crea nuovo eseguibile (.exe)
echo 3. Crea pacchetto di distribuzione completo
echo 4. Test dell'eseguibile esistente
echo 5. Apri cartella di distribuzione
echo 6. Esci
echo.
set /p choice="Inserisci la tua scelta (1-6): "

if "%choice%"=="1" goto dev_mode
if "%choice%"=="2" goto build_exe
if "%choice%"=="3" goto build_distribution
if "%choice%"=="4" goto test_exe
if "%choice%"=="5" goto open_dist
if "%choice%"=="6" goto exit
goto menu

:dev_mode
echo.
echo Avvio in modalità sviluppo...
python spotify_bot_gui.py
pause
goto menu

:build_exe
echo.
echo Creazione eseguibile...
echo Pulisco build precedenti...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo Avvio PyInstaller...
pyinstaller --onefile --windowed --name "SpotifyBot" spotify_bot_gui.py

if exist "dist\SpotifyBot.exe" (
    echo.
    echo ✓ Eseguibile creato con successo!
    echo Percorso: dist\SpotifyBot.exe
) else (
    echo.
    echo ✗ Errore nella creazione dell'eseguibile!
)
pause
goto menu

:build_distribution
echo.
echo Creazione pacchetto di distribuzione...

:: Crea eseguibile se non esiste
if not exist "dist\SpotifyBot.exe" (
    echo Eseguibile non trovato. Creo prima l'eseguibile...
    pyinstaller --clean spotify_bot.spec
)

:: Pulisci e crea cartella distribuzione
if exist "SpotifyBot_Distribution" rmdir /s /q "SpotifyBot_Distribution"
mkdir "SpotifyBot_Distribution"

:: Copia SOLO l'eseguibile (tutto il resto è già incluso)
copy "dist\SpotifyBot.exe" "SpotifyBot_Distribution\"

:: Crea README
echo Spotify Bot - Versione Eseguibile > "SpotifyBot_Distribution\README.txt"
echo. >> "SpotifyBot_Distribution\README.txt"
echo ISTRUZIONI: >> "SpotifyBot_Distribution\README.txt"
echo 1. Assicurati di avere Google Chrome installato >> "SpotifyBot_Distribution\README.txt"
echo 2. Fai doppio clic su SpotifyBot.exe per avviare >> "SpotifyBot_Distribution\README.txt"
echo 3. Configura le impostazioni e clicca Avvia Bot >> "SpotifyBot_Distribution\README.txt"
echo. >> "SpotifyBot_Distribution\README.txt"
echo Tutti i file necessari sono inclusi nell'eseguibile! >> "SpotifyBot_Distribution\README.txt"

:: Crea ZIP
powershell Compress-Archive -Path "SpotifyBot_Distribution\*" -DestinationPath "SpotifyBot_v1.2.0.zip" -Force

echo.
echo ✓ Pacchetto di distribuzione creato!
echo - Cartella: SpotifyBot_Distribution\
echo - ZIP: SpotifyBot_v1.2.0.zip
echo - L'eseguibile ora include TUTTO automaticamente!
pause
goto menu

:test_exe
echo.
echo Test dell'eseguibile...
if exist "SpotifyBot_Distribution\SpotifyBot.exe" (
    echo Avvio SpotifyBot.exe...
    start "" "SpotifyBot_Distribution\SpotifyBot.exe"
) else if exist "dist\SpotifyBot.exe" (
    echo Avvio SpotifyBot.exe da dist...
    start "" "dist\SpotifyBot.exe"
) else (
    echo ✗ Eseguibile non trovato! Crealo prima con l'opzione 2 o 3.
    pause
)
goto menu

:open_dist
echo.
if exist "SpotifyBot_Distribution" (
    echo Apertura cartella di distribuzione...
    start "" "SpotifyBot_Distribution"
) else (
    echo ✗ Cartella di distribuzione non trovata!
    echo Creala con l'opzione 3.
    pause
)
goto menu

:exit
echo.
echo Grazie per aver usato Spotify Bot Build Tool!
pause
exit
