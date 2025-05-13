import os
from dotenv import load_dotenv
from twocaptcha import TwoCaptcha
import sys

def test_captcha_service():
    print("=======================================")
    print("Test del servizio di risoluzione CAPTCHA")
    print("=======================================")
    
    # Carica le variabili d'ambiente
    load_dotenv()
    
    # Ottieni la chiave API
    api_key = os.getenv('TWOCAPTCHA_API_KEY')
    
    if not api_key or api_key == 'tua_chiave_api_qui':
        print("ERRORE: Chiave API non configurata.")
        print("Per favore, modifica il file .env e inserisci la tua chiave API.")
        print("Esempio: TWOCAPTCHA_API_KEY=abc123def456...")
        return False
        
    print(f"Chiave API trovata: {api_key[:4]}...{api_key[-4:]}")
    
    # Inizializza il solutore
    solver = TwoCaptcha(api_key)
    
    # Verifica il saldo dell'account
    try:
        balance = solver.balance()
        print(f"Saldo dell'account: ${balance}")
        if float(balance) <= 0:
            print("ATTENZIONE: Il tuo saldo è esaurito. Ricarica il tuo account per utilizzare il servizio.")
            return False
    except Exception as e:
        print(f"ERRORE durante la verifica del saldo: {str(e)}")
        print("La chiave API potrebbe non essere valida o ci sono problemi di connessione al servizio.")
        return False
    
    print("\nTest completato con successo!")
    print("Il servizio di risoluzione CAPTCHA è correttamente configurato.")
    
    return True

if __name__ == "__main__":
    success = test_captcha_service()
    if not success:
        print("\nLa configurazione del servizio CAPTCHA non è corretta.")
        print("Consulta il file guida_captcha.md per istruzioni dettagliate.")
    else:
        print("\nConfigura USE_CAPTCHA_SERVICE = True nel file config.py per attivare la risoluzione automatica.")
    
    input("Premi INVIO per uscire...")
