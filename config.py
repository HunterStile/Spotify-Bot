import random

# Scegli se eseguere una nuova creazione con True, accessi ad account gia creati scritti in account_spotify.csv con False 
CREAZIONE = True
#scegliere True per usare proxy, False senza.
PROXY = False
DOPPIOPROXY = False
#scegliere se abilitare la routine di seguire le playlist
SEGUI_PLAYLIST = True
#scegliere se ablitare la routine di ascoltare canzoni
ASCOLTA_CANZONI = True
#scegliere i profili proxy da ruotare.
PROXYLIST = [
    'profilo1.ppx',
    'profilo2.ppx'
]
#SCELTA DELLA PLAYLIST DOVE ASCOLTARE LE CANZONI
PLAYLIST_SCELTA = [
    'https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC',
    'https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R',   # New Generation
    'https://open.spotify.com/playlist/110gM33fjQUsNASKxTG4LV'  # Pop-Punk
]
POSIZIONI_SCELTE = ['1','4']
MIN_POSIZIONI = 1
MAX_POSIZIONI = 1
MIN_RIPETIZIONI = 1
MAX_RIPETIZIONI = 1

# SCELTA DELLE PLAYLIST
PLAYLIST_URLS = [
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

configurazione_bot = {
    # Impostazioni generali
    'crea_account': CREAZIONE,
    'max_iterazioni': 100,
    'input_utente': False,
    'ripetizione': True,

    # Configurazione Proxy
    'usa_proxy': PROXY,  # Abilita/disabilita l'uso dei proxy
    'proxy_list': PROXYLIST,
    'proxy_list_first': PROXYLIST,

    # Configurazione playlist da seguire
    'segui_playlist': SEGUI_PLAYLIST,
    'playlist_urls': PLAYLIST_URLS,
    
    # Configurazione ascolto canzoni
    'ascolta_canzoni': ASCOLTA_CANZONI,
    'playlist_ascolto': random.choice(PLAYLIST_SCELTA),
    # Posizioni e ripetizioni di ascolto casuali
    'posizioni_ascolto': random.sample(POSIZIONI_SCELTE, k=random.randint(MIN_POSIZIONI, MAX_POSIZIONI)),
    'ripetizioni_per_posizione': {
        posizione: random.randint(MIN_RIPETIZIONI, MAX_RIPETIZIONI) 
        for posizione in random.sample(POSIZIONI_SCELTE, k=random.randint(MIN_POSIZIONI, MAX_POSIZIONI))
    },
    
}