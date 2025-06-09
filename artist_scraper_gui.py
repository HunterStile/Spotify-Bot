import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import threading
import json
import os
import sys
from time import sleep

# Import delle funzioni del nuovo scraper
from artist_scraper_functions import (
    esegui_artist_scraper,
    get_artist_scraper_config
)

class ArtistScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Spotify Artist Scraper - Trova Artisti Emergenti")
        master.geometry("1000x800")
        
        # Stessi colori del bot principale
        self.bg_color = "#121212"  # Spotify dark background
        self.accent_color = "#1DB954"  # Spotify green
        self.text_color = "#FFFFFF"  # White text
        self.secondary_bg = "#212121"  # Slightly lighter background
        self.disabled_color = "#535353"  # Gray for disabled elements
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors to match Spotify theme
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabelframe', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TCheckbutton', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton', background=self.accent_color, foreground=self.text_color)
        self.style.map('TButton', 
                      background=[('active', self.accent_color), ('disabled', self.disabled_color)])
        
        master.configure(bg=self.bg_color)
        
        # Config file
        self.config_file = "artist_scraper_config.json"
        
        # Variables
        self.init_variables()
        
        # Load configuration
        self.load_config()
        
        # Thread control
        self.scraper_thread = None
        self.stop_event = threading.Event()
        
        # Create main frame
        self.main_frame = ttk.Frame(master, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create widgets
        self.create_widgets()
        
    def init_variables(self):
        """Inizializza le variabili tkinter"""
        self.max_artisti_var = tk.IntVar(value=30)
        self.soglia_ascoltatori_var = tk.IntVar(value=100000)
        self.usa_stealth_var = tk.BooleanVar(value=True)
        self.secondo_schermo_var = tk.BooleanVar(value=False)
        self.output_filename_var = tk.StringVar(value="artisti_emergenti.csv")
        
        # Playlist predefinite dei curatori
        default_playlists = """https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd
https://open.spotify.com/playlist/37i9dQZF1DXarRatq9Oe86
https://open.spotify.com/playlist/37i9dQZF1DX0ieeqLrWI4T
https://open.spotify.com/playlist/37i9dQZF1DX4SBhb3fqCJd"""
        
        self.playlist_urls_var = tk.StringVar(value=default_playlists)
        
    def create_header(self):
        """Crea l'header della GUI"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title con emoji e font custom
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title = tk.Label(header_frame, text="🎤 Spotify Artist Scraper", 
                        font=title_font, bg=self.bg_color, fg=self.accent_color)
        title.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle = tk.Label(header_frame, text="Trova artisti emergenti e i loro contatti",
                           bg=self.bg_color, fg=self.text_color)
        subtitle.pack(side=tk.LEFT, padx=(10, 0))
        
        # Version
        version_label = tk.Label(header_frame, text="v1.0.0", 
                               bg=self.bg_color, fg=self.text_color)
        version_label.pack(side=tk.RIGHT)
        
    def create_widgets(self):
        """Crea tutti i widget della GUI"""
        # Create columns
        left_column = ttk.Frame(self.main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(self.main_frame)
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # LEFT COLUMN
        self.create_config_section(left_column)
        self.create_output_section(left_column)
        self.create_control_section(left_column)
        
        # RIGHT COLUMN  
        self.create_playlist_section(right_column)
        self.create_console_section(right_column)
        
    def create_config_section(self, parent):
        """Sezione configurazioni principali"""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configurazione Scraper", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Max artisti per playlist
        ttk.Label(config_frame, text="Max Artisti per Playlist:").grid(row=0, column=0, sticky=tk.W, pady=5)
        artisti_spinbox = ttk.Spinbox(config_frame, from_=10, to=100, width=10, 
                                     textvariable=self.max_artisti_var)
        artisti_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Soglia ascoltatori
        ttk.Label(config_frame, text="Soglia Max Ascoltatori:").grid(row=1, column=0, sticky=tk.W, pady=5)
        soglia_spinbox = ttk.Spinbox(config_frame, from_=10000, to=1000000, increment=10000,
                                    width=15, textvariable=self.soglia_ascoltatori_var)
        soglia_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Opzioni browser
        ttk.Checkbutton(config_frame, text="🕵️ Usa Modalità Stealth", 
                       variable=self.usa_stealth_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(config_frame, text="🖥️ Secondo Schermo", 
                       variable=self.secondo_schermo_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
    def create_output_section(self, parent):
        """Sezione configurazione output"""
        output_frame = ttk.LabelFrame(parent, text="💾 Output", padding=15)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(output_frame, text="Nome File CSV:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        filename_frame = ttk.Frame(output_frame)
        filename_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        filename_entry = ttk.Entry(filename_frame, textvariable=self.output_filename_var, width=25)
        filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(filename_frame, text="📁", width=3,
                               command=self.browse_output_file)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
    def create_control_section(self, parent):
        """Sezione controlli principali"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Controlli", padding=15)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pulsanti principali
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(btn_frame, text="🚀 Avvia Scraper", 
                                   command=self.start_scraper)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹️ Ferma", 
                                  command=self.stop_scraper, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_config_btn = ttk.Button(btn_frame, text="💾 Salva Config", 
                                    command=self.save_config)
        save_config_btn.pack(side=tk.RIGHT)
        
    def create_playlist_section(self, parent):
        """Sezione playlist da analizzare"""
        playlist_frame = ttk.LabelFrame(parent, text="🎵 Playlist Curatori da Analizzare", padding=15)
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Info label
        info_label = tk.Label(playlist_frame, 
                             text="Inserisci gli URL delle playlist di curatori conosciuti (una per riga):",
                             bg=self.bg_color, fg=self.text_color, anchor='w')
        info_label.pack(fill=tk.X, pady=(0, 5))
        
        # Text area con scrollbar
        text_frame = ttk.Frame(playlist_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.playlist_text = tk.Text(text_frame, height=8, wrap=tk.WORD,
                                    bg=self.secondary_bg, fg=self.text_color,
                                    insertbackground=self.text_color)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.playlist_text.yview)
        self.playlist_text.configure(yscrollcommand=scrollbar.set)
        
        self.playlist_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate with default playlists
        self.playlist_text.insert(tk.END, self.playlist_urls_var.get())
        
        # Buttons per playlist preimpostate
        preset_frame = ttk.Frame(playlist_frame)
        preset_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(preset_frame, text="🎯 Playlist Top Global", 
                  command=self.load_global_playlists).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(preset_frame, text="🇮🇹 Playlist Italia", 
                  command=self.load_italy_playlists).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(preset_frame, text="🎸 Playlist Indie", 
                  command=self.load_indie_playlists).pack(side=tk.LEFT)
        
    def create_console_section(self, parent):
        """Sezione console output"""
        console_frame = ttk.LabelFrame(parent, text="📋 Console Output", padding=15)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console text area
        console_text_frame = ttk.Frame(console_frame)
        console_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console_text = tk.Text(console_text_frame, height=15, state='disabled',
                                   bg=self.secondary_bg, fg=self.text_color,
                                   wrap=tk.WORD)
        
        console_scrollbar = ttk.Scrollbar(console_text_frame, orient=tk.VERTICAL, 
                                         command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=console_scrollbar.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear console button
        clear_btn = ttk.Button(console_frame, text="🗑️ Pulisci Console", 
                              command=self.clear_console)
        clear_btn.pack(pady=(10, 0))
        
    def browse_output_file(self):
        """Apri dialog per scegliere file output"""
        filename = filedialog.asksaveasfilename(
            title="Salva risultati come...",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.output_filename_var.set(os.path.basename(filename))
            
    def load_global_playlists(self):
        """Carica playlist globali predefinite"""
        global_playlists = """https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd
https://open.spotify.com/playlist/37i9dQZF1DXarRatq9Oe86
https://open.spotify.com/playlist/37i9dQZF1DX4SBhb3fqCJd
https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP"""
        
        self.playlist_text.delete(1.0, tk.END)
        self.playlist_text.insert(tk.END, global_playlists)
        self.log_to_console("📋 Caricate playlist globali predefinite")
        
    def load_italy_playlists(self):
        """Carica playlist italiane predefinite"""
        italy_playlists = """https://open.spotify.com/playlist/37i9dQZF1DX0qJB4PDHC9i
https://open.spotify.com/playlist/37i9dQZF1DX1rVvRgjX59F
https://open.spotify.com/playlist/37i9dQZF1DXbIeCFU20wRm
https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn
https://open.spotify.com/playlist/37i9dQZF1DWVlYsZJXqdym"""
        
        self.playlist_text.delete(1.0, tk.END)
        self.playlist_text.insert(tk.END, italy_playlists)
        self.log_to_console("🇮🇹 Caricate playlist italiane predefinite")
        
    def load_indie_playlists(self):
        """Carica playlist indie predefinite"""
        indie_playlists = """https://open.spotify.com/playlist/37i9dQZF1DXdbXVyLdB6uP
https://open.spotify.com/playlist/37i9dQZF1DX26DKvjp0s9M
https://open.spotify.com/playlist/37i9dQZF1DWVlYsZJXqdym
https://open.spotify.com/playlist/37i9dQZF1DX6ujZpAN0v9r
https://open.spotify.com/playlist/37i9dQZF1DX82GYcclJ3Ug"""
        
        self.playlist_text.delete(1.0, tk.END)
        self.playlist_text.insert(tk.END, indie_playlists)
        self.log_to_console("🎸 Caricate playlist indie predefinite")
        
    def log_to_console(self, message):
        """Aggiunge messaggio alla console"""
        self.console_text.configure(state='normal')
        self.console_text.insert(tk.END, f"{message}\n")
        self.console_text.configure(state='disabled')
        self.console_text.see(tk.END)
        self.master.update()
        
    def clear_console(self):
        """Pulisce la console"""
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')
        
    def start_scraper(self):
        """Avvia il processo di scraping"""
        # Validate input
        playlist_urls = [url.strip() for url in self.playlist_text.get(1.0, tk.END).split('\n') 
                        if url.strip() and 'spotify.com/playlist' in url]
        
        if not playlist_urls:
            messagebox.showerror("Errore", "Inserisci almeno una playlist valida!")
            return
            
        # Save current config
        self.save_config()
        
        # Prepare configuration
        config = {
            'max_artisti_per_playlist': self.max_artisti_var.get(),
            'soglia_ascoltatori_max': self.soglia_ascoltatori_var.get(),
            'usa_stealth': self.usa_stealth_var.get(),
            'secondo_schermo': self.secondo_schermo_var.get(),
            'output_filename': self.output_filename_var.get(),
            'playlist_curatori': playlist_urls,
            'stop_event': self.stop_event
        }
        
        # Update UI
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.stop_event.clear()
        
        # Clear console
        self.clear_console()
        self.log_to_console("🚀 Avvio Spotify Artist Scraper...")
        self.log_to_console(f"📋 Playlist da analizzare: {len(playlist_urls)}")
        self.log_to_console(f"🎯 Max artisti per playlist: {config['max_artisti_per_playlist']}")
        self.log_to_console(f"👥 Soglia ascoltatori: {config['soglia_ascoltatori_max']:,}")
        
        # Start scraper in separate thread
        self.scraper_thread = threading.Thread(target=self.run_scraper, args=(config,), daemon=True)
        self.scraper_thread.start()
        
    def run_scraper(self, config):
        """Esegue lo scraper in un thread separato"""
        try:
            # Redirect print to console
            original_print = print
            
            def console_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                self.master.after(0, self.log_to_console, message)
                
            # Replace print temporarily
            __builtins__['print'] = console_print
            
            # Run the scraper
            esegui_artist_scraper(config)
            
            # Restore original print
            __builtins__['print'] = original_print
            
            # Update UI on completion
            self.master.after(0, self.scraper_completed)
            
        except Exception as e:
            error_msg = f"❌ Errore durante l'esecuzione: {str(e)}"
            self.master.after(0, self.log_to_console, error_msg)
            self.master.after(0, self.scraper_completed)
            
    def stop_scraper(self):
        """Ferma il processo di scraping"""
        self.stop_event.set()
        self.log_to_console("⏹️ Richiesta di stop inviata...")
        
    def scraper_completed(self):
        """Chiamata quando lo scraper è completato"""
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.log_to_console("✅ Scraping completato!")
        
        # Show completion message
        messagebox.showinfo("Completato", 
                           f"Scraping completato! Controlla il file: {self.output_filename_var.get()}")
        
    def save_config(self):
        """Salva la configurazione corrente"""
        config = {
            'max_artisti': self.max_artisti_var.get(),
            'soglia_ascoltatori': self.soglia_ascoltatori_var.get(),
            'usa_stealth': self.usa_stealth_var.get(),
            'secondo_schermo': self.secondo_schermo_var.get(),
            'output_filename': self.output_filename_var.get(),
            'playlist_urls': self.playlist_text.get(1.0, tk.END).strip()
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            self.log_to_console("💾 Configurazione salvata")
        except Exception as e:
            self.log_to_console(f"❌ Errore salvataggio config: {str(e)}")
            
    def load_config(self):
        """Carica la configurazione salvata"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.max_artisti_var.set(config.get('max_artisti', 30))
                self.soglia_ascoltatori_var.set(config.get('soglia_ascoltatori', 100000))
                self.usa_stealth_var.set(config.get('usa_stealth', True))
                self.secondo_schermo_var.set(config.get('secondo_schermo', False))
                self.output_filename_var.set(config.get('output_filename', 'artisti_emergenti.csv'))
                
                if 'playlist_urls' in config:
                    self.playlist_urls_var.set(config['playlist_urls'])
                    
        except Exception as e:
            print(f"Errore caricamento config: {str(e)}")

def main():
    if sys.platform.startswith('win'):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
            
    root = tk.Tk()
    app = ArtistScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
