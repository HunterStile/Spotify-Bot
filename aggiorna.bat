@echo off
cd /D "C:\Users\Luigi\Desktop\GITHUB\Spotify-Bot"

echo ===================================
echo Spotify Bot - Aggiornamento Automatico
echo ===================================

:: Controlla se ci sono modifiche locali non commesse
git diff --quiet
if %ERRORLEVEL% NEQ 0 (
    echo Ci sono modifiche locali non commesse. Le modifiche verranno scartate.
    pause
    git checkout -- .
)

:: Esegui il pull della repository
git pull

:: Verifica se è presente il file .env e crealo se non esiste
if not exist .env (
    echo Creazione del file .env per le chiavi API CAPTCHA...
    (
        echo # Chiave API per il servizio 2captcha
        echo # Registrati su https://2captcha.com per ottenere una chiave API
        echo TWOCAPTCHA_API_KEY=tua_chiave_api_qui
        echo.
        echo # Impostazioni alternative per altri servizi CAPTCHA
        echo # ANTICAPTCHA_API_KEY=tua_chiave_api_qui
        echo # CAPSOLVER_API_KEY=tua_chiave_api_qui
    ) > .env
    echo File .env creato. Per favore, inserisci la tua chiave API nel file.
)

echo ===================================
echo Aggiornamento completato!
echo.
echo NOTA: Per utilizzare la risoluzione automatica dei CAPTCHA:
echo 1. Assicurati di aver impostato USE_CAPTCHA_SERVICE = True in config.py
echo 2. Inserisci la tua chiave API nel file .env
echo ===================================

pause
