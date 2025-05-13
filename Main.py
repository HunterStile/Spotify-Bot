import random
from time import sleep
from funzioni.spotify_functions import *
from config import *
import re
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

def parse_playlist_config(playlist_urls):
    """
    Parse playlist URLs to extract optional position configurations
    Format: playlist_url;1,3,5 or just playlist_url
    """
    playlist_config = {}
    for url in playlist_urls:
        parts = url.split(';')
        playlist_url = parts[0]
        
        if len(parts) > 1:
            positions = [str(p.strip()) for p in parts[1].split(',')]
            playlist_config[playlist_url] = positions
    
    return playlist_config

def esegui_bot_spotify(config):
    count_creazione = 0
    count_accesso = 0
    ripetizione = config.get('ripetizione', True)
    count = 0
    
    # Get the stop event from config if available
    stop_event = config.get('stop_event', None)
    driver = None

    # Cleanup environment if clean_start is requested
    if config.get('clean_start', False):
        print("Inizializzazione dell'ambiente pulito...")
        try:
            # Clear any temporary browser files that might cause issues
            if os.path.exists('chrome_debug.log'):
                os.remove('chrome_debug.log')
                
            # You can add more cleanup steps here as needed
        except Exception as e:
            print(f"Errore durante la pulizia iniziale: {str(e)}")

    while ripetizione and (config.get('max_iterazioni', float('inf')) > count):
        # Check for stop event at the beginning of each iteration
        if stop_event and stop_event.is_set():
            print("Interruzione richiesta, arresto del bot...")
            break
        
        count += 1

        if config.get('crea_account', False):
            count_creazione += 1
            print(f"{count_creazione}° Creazione")
        else:
            count_accesso += 1
            print(f"{count_accesso}° Accesso")
        
        try:
            # Gestione Proxy (opzionale)
            if config.get('usa_proxy', False):
                proxy_list = None
                if config.get('doppio_proxy', False):
                    # Se doppio proxy è attivo, usa proxy_list_first
                    proxy_list = config.get('proxy_list_first', [])
                    print("Usando lista proxy primaria (doppio proxy attivo):", proxy_list)
                else:
                    # Altrimenti usa proxy_list normale
                    proxy_list = config.get('proxy_list', [])
                    print("Usando lista proxy standard:", proxy_list)
                
                if proxy_list and len(proxy_list) > 0:
                    config_file_name = random.choice(proxy_list)
                    print(f"Selezionato proxy: {config_file_name}")
                    change_proxy(config_file_name)
                else:
                    print("Attenzione: Lista proxy vuota!")
            
            # Configurazione browser
            user_agent = get_random_user_agent()
            driver = configurazione_browser(user_agent, config.get('disable_stealth', False))

            # Check for stop event after browser setup
            if stop_event and stop_event.is_set():
                print("Interruzione richiesta, chiusura del browser...")
                if driver:
                    driver.quit()
                break

            # Creazione/Accesso account
            if config.get('crea_account', False):
                # Crea nuovo account
                credenziali = crea_account(
                    driver, 
                    config.get('doppio_proxy', False), 
                    config.get('stop_for_robot', False),
                    proxy_list=config.get('proxy_list', []),
                    proxy_list_first=config.get('proxy_list_first', []) if config.get('doppio_proxy', False) else None,
                    use_captcha_service=config.get('USE_CAPTCHA_SERVICE', True),
                    captcha_service=config.get('CAPTCHA_SERVICE', '2captcha')
                )
                
                # Check for stop event after account creation
                if stop_event and stop_event.is_set():
                    print("Interruzione richiesta, chiusura del browser...")
                    if driver:
                        driver.quit()
                    break
                
                if isinstance(credenziali,tuple):
                    email = credenziali[0]
                    password = credenziali[1]
                    driver = credenziali[2]
                else:
                    print("Bot rilevato, attendi un attimo...")

                    if config.get('reset_router', False):
                        tipo_router = config.get('tipo_router', '')
                        if tipo_router == 'tim':
                            reset_router_tim(driver)
                            driver.close()
                        elif tipo_router == 'vodafone':
                            reset_router_vodafone(driver)
                            driver.close()
                        else:
                            print("Non posso cambiare il tipo di router scelto..")
                            driver.close()

                    attendi_con_messaggio(config.get('tempo_ripartenza', 7200), stop_event)
                    if stop_event and stop_event.is_set():
                        break
                    continue
            else:
                # Carica account da CSV
                with open(file, newline='', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=',')
                    next(csvreader)  # salta intestazione
                    
                    # Leggi tutti gli account rimanenti
                    accounts = list(csvreader)
                    
                    # Se non ci sono più account, esci dal ciclo
                    if not accounts:
                        print("Nessun account rimanente nel file CSV")
                        break
                    
                    # Prendi il primo account
                    row = accounts[0]
                    email, password = row[0], row[1]
                    
                    errore = Accesso_spotify(driver, email, password)
                    if errore:
                        print("Accesso non riuscito, rimuovo questo account...")
                        
                        # Riscrivi il file CSV escludendo l'account che non ha funzionato
                        with open(file, 'w', newline='', encoding='utf-8') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            # Riscrivi l'intestazione
                            csvwriter.writerow(['Email', 'Password'])
                            # Riscrivi gli altri account
                            for account in accounts[1:]:
                                csvwriter.writerow(account)
                        
                        # Continua con il prossimo ciclo per provare con l'account successivo
                        continue
                    
                    # Se l'accesso ha successo, sposta l'account in fondo al CSV
                    with open(file, 'w', newline='', encoding='utf-8') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        # Riscrivi l'intestazione
                        csvwriter.writerow(['Email', 'Password'])
                        # Riscrivi tutti gli altri account
                        for account in accounts[1:]:
                            csvwriter.writerow(account)
                        # Aggiungi l'account usato in fondo
                        csvwriter.writerow(row)
            
            # Check for stop event before playlist operations
            if stop_event and stop_event.is_set():
                print("Interruzione richiesta, chiusura del browser...")
                if driver:
                    driver.quit()
                break
                
            # Seguire playlist dinamicamente
            if config.get('segui_playlist', False):
                playlist_da_seguire = config.get('playlist_follow', [])
                for playlist in playlist_da_seguire:
                    # Check for stop event in playlist loop
                    if stop_event and stop_event.is_set():
                        break
                    seguo_playlist(driver, playlist)
            
            # Check for stop event before listening to songs
            if stop_event and stop_event.is_set():
                print("Interruzione richiesta, chiusura del browser...")
                if driver:
                    driver.quit()
                break
                
            # Ascoltare canzoni con configurazione avanzata
            if config.get('ascolta_canzoni', False):
                # Modalità di selezione delle posizioni
                modalita_posizioni = config.get('modalita_posizioni', 'random')
                
                # Scegli una playlist
                playlist_ascolto = random.choice(config.get('playlist_urls', []))
                
                # Estrai URL pulito
                playlist_url_clean = playlist_ascolto.split(';')[0]
      
                scegli_playlist(driver, playlist_url_clean)
                
                # Gestisci la selezione delle posizioni
                if modalita_posizioni == 'random':
                    # Genera una posizione casuale tra 1 e 20
                    posizione = str(random.randint(1, 20))
                    volte_ripetizione = random.randint(1, 1)
                    
                    # Ascolta la canzone
                    for _ in range(volte_ripetizione):
                        # Check for stop event in song loop
                        if stop_event and stop_event.is_set():
                            break
                        Sento_canzone(driver, posizione)
                
                elif modalita_posizioni == 'statico':
                    # Ottieni tutte le playlist con configurazioni
                    playlist_posizioni_fisse = parse_playlist_config(config.get('playlist_urls', []))
                    
                    # Itera su tutte le playlist con posizioni specificate
                    for playlist_url_clean, posizioni in playlist_posizioni_fisse.items():
                        # Check for stop event in playlist loop
                        if stop_event and stop_event.is_set():
                            break
                            
                        # Scegli la playlist
                        scegli_playlist(driver, playlist_url_clean)
                        
                        # Ascolta le posizioni specificate
                        for posizione in posizioni:
                            # Check for stop event in position loop
                            if stop_event and stop_event.is_set():
                                break
                                
                            volte_ripetizione = random.randint(1, 1)
                            for _ in range(volte_ripetizione):
                                # Check for stop event in repetition loop
                                if stop_event and stop_event.is_set():
                                    break
                                Sento_canzone(driver, posizione)
                    else:
                        print(f"Playlist non trovata nella configurazione: {playlist_ascolto}")
            
            # Input utente per continuare (opzionale)
            if config.get('input_utente', False):
                risposta = input("Vuoi continuare con un'altra iterazione? (s/n): ")
                ripetizione = risposta.lower() == 's'
            else:
                # Se non è richiesto input utente, usa il valore di default
                ripetizione = config.get('ripetizione', False)
        
        except Exception as e:
            print(f"Errore durante l'esecuzione: {e}")
        
        finally:
            # Chiudi sempre il driver
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    print(f"Errore durante la chiusura del driver: {e}")
    
    print("Tutte le riproduzioni sono state eseguite!")
    
    # Make sure driver is closed on exit
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Errore durante la chiusura finale del driver: {e}")

def attendi_con_messaggio(secondi, stop_event=None):
    """
    Attendi per un certo numero di secondi, mostrando messaggi periodici
    e controllando se è stato richiesto l'arresto.
    """
    intervallo_messaggio = 600  # 10 minuti in secondi
    for i in range(secondi, 0, -1):
        # Check if stop requested
        if stop_event and stop_event.is_set():
            print("Interruzione richiesta durante l'attesa.")
            return
            
        if i % intervallo_messaggio == 0 or i == secondi:  # Stampa ogni 10 minuti o all'inizio
            print(f"Aspettando... {i} secondi rimasti")
        sleep(1)
    print("\nRiprendo il bot...")

# Chiamata principale
if __name__ == "__main__":
    print("Benvenuto nel bot Spotify by HunterStile!")
    esegui_bot_spotify(configurazione_bot)