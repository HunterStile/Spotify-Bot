# 🔍 CONTACT FINDER - DOCUMENTAZIONE

## 📋 Panoramica

Il **Contact Finder** è un modulo avanzato che arricchisce automaticamente i dati degli artisti emergenti trovando i loro contatti social ed email attraverso ricerche automatiche sui motori di ricerca.

## 🎯 Funzionalità Principali

### 📱 Social Media Supported
- **Instagram** - Trova profili e handle
- **Facebook** - Pagine ufficiali e profili
- **TikTok** - Account e handle
- **Twitter/X** - Profili e username
- **YouTube** - Canali ufficiali
- **Email** - Indirizzi per booking e contatti

### 🌐 Motori di Ricerca
- **Google** - Ricerca principale con parsing avanzato
- **Bing** - Motore secondario per coverage extra

### ⚙️ Funzionalità Avanzate
- **Modalità Stealth** - Anti-detection per evitare blocchi
- **User Agent Rotation** - Rotazione automatica user agents
- **Delay Configurabile** - Controllo velocità per evitare rate limiting
- **Verifica Profili** - Opzionale: verifica esistenza profili trovati
- **Export CSV** - Salvataggio dati arricchiti
- **Salvataggio Incrementale** - Backup ogni 5 artisti processati

## 📊 Input/Output

### Input (CSV)
Il modulo legge il file CSV generato dall'Artist Scraper:
```csv
Nome Artista,Spotify URL,Ascoltatori Mensili,Data Scraping,Periodo Carriera
Skinni,https://open.spotify.com/intl-it/artist/3WJG7q90wprkG8iUcM36XM,2306,2025-06-09 17:44:51,2023-2025
```

### Output (CSV Arricchito)
Genera un nuovo CSV con i contatti trovati:
```csv
Nome Artista,Spotify URL,Ascoltatori Mensili,Data Scraping,Periodo Carriera,Instagram,Facebook,TikTok,Twitter,YouTube,Email,Sito Web,Data Ricerca Contatti
Skinni,https://open.spotify.com/intl-it/artist/3WJG7q90wprkG8iUcM36XM,2306,2025-06-09 17:44:51,2023-2025,@skinni_official,facebook.com/skinnimusic,,@skinni_music,,booking@skinni.com,skinni.com,2025-06-09 18:00:00
```

## 🚀 Utilizzo

### Via GUI
1. Lancia `contact_finder_gui.py`
2. Seleziona il file CSV input degli artisti
3. Configura i parametri di ricerca
4. Avvia la ricerca contatti

### Via Codice
```python
from contact_finder import ContactFinder, get_contact_finder_config

# Configurazione
config = get_contact_finder_config()
config['csv_input_file'] = 'artisti-emergenti.csv'
config['csv_output_file'] = 'artisti-con-contatti.csv'

# Esecuzione
finder = ContactFinder(config)
success = finder.process_csv()
```

## ⚙️ Configurazione

### Parametri Principali
```python
{
    'csv_input_file': 'artisti-emergenti.csv',     # File input
    'csv_output_file': 'artisti-con-contatti.csv', # File output
    'search_engines': ['google'],                   # Motori da usare
    'max_results_per_search': 3,                   # Risultati per query
    'delay_between_searches': (3, 7),              # Delay random (sec)
    'use_stealth_mode': True,                      # Modalità stealth
    'verify_social_profiles': False,               # Verifica esistenza
    'headless': False                              # Browser nascosto
}
```

### Query di Ricerca Automatiche
Per ogni artista, il sistema esegue automaticamente queste ricerche:
- `"Artist Name" instagram contact`
- `"Artist Name" facebook page`
- `"Artist Name" email booking`
- `"Artist Name" social media`
- `"Artist Name" official website`
- `"Artist Name" tiktok`
- `"Artist Name" twitter`
- `"Artist Name" youtube channel`

## 🔧 Pattern di Estrazione

### Instagram
- `instagram.com/username`
- `@username`
- `ig.me/username`

### Facebook
- `facebook.com/pagename`
- `fb.me/pagename`

### Email
- `email@domain.com`
- `mail: email@domain.com`
- Supporta spazi e variazioni

### Altri Social
Pattern specifici per TikTok, Twitter, YouTube con validazione lunghezza e caratteri.

## 📈 Performance

### Velocità
- **~2-5 minuti** per artista (dipende da delay configurato)
- **Salvataggio incrementale** ogni 5 artisti
- **Recovery automatico** in caso di interruzione

### Rate Limiting
- Delay configurabile tra ricerche (default: 3-7 secondi)
- User agent rotation automatica
- Modalità stealth per evitare detection

## 🛡️ Sicurezza e Anti-Detection

### Modalità Stealth
- Rimozione proprietà `webdriver`
- User agent rotation
- Delay randomici
- Esclusione switch automation

### Rate Limiting Intelligente
- Delay variabile tra ricerche
- Rotazione IP opzionale (configurabile)
- Rispetto robots.txt

## 📋 Troubleshooting

### Problemi Comuni

**Chrome/ChromeDriver Issues**
```bash
# Assicurati che ChromeDriver sia aggiornato
# Controlla la compatibilità versione Chrome
```

**Rate Limiting**
```python
# Aumenta i delay se ricevi blocchi
config['delay_between_searches'] = (5, 10)
```

**Profili Non Trovati**
```python
# Disabilita verifica per velocità
config['verify_social_profiles'] = False
```

## 📊 Statistiche di Esempio

Dopo il processamento, il sistema mostra:
```
📈 STATISTICHE CONTATTI:
  📱 Instagram: 15/20 (75.0%)
  📱 Facebook: 12/20 (60.0%)
  📱 TikTok: 8/20 (40.0%)
  📱 Twitter: 10/20 (50.0%)
  📱 YouTube: 5/20 (25.0%)
  📱 Email: 3/20 (15.0%)
  📱 Sito Web: 7/20 (35.0%)
```

## 🔄 Integrazione

### Con Artist Scraper
1. Esegui Artist Scraper per ottenere lista artisti emergenti
2. Usa il CSV output come input per Contact Finder
3. Ottieni CSV arricchito con tutti i contatti

### Con Spotify Bot Suite
- Integrato nel launcher principale
- Configurazione persistente
- Workflow automatizzato

## 📝 Note Tecniche

- **Selenium WebDriver** per navigazione web
- **Regex avanzate** per estrazione contatti
- **Threading** per GUI responsiva
- **CSV DictReader/Writer** per manipolazione dati
- **Requests** per verifica profili (opzionale)
