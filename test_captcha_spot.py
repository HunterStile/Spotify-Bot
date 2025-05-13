import sys
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Imposta il percorso corretto per importare le funzioni
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funzioni.spotify_functions import risolvi_captcha, configurazione_browser, debug_captcha_screenshot

def test_captcha_solver():
    """Test della funzione di risoluzione CAPTCHA specifica per Spotify"""
    print("="*50)
    print("Test del risolutore CAPTCHA di Spotify")
    print("="*50)
    
    # Carica le variabili d'ambiente
    load_dotenv()
    api_key = os.getenv('TWOCAPTCHA_API_KEY')
    
    if not api_key or api_key == "tua_chiave_api_qui":
        print("ERRORE: Chiave API 2captcha non configurata correttamente nel file .env")
        print("Per favore, modifica il file .env e inserisci la tua chiave API.")
        return
        
    print(f"Chiave API trovata: {api_key[:4]}...{api_key[-4:]}")
    
    # Configurazione del browser con un user-agent generico
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    driver = configurazione_browser(user_agent, disable_stealth=False)
    
    try:
        # Vai al sito di iscrizione di Spotify
        print("Navigazione verso la pagina di iscrizione di Spotify...")
        driver.get("https://www.spotify.com/it/signup/")
        
        # Attendi che la pagina si carichi
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        # Accetta i cookie se presenti
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            cookie_button.click()
            print("Cookie accettati")
        except:
            print("Nessun popup cookie trovato o già accettato")
        
        # Simula la compilazione del form fino ad arrivare al CAPTCHA
        print("Compilazione del modulo di iscrizione...")
        
        # Inserisci email
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            email_field.clear()
            email_field.send_keys(f"test{int(time.time())}@example.com")
            
            # Clicca sul pulsante Avanti
            next_button = driver.find_element(By.XPATH, '//button[contains(., "Avanti")]')
            next_button.click()
            print("Email inserita, pulsante Avanti cliccato")
        except Exception as e:
            print(f"Errore durante l'inserimento dell'email: {str(e)}")
        
        time.sleep(3)
        
        # Simula altre azioni finché non appare il CAPTCHA
        try:
            # Aggiungi altre azioni se necessario per raggiungere il CAPTCHA
            pass
        except:
            pass
        
        # Esegui uno screenshot dello stato attuale
        debug_captcha_screenshot(driver, "before_captcha_test")
        
        # Verifica se è presente un CAPTCHA
        print("Verifica della presenza di un CAPTCHA...")
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        captcha_present = (
            "captcha" in body_text or 
            "robot" in body_text or 
            len(driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")) > 0 or
            len(driver.find_elements(By.XPATH, "//iframe[contains(@src, 'hcaptcha')]")) > 0
        )
        
        if captcha_present:
            print("CAPTCHA rilevato! Tentativo di risoluzione...")
            
            # Tenta di risolvere il CAPTCHA
            start_time = time.time()
            success = risolvi_captcha(driver, driver.current_url)
            end_time = time.time()
            
            # Esegui uno screenshot dopo il tentativo
            debug_captcha_screenshot(driver, "after_captcha_test")
            
            if success:
                print(f"CAPTCHA risolto con successo in {end_time - start_time:.2f} secondi!")
                
                # Attendi un momento per vedere il risultato
                time.sleep(5)
                
                # Verifica il risultato
                body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                if "robot" not in body_text and "captcha" not in body_text:
                    print("Verifica superata: il testo relativo al robot check non è più presente.")
                else:
                    print("AVVISO: Il testo relativo al robot check sembra ancora presente.")
            else:
                print("Impossibile risolvere il CAPTCHA.")
        else:
            print("Nessun CAPTCHA rilevato durante il test.")
            
        print("\nTest completato.")
    
    except Exception as e:
        print(f"Errore durante il test: {str(e)}")
    finally:
        # Aspetta prima di chiudere per vedere il risultato
        print("Il browser verrà chiuso automaticamente tra 10 secondi...")
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    test_captcha_solver()
