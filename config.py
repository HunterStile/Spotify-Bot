import random

# Scegli se eseguere una nuova creazione con True, accessi ad account gia creati scritti in account_spotify.csv con False 
CREAZIONE = True
#scegliere True per usare proxy, False senza.
PROXY = False
DOPPIOPROXY = False
#Gestione richiesta robot
STOP_FOR_ROBOT = True
TEMPO_RIPARTENZA = 7200
#Gestione del reset
RESET_ROUTER = False
TIPO_ROUTER = 'tim'
#scegliere se abilitare la routine di seguire le playlist
SEGUI_PLAYLIST = True
#scegliere se ablitare la routine di ascoltare canzoni
ASCOLTA_CANZONI = True

MAX_ITERAZIONE = 100
#scegliere i profili proxy da ruotare.
PROXYLIST = [
    'profilo1.ppx',
    'profilo2.ppx'
]

# SCELTA DELLE PLAYLIST
PLAYLIST_FOLLOW = [
    'https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC',   # Pop-Punk
    'https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry',   # Trap Italia
    'https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R',   # New Generation
    'https://open.spotify.com/playlist/110gM33fjQUsNASKxTG4LV',   # New Music
    'https://open.spotify.com/playlist/2EAacye5AQOZu9WN8Z5k4X',   # Top Music
    'https://open.spotify.com/playlist/52DGNZbiGch7ewRJOmVuLS',   # Indie Italia
    'https://open.spotify.com/playlist/77EE22OcfpL3fL7wDkagpX',
    'https://open.spotify.com/playlist/6ke0AGVivZiVVUkqSHWTAQ',
    'https://open.spotify.com/playlist/1CZFCCGYLzYh1BpxAXHy4b',
    'https://open.spotify.com/playlist/1Hgl2BCI250xGtyGFXuJpB',
    'https://open.spotify.com/playlist/3F82VLnmyuQ0ujPQPnxdRy'
]


#SCELTA DELLA PLAYLIST DOVE ASCOLTARE LE CANZONI
# Playlist con configurazioni specifiche
PLAYLIST_URLS = [
    'https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC;1,3,5',   # Pop-Punk con posizioni specifiche
    'https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry',         # Trap Italia (casuale)
    'https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R;2,4,6',   # New Generation con posizioni
    'https://open.spotify.com/playlist/2EAacye5AQOZu9WN8Z5k4X',         # Top Music (casuale) 
    'https://open.spotify.com/playlist/52DGNZbiGch7ewRJOmVuLS;7,9,11'   # Indie Italia con posizioni
]

MODALITA_POSIZIONI = 'random'  # Valori possibili: 'random' o 'statico'


#Altri
RIPETIZIONE = True
INPUT_UTENTE = False

configurazione_bot = {
    # Impostazioni generali
    'crea_account': CREAZIONE,
    'max_iterazioni': MAX_ITERAZIONE,
    'input_utente': INPUT_UTENTE,
    'ripetizione': RIPETIZIONE,

    # Configurazione Proxy
    'usa_proxy': PROXY,  # Abilita/disabilita l'uso dei proxy
    'proxy_list': PROXYLIST,
    'proxy_list_first': PROXYLIST,

    # Configurazione playlist da seguire
    'segui_playlist': SEGUI_PLAYLIST,
    'playlist_urls': PLAYLIST_URLS,
    'playlist_follow': PLAYLIST_FOLLOW,
    
    # Nuovo flag per la modalità di selezione delle posizioni
    'modalita_posizioni': MODALITA_POSIZIONI,
    
    # Configurazione ascolto canzoni
    'ascolta_canzoni': ASCOLTA_CANZONI,
}