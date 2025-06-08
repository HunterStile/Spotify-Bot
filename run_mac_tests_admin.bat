@echo off
:: Script per test MAC address con privilegi amministratore

echo ========================================
echo  TEST MAC ADDRESS - RICHIEDE ADMIN
echo ========================================
echo.

:: Verifica privilegi amministratore
net session >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Privilegi amministratore: OK
    echo.
) else (
    echo ❌ Questo script richiede privilegi di amministratore
    echo.
    echo Per risolvere:
    echo 1. Fai clic destro su questo file .bat
    echo 2. Seleziona "Esegui come amministratore"
    echo.
    pause
    exit /b 1
)

:menu
echo Seleziona il test da eseguire:
echo.
echo 1. Test MAC con fallback (Consigliato)
echo 2. Test MAC originale (mac_changer.py)
echo 3. Test solo PowerShell
echo 4. Mostra MAC attuale
echo 5. Test veloce cambio MAC
echo 6. Esci
echo.

set /p choice="Inserisci la tua scelta (1-6): "

if "%choice%"=="1" goto test_fallback
if "%choice%"=="2" goto test_originale
if "%choice%"=="3" goto test_powershell
if "%choice%"=="4" goto show_mac
if "%choice%"=="5" goto test_veloce
if "%choice%"=="6" goto fine
goto menu

:test_fallback
echo.
echo ============================================
echo  TEST MAC CON FALLBACK AUTOMATICO
echo ============================================
python test_mac_fallback.py
echo.
pause
goto menu

:test_originale
echo.
echo ============================================
echo  TEST MAC ORIGINALE
echo ============================================
python test_simple_mac_mail.py
echo.
pause
goto menu

:test_powershell
echo.
echo ============================================
echo  TEST SOLO POWERSHELL
echo ============================================
python -c "
import sys
sys.path.append('funzioni')
from mac_changer import MacChanger
changer = MacChanger()
success = changer.change_mac_with_powershell()
print(f'Risultato: {success}')
"
echo.
pause
goto menu

:show_mac
echo.
echo ============================================
echo  MAC ADDRESS ATTUALE
echo ============================================
echo Comando getmac:
getmac
echo.
echo Comando ipconfig:
ipconfig /all | findstr "Indirizzo fisico"
echo.
pause
goto menu

:test_veloce
echo.
echo ============================================
echo  TEST VELOCE CAMBIO MAC
echo ============================================
echo Prima del cambio:
getmac /fo csv | findstr -v "Nome"
echo.
echo Cambio MAC in corso...
python -c "
import sys
sys.path.append('funzioni')
from mac_changer import MacChanger
changer = MacChanger()
result = changer.change_mac_auto('powershell')
print(f'Cambio MAC: {'Riuscito' if result else 'Fallito'}')
"
echo.
echo Dopo il cambio:
getmac /fo csv | findstr -v "Nome"
echo.
pause
goto menu

:fine
echo.
echo Arrivederci!
exit
