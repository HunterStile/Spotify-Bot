===============================================
    SPOTIFY BOT - CONTROL PANEL
===============================================

INSTALLAZIONE E USO:

1. Assicurati di avere Google Chrome installato sul tuo computer

2. Estrai tutti i file in una cartella sul desktop

3. Fai doppio clic su SpotifyBot.exe per avviare l'applicazione

4. Configura le impostazioni nell'interfaccia grafica:
   - Inserisci le URL delle playlist
   - Configura i proxy se necessario
   - Imposta il numero di bot simultanei
   - Scegli le opzioni desiderate

5. Clicca "Avvia Bot" per iniziare

===============================================
NOTE IMPORTANTI:
===============================================

- Mantieni chromedriver.exe nella stessa cartella dell'eseguibile
- Il bot richiede una connessione internet attiva
- Usa il bot responsabilmente e rispetta i termini di servizio di Spotify
- Se Chrome si aggiorna, potresti dover aggiornare chromedriver.exe
- In caso di problemi, verifica che Chrome sia installato e aggiornato

===============================================
CONFIGURAZIONE:
===============================================

PLAYLIST DA ASCOLTARE:
Formato: url_playlist;posizione1,posizione2,posizione3
Esempio: https://open.spotify.com/playlist/xyz;1,5,10

PLAYLIST DA SEGUIRE:
Una URL per riga

PROXY:
Formato: ip:porta:username:password
Oppure: ip:porta (se senza autenticazione)


===============================================
PATCH NOTES:
===============================================

## 🆕 VERSIONE 1.2.2 - EXECUTABLE CSV FIX
**📅 Data di rilascio**: 08/06/2025  
**🏷️ Tipo**: Critical Bug Fix - CSV File Access

### 🔧 **BUG FIXES CRITICI**

#### 📁 **Sistema CSV Files Completamente Risolto**
- **✅ RISOLTO: CSV Account non accessibile in eseguibile**
  - Implementata funzione `get_writable_csv_path()` per gestione `account_spotify.csv`
  - File CSV copiato automaticamente in directory utente scrivibile (`~/SpotifyBot/`)
  - Accesso agli account esistenti ora funziona correttamente nell'eseguibile

- **✅ RISOLTO: Salvataggio account creati in eseguibile**
  - Implementata funzione `get_writable_csv_creati_path()` per gestione `account_spotify_creati.csv`
  - Account creati vengono salvati correttamente anche nell'exe compilato
  - Creazione automatica header CSV se file non esiste

===============================================
