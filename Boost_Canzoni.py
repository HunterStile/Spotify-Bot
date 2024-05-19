from funzioni.spotify_functions import *

## >main<
print("Benvenuto nel bot Spotify by HunterStile!") 
all_posizione = [posizione8,posizione9,posizione10,posizione11,posizione12,posizione13,posizione14,posizione15,posizione16,posizione18]

#scegli chi bustare!
#pop-punk - PLAYLIST1
#trap-italia - PLAYLIST2
#new-generation - PLAYLIST3
#new-music - PLAYLIST4
#top-music - PLAYLIST5
#inde-italia - PLAYLIST6
#start

file = 'account_spotify.csv'
with open(file, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)  # salta la prima riga con l'intestazione
    for row in csvreader:
        posizione_casuale = random.choice(all_posizione)
        count = count + 1
        print(count,'° Account')
        email = row[0]
        password = row[1]
        driver = configurazione_browser()
        errore = Accesso_spotify(driver,email,password)
        if errore == False:
            scegli_playlist(driver,playlist1) #poppunk
            Sento_canzone(driver,posizione11)
            sleep(120)
            
        else:
            print("Accesso non riusciuto, riprovo con il prossimo account...")
        driver.close()

input("Tutte le riproduzioni sono state effettuate!")














