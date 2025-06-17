"""
🔍 CONTACT FINDER GUI
Interfaccia grafica per la ricerca automatica di contatti degli artisti emergenti
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
import threading
import json
import os
from datetime import datetime
import sys
import queue

from contact_finder import ContactFinder, get_contact_finder_config


class ContactFinderGUI:
    """Interfaccia grafica per il Contact Finder"""
    
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.init_variables()
        self.create_widgets()
        self.load_config()
        
        # Queue per comunicazione thread
        self.message_queue = queue.Queue()
        self.check_queue()
        
        # Contact Finder instance
        self.contact_finder = None
        self.processing_thread = None
        
    def setup_window(self):
        """Configurazione finestra principale"""
        self.master.title("🔍 Contact Finder - Trova Contatti Artisti")
        self.master.geometry("900x700")
        self.master.configure(bg='#1e1e1e')
        
        # Stile Spotify-like
        self.bg_color = '#1e1e1e'
        self.card_color = '#2a2a2a'
        self.accent_color = '#1db954'
        self.text_color = '#ffffff'
        self.secondary_color = '#b3b3b3'
        
        # Frame principale
        self.main_frame = tk.Frame(self.master, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
    def init_variables(self):
        """Inizializza le variabili tkinter"""
        self.input_file_var = tk.StringVar(value="artisti-emergenti.csv")
        self.output_file_var = tk.StringVar(value="artisti-con-contatti.csv")
        self.max_results_var = tk.IntVar(value=3)
        self.delay_min_var = tk.IntVar(value=3)
        self.delay_max_var = tk.IntVar(value=7)
        self.use_stealth_var = tk.BooleanVar(value=True)
        self.headless_var = tk.BooleanVar(value=False)
        self.verify_profiles_var = tk.BooleanVar(value=False)
        
        # Social networks checkboxes
        self.search_instagram_var = tk.BooleanVar(value=True)
        self.search_facebook_var = tk.BooleanVar(value=True)
        self.search_tiktok_var = tk.BooleanVar(value=True)
        self.search_twitter_var = tk.BooleanVar(value=True)
        self.search_youtube_var = tk.BooleanVar(value=True)
        self.search_email_var = tk.BooleanVar(value=True)
        
        # Search engines
        self.use_google_var = tk.BooleanVar(value=True)
        self.use_bing_var = tk.BooleanVar(value=False)
        
        # Processing state
        self.is_processing = False
        
        # Config file
        self.config_file = "contact_finder_config.json"
        
    def create_widgets(self):
        """Crea tutti i widget della GUI"""
        self.create_header()
        
        # Container principale con scrollbar
        canvas = tk.Canvas(self.main_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Sezioni
        self.create_file_section(scrollable_frame)
        self.create_search_config_section(scrollable_frame)
        self.create_social_networks_section(scrollable_frame)
        self.create_search_engines_section(scrollable_frame)
        self.create_advanced_section(scrollable_frame)
        self.create_control_section(scrollable_frame)
        self.create_console_section(scrollable_frame)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_header(self):
        """Crea l'header della GUI"""
        header_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title con emoji e font custom
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title = tk.Label(header_frame, text="🔍 Contact Finder", 
                        font=title_font, bg=self.bg_color, fg=self.accent_color)
        title.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle = tk.Label(header_frame, text="Trova contatti social ed email degli artisti emergenti",
                           bg=self.bg_color, fg=self.text_color)
        subtitle.pack(side=tk.LEFT, padx=(10, 0))
        
        # Version
        version_label = tk.Label(header_frame, text="v1.0.0", 
                               bg=self.bg_color, fg=self.secondary_color)
        version_label.pack(side=tk.RIGHT)
        
    def create_file_section(self, parent):
        """Sezione configurazione file"""
        file_frame = ttk.LabelFrame(parent, text="📁 Configurazione File", padding=15)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File input
        ttk.Label(file_frame, text="File CSV Input:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(file_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        input_entry = ttk.Entry(input_frame, textvariable=self.input_file_var, width=40)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_input_btn = ttk.Button(input_frame, text="📁", width=3,
                                     command=self.browse_input_file)
        browse_input_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # File output
        ttk.Label(file_frame, text="File CSV Output:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        output_frame = ttk.Frame(file_frame)
        output_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=40)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_output_btn = ttk.Button(output_frame, text="📁", width=3,
                                      command=self.browse_output_file)
        browse_output_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        file_frame.columnconfigure(0, weight=1)
        
    def create_search_config_section(self, parent):
        """Sezione configurazione ricerca"""
        search_frame = ttk.LabelFrame(parent, text="🔍 Configurazione Ricerca", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Max risultati per ricerca
        ttk.Label(search_frame, text="Max Risultati per Ricerca:").grid(row=0, column=0, sticky=tk.W, pady=5)
        results_spinbox = ttk.Spinbox(search_frame, from_=1, to=10, width=10, 
                                     textvariable=self.max_results_var)
        results_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Delay tra ricerche
        ttk.Label(search_frame, text="Delay tra Ricerche (sec):").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        delay_frame = ttk.Frame(search_frame)
        delay_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Spinbox(delay_frame, from_=1, to=10, width=5, textvariable=self.delay_min_var).pack(side=tk.LEFT)
        ttk.Label(delay_frame, text=" - ").pack(side=tk.LEFT)
        ttk.Spinbox(delay_frame, from_=1, to=10, width=5, textvariable=self.delay_max_var).pack(side=tk.LEFT)
        
    def create_social_networks_section(self, parent):
        """Sezione selezione social network"""
        social_frame = ttk.LabelFrame(parent, text="📱 Social Network da Cercare", padding=15)
        social_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Organizza in due colonne
        social_checks = [
            ("📷 Instagram", self.search_instagram_var),
            ("📘 Facebook", self.search_facebook_var),
            ("🎵 TikTok", self.search_tiktok_var),
            ("🐦 Twitter/X", self.search_twitter_var),
            ("📺 YouTube", self.search_youtube_var),
            ("📧 Email", self.search_email_var)
        ]
        
        for i, (text, var) in enumerate(social_checks):
            row = i // 2
            col = i % 2
            ttk.Checkbutton(social_frame, text=text, variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=(0, 20), pady=5)
                
    def create_search_engines_section(self, parent):
        """Sezione motori di ricerca"""
        engine_frame = ttk.LabelFrame(parent, text="🌐 Motori di Ricerca", padding=15)
        engine_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(engine_frame, text="🔍 Google", variable=self.use_google_var).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        ttk.Checkbutton(engine_frame, text="🅱️ Bing", variable=self.use_bing_var).grid(
            row=0, column=1, sticky=tk.W, padx=(20, 0), pady=5)
            
    def create_advanced_section(self, parent):
        """Sezione opzioni avanzate"""
        advanced_frame = ttk.LabelFrame(parent, text="⚙️ Opzioni Avanzate", padding=15)
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(advanced_frame, text="🕵️ Modalità Stealth", 
                       variable=self.use_stealth_var).grid(row=0, column=0, sticky=tk.W, pady=5)
                       
        ttk.Checkbutton(advanced_frame, text="👻 Modalità Headless", 
                       variable=self.headless_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0), pady=5)
                       
        ttk.Checkbutton(advanced_frame, text="✅ Verifica Profili", 
                       variable=self.verify_profiles_var).grid(row=1, column=0, sticky=tk.W, pady=5)
                       
    def create_control_section(self, parent):
        """Sezione controlli principali"""
        control_frame = tk.Frame(parent, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pulsanti principali
        self.start_btn = ttk.Button(control_frame, text="🚀 Avvia Ricerca Contatti", 
                                   command=self.start_search)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Ferma", 
                                  command=self.stop_search, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
    def create_console_section(self, parent):
        """Sezione console output"""
        console_frame = ttk.LabelFrame(parent, text="📊 Console Output", padding=15)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console text widget con scrollbar
        console_container = tk.Frame(console_frame)
        console_container.pack(fill=tk.BOTH, expand=True)
        
        self.console_text = tk.Text(console_container, 
                                   bg='#0d1117', 
                                   fg='#c9d1d9',
                                   font=('Consolas', 10),
                                   wrap=tk.WORD,
                                   height=12)
        
        console_scrollbar = ttk.Scrollbar(console_container, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=console_scrollbar.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear button
        clear_btn = ttk.Button(console_frame, text="🗑️ Pulisci Console", 
                              command=self.clear_console)
        clear_btn.pack(pady=(10, 0))
        
    def browse_input_file(self):
        """Apri dialog per scegliere file input"""
        filename = filedialog.askopenfilename(
            title="Seleziona file CSV artisti",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_var.set(filename)
            
    def browse_output_file(self):
        """Apri dialog per scegliere file output"""
        filename = filedialog.asksaveasfilename(
            title="Salva risultati come...",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
            
    def log_to_console(self, message):
        """Aggiunge un messaggio alla console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)
        self.master.update_idletasks()
        
    def clear_console(self):
        """Pulisce la console"""
        self.console_text.delete(1.0, tk.END)
        
    def get_current_config(self):
        """Ottiene la configurazione corrente dalla GUI"""
        config = get_contact_finder_config()
        
        # Aggiorna con valori GUI
        config.update({
            'csv_input_file': self.input_file_var.get(),
            'csv_output_file': self.output_file_var.get(),
            'max_results_per_search': self.max_results_var.get(),
            'delay_between_searches': (self.delay_min_var.get(), self.delay_max_var.get()),
            'use_stealth_mode': self.use_stealth_var.get(),
            'headless': self.headless_var.get(),
            'verify_social_profiles': self.verify_profiles_var.get(),
        })
        
        # Search engines
        engines = []
        if self.use_google_var.get():
            engines.append('google')
        if self.use_bing_var.get():
            engines.append('bing')
        config['search_engines'] = engines
        
        # Social networks
        social_networks = []
        if self.search_instagram_var.get():
            social_networks.append('instagram')
        if self.search_facebook_var.get():
            social_networks.append('facebook')
        if self.search_tiktok_var.get():
            social_networks.append('tiktok')
        if self.search_twitter_var.get():
            social_networks.append('twitter')
        if self.search_youtube_var.get():
            social_networks.append('youtube')
        config['search_social_networks'] = social_networks
        config['search_emails'] = self.search_email_var.get()
        
        return config
        
    def start_search(self):
        """Avvia la ricerca contatti"""
        if self.is_processing:
            return
            
        # Validazione
        if not os.path.exists(self.input_file_var.get()):
            messagebox.showerror("Errore", "File CSV input non trovato!")
            return
            
        if not any([self.use_google_var.get(), self.use_bing_var.get()]):
            messagebox.showerror("Errore", "Seleziona almeno un motore di ricerca!")
            return
            
        # Salva configurazione
        self.save_config()
        
        # Avvia processing in thread separato
        self.is_processing = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        self.log_to_console("🚀 Avvio ricerca contatti...")
        
        config = self.get_current_config()
        self.processing_thread = threading.Thread(target=self.run_contact_search, args=(config,))
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
    def run_contact_search(self, config):
        """Esegue la ricerca contatti in thread separato"""
        try:
            # Redirect delle stampe alla GUI
            class GUIWriter:
                def __init__(self, gui):
                    self.gui = gui
                def write(self, message):
                    if message.strip():
                        self.gui.message_queue.put(message.strip())
                def flush(self):
                    pass
                    
            # Salva stdout originale
            original_stdout = sys.stdout
            sys.stdout = GUIWriter(self)
            
            # Esegui ricerca
            contact_finder = ContactFinder(config)
            success = contact_finder.process_csv()
            
            # Messaggio finale
            if success:
                self.message_queue.put("✅ Ricerca contatti completata con successo!")
            else:
                self.message_queue.put("❌ Ricerca contatti fallita!")
                
        except Exception as e:
            self.message_queue.put(f"❌ Errore durante la ricerca: {str(e)}")
        finally:
            # Ripristina stdout
            sys.stdout = original_stdout
            self.message_queue.put("FINISHED")
            
    def stop_search(self):
        """Ferma la ricerca contatti"""
        if self.contact_finder and self.contact_finder.driver:
            try:
                self.contact_finder.driver.quit()
            except:
                pass
                
        self.is_processing = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        
        self.log_to_console("⏹️ Ricerca interrotta dall'utente")
        
    def check_queue(self):
        """Controlla i messaggi dal thread"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                if message == "FINISHED":
                    self.is_processing = False
                    self.start_btn.config(state=tk.NORMAL)
                    self.stop_btn.config(state=tk.DISABLED)
                    self.progress.stop()
                else:
                    self.log_to_console(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.master.after(100, self.check_queue)
        
    def save_config(self):
        """Salva la configurazione corrente"""
        config = {
            'input_file': self.input_file_var.get(),
            'output_file': self.output_file_var.get(),
            'max_results': self.max_results_var.get(),
            'delay_min': self.delay_min_var.get(),
            'delay_max': self.delay_max_var.get(),
            'use_stealth': self.use_stealth_var.get(),
            'headless': self.headless_var.get(),
            'verify_profiles': self.verify_profiles_var.get(),
            'search_instagram': self.search_instagram_var.get(),
            'search_facebook': self.search_facebook_var.get(),
            'search_tiktok': self.search_tiktok_var.get(),
            'search_twitter': self.search_twitter_var.get(),
            'search_youtube': self.search_youtube_var.get(),
            'search_email': self.search_email_var.get(),
            'use_google': self.use_google_var.get(),
            'use_bing': self.use_bing_var.get()
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
                
                self.input_file_var.set(config.get('input_file', 'artisti-emergenti.csv'))
                self.output_file_var.set(config.get('output_file', 'artisti-con-contatti.csv'))
                self.max_results_var.set(config.get('max_results', 3))
                self.delay_min_var.set(config.get('delay_min', 3))
                self.delay_max_var.set(config.get('delay_max', 7))
                self.use_stealth_var.set(config.get('use_stealth', True))
                self.headless_var.set(config.get('headless', False))
                self.verify_profiles_var.set(config.get('verify_profiles', False))
                self.search_instagram_var.set(config.get('search_instagram', True))
                self.search_facebook_var.set(config.get('search_facebook', True))
                self.search_tiktok_var.set(config.get('search_tiktok', True))
                self.search_twitter_var.set(config.get('search_twitter', True))
                self.search_youtube_var.set(config.get('search_youtube', True))
                self.search_email_var.set(config.get('search_email', True))
                self.use_google_var.set(config.get('use_google', True))
                self.use_bing_var.set(config.get('use_bing', False))
                
        except Exception as e:
            print(f"Errore caricamento config: {str(e)}")


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = ContactFinderGUI(root)
    
    # Messaggio iniziale
    app.log_to_console("🔍 Contact Finder avviato!")
    app.log_to_console("📋 Carica un file CSV di artisti emergenti e avvia la ricerca")
    
    root.mainloop()


if __name__ == "__main__":
    main()
