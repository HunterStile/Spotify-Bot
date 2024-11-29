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

#variabili
primo=1
secondo=2

#Scelta PROXY
#config_file_name = random.choice(proxy_list)
#changhe_proxy(config_file_name)  # Configura il proxy

with open(file, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)  # salta la prima riga con l'intestazione
    for row in csvreader:
        count = count + 1
        print(count,'° Account')
        email = row[0]
        password = row[1]
        driver = configurazione_browser()
        errore = Accesso_spotify(driver,email,password)
        if errore == False:
            scegli_playlist(driver,playlist4) #poppunk
            Sento_canzone(driver,primo)
            Sento_canzone(driver,secondo)
            
            
        else:
            print("Accesso non riusciuto, riprovo con il prossimo account...")
        driver.close()

input("Tutte le riproduzioni sono state effettuate!")














