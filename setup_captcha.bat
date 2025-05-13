@echo off
cls
echo ================================================
echo         SPOTIFY BOT - CONFIGURAZIONE CAPTCHA
echo ================================================
echo.

REM Verifica se il file .env esiste
if not exist ".env" (
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
    echo File .env creato.
) else (
    echo File .env trovato.
)

echo.
echo ------------------------------------------------
echo MENU SETUP CAPTCHA
echo ------------------------------------------------
echo [1] Configurare la chiave API 2captcha
echo [2] Testare la configurazione CAPTCHA
echo [3] Attivare/Disattivare il servizio CAPTCHA
echo [4] Eseguire un test su Spotify
echo [5] Leggere la guida
echo [6] Uscire
echo.

set /p scelta="Seleziona un'opzione (1-6): "

if "%scelta%"=="1" (
    echo.
    echo ------------------------------------------------
    echo Configurazione della chiave API 2captcha
    echo ------------------------------------------------
    echo.
    echo Vai su https://2captcha.com, registrati e ottieni la tua chiave API.
    echo.
    set /p chiave="Inserisci la tua chiave API 2captcha: "
    
    REM Prepara il nuovo contenuto del file .env
    (
        echo # Chiave API per il servizio 2captcha
        echo # Registrati su https://2captcha.com per ottenere una chiave API
        echo TWOCAPTCHA_API_KEY=%chiave%
        echo.
        echo # Impostazioni alternative per altri servizi CAPTCHA
        echo # ANTICAPTCHA_API_KEY=tua_chiave_api_qui
        echo # CAPSOLVER_API_KEY=tua_chiave_api_qui
    ) > .env
    
    echo.
    echo Chiave API salvata con successo!
    timeout /t 3 > nul
    call %0
) else if "%scelta%"=="2" (
    echo.
    echo ------------------------------------------------
    echo Test della configurazione CAPTCHA
    echo ------------------------------------------------
    echo.
    python test_captcha.py
    echo.
    pause
    call %0
) else if "%scelta%"=="3" (
    echo.
    echo ------------------------------------------------
    echo Attivazione/Disattivazione del servizio CAPTCHA
    echo ------------------------------------------------
    echo.
    echo Modifica del file config.py...
    
    REM Leggi lo stato attuale
    set "stato_trovato="
    for /f "tokens=1,3 delims= " %%a in ('findstr /C:"USE_CAPTCHA_SERVICE" config.py') do (
        if "%%a"=="USE_CAPTCHA_SERVICE" (
            if "%%b"=="True" (
                set "stato_trovato=True"
            ) else if "%%b"=="False" (
                set "stato_trovato=False"
            )
        )
    )
    
    if "%stato_trovato%"=="True" (
        echo Il servizio CAPTCHA è attualmente ATTIVO.
        set /p conferma="Vuoi DISATTIVARLO? (s/n): "
        if /i "%conferma%"=="s" (
            powershell -Command "(Get-Content config.py) -replace 'USE_CAPTCHA_SERVICE = True', 'USE_CAPTCHA_SERVICE = False' | Set-Content config.py"
            echo Servizio CAPTCHA DISATTIVATO.
        )
    ) else (
        echo Il servizio CAPTCHA è attualmente DISATTIVATO.
        set /p conferma="Vuoi ATTIVARLO? (s/n): "
        if /i "%conferma%"=="s" (
            powershell -Command "(Get-Content config.py) -replace 'USE_CAPTCHA_SERVICE = False', 'USE_CAPTCHA_SERVICE = True' | Set-Content config.py"
            echo Servizio CAPTCHA ATTIVATO.
        )
    )
    
    timeout /t 3 > nul
    call %0
) else if "%scelta%"=="4" (
    echo.
    echo ------------------------------------------------
    echo Test di risoluzione CAPTCHA su Spotify
    echo ------------------------------------------------
    echo.
    python test_captcha_spot.py
    echo.
    pause
    call %0
) else if "%scelta%"=="5" (
    echo.
    echo Apertura della guida...
    start guida_captcha.md
    timeout /t 2 > nul
    call %0
) else if "%scelta%"=="6" (
    echo.
    echo Uscita...
    exit /b
) else (
    echo.
    echo Opzione non valida. Riprova.
    timeout /t 2 > nul
    call %0
)
