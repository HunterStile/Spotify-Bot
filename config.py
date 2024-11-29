# Lista dei profili proxy su proxifier disponibili
proxy_list = [
    'dinamico.ppx'
]

#playlist
playlist1='https://open.spotify.com/playlist/1TmUjkWHXsKgTsIKvJiCJC'  #pop-punk 
playlist2='https://open.spotify.com/playlist/1qEvrxdkHTJdrtxHlG80Ry'  #trap-italia
playlist3='https://open.spotify.com/playlist/55aJEEvbqcQNF2MRQncP5R'  #new-generation
playlist4='https://open.spotify.com/playlist/110gM33fjQUsNASKxTG4LV'  #new-music
playlist5='https://open.spotify.com/playlist/2EAacye5AQOZu9WN8Z5k4X'  #top-music
playlist6='https://open.spotify.com/playlist/52DGNZbiGch7ewRJOmVuLS'  #Indieitalia

# Esempio di configurazione nel file config.py
configurazione_bot = {
    # Impostazioni generali
    'crea_account': True,
    'max_iterazioni': 3,
    'input_utente': False,
    'ripetizione': True,

    # Configurazione Proxy
    'usa_proxy': True,  # Abilita/disabilita l'uso dei proxy
    'proxy_list': [
        'profilo1.ppx'
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
        'https://open.spotify.com/playlist/52DGNZbiGch7ewRJOmVuLS'    # Indie Italia
    ],
    
    # Configurazione ascolto canzoni
    'ascolta_canzoni': False,
    'playlist_ascolto': 'https://open.spotify.com/playlist/110gM33fjQUsNASKxTG4LV',  # New Music
    
    # Posizioni e ripetizioni di ascolto
    'posizioni_ascolto': ['6', '3', '1'],  # Liste delle posizioni da ascoltare
    'ripetizioni_per_posizione': {
        '6': 2,  # Ascolta 2 volte la posizione 6
        '3': 1,  # Ascolta 1 volta la posizione 3
        '1': 3   # Ascolta 3 volte la posizione 1
    },
    
    # Intervallo tra gli ascolti
    'intervallo_ascolto': 120  # Secondi tra un ascolto e l'altro
}