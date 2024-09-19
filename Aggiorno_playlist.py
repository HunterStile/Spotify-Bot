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

#Variabili
email = 'valentinaferraripromo@gmail.com'
password = 'Napoli10!!'
playlist_scelta = playlist1
playlist_target = 'https://open.spotify.com/playlist/5IMFrVKaonvz1AHWOhaX2A?'
brani_da_eliminare = 26
brani_da_aggiungere = 26
posizione_playlist = 3  #posizione della playlist nel menu
start_posizione_eliminazione = 2

#Configurazione browser
driver = configurazione_browser()

#Login
Accesso_spotify(driver, email, password)

#Eliminazione brani
scegli_playlist(driver,playlist_scelta)
count = 0
for count in range(brani_da_eliminare):
    elimina_brano(driver, start_posizione_eliminazione)

#Inserimento brani
count = 0
for count in range(brani_da_aggiungere):
    count = count + 1
    posizione = count
    aggiungi_brano(driver, posizione, playlist_target,posizione_playlist)


