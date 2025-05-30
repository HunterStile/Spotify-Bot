@echo off
echo Creating Spotify Bot Distribution Package...
echo.

:: Create distribution folder
if not exist "SpotifyBot_Distribution" mkdir "SpotifyBot_Distribution"

:: Copy the main executable
copy "dist\SpotifyBot.exe" "SpotifyBot_Distribution\"

:: Copy necessary configuration files
copy "config.py" "SpotifyBot_Distribution\"
copy "chromedriver.exe" "SpotifyBot_Distribution\"
copy "user_agents.txt" "SpotifyBot_Distribution\"

:: Copy the functions folder
if not exist "SpotifyBot_Distribution\funzioni" mkdir "SpotifyBot_Distribution\funzioni"
copy "funzioni\*.py" "SpotifyBot_Distribution\funzioni\"

if not exist "SpotifyBot_Distribution\funzioni\Setup" mkdir "SpotifyBot_Distribution\funzioni\Setup"
copy "funzioni\Setup\*.txt" "SpotifyBot_Distribution\funzioni\Setup\"

:: Create a readme file for distribution
echo Creating README for distribution...

echo Spotify Bot - Executable Distribution > "SpotifyBot_Distribution\README.txt"
echo. >> "SpotifyBot_Distribution\README.txt"
echo INSTALLAZIONE E USO: >> "SpotifyBot_Distribution\README.txt"
echo. >> "SpotifyBot_Distribution\README.txt"
echo 1. Assicurati di avere Google Chrome installato sul tuo computer >> "SpotifyBot_Distribution\README.txt"
echo 2. Estrai tutti i file in una cartella >> "SpotifyBot_Distribution\README.txt"
echo 3. Fai doppio clic su SpotifyBot.exe per avviare l'applicazione >> "SpotifyBot_Distribution\README.txt"
echo 4. Configura le impostazioni nell'interfaccia grafica >> "SpotifyBot_Distribution\README.txt"
echo 5. Clicca "Avvia Bot" per iniziare >> "SpotifyBot_Distribution\README.txt"
echo. >> "SpotifyBot_Distribution\README.txt"
echo NOTE IMPORTANTI: >> "SpotifyBot_Distribution\README.txt"
echo - Mantieni chromedriver.exe nella stessa cartella dell'eseguibile >> "SpotifyBot_Distribution\README.txt"
echo - Il bot richiede una connessione internet attiva >> "SpotifyBot_Distribution\README.txt"
echo - Usa il bot responsabilmente e rispetta i termini di servizio di Spotify >> "SpotifyBot_Distribution\README.txt"
echo. >> "SpotifyBot_Distribution\README.txt"
echo Versione: 1.2.0 >> "SpotifyBot_Distribution\README.txt"
echo Data build: %date% >> "SpotifyBot_Distribution\README.txt"

echo.
echo ========================================
echo DISTRIBUTION PACKAGE CREATED!
echo ========================================
echo.
echo La cartella SpotifyBot_Distribution contiene tutto il necessario
echo per distribuire il bot. Puoi comprimere questa cartella e condividerla.
echo.
echo Contenuto:
echo - SpotifyBot.exe (applicazione principale)
echo - chromedriver.exe (driver per Chrome)
echo - config.py (configurazioni)
echo - user_agents.txt (user agents per stealth)
echo - funzioni/ (cartella con le funzioni)
echo - README.txt (istruzioni per l'utente)
echo.
pause
