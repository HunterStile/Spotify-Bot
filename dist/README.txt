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

# 🆕 VERSIONE 1.2.1 - MAC ADDRESS SPOOFING
**📅 Data di rilascio**: 08/06/2025  
**🏷️ Tipo**: Minor Update - Advanced Anti-Detection

### ✨ **NUOVE FUNZIONALITÀ**

#### 🔧 **Sistema Reset MAC Address Avanzato**
- **Reset MAC Automatico**: Cambio automatico MAC address durante rilevamento robot/CAPTCHA
- **Metodi Multipli**: Fallback automatico tra PowerShell e Netsh per massima compatibilità
- **Vendor Prefix Realistici**: Utilizzo prefissi reali (Intel, Microsoft, VirtualBox, VMware)
- **Verifica Privilegi Admin**: Controllo automatico permessi amministratore
- **Logging Dettagliato**: Output completo operazioni MAC per debugging

#### 🎮 **Integrazione GUI Completa**
- **Checkbox "Reset MAC"**: Nuova opzione nel Router Reset Frame
- **Configurazione Persistente**: Salvataggio impostazione reset MAC in `gui_config.json`
- **Workflow Integrato**: Reset MAC + Reset Router per massima efficacia anti-detection
- **Controlli Pre-Volo**: Validazione configurazioni MAC prima dell'avvio

### 🔧 **MIGLIORAMENTI TECNICI**

#### 🛡️ **Anti-Detection Potenziato**
- **Hardware Fingerprinting**: Mascheramento completo identità hardware
- **Network Layer Evasion**: Cambio MAC a livello network adapter
- **Randomizzazione Intelligente**: Generazione MAC con pattern realistici
- **Fallback Robusto**: Sistema doppio per gestire diverse configurazioni Windows

#### ⚙️ **Architettura Modulare**
- **MacChanger Class**: Classe dedicata con metodi PowerShell e Netsh
- **Compatibility Functions**: Funzioni di compatibilità per integrazione esistente
- **Error Handling**: Gestione robusta errori con retry automatici
- **Admin Detection**: Rilevamento automatico privilegi tramite ctypes

===============================================
