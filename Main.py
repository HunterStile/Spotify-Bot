import random
from time import sleep
from funzioni.spotify_functions import *
from config import *
import re

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
    ripetizione = True
    count = 0  # Initialize count for tracking iterations

     # Parse playlist configurations
    playlist_posizioni_fisse = parse_playlist_config(config.get('playlist_urls', []))

    while ripetizione and (config.get('max_iterazioni', float('inf')) > count):
        count += 1  # Increment iteration count

        if config.get('crea_account', False):
            count_creazione += 1
            print(f"{count_creazione}° Creazione")
        else:
            count_accesso += 1
            print(f"{count_accesso}° Accesso")
        
        # Configurazione browser
        driver = configurazione_browser()
        
        try:
            # Gestione Proxy (opzionale)
            if config.get('usa_proxy', False):
                proxy_list = config.get('proxy_list_first', [])
                if proxy_list:
                    config_file_name = random.choice(proxy_list)
                    change_proxy(config_file_name)
                    
            # Creazione/Accesso account
            if config.get('crea_account', False):
                # Crea nuovo account
                credenziali = crea_account(driver, DOPPIOPROXY,STOP_FOR_ROBOT)
                if isinstance(credenziali,tuple):
                    email = credenziali[0]
                    password = credenziali[1]
                    driver = credenziali[2]
                else:
                    print("Bot rilevato,attendi un attimo...")

                    if RESET_ROUTER == True:
                        if TIPO_ROUTER == 'tim':
                            reset_router_tim(driver)
                            driver.close()
                        elif TIPO_ROUTER == 'vodaone':
                            reset_router_vodafone(driver)
                            driver.close()
                        else:
                            print("Non posso cambiare il tipo di router scelto..")
                            driver.close()

                    attendi_con_messaggio(TEMPO_RIPARTENZA)
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
            
             # Seguire playlist dinamicamente
            if config.get('segui_playlist', False):
                playlist_da_seguire = config.get('playlist_follow', [])
                for playlist in playlist_da_seguire:
                    seguo_playlist(driver, playlist)
            
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
                        Sento_canzone(driver, posizione)
                
                elif modalita_posizioni == 'statico':
                    # Controlla se ci sono posizioni specificate per questa playlist
                    if playlist_url_clean in playlist_posizioni_fisse:
                        posizioni = playlist_posizioni_fisse[playlist_url_clean]
                        
                        # Ascolta le posizioni specificate
                        for posizione in posizioni:
                            volte_ripetizione = random.randint(1, 1)
                            for _ in range(volte_ripetizione):
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
            if isinstance(credenziali,tuple):
                driver.close()
    
    print("Tutte le riproduzioni sono state eseguite!")

def attendi_con_messaggio(secondi):
    intervallo_messaggio = 600  # 10 minuti in secondi
    for i in range(secondi, 0, -1):
        if i % intervallo_messaggio == 0 or i == secondi:  # Stampa ogni 10 minuti o all'inizio
            print(f"Aspettando... {i} secondi rimasti")
        sleep(1)
    print("\nRiprendo il bot...")

# Chiamata principale
if __name__ == "__main__":
    print("Benvenuto nel bot Spotify by HunterStile!")
    esegui_bot_spotify(configurazione_bot)