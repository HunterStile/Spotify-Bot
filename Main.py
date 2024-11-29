import random
from time import sleep
from funzioni.spotify_functions import *
from config import *

def esegui_bot_spotify(config):
    """
    Esegue il bot Spotify con configurazione dinamica e scalabile.
    
    :param config: Dizionario di configurazione avanzata
    """
    count = 0
    ripetizione = True
    
    while ripetizione and (config.get('max_iterazioni', float('inf')) > count):
        count += 1
        print(f"{count}° Creazione")
        
        # Configurazione browser
        driver = configurazione_browser()
        
        try:
             # Gestione Proxy (opzionale)
            if config.get('usa_proxy', False):
                proxy_list = config.get('proxy_list', [])
                if proxy_list:
                    config_file_name = random.choice(proxy_list)
                    changhe_proxy(config_file_name)  # Funzione per cambiare proxy
                    print(f"Proxy configurato: {config_file_name}")

                    
            # Creazione account (opzionale)
            if config.get('crea_account', False):
                credenziali = crea_account(driver)
                email = credenziali[0]
                password = credenziali[1]
                driver = credenziali[2]
            
            # Seguire playlist dinamicamente
            if config.get('segui_playlist', False):
                playlist_da_seguire = config.get('playlist_urls', [])
                for playlist in playlist_da_seguire:
                    seguo_playlist(driver, playlist)
            
            # Ascoltare canzoni con configurazione avanzata
            if config.get('ascolta_canzoni', False):
                # Playlist per l'ascolto
                playlist_ascolto = config.get('playlist_ascolto', '')
                scegli_playlist(driver, playlist_ascolto)
                
                # Configurazione ascolto canzone
                posizioni = config.get('posizioni_ascolto', [])
                ripetizioni_per_posizione = config.get('ripetizioni_per_posizione', {})
                
                for posizione in posizioni:
                    # Numero di ripetizioni per questa posizione (default 1 se non specificato)
                    volte_ripetizione = ripetizioni_per_posizione.get(posizione, 1)
                    
                    for _ in range(volte_ripetizione):
                        Sento_canzone(driver, str(posizione))
                        sleep(config.get('intervallo_ascolto', 120))
            
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
            driver.close()
    
    print("Tutte le riproduzioni sono state eseguite!")

    # Chiamata principale
if __name__ == "__main__":
    print("Benvenuto nel bot Spotify by HunterStile!")
    esegui_bot_spotify(configurazione_bot)