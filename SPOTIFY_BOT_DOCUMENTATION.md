# 🎵 SPOTIFY BOT - DOCUMENTAZIONE COMPLETA
*Created by HunterStile*

## 📋 INDICE
1. [Panoramica Generale](#panoramica-generale)
2. [Architettura del Sistema](#architettura-del-sistema)
3. [Funzionamento Dettagliato](#funzionamento-dettagliato)
4. [Guida all'Interfaccia GUI](#guida-allinterfaccia-gui)
5. [Configurazioni Avanzate](#configurazioni-avanzate)
6. [Risoluzione Problemi](#risoluzione-problemi)
7. [Patch Notes](#patch-notes)

---

## 🎯 PANORAMICA GENERALE

**Spotify Bot** è un'applicazione di automazione avanzata progettata per eseguire operazioni automatizzate su Spotify Web Player. Il bot è in grado di creare account, seguire playlist e simulare l'ascolto di brani musicali in modo completamente automatizzato.

### ⭐ Caratteristiche Principali
- **Creazione Account Automatica**: Genera account Spotify utilizzando dati casuali
- **Gestione Multi-Account**: Supporta rotazione e gestione di più account
- **Ascolto Intelligente**: Simula l'ascolto con modalità casuale o posizioni fisse
- **Sistema Proxy Avanzato**: Supporto per proxy singoli e doppi
- **Multithreading**: Esecuzione simultanea di più istanze bot
- **Interfaccia Grafica Moderna**: GUI intuitiva con tema scuro Spotify
- **Protezione Anti-Detection**: Sistema stealth per evitare rilevamenti automatici
- **Gestione Router**: Reset automatico router TIM/Vodafone

---

## 🏗️ ARCHITETTURA DEL SISTEMA

### 📁 Struttura File Principali

```
Spotify-Bot/
├── 🎯 spotify_bot_gui.py        # Interfaccia grafica principale
├── ⚙️ Main.py                   # Logica di esecuzione bot
├── 🔧 config.py                 # Configurazioni globali
├── 📊 account_spotify.csv       # Database account esistenti
├── 📝 account_spotify_creati.csv # Log account creati
├── 🌐 chromedriver.exe          # Driver browser automation
├── 🕵️ user_agents.txt           # User agents per stealth
└── funzioni/
    └── 🔌 spotify_functions.py  # Libreria funzioni core
```

### 🧩 Componenti Principali

#### 1. **GUI Controller** (`spotify_bot_gui.py`)
- Gestisce l'interfaccia utente
- Coordina l'esecuzione multithreading
- Salva/carica configurazioni
- Monitora stato dei bot

#### 2. **Bot Engine** (`Main.py`)
- Orchestratore principale delle operazioni
- Gestisce il ciclo di vita dei bot
- Implementa logica di business
- Coordina le funzioni Spotify

#### 3. **Spotify Functions** (`spotify_functions.py`)
- Libreria delle operazioni Spotify
- Gestione browser automation
- Funzioni di rete e proxy
- Utilità di sistema

#### 4. **Configuration Manager** (`config.py`)
- Impostazioni globali predefinite
- Configurazioni playlist e proxy
- Parametri di comportamento

---

## ⚙️ FUNZIONAMENTO DETTAGLIATO

### 🔄 Ciclo di Esecuzione Bot

#### **FASE 1: Inizializzazione**
```
1. Caricamento configurazioni
2. Verifica risorse (ChromeDriver, user_agents.txt)
3. Inizializzazione semafori multithreading
4. Preparazione ambiente pulito
```

#### **FASE 2: Configurazione Browser**
```
1. Selezione User-Agent casuale
2. Configurazione opzioni Chrome
3. Applicazione protezioni stealth (se abilitato)
4. Posizionamento finestra (primo/secondo schermo)
```

#### **FASE 3: Gestione Proxy (Opzionale)**
```
IF proxy attivi:
    1. Selezione proxy casuale dalla lista
    2. Configurazione Proxifier
    3. Test connessione
    IF doppio proxy:
        - Usa lista proxy primaria
    ELSE:
        - Usa lista proxy standard
```

#### **FASE 4: Operazioni Account**

**🆕 Creazione Nuovo Account:**
```
1. Navigazione a spotify.com/signup
2. Generazione dati casuali:
   - Nome (Faker library)
   - Email @alicie.it
   - Password standard: "Napoli10!!"
   - Data nascita casuale (1996-2005)
   - Genere casuale
3. Compilazione form registrazione
4. Gestione CAPTCHA/robot detection
5. Verifica successo creazione
6. Salvataggio credenziali in CSV
```

**🔑 Accesso Account Esistente:**
```
1. Lettura account da account_spotify.csv
2. Navigazione a open.spotify.com
3. Inserimento credenziali
4. Verifica successo login
5. Rotazione account (sposta in fondo al CSV)
6. Rimozione account non funzionanti
```

#### **FASE 5: Operazioni Playlist**

**👥 Seguire Playlist:**
```
FOR each playlist in PLAYLIST_FOLLOW:
    1. Navigazione alla playlist
    2. Click pulsante "Segui" ([data-testid="add-button"])
    3. Verifica successo operazione
```

**🎵 Ascolto Canzoni:**

*Modalità Casuale:*
```
1. Selezione playlist casuale da PLAYLIST_URLS
2. Generazione posizione random (1-20)
3. Click doppio sulla canzone
4. Attesa ascolto (120-160 secondi)
```

*Modalità Statica:*
```
FOR each playlist with positions (url;pos1,pos2,pos3):
    1. Parsing configurazione posizioni
    2. Navigazione alla playlist
    FOR each posizione specificata:
        1. Click doppio sulla canzone
        2. Attesa ascolto completa
```

#### **FASE 6: Gestione Errori e Recovery**

**🤖 Robot Detection:**
```
IF rilevato CAPTCHA:
    IF stop_for_robot = True:
        - Arresto bot
        - Log richiesta robot
    ELSE:
        - Attesa tempo_ripartenza
        - Reset router (se configurato)
        - Retry operazione
```

**🌐 Reset Router:**
```
TIM Router:
    1. Login 192.168.1.1
    2. Navigazione Gestione → Device Manager
    3. Click Restart → Conferma

Vodafone Router:
    1. Login 192.168.1.1  
    2. Navigazione Impostazioni → Riavvio
    3. Click Riavvia → Applica
```

---

## 🖥️ GUIDA ALL'INTERFACCIA GUI

### 🎨 Layout Generale

L'interfaccia utilizza un **design dark** ispirato a Spotify con colori:
- **Background**: #121212 (nero Spotify)
- **Accent**: #1DB954 (verde Spotify)
- **Testo**: #FFFFFF (bianco)
- **Secondario**: #212121 (grigio scuro)

### 📊 Sezioni Principali

#### **🔧 COLONNA SINISTRA: Configurazioni**

**⚙️ Configurazione Principale**
- ☑️ **Crea Nuovo Account**: Attiva creazione automatica account
- ☑️ **Usa Proxy**: Abilita sistema proxy
- ☑️ **Usa Doppio Proxy**: Attiva configurazione proxy avanzata
- ☑️ **Segui Playlist**: Attiva funzione auto-follow
- ☑️ **Ascolta Canzoni**: Abilita simulazione ascolto
- ☑️ **Disabilita Stealth**: Disattiva protezioni anti-detection
- ☑️ **Usa Secondo Schermo**: Posiziona browser su monitor secondario
- 🔢 **Iterazioni Max**: Numero massimo cicli per bot

**🚀 Configurazione Multithreading**
- 🤖 **Numero Bot Simultanei**: Istanze bot parallele (1-10)
- 🌐 **Numero Max Chrome**: Limite browser aperti (1-10)
- ⚠️ **Nota**: Chrome max ≤ Bot max per gestione memoria

**🎯 Modalità Posizioni**
- 🎲 **Casuale**: Selezione posizioni random (1-20)
- 📍 **Statico**: Usa posizioni specificate in playlist URL

**🤖 Rilevamento Robot**
- ☑️ **Ferma per Rilevamento Robot**: Arresta bot se CAPTCHA
- ⏱️ **Tempo Ripartenza (sec)**: Attesa prima retry (default: 7200)

**🌐 Reset Router**
- ☑️ **Reset Router**: Abilita riavvio automatico
- 📡 **Tipo Router**: TIM / Vodafone

#### **📋 COLONNA DESTRA: Liste e Contenuti**

**🎵 Configurazione Playlist**

*Playlist da Ascoltare:*
```
Formato: url;posizione1,posizione2,posizione3
Esempio: 
https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC;1,5,10
https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry
```

*Playlist da Seguire:*
```
Formato: una URL per riga
Esempio:
https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC
https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry
```

**🌐 Liste Proxy**

*Lista Proxy Principale:*
```
Formato: nome_file.ppx (uno per riga)
Esempio:
profilo1.ppx
profilo2.ppx
profilo3.ppx
```

*Lista Proxy Primaria:*
```
Usata con "Doppio Proxy" attivo
Stesso formato della lista principale
```

#### **🎮 Pannello Controlli**

**🔘 Pulsanti Azione**
- ▶️ **Avvia Bot**: Inizia esecuzione con configurazioni attuali
- ⏹️ **Ferma Bot**: Arresto graceful di tutti i bot
- 💾 **Salva Configurazione**: Memorizza impostazioni correnti
- 🔄 **Aggiorna ChromeDriver**: Download versione più recente

**📺 Console Output**
- Finestra di log in tempo reale
- Messaggi colorati per bot multipli
- Scroll automatico agli ultimi messaggi
- Stato operazioni e errori

### 🎛️ Interazioni Avanzate

#### **🔄 Salvataggio Automatico**
La GUI salva automaticamente in `gui_config.json`:
- Tutte le impostazioni checkbox
- Liste proxy e playlist
- Configurazioni multithreading
- Modalità e parametri

#### **🚨 Validazioni Input**
Prima dell'avvio, il sistema verifica:
- Proxy configurati se abilitati
- Playlist specificate se ascolto attivo
- Doppio proxy con lista primaria
- Coherenza configurazioni

#### **⚡ Gestione Multithreading**
- Semaforo per limitare istanze Chrome
- Thread pool per bot paralleli
- Stop event condiviso per arresto coordinato
- Redirect output con prefissi bot

---

## 🔧 CONFIGURAZIONI AVANZATE

### 📝 File config.py

```python
# Configurazioni Base
CREAZIONE = True                    # True=crea account, False=usa esistenti
PROXY = False                      # Abilita sistema proxy
DOPPIOPROXY = False               # Doppio proxy per sicurezza extra
SEGUI_PLAYLIST = True             # Auto-follow playlist
ASCOLTA_CANZONI = True           # Simula ascolto
DISABLE_STEALTH = False          # Disabilita protezioni

# Gestione Robot/Errori
STOP_FOR_ROBOT = False           # Ferma se CAPTCHA
TEMPO_RIPARTENZA = 7200         # 2 ore attesa
RESET_ROUTER = False            # Auto-reset router
TIPO_ROUTER = 'vodafone'        # 'tim' o 'vodafone'

# Parametri Esecuzione
MAX_ITERAZIONE = 100             # Cicli massimi per bot
MODALITA_POSIZIONI = 'random'   # 'random' o 'statico'
```

### 🌐 Configurazione Proxy

**Requisiti Proxifier:**
- Software Proxifier installato
- Profili .ppx configurati in:
  `C:\Users\[USER]\AppData\Roaming\Proxifier4\Profiles\`

**Profili Supportati:**
```
profilo1.ppx    # Proxy configuration 1
profilo2.ppx    # Proxy configuration 2
...
```

### 🎵 Configurazione Playlist Avanzata

**Formato URL con Posizioni:**
```
https://open.spotify.com/playlist/[ID];1,3,5,10,15
```
- **Sezione 1**: URL playlist standard
- **Sezione 2**: Posizioni specifiche separate da virgola

**Esempi Configurazioni:**
```python
PLAYLIST_URLS = [
    # Pop-Punk con posizioni fisse 1 e 5
    'https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC;1,5',
    
    # Trap Italia modalità casuale (nessuna posizione)
    'https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry',
    
    # New Generation con posizioni multiple
    'https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R;1,6,12,18'
]
```

### 🛡️ Sistema Stealth

**Protezioni Implementate:**
- User-Agent randomization da `user_agents.txt`
- Disabilitazione flag automation
- Stealth plugin selenium-stealth
- Nascondimento proprietà webdriver
- Modalità incognito forzata

**Configurazione Browser:**
```python
# Opzioni Anti-Detection
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Stealth Plugin
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True
)
```

---

## 🚨 RISOLUZIONE PROBLEMI

### ❌ Errori Comuni

#### **1. ChromeDriver Non Trovato**
```
Errore: "chromedriver.exe not found"
Soluzione:
1. Verificare presenza chromedriver.exe nella root
2. Usare pulsante "Aggiorna ChromeDriver" in GUI
3. Controllare path in funzioni/Setup/path_driver.txt
```

#### **2. Proxy Non Funzionante**
```
Errore: "Proxy connection failed"
Soluzione:
1. Verificare installazione Proxifier
2. Controllare profili .ppx in AppData
3. Testare proxy manualmente
4. Verificare credenziali proxy
```

#### **3. Bot Rilevato**
```
Errore: "Bot detected / CAPTCHA"
Soluzione:
1. Attivare "Ferma per Rilevamento Robot"
2. Aumentare tempo_ripartenza
3. Cambiare proxy più frequentemente
4. Ridurre numero bot simultanei
```

#### **4. Account Non Validi**
```
Errore: "Login failed"
Soluzione:
1. Verificare formato account_spotify.csv
2. Controllare credenziali manualmente
3. Il bot rimuove automaticamente account non validi
```

#### **5. Errori Multithreading**
```
Errore: "Too many Chrome instances"
Soluzione:
1. Ridurre "Numero Max Chrome"
2. Aumentare RAM disponibile
3. Chiudere altri programmi
4. Usare "Ferma Bot" prima di riavviare
```

### 🔧 Diagnostica Avanzata

#### **Log Files Generati:**
- `email_field_error.png` - Errore campo email
- `password_field_error.png` - Errore campo password
- `login_error.png` - Errore login generale
- `chrome_debug.log` - Debug browser

#### **Comandi Diagnostici:**
```bash
# Verifica processi Chrome
tasklist | findstr chrome

# Termina processi bloccati
taskkill /f /im chrome.exe

# Pulisci cache Selenium
rmdir /s "%TEMP%\selenium"
```

### 🛠️ Manutenzione Sistema

#### **Pulizia Periodica:**
1. Svuota cache browser
2. Aggiorna ChromeDriver
3. Verifica account CSV
4. Controlla log errori
5. Testa proxy attivi

#### **Ottimizzazione Performance:**
1. Riduci bot simultanei se memoria limitata
2. Usa SSD per migliori performance
3. Chiudi programmi non necessari
4. Monitora utilizzo CPU/RAM

---

## 📈 METRICHE E MONITORAGGIO

### 📊 KPI Principali

**Creazione Account:**
- Tasso successo creazione
- Tempo medio per account
- Account creati per ora
- Rilevamenti robot

**Ascolto Musica:**
- Brani riprodotti totali
- Tempo ascolto cumulativo
- Playlist seguite
- Errori riproduzione

**Performance Sistema:**
- Utilizzo CPU/RAM
- Stabilità connessione
- Errori proxy
- Uptime bot

### 📋 File di Log

**account_spotify_creati.csv:**
```csv
Email,Password
username1@alicie.it,Napoli10!!
username2@alicie.it,Napoli10!!
```

**GUI Console Output:**
```
[Bot #1] Inizializzazione Bot #1...
[Bot #1] ChromeDriver configurato automaticamente
[Bot #1] Account in creazione...
[Bot #2] Tentativo di accesso con: user@alicie.it
[Bot #1] Account Creato!
```

---

## 📚 APPENDICI

### 🔗 Dipendenze Richieste

```txt
selenium>=4.15.0
webdriver-manager>=4.0.0
faker>=20.0.0
pyautogui>=0.9.54
python-dotenv>=1.0.0
selenium-stealth>=1.0.6
tkinter (built-in)
threading (built-in)
concurrent.futures (built-in)
```

### 📖 Riferimenti XPath

**Spotify Web Player Elements:**
```python
# Login
login_button = '//*[@id="global-nav-bar"]/div[3]/div[1]/div[2]/button[2]'
username_field = '//*[@id="login-username"]'
password_field = '//*[@id="login-password"]'

# Playlist
follow_button = '[data-testid="add-button"]'
song_position = '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[{}]/div'

# Account Creation
signup_email = '//*[@id="username"]'
signup_password = '//*[@id="new-password"]'
signup_name = '//*[@id="displayName"]'
```

### 🌍 Supporto Browser

**Chrome Supportato:**
- Chrome 120+
- Chrome Beta
- Chromium
- Chrome Canary (con configurazione)

**Configurazioni Testate:**
- Windows 10/11
- Chrome 120.0.6099.x
- ChromeDriver 120.0.6099.x
- Risoluzione 1920x1080+

---

*Documentazione aggiornata alla versione 1.2.0*
*© 2024 HunterStile - Tutti i diritti riservati*
