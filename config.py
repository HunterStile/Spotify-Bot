import random

POSIZIONI_DISPONIBILI = ['1', '2', '3', '4','5']
MIN_POSIZIONI = 1
MAX_POSIZIONI = 3
MIN_RIPETIZIONI = 1
MAX_RIPETIZIONI = 1


configurazione_bot = {
    # Impostazioni generali
    'crea_account': True,
    'max_iterazioni': 3,
    'input_utente': False,
    'ripetizione': True,

    # Configurazione Proxy
    'usa_proxy': False,  # Abilita/disabilita l'uso dei proxy
    'proxy_list': [
        'profilo1.ppx',
        'profilo2.ppx'
    ],
    
    # Configurazione playlist da seguire
    'segui_playlist': True,
    'playlist_urls': [
        'https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC',   # Pop-Punk
        'https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry',   # Trap Italia
        'https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R',   # New Generation
        'https://open.spotify.com/playlist/110gM33fjQUsNASKxTG4LV',   # New Music
        'https://open.spotify.com/playlist/2EAacye5AQOZu9WN8Z5k4X',   # Top Music
        'https://open.spotify.com/playlist/52DGNZbiGch7ewRJOmVuLS',    # Indie Italia
        'https://open.spotify.com/playlist/77EE22OcfpL3fL7wDkagpX',
        'https://open.spotify.com/playlist/6ke0AGVivZiVVUkqSHWTAQ',
        'https://open.spotify.com/playlist/1CZFCCGYLzYh1BpxAXHy4b',
        'https://open.spotify.com/playlist/1Hgl2BCI250xGtyGFXuJpB',
        'https://open.spotify.com/playlist/3F82VLnmyuQ0ujPQPnxdRy'      
    ],
    
    # Configurazione ascolto canzoni
    'ascolta_canzoni': True,
    'playlist_ascolto': random.choice([
        'https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC',   
        'https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry',   
        'https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R',   
        'https://open.spotify.com/playlist/110gM33fjQUsNASKxTG4LV',   
        'https://open.spotify.com/playlist/2EAacye5AQOZu9WN8Z5k4X',   
        'https://open.spotify.com/playlist/52DGNZbiGch7ewRJOmVuLS'
    ]),
    
    # Posizioni e ripetizioni di ascolto casuali
    'posizioni_ascolto': random.sample(POSIZIONI_DISPONIBILI, k=random.randint(MIN_POSIZIONI, MAX_POSIZIONI)),
    'ripetizioni_per_posizione': {
        posizione: random.randint(MIN_RIPETIZIONI, MAX_RIPETIZIONI) 
        for posizione in random.sample(POSIZIONI_DISPONIBILI, k=random.randint(MIN_POSIZIONI, MAX_POSIZIONI))
    },
    
    # Intervallo tra gli ascolti
     'intervallo_ascolto': random.randint(120, 150)
}