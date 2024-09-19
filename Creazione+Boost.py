from funzioni.spotify_functions import *
from config import *
## >main<
print("Benvenuto nel bot Spotify by HunterStile!") 

#scegli chi bustare!
#pop-punk - PLAYLIST1
#trap-italia - PLAYLIST2
#new-generation - PLAYLIST3
#new-music - PLAYLIST4
#top-music - PLAYLIST5
#inde-italia - PLAYLIST6
#start

#Variabili
posizione = '11'

#Scelta PROXY
#config_file_name = random.choice(proxy_list)
#changhe_proxy(config_file_name)  # Configura il proxy

ripetizione = True
while ripetizione == True:
    count = count + 1
    print(count,"° Creazione")
    #Configurazione browser
    driver = configurazione_browser()
    #Recupero credenziali
    credenziali = crea_account(driver)
    email = credenziali[0]
    password = credenziali[1] 
    driver = credenziali[2]
    
    #Seguo le playlist        
    seguo_playlist(driver,playlist1)
    seguo_playlist(driver,playlist2)
    seguo_playlist(driver,playlist3)
    seguo_playlist(driver,playlist4)
    seguo_playlist(driver,playlist5)
    seguo_playlist(driver,playlist6)

    #Bosting canzoni
    scegli_playlist(driver,playlist1) #poppunk
    Sento_canzone(driver,posizione) 

    #scelta ripetizione
    ripetizione = True
    driver.close()

print("Tutte le riproduzione sono state eseguite!")
    



















