import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import threading
import sys
import os
import json
import importlib.util
import ctypes
import time
from time import sleep
import queue
import concurrent.futures

# Funzione per gestire i percorsi in PyInstaller
def get_resource_path(relative_path):
    """Ottiene il percorso assoluto per i file risorsa, funziona sia in dev che in exe"""
    try:
        # PyInstaller crea una cartella temporanea e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Percorso normale quando non è in un eseguibile
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Import the existing bot configuration and execution function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Carica config.py usando il percorso corretto
config_path = get_resource_path("config.py")
spec = importlib.util.spec_from_file_location("config", config_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)

# Aggiungi il percorso base al sys.path per gli import
sys.path.insert(0, get_resource_path('.'))

from Main import *
from config import *

class SpotifyBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Spotify Bot Control Panel")
        master.geometry("900x700")
        
        # Define colors
        self.bg_color = "#121212"  # Spotify dark background
        self.accent_color = "#1DB954"  # Spotify green
        self.text_color = "#FFFFFF"  # White text
        self.secondary_bg = "#212121"  # Slightly lighter background for contrast
        self.disabled_color = "#535353"  # Gray for disabled elements
        
        # Configure the style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure colors
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabelframe', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TCheckbutton', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TRadiobutton', background=self.bg_color, foreground=self.text_color)
        
        # Configure the button style
        self.style.configure('TButton', background=self.accent_color, foreground=self.text_color)
        self.style.map('TButton', 
                  background=[('active', self.accent_color), ('disabled', self.disabled_color)],
                  foreground=[('disabled', self.text_color)])

        # Make the root window use our background color
        master.configure(bg=self.bg_color)
        
        # Config file path
        self.config_file = "gui_config.json"
          # Initialize variables with None first
        self.crea_account_var = None
        self.proxy_var = None
        self.doppio_proxy_var = None
        self.segui_playlist_var = None
        self.ascolta_canzoni_var = None
        self.max_iterazioni_var = None
        self.modalita_posizioni_var = None
        self.proxy_list_var = None
        self.proxy_list_first_var = None
        self.playlist_urls_var = None
        self.playlist_follow_var = None
        self.stop_for_robot_var = None
        self.tempo_ripartenza_var = None
        self.reset_router_var = None
        self.tipo_router_var = None
        self.reset_mac_var = None
        self.disable_stealth_var = None
        self.secondo_schermo_var = None
        
        # Variabili per multithreading
        self.concurrent_bots_var = None
        self.max_chrome_var = None
        
        # Load saved configuration or use defaults
        self.load_config()
        
        # Bot Thread
        self.bot_threads = []
        self.stop_event = threading.Event()
        self.thread_pool = None
        self.chrome_semaphore = None

        # Create main frame
        self.main_frame = ttk.Frame(master, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top bar with logo/title
        self.create_header()
        
        # Create the actual UI widgets
        self.create_widgets()
        
    def create_header(self):
        # Header frame
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title label with custom font
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title = tk.Label(header_frame, text="Spotify Bot Controller", 
                         font=title_font, bg=self.bg_color, fg=self.accent_color)
        title.pack(side=tk.LEFT)
        
        # Add a small Spotify-like icon or separator here if desired
        
        # Version info
        version_label = tk.Label(header_frame, text="v1.2.1", 
                               bg=self.bg_color, fg=self.text_color)
        version_label.pack(side=tk.RIGHT)

    def create_widgets(self):
        # Create two columns
        left_column = ttk.Frame(self.main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_column = ttk.Frame(self.main_frame)
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # LEFT COLUMN COMPONENTS
        
        # Main Configuration Frame
        config_frame = ttk.LabelFrame(left_column, text="Configurazione Principale", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 10))
          # Use a grid layout for better alignment
        ttk.Checkbutton(config_frame, text="Crea Nuovo Account", variable=self.crea_account_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Usa Proxy", variable=self.proxy_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Usa Doppio Proxy", variable=self.doppio_proxy_var).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Segui Playlist", variable=self.segui_playlist_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Ascolta Canzoni", variable=self.ascolta_canzoni_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Disabilita Stealth", variable=self.disable_stealth_var).grid(row=2, column=1, sticky=tk.W, pady=2)
        ttk.Checkbutton(config_frame, text="Usa Secondo Schermo", variable=self.secondo_schermo_var).grid(row=3, column=1, sticky=tk.W, pady=2)
          # Max Iterations
        iter_frame = ttk.Frame(config_frame)
        iter_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Label(iter_frame, text="Iterazioni Max:").pack(side=tk.LEFT)
        ttk.Entry(iter_frame, textvariable=self.max_iterazioni_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Multithreading Configuration Frame
        multithreading_frame = ttk.LabelFrame(left_column, text="Configurazione Multithreading", padding=10)
        multithreading_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Bot instances control
        bot_instances_frame = ttk.Frame(multithreading_frame)
        bot_instances_frame.pack(fill=tk.X, pady=3)
        ttk.Label(bot_instances_frame, text="Numero di Bot Simultanei:").pack(side=tk.LEFT)
        ttk.Spinbox(bot_instances_frame, from_=1, to=10, textvariable=self.concurrent_bots_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Chrome instances control
        chrome_instances_frame = ttk.Frame(multithreading_frame)
        chrome_instances_frame.pack(fill=tk.X, pady=3)
        ttk.Label(chrome_instances_frame, text="Numero Max di Chrome:").pack(side=tk.LEFT)
        ttk.Spinbox(chrome_instances_frame, from_=1, to=10, textvariable=self.max_chrome_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Info about multithreading
        info_label = tk.Label(multithreading_frame, 
                               text="Nota: Il numero di Chrome attivi contemporaneamente non può superare\n"
                                    "il numero di Bot. Se hai problemi di memoria, riduci questi valori.", 
                               bg=self.bg_color, fg="#FFA500", justify=tk.LEFT)
        info_label.pack(anchor='w', pady=(5, 0))
        
        # Position Mode Frame
        position_frame = ttk.LabelFrame(left_column, text="Modalità Posizioni", padding=10)
        position_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Radio buttons for position mode
        ttk.Radiobutton(position_frame, text="Casuale", variable=self.modalita_posizioni_var, value='random').pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(position_frame, text="Statico", variable=self.modalita_posizioni_var, value='statico').pack(side=tk.LEFT, padx=10)
        
        # Robot Detection Frame
        robot_frame = ttk.LabelFrame(left_column, text="Rilevamento Robot", padding=10)
        robot_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(robot_frame, text="Ferma per Rilevamento Robot", variable=self.stop_for_robot_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(robot_frame, text="Tempo di Ripartenza (sec):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(robot_frame, textvariable=self.tempo_ripartenza_var, width=8).grid(row=1, column=1, sticky=tk.W, pady=2)
          # Router Reset Frame
        router_frame = ttk.LabelFrame(left_column, text="Reset Router", padding=10)
        router_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(router_frame, text="Reset Router", variable=self.reset_router_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(router_frame, text="Reset MAC", variable=self.reset_mac_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(router_frame, text="Tipo Router:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(router_frame, text="TIM", variable=self.tipo_router_var, value='tim').grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(router_frame, text="Vodafone", variable=self.tipo_router_var, value='vodafone').grid(row=1, column=2, sticky=tk.W, pady=2)
        
        # RIGHT COLUMN COMPONENTS
        
        # Playlist Configuration
        playlist_frame = ttk.LabelFrame(right_column, text="Configurazione Playlist", padding=10)
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Playlist URLs for listening
        ttk.Label(playlist_frame, text="Playlist da Ascoltare (formato: url;pos1,pos2,pos3)").pack(anchor='w', pady=(0, 2))
        playlist_urls_text = tk.Text(playlist_frame, height=6, bg=self.secondary_bg, fg=self.text_color)
        playlist_urls_text.insert(tk.END, self.playlist_urls_var.get())
        playlist_urls_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        playlist_urls_text.bind('<KeyRelease>', lambda e: self.playlist_urls_var.set(playlist_urls_text.get("1.0", tk.END).strip()))
        
        # Playlist URLs for following
        ttk.Label(playlist_frame, text="Playlist da Seguire (una per riga)").pack(anchor='w', pady=(0, 2))
        playlist_follow_text = tk.Text(playlist_frame, height=6, bg=self.secondary_bg, fg=self.text_color)
        playlist_follow_text.insert(tk.END, self.playlist_follow_var.get())
        playlist_follow_text.pack(fill=tk.BOTH, expand=True)
        playlist_follow_text.bind('<KeyRelease>', lambda e: self.playlist_follow_var.set(playlist_follow_text.get("1.0", tk.END).strip()))
        
        # Proxy Lists
        proxy_frame = ttk.LabelFrame(right_column, text="Liste Proxy", padding=10)
        proxy_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Main Proxy List
        ttk.Label(proxy_frame, text="Lista Proxy Principale (una per riga)").pack(anchor='w', pady=(0, 2))
        proxy_text = tk.Text(proxy_frame, height=5, bg=self.secondary_bg, fg=self.text_color)
        proxy_text.insert(tk.END, self.proxy_list_var.get())
        proxy_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        proxy_text.bind('<KeyRelease>', lambda e: self.proxy_list_var.set(proxy_text.get("1.0", tk.END).strip()))
        
        # First Proxy List
        ttk.Label(proxy_frame, text="Lista Proxy Primaria (usata con Doppio Proxy)").pack(anchor='w', pady=(0, 2))
        proxy_first_text = tk.Text(proxy_frame, height=5, bg=self.secondary_bg, fg=self.text_color)
        proxy_first_text.insert(tk.END, self.proxy_list_first_var.get())
        proxy_first_text.pack(fill=tk.BOTH, expand=True)
        proxy_first_text.bind('<KeyRelease>', lambda e: self.proxy_list_first_var.set(proxy_first_text.get("1.0", tk.END).strip()))
        
        # Update proxy text states based on checkbox
        def update_proxy_states(*args):
            proxy_enabled = self.proxy_var.get()
            double_proxy_enabled = self.doppio_proxy_var.get()
            
            proxy_text['state'] = 'normal' if proxy_enabled else 'disabled'
            proxy_first_text['state'] = 'normal' if proxy_enabled and double_proxy_enabled else 'disabled'
        
        # Bind the update function to the checkboxes
        self.proxy_var.trace('w', update_proxy_states)
        self.doppio_proxy_var.trace('w', update_proxy_states)
        
        # Control Buttons and Console Output
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        # Buttons Frame with more space
        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Avvia Bot", command=self.start_bot, width=15)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(button_frame, text="Ferma Bot", command=self.stop_bot, width=15, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        save_button = ttk.Button(button_frame, text="Salva Configurazione", command=self.save_config, width=20)
        save_button.pack(side=tk.LEFT, padx=10)
        
        # Pulsante per aggiornare ChromeDriver
        update_driver_button = ttk.Button(button_frame, text="Aggiorna ChromeDriver", command=self.update_chromedriver, width=18)
        update_driver_button.pack(side=tk.LEFT, padx=10)
        
        # Console Output
        console_frame = ttk.LabelFrame(self.main_frame, text="Console Output", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.console_text = tk.Text(console_frame, height=10, bg=self.secondary_bg, fg=self.text_color, state='disabled')
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to console
        scrollbar = ttk.Scrollbar(self.console_text, command=self.console_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console_text.config(yscrollcommand=scrollbar.set)
        
        # Initial state update
        update_proxy_states()

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                
                # Bot Configuration Variables with saved values or defaults
                self.crea_account_var = tk.BooleanVar(value=saved_config.get('crea_account', config_module.CREAZIONE))
                self.proxy_var = tk.BooleanVar(value=saved_config.get('usa_proxy', config_module.PROXY))
                self.doppio_proxy_var = tk.BooleanVar(value=saved_config.get('doppio_proxy', config_module.DOPPIOPROXY))
                self.segui_playlist_var = tk.BooleanVar(value=saved_config.get('segui_playlist', config_module.SEGUI_PLAYLIST))
                self.ascolta_canzoni_var = tk.BooleanVar(value=saved_config.get('ascolta_canzoni', config_module.ASCOLTA_CANZONI))
                self.stop_for_robot_var = tk.BooleanVar(value=saved_config.get('stop_for_robot', config_module.STOP_FOR_ROBOT))
                self.reset_router_var = tk.BooleanVar(value=saved_config.get('reset_router', config_module.RESET_ROUTER))
                self.reset_mac_var = tk.BooleanVar(value=saved_config.get('reset_mac', config_module.RESET_MAC))
                self.disable_stealth_var = tk.BooleanVar(value=saved_config.get('disable_stealth', config_module.DISABLE_STEALTH))
                self.secondo_schermo_var = tk.BooleanVar(value=saved_config.get('secondo_schermo', False))
                
                self.max_iterazioni_var = tk.IntVar(value=saved_config.get('max_iterazioni', config_module.MAX_ITERAZIONE))
                self.tempo_ripartenza_var = tk.IntVar(value=saved_config.get('tempo_ripartenza', config_module.TEMPO_RIPARTENZA))
                
                self.modalita_posizioni_var = tk.StringVar(value=saved_config.get('modalita_posizioni', config_module.MODALITA_POSIZIONI))
                self.tipo_router_var = tk.StringVar(value=saved_config.get('tipo_router', config_module.TIPO_ROUTER))
                
                # Handle lists properly
                proxy_list = saved_config.get('proxy_list', config_module.PROXYLIST)
                proxy_list_first = saved_config.get('proxy_list_first', config_module.PROXYLIST)
                playlist_urls = saved_config.get('playlist_urls', config_module.PLAYLIST_URLS)
                playlist_follow = saved_config.get('playlist_follow', config_module.PLAYLIST_FOLLOW)
                
                # Filter out empty strings from lists
                proxy_list = [x for x in proxy_list if x.strip()]
                proxy_list_first = [x for x in proxy_list_first if x.strip()]
                playlist_urls = [x for x in playlist_urls if x.strip()]
                playlist_follow = [x for x in playlist_follow if x.strip()]
                
                self.proxy_list_var = tk.StringVar(value='\n'.join(proxy_list))
                self.proxy_list_first_var = tk.StringVar(value='\n'.join(proxy_list_first))
                self.playlist_urls_var = tk.StringVar(value='\n'.join(playlist_urls))
                self.playlist_follow_var = tk.StringVar(value='\n'.join(playlist_follow))
                
                # Variabili per multithreading
                self.concurrent_bots_var = tk.IntVar(value=saved_config.get('concurrent_bots', 1))
                self.max_chrome_var = tk.IntVar(value=saved_config.get('max_chrome', 1))
                
                print("Configurazione caricata con successo da", self.config_file)
            else:
                print("Nessuna configurazione salvata trovata, utilizzando valori predefiniti")
                # Use defaults from config module
                self.crea_account_var = tk.BooleanVar(value=config_module.CREAZIONE)
                self.proxy_var = tk.BooleanVar(value=config_module.PROXY)
                self.doppio_proxy_var = tk.BooleanVar(value=config_module.DOPPIOPROXY)
                self.segui_playlist_var = tk.BooleanVar(value=config_module.SEGUI_PLAYLIST)
                self.ascolta_canzoni_var = tk.BooleanVar(value=config_module.ASCOLTA_CANZONI)
                self.stop_for_robot_var = tk.BooleanVar(value=config_module.STOP_FOR_ROBOT)
                self.reset_router_var = tk.BooleanVar(value=config_module.RESET_ROUTER)
                self.disable_stealth_var = tk.BooleanVar(value=config_module.DISABLE_STEALTH)
                
                self.max_iterazioni_var = tk.IntVar(value=config_module.MAX_ITERAZIONE)
                self.tempo_ripartenza_var = tk.IntVar(value=config_module.TEMPO_RIPARTENZA)
                
                self.modalita_posizioni_var = tk.StringVar(value=config_module.MODALITA_POSIZIONI)
                self.tipo_router_var = tk.StringVar(value=config_module.TIPO_ROUTER)
                
                self.proxy_list_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
                self.proxy_list_first_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
                self.playlist_urls_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_URLS))
                self.playlist_follow_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_FOLLOW))
                
                # Variabili per multithreading
                self.concurrent_bots_var = tk.IntVar(value=1)
                self.max_chrome_var = tk.IntVar(value=1)
                
        except Exception as e:
            print(f"Errore durante il caricamento della configurazione: {str(e)}")
            messagebox.showerror("Errore Configurazione", f"Errore durante il caricamento della configurazione: {str(e)}")
            # Use defaults if there's an error
            self.crea_account_var = tk.BooleanVar(value=config_module.CREAZIONE)
            self.proxy_var = tk.BooleanVar(value=config_module.PROXY)
            self.doppio_proxy_var = tk.BooleanVar(value=config_module.DOPPIOPROXY)
            self.segui_playlist_var = tk.BooleanVar(value=config_module.SEGUI_PLAYLIST)
            self.ascolta_canzoni_var = tk.BooleanVar(value=config_module.ASCOLTA_CANZONI)
            self.stop_for_robot_var = tk.BooleanVar(value=config_module.STOP_FOR_ROBOT)
            self.reset_router_var = tk.BooleanVar(value=config_module.RESET_ROUTER)
            self.reset_mac_var = tk.BooleanVar(value=config_module.RESET_MAC)
            self.disable_stealth_var = tk.BooleanVar(value=config_module.DISABLE_STEALTH)
            self.secondo_schermo_var = tk.BooleanVar(value=False)
            
            self.max_iterazioni_var = tk.IntVar(value=config_module.MAX_ITERAZIONE)
            self.tempo_ripartenza_var = tk.IntVar(value=config_module.TEMPO_RIPARTENZA)
            
            self.modalita_posizioni_var = tk.StringVar(value=config_module.MODALITA_POSIZIONI)
            self.tipo_router_var = tk.StringVar(value=config_module.TIPO_ROUTER)
            
            self.proxy_list_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
            self.proxy_list_first_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
            self.playlist_urls_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_URLS))
            self.playlist_follow_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_FOLLOW))
            
            # Variabili per multithreading
            self.concurrent_bots_var = tk.IntVar(value=1)
            self.max_chrome_var = tk.IntVar(value=1)
    
    def save_config(self):
        config_data = {
            'crea_account': self.crea_account_var.get(),
            'usa_proxy': self.proxy_var.get(),
            'doppio_proxy': self.doppio_proxy_var.get(),
            'segui_playlist': self.segui_playlist_var.get(),
            'ascolta_canzoni': self.ascolta_canzoni_var.get(),            'stop_for_robot': self.stop_for_robot_var.get(),            'reset_router': self.reset_router_var.get(),
            'reset_mac': self.reset_mac_var.get(),
            'disable_stealth': self.disable_stealth_var.get(),
            'secondo_schermo': self.secondo_schermo_var.get(),
            'max_iterazioni': self.max_iterazioni_var.get(),
            'tempo_ripartenza': self.tempo_ripartenza_var.get(),
            'modalita_posizioni': self.modalita_posizioni_var.get(),
            'tipo_router': self.tipo_router_var.get(),
            'proxy_list': [x for x in self.proxy_list_var.get().split('\n') if x.strip()],
            'proxy_list_first': [x for x in self.proxy_list_first_var.get().split('\n') if x.strip()],
            'playlist_urls': [x for x in self.playlist_urls_var.get().split('\n') if x.strip()],
            'playlist_follow': [x for x in self.playlist_follow_var.get().split('\n') if x.strip()],
            'concurrent_bots': self.concurrent_bots_var.get(),
            'max_chrome': self.max_chrome_var.get()
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            # Display a success message in the console
            self.log_to_console("Configurazione salvata con successo.")
        except Exception as e:
            messagebox.showerror("Errore di Salvataggio", f"Errore durante il salvataggio della configurazione: {str(e)}")
    
    def log_to_console(self, message):
        """Add a message to the console widget"""
        self.console_text.configure(state='normal')
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)
        self.console_text.configure(state='disabled')

    def update_chromedriver(self):
        """Aggiorna ChromeDriver alla versione più recente"""
        try:
            # Importa le funzioni necessarie
            from funzioni.spotify_functions import aggiorna_chromedriver, get_chrome_version
            
            # Mostra messaggio di inizio
            self.log_to_console("Controllo della versione di Chrome installata...")
            
            # Controlla la versione di Chrome
            chrome_version = get_chrome_version()
            if chrome_version:
                self.log_to_console(f"Chrome versione rilevata: {chrome_version}")
            else:
                self.log_to_console("Impossibile rilevare la versione di Chrome, procedo comunque...")
            
            # Avvia aggiornamento in un thread separato per non bloccare la GUI
            def update_in_thread():
                try:
                    self.log_to_console("Avvio aggiornamento ChromeDriver...")
                    success = aggiorna_chromedriver()
                    
                    if success:
                        self.log_to_console("✓ ChromeDriver aggiornato con successo!")
                        messagebox.showinfo("Aggiornamento Completato", 
                                          "ChromeDriver è stato aggiornato alla versione più recente.")
                    else:
                        self.log_to_console("✗ Errore durante l'aggiornamento di ChromeDriver.")
                        messagebox.showerror("Errore Aggiornamento", 
                                           "Si è verificato un errore durante l'aggiornamento di ChromeDriver.")
                except Exception as e:
                    error_msg = f"Errore durante l'aggiornamento: {str(e)}"
                    self.log_to_console(f"✗ {error_msg}")
                    messagebox.showerror("Errore", error_msg)
            
            # Esegui l'aggiornamento in un thread separato
            update_thread = threading.Thread(target=update_in_thread, daemon=True)
            update_thread.start()
            
        except ImportError as e:
            error_msg = f"Errore nell'importazione delle funzioni: {str(e)}"
            self.log_to_console(error_msg)
            messagebox.showerror("Errore", error_msg)
        except Exception as e:
            error_msg = f"Errore inaspettato: {str(e)}"
            self.log_to_console(error_msg)
            messagebox.showerror("Errore", error_msg)
    
    def start_bot(self):
        # Save configuration before starting the bot
        self.save_config()
        
        # Clean up any existing processes BEFORE starting new ones
        self.log_to_console("Pulizia dell'ambiente di esecuzione...")
        self.terminate_selenium_drivers()
        
        # Short delay to ensure processes are fully terminated
        self.log_to_console("Attendere mentre si preparano le risorse...")
        self.master.update()  # Update the GUI to show the message
        sleep(1.5)  # Wait a bit to ensure all processes are terminated
        
        # Clear the console
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')
        
        # Get multithreading settings
        concurrent_bots = self.concurrent_bots_var.get()
        max_chrome = min(self.max_chrome_var.get(), concurrent_bots)
        
        self.log_to_console(f"Avvio di {concurrent_bots} bot(s) con massimo {max_chrome} istanze Chrome simultanee...")
        
        # Prepare configuration dictionary
        configurazione_bot_base = {
            'crea_account': self.crea_account_var.get(),
            'max_iterazioni': self.max_iterazioni_var.get(),
            'input_utente': INPUT_UTENTE,
            'ripetizione': RIPETIZIONE,
            
            'usa_proxy': self.proxy_var.get(),
            'proxy_list': [x.strip() for x in self.proxy_list_var.get().split('\n') if x.strip()],
            'proxy_list_first': [x.strip() for x in self.proxy_list_first_var.get().split('\n') if x.strip()],
            
            'doppio_proxy': self.doppio_proxy_var.get(),
            'stop_for_robot': self.stop_for_robot_var.get(),
            'tempo_ripartenza': self.tempo_ripartenza_var.get(),            'reset_router': self.reset_router_var.get(),
            'reset_mac': self.reset_mac_var.get(),
            'tipo_router': self.tipo_router_var.get(),
            
            'segui_playlist': self.segui_playlist_var.get(),
            'playlist_urls': [x.strip() for x in self.playlist_urls_var.get().split('\n') if x.strip()],
            'playlist_follow': [x.strip() for x in self.playlist_follow_var.get().split('\n') if x.strip()],
            
            'modalita_posizioni': self.modalita_posizioni_var.get(),            'ascolta_canzoni': self.ascolta_canzoni_var.get(),
            'clean_start': True,  # Flag to indicate a clean start
            'disable_stealth': self.disable_stealth_var.get(),
            'secondo_schermo': self.secondo_schermo_var.get()
        }
        
        # Validazione delle configurazioni
        if configurazione_bot_base['usa_proxy'] and configurazione_bot_base['doppio_proxy']:
            if not configurazione_bot_base['proxy_list_first']:
                messagebox.showwarning("Configurazione Incompleta", 
                    "Hai attivato il doppio proxy ma la lista proxy primaria è vuota!")
                return
        
        if configurazione_bot_base['usa_proxy'] and not configurazione_bot_base['proxy_list']:
            messagebox.showwarning("Configurazione Incompleta", 
                "Hai attivato l'uso dei proxy ma la lista proxy è vuota!")
            return
        
        if configurazione_bot_base['segui_playlist'] and not configurazione_bot_base['playlist_follow']:
            messagebox.showwarning("Configurazione Incompleta", 
                "Hai attivato il seguire playlist ma non hai specificato playlist da seguire!")
            return
        
        if configurazione_bot_base['ascolta_canzoni'] and not configurazione_bot_base['playlist_urls']:
            messagebox.showwarning("Configurazione Incompleta", 
                "Hai attivato l'ascolto delle canzoni ma non hai specificato playlist da ascoltare!")
            return
        
        # Crea un evento di stop condiviso e semaforo per limitare le istanze Chrome
        self.stop_event.clear()
        self.chrome_semaphore = threading.Semaphore(max_chrome)
        
        # Inizializza il thread pool
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_bots)
        self.bot_threads = []
        
        # Avvia i bot in thread separati
        for i in range(concurrent_bots):
            # Copia di configurazione per ciascun bot
            configurazione_bot = configurazione_bot_base.copy()
            
            # Aggiungi identificatore univoco e riferimenti necessari al thread
            configurazione_bot['bot_id'] = i + 1
            configurazione_bot['stop_event'] = self.stop_event
            configurazione_bot['chrome_semaphore'] = self.chrome_semaphore
            configurazione_bot['gui_instance'] = self
            
            # Distribuisci le playlist tra i bot se sono in modalità statica
            if configurazione_bot['modalita_posizioni'] == 'statico' and i > 0:
                # Rotazione dell'elenco playlist per una migliore distribuzione
                shuffled_urls = configurazione_bot['playlist_urls'].copy()
                random.shuffle(shuffled_urls)
                configurazione_bot['playlist_urls'] = shuffled_urls
            
            # Avvia il thread del bot
            self.log_to_console(f"Inizializzazione Bot #{i+1}...")
            bot_thread = self.thread_pool.submit(self.run_bot, configurazione_bot)
            self.bot_threads.append(bot_thread)
            
            # Breve pausa tra l'avvio di ciascun bot per evitare conflitti
            sleep(0.5)
        
        # Update Button States
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
    
    def run_bot(self, configurazione_bot):
        try:
            # Ottieni l'ID del bot per i messaggi di log
            bot_id = configurazione_bot.get('bot_id', 0)
            
            # Reindirizza stdout a console text widget con prefisso bot_id
            class BotTextRedirector:
                def __init__(self, widget, bot_id=None, tag="stdout"):
                    self.widget = widget
                    self.tag = tag
                    self.bot_id = bot_id
                
                def write(self, str):
                    if str.strip():  # Evita linee vuote
                        # Aggiungi prefisso solo se il messaggio non è vuoto
                        prefix = f"[Bot #{self.bot_id}] " if self.bot_id else ""
                        self.widget.configure(state='normal')
                        self.widget.insert(tk.END, prefix + str)
                        self.widget.see(tk.END)
                        self.widget.configure(state='disabled')
                
                def flush(self):
                    pass
            
            # Crea un oggetto redirezione specifico per questo bot
            bot_stdout = BotTextRedirector(self.console_text, bot_id)
            
            # Acquisisci il semaforo per Chrome prima di eseguire il bot
            chrome_semaphore = configurazione_bot.get('chrome_semaphore')
            if chrome_semaphore:
                bot_stdout.write(f"In attesa di una posizione disponibile nel pool Chrome ({self.max_chrome_var.get()} max)...\n")
                chrome_semaphore.acquire()
                bot_stdout.write("Posizione Chrome acquisita, avvio del bot!\n")
            
            try:
                # Reindirizza temporaneamente l'output
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = bot_stdout
                sys.stderr = bot_stdout
                
                # Esegui il bot con la configurazione specifica
                esegui_bot_spotify(configurazione_bot)
            
            finally:
                # Ripristina stdout e rilascia il semaforo
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                if chrome_semaphore:
                    chrome_semaphore.release()
                    # Messaggio di rilascio del semaforo (usando la versione salvata di stdout)
                    bot_stdout.write("Istanza Chrome rilasciata, ora disponibile per altri bot.\n")
        
        except Exception as e:
            error_msg = f"Errore Bot #{bot_id}: {str(e)}"
            self.log_to_console(error_msg)
            print(error_msg)  # Stampa anche nella console di sistema per debug
        
        # Non chiamare reset_ui qui, poiché potrebbe essere chiamato da ogni thread
        # e causare il ripristino dell'UI mentre altri thread sono ancora in esecuzione
    
    def stop_bot(self):
        """
        Implements graceful shutdown mechanism with driver cleanup.
        This method ensures all Selenium drivers are properly closed.
        """
        # Set the stop event to signal the bot to stop
        self.stop_event.set()
        self.log_to_console("Bot in fase di arresto...")
        
        # Try to terminate any active Selenium processes
        self.terminate_selenium_drivers()
        
        messagebox.showinfo("Bot Fermato", "L'esecuzione del bot è stata interrotta.")
        
        # Reset UI
        self.reset_ui()
    
    def terminate_selenium_drivers(self):
        """
        Force terminate any running Selenium driver processes
        and ensure they are properly cleaned up
        """
        try:
            # Try to find and kill Selenium driver processes
            if sys.platform.startswith('win'):
                # On Windows
                self.log_to_console("Terminazione dei processi di Chrome/Selenium...")
                os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
                os.system("taskkill /f /im chrome.exe >nul 2>&1")
                
                # More aggressive process killing for orphaned processes
                os.system("wmic process where \"name like '%chrome%'\" delete >nul 2>&1")
                
                # Clean up temp files that might cause issues
                temp_dir = os.environ.get('TEMP', '')
                if temp_dir and os.path.exists(temp_dir):
                    self.log_to_console("Pulizia dei file temporanei di Chrome...")
                    chrome_temp = os.path.join(temp_dir, 'chrome_*')
                    os.system(f'del /q /f /s "{chrome_temp}" >nul 2>&1')
                    
            elif sys.platform.startswith('linux'):
                # On Linux
                self.log_to_console("Terminazione dei processi di Chrome/Selenium...")
                os.system("pkill -9 -f chromedriver")
                os.system("pkill -9 -f chrome")
                
                # Clean Linux temp files
                os.system("rm -rf /tmp/.com.google.Chrome*")
                os.system("rm -rf /tmp/.org.chromium.Chromium*")
                
            elif sys.platform.startswith('darwin'):
                # On macOS
                self.log_to_console("Terminazione dei processi di Chrome/Selenium...")
                os.system("pkill -9 -f chromedriver")
                os.system("pkill -9 -f 'Google Chrome'")
                
                # Clean macOS temp files
                os.system("rm -rf ~/Library/Caches/Google/Chrome")
                
            # Short delay to ensure processes have time to terminate
            self.log_to_console("Attesa per chiusura completa dei processi...")
            sleep(1)  # Usa sleep dal 'from time import sleep' invece di time.sleep
            self.log_to_console("Terminazione dei processi completata.")
            
        except Exception as e:
            self.log_to_console(f"Errore durante la terminazione dei processi: {str(e)}")
            
    def reset_ui(self):
        # Reset button states
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def main():
    if sys.platform.startswith('win'):
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        
        # Get the console window
        console_window = kernel32.GetConsoleWindow()
        
        # Completely hide the console window
        user32.ShowWindow(console_window, 0)  # SW_HIDE
        kernel32.CloseHandle(console_window)
        
    root = tk.Tk()
    app = SpotifyBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()