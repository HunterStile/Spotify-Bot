# 🎵 Spotify Bot - Automazione Spotify Avanzata

<div align="center">
  <img src="https://img.shields.io/badge/Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white" alt="Spotify"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Version-1.2.0-brightgreen?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"/>
</div>

<div align="center">
  <h3>🚀 Bot di automazione avanzato per Spotify con GUI moderna e multithreading</h3>
  <p><em>Automatizza creazione account, seguimento playlist e ascolto musica su Spotify</em></p>
</div>

---

## 📋 Caratteristiche Principali

### 🎯 **Automazione Completa**
- ✅ **Creazione Account Automatica** - Genera account Spotify con dati casuali
- ✅ **Multi-Account Management** - Gestione rotazione account esistenti
- ✅ **Auto-Follow Playlist** - Seguimento automatico playlist specificate
- ✅ **Simulazione Ascolto** - Riproduzione intelligente con modalità casuale/fissa

### 🛡️ **Sistema Anti-Detection**
- 🕵️ **Modalità Stealth** - Protezioni anti-rilevamento avanzate
- 🌐 **User-Agent Randomization** - Rotazione automatica user agents
- 🤖 **Selenium Stealth** - Nascondimento automazione browser
- 📍 **Proxy Support** - Sistema proxy singolo e doppio

### 🔧 **Interfaccia e Controllo**
- 🎨 **GUI Moderna** - Interfaccia grafica dark theme Spotify
- ⚡ **Multithreading** - Esecuzione simultanea bot multipli
- 💾 **Configurazione Persistente** - Salvataggio automatico impostazioni
- 📊 **Monitoring Real-time** - Console log colorata con stato operazioni

---

## 🚀 Quick Start

### 1️⃣ **Installazione**

#### **Opzione A: Eseguibile Standalone** ⭐ *Consigliato*
```bash
# Scarica la release
1. Vai su GitHub Releases
2. Scarica dist.zip
3. Estrai i file
4. Esegui spotifybot.exe
```
> **💡 Nessuna installazione Python richiesta!**

#### **Opzione B: Da Codice Sorgente**
```bash
# Clona il repository
git clone https://github.com/HunterStile/Spotify-Bot.git
cd Spotify-Bot

# Installa dipendenze
pip install -r requirements.txt
```

### 2️⃣ **Avvio Rapido**

#### **Con Eseguibile**
```bash
# Esegui l'eseguibile standalone
./spotifybot.exe
```

#### **Con Python**
```bash
# Esegui l'interfaccia grafica
python spotify_bot_gui.py
```

### 3️⃣ **Configurazione Base**
1. **✅ Abilita "Crea Nuovo Account"** per generazione automatica
2. **🔢 Imposta "Iterazioni Max"** (default: 100)
3. **▶️ Clicca "Avvia Bot"** per iniziare l'automazione

---

## 🏗️ Architettura del Sistema

```
Spotify-Bot/
├── 🎯 spotify_bot_gui.py          # Interfaccia grafica principale
├── ⚙️ Main.py                     # Engine di esecuzione bot
├── 🔧 config.py                   # Configurazioni globali
├── 📊 account_spotify.csv         # Database account esistenti
├── 📝 account_spotify_creati.csv  # Log account creati
├── 🌐 chromedriver.exe            # Driver browser automation
├── 🕵️ user_agents.txt             # User agents per stealth
├── funzioni/
│   └── 🔌 spotify_functions.py    # Libreria funzioni core
└── 📚 SPOTIFY_BOT_DOCUMENTATION.md # Documentazione completa
```

---

## 🎛️ Configurazioni Principali

### ⚙️ **Modalità Operative**
| Opzione | Descrizione | Default |
|---------|-------------|---------|
| **Crea Account** | Genera nuovi account Spotify | ✅ |
| **Usa Proxy** | Abilita sistema proxy | ❌ |
| **Segui Playlist** | Auto-follow playlist specificate | ✅ |
| **Ascolta Canzoni** | Simula riproduzione musicale | ✅ |
| **Modalità Stealth** | Protezioni anti-detection | ✅ |

### 🚀 **Multithreading**
- **Bot Simultanei**: 1-10 istanze parallele
- **Max Chrome**: Limite browser aperti simultaneamente
- **Gestione Memoria**: Semafori per controllo risorse

### 🌐 **Sistema Proxy**
- **Proxy Singolo**: Lista proxy standard
- **Doppio Proxy**: Configurazione avanzata con proxy primari
- **Proxifier Integration**: Supporto profili .ppx

---

## 🎵 Configurazione Playlist

### 📋 **Lista Playlist da Seguire**
```
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd
```

### 🎧 **Playlist per Ascolto**
```
# Modalità Casuale
https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R

# Modalità Posizioni Fisse
https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R;1,6,12,18
```

---

## 🔧 Requisiti di Sistema

### 📋 **Software Richiesto**
- **Sistema Operativo**: Windows 10/11, macOS, Linux
- **Python**: 3.8 o superiore
- **Browser**: Google Chrome (versione recente)
- **RAM**: Minimo 4GB (8GB consigliato per multithreading)

### 📦 **Dipendenze Python**
```txt
selenium>=4.15.0
webdriver-manager>=4.0.0
faker>=20.0.0
pyautogui>=0.9.54
selenium-stealth>=1.0.6
tkinter (built-in)
```

---

## 🖥️ Guida all'Interfaccia

### 🎨 **Layout Principale**
La GUI utilizza un design moderno con tema scuro ispirato a Spotify:
- **🎨 Background**: #121212 (nero Spotify)
- **💚 Accent**: #1DB954 (verde Spotify)
- **⚪ Testo**: #FFFFFF (bianco)

### 📊 **Sezioni Interfaccia**
1. **🔧 Colonna Sinistra**: Configurazioni principali e multithreading
2. **📋 Colonna Destra**: Liste proxy/playlist e contenuti
3. **🎮 Pannello Controlli**: Pulsanti azione e console output
4. **💾 Auto-Save**: Salvataggio automatico in `gui_config.json`

---

## 🚨 Risoluzione Problemi

### ❌ **Errori Comuni**

#### **ChromeDriver Non Trovato**
```bash
# Soluzione: Aggiorna ChromeDriver dalla GUI
Pulsante "Aggiorna ChromeDriver" → Download automatico
```

#### **Proxy Non Funzionante**
```bash
# Verifica installazione Proxifier
# Controlla profili .ppx in %APPDATA%\Proxifier4\Profiles\
```

#### **Bot Rilevato**
```bash
# Abilita protezioni stealth
# Usa proxy per cambio IP
# Attendi tempi casuali tra operazioni
```

### 🔧 **Comandi Diagnostici**
```bash
# Verifica processi Chrome
tasklist | findstr chrome

# Termina processi bloccati
taskkill /f /im chrome.exe

# Pulisci cache temporanea
rmdir /s "%TEMP%\selenium"
```

---

## 📈 Funzionamento Bot

### 🔄 **Ciclo di Esecuzione**
1. **🚀 Inizializzazione** - Caricamento configurazioni e verifica risorse
2. **🌐 Setup Browser** - Configurazione Chrome con protezioni stealth
3. **🔗 Gestione Proxy** - Attivazione proxy se configurati
4. **👤 Operazioni Account** - Creazione/accesso account Spotify
5. **🎵 Azioni Playlist** - Seguimento playlist e simulazione ascolto
6. **🛡️ Error Recovery** - Gestione errori e reset automatico

### 📊 **Metriche Monitorate**
- **Account creati/ora**
- **Tasso successo operazioni**
- **Brani riprodotti**
- **Errori e rilevamenti**
- **Performance sistema**

---

## 🔄 Aggiornamenti e Versioni

### 📋 **Versione Corrente: 1.2.0**
- ✅ Multithreading avanzato
- ✅ GUI moderna rinnovata
- ✅ Sistema proxy doppio
- ✅ Modalità stealth migliorata
- ✅ Gestione errori robusta

### 🗓️ **Roadmap Futura**
- 🔮 Supporto Spotify API
- 🎯 Targeting demografico
- 📱 Versione mobile/web
- 🤖 AI per bypass detection
- 📊 Dashboard analytics

---

## ⚖️ Considerazioni Legali

### ⚠️ **Disclaimer**
Questo software è fornito esclusivamente per scopi educativi e di ricerca. L'utilizzo del bot potrebbe violare i Termini di Servizio di Spotify.

### 📝 **Responsabilità**
- ✅ Usa il bot responsabilmente
- ✅ Rispetta i limiti di rate
- ✅ Non utilizzare per scopi commerciali
- ✅ Considera impatto sui server Spotify

---

## 🤝 Contributi

### 🎯 **Come Contribuire**
1. **🍴 Fork** il repository
2. **🌿 Crea** un branch per le tue modifiche
3. **✨ Implementa** migliorie o fix
4. **📤 Invia** una Pull Request

### 🐛 **Segnalazione Bug**
Apri una [Issue](https://github.com/HunterStile/Spotify-Bot/issues) con:
- Descrizione dettagliata del problema
- Steps per riprodurre l'errore
- Log e screenshot
- Configurazione sistema

---

## 📞 Supporto

### 💬 **Contatti**
- **👨‍💻 Sviluppatore**: HunterStile
- **📧 Email**: talkchainsrl@gmail.com
- **🐛 Issues**: [GitHub Issues](https://github.com/HunterStile/Spotify-Bot/issues)
- **📚 Docs**: [`SPOTIFY_BOT_DOCUMENTATION.md`](./SPOTIFY_BOT_DOCUMENTATION.md)

### 📖 **Documentazione**
- **📋 Guida Completa**: [`SPOTIFY_BOT_DOCUMENTATION.md`](./SPOTIFY_BOT_DOCUMENTATION.md)
- **📝 Patch Notes**: [`PATCH_NOTES.md`](./PATCH_NOTES.md)
- **🏗️ Build Guide**: [`BUILD_GUIDE.md`](./BUILD_GUIDE.md)

---

<div align="center">
  <h3>⭐ Se questo progetto ti è utile, lascia una stella!</h3>
  <p><em>Creato con ❤️ da HunterStile</em></p>
  <p><strong>© 2024 - Tutti i diritti riservati</strong></p>
</div>
