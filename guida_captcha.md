# Guida alla Risoluzione Automatica dei CAPTCHA per Spotify Bot

## Introduzione
Questo documento fornisce istruzioni dettagliate su come configurare e utilizzare la funzionalità di risoluzione automatica dei CAPTCHA nel tuo Spotify Bot. Con questa implementazione, il bot può continuare a funzionare anche quando Spotify richiede la verifica CAPTCHA, eliminando la necessità di intervento manuale.

## Cos'è un CAPTCHA?
I CAPTCHA sono test progettati per distinguere gli utenti umani dai bot. Spotify li utilizza per proteggere il proprio servizio dall'automazione massiva. Quando il bot viene rilevato come "non umano", Spotify mostra un CAPTCHA che deve essere risolto per procedere.

## Prerequisiti
1. **Account su un servizio di risoluzione CAPTCHA**:
   - [2Captcha](https://2captcha.com) (consigliato) - Ottimo rapporto qualità/prezzo
   - [Anti-Captcha](https://anti-captcha.com) - Alternativa affidabile
   - [Capsolver](https://capsolver.com) - Opzione più recente

2. **Credito sufficiente** sul tuo account del servizio scelto
3. **Chiave API** ottenuta dal servizio

## Configurazione Passo-Passo

### 1. Registrazione al servizio 2captcha
1. Vai su [2captcha.com](https://2captcha.com) e crea un account
2. Effettua un deposito (minimo consigliato: 10€)
3. Vai nella sezione "Account" o "API" per ottenere la tua chiave API

### 2. Configurazione del file .env
Il file `.env` deve contenere la tua chiave API:

```
# Chiave API per il servizio 2captcha
TWOCAPTCHA_API_KEY=abc123def456...  # Inserisci qui la tua chiave API reale
```

Per creare o modificare il file .env:
1. Apri Blocco note o un altro editor di testo
2. Inserisci la chiave come mostrato sopra
3. Salva il file come `.env` nella directory principale del bot

### 3. Attivazione nel file config.py
Nel file `config.py`, assicurati che le seguenti opzioni siano configurate:

```python
#Opzioni per la risoluzione automatica dei CAPTCHA
USE_CAPTCHA_SERVICE = True  # Attiva il servizio di risoluzione CAPTCHA
CAPTCHA_SERVICE = '2captcha'  # Il servizio selezionato
```

### 4. Verifica della configurazione
Esegui lo script di test per verificare che tutto sia configurato correttamente:
```
python test_captcha.py
```

## Funzionamento Avanzato

### Tipi di CAPTCHA supportati
Il sistema è stato progettato per gestire automaticamente diversi tipi di CAPTCHA che possono apparire su Spotify:

1. **reCAPTCHA v2** - I classici "Sono un robot" con selezione immagini
2. **reCAPTCHA v3** - Versione invisibile che valuta il comportamento dell'utente
3. **hCaptcha** - Alternative a reCAPTCHA utilizzate da alcuni siti
4. **CAPTCHA personalizzati di Spotify** - Verifiche specifiche implementate da Spotify

### Strategie implementate
Il sistema utilizza diverse strategie in sequenza per risolvere i CAPTCHA:

1. **Rilevamento intelligente** - Identifica automaticamente il tipo di CAPTCHA presente
2. **Risoluzione tramite API** - Invia il CAPTCHA al servizio esterno
3. **Interazione diretta** - Tenta di interagire con gli elementi visibili dopo la risoluzione
4. **Strategie di fallback** - Tentativi alternativi se i metodi principali falliscono

### Debug e analisi
Per scopi di troubleshooting, vengono salvati screenshot del processo:

- `captcha_prima_[timestamp].png` - Lo stato prima del tentativo di risoluzione
- `captcha_dopo_[timestamp].png` - Lo stato dopo la risoluzione
- `captcha_frame_[n]_[timestamp].png` - Screenshot degli iframe del CAPTCHA

## Costi e Considerazioni

### Costi del servizio
- **2Captcha**: da $0.50 a $2.99 per 1000 CAPTCHA (circa 0.001-0.003€ per singolo CAPTCHA)
- Con un deposito di 10€, puoi risolvere diverse migliaia di CAPTCHA

### Ottimizzazione dei costi
1. Utilizza `USE_CAPTCHA_SERVICE = False` e `STOP_FOR_ROBOT = True` quando non sei presente
2. Attiva il servizio solo quando necessario utilizzare il bot in modo autonomo
3. Verifica periodicamente il saldo del tuo account 2captcha

### Prestazioni attese
- **Tempo medio di risoluzione**: 5-20 secondi
- **Tasso di successo**: 85-95% per i CAPTCHA standard
- **Durata credito**: Un deposito di 10€ può durare da settimane a mesi, a seconda dell'uso

## Risoluzione dei problemi

### Problemi comuni e soluzioni
1. **"Errore: Chiave API non trovata"**
   - Verifica che il file `.env` sia nella posizione corretta con la chiave API inserita

2. **"Impossibile risolvere il CAPTCHA"**
   - Controlla il saldo del tuo account 2captcha
   - Verifica la connessione internet
   - Prova a utilizzare un proxy diverso

3. **"CAPTCHA risolto ma non accettato da Spotify"**
   - Prova ad aumentare i tempi di attesa (`sleep`) dopo la risoluzione
   - Potrebbe essere necessario aggiornare lo script se Spotify ha modificato il suo sistema

### Test e diagnostica
Usa lo script `test_captcha_spot.py` per verificare il funzionamento diretto con Spotify:
```
python test_captcha_spot.py
```

## Supporto e aggiornamenti
Per assistenza o per segnalare problemi, contatta il supporto. Il sistema viene regolarmente aggiornato per adattarsi ai cambiamenti nei sistemi CAPTCHA di Spotify.
