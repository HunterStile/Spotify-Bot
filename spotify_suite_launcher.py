import tkinter as tk
from tkinter import ttk, font, messagebox
import subprocess
import sys
import os

class SpotifyBotLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Spotify Bot Suite - Launcher")
        master.geometry("650x750")
        master.resizable(False, False)
        
        # Spotify theme colors
        self.bg_color = "#121212"
        self.accent_color = "#1DB954"
        self.text_color = "#FFFFFF"
        self.secondary_bg = "#212121"
        
        master.configure(bg=self.bg_color)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton', background=self.accent_color, foreground=self.text_color)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.master, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_font = font.Font(family="Arial", size=24, weight="bold")
        header = tk.Label(main_frame, text="🎵 Spotify Bot Suite", 
                         font=header_font, bg=self.bg_color, fg=self.accent_color)
        header.pack(pady=(0, 5))
        
        subtitle = tk.Label(main_frame, text="Scegli il modulo da avviare", 
                           font=("Arial", 12), bg=self.bg_color, fg=self.text_color)
        subtitle.pack(pady=(0, 25))
        
        # Scrollable frame for cards
        canvas = tk.Canvas(main_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bot cards
        self.create_bot_card(
            scrollable_frame,
            "🎧 Spotify Bot Originale",
            [
                "✅ Creazione account automatica",
                "✅ Gestione multi-account",  
                "✅ Auto-follow playlist",
                "✅ Simulazione ascolto",
                "✅ Sistema anti-detection",
                "✅ Multithreading avanzato"
            ],
            "spotify_bot_gui.py",
            0
        )
        
        self.create_bot_card(
            scrollable_frame,
            "🎤 Artist Scraper",
            [
                "🔍 Trova artisti emergenti",
                "📊 Analizza playlist di curatori",
                "📧 Estrae email e contatti",
                "📱 Trova profili social",
                "💾 Export CSV dettagliato",
                "🎯 Filtri per ascoltatori"
            ],
            "artist_scraper_gui.py",
            1
        )
        
        self.create_bot_card(
            scrollable_frame,
            "🔍 Contact Finder",
            [
                "📱 Ricerca automatica contatti",
                "🔎 Scan Instagram, Facebook, TikTok",
                "📧 Trova email e booking",
                "🌐 Multimotore di ricerca",
                "📊 Arricchisce CSV artisti",
                "⚙️ Modalità stealth avanzata"
            ],
            "contact_finder_gui.py",
            2
        )
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        version_label = tk.Label(footer_frame, text="Suite v1.4.0 by HunterStile", 
                               bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        version_label.pack()
        
    def create_bot_card(self, parent, title, features, script_name, row):
        """Crea una card per un bot"""
        # Card frame con stile migliorato
        card_frame = tk.Frame(parent, bg=self.secondary_bg, relief=tk.RAISED, bd=1)
        card_frame.pack(fill=tk.X, pady=12, padx=10, ipady=20, ipadx=20)
        
        # Title
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(card_frame, text=title, font=title_font,
                              bg=self.secondary_bg, fg=self.accent_color)
        title_label.pack(pady=(0, 15))
        
        # Features container
        features_container = tk.Frame(card_frame, bg=self.secondary_bg)
        features_container.pack(fill=tk.X, pady=(0, 20))
        
        # Organizza le features in due colonne se necessario
        if len(features) > 4:
            # Due colonne
            left_frame = tk.Frame(features_container, bg=self.secondary_bg)
            right_frame = tk.Frame(features_container, bg=self.secondary_bg)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
            right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
            
            mid_point = (len(features) + 1) // 2
            for i, feature in enumerate(features):
                target_frame = left_frame if i < mid_point else right_frame
                feature_label = tk.Label(target_frame, text=feature, 
                                       bg=self.secondary_bg, fg=self.text_color,
                                       font=("Arial", 10), anchor='w')
                feature_label.pack(fill=tk.X, pady=3)
        else:
            # Una colonna centrata
            for feature in features:
                feature_label = tk.Label(features_container, text=feature, 
                                       bg=self.secondary_bg, fg=self.text_color,
                                       font=("Arial", 10), anchor='center')
                feature_label.pack(fill=tk.X, pady=3)
        
        # Launch button con stile migliorato
        launch_btn = tk.Button(card_frame, text="🚀 AVVIA MODULO", 
                              command=lambda: self.launch_script(script_name),
                              bg=self.accent_color, fg=self.text_color,
                              font=("Arial", 12, "bold"), relief=tk.FLAT,
                              padx=30, pady=12, cursor="hand2")
        launch_btn.pack(pady=(5, 0))
        
        # Hover effects
        def on_enter(e):
            launch_btn.configure(bg="#1ed760")
            
        def on_leave(e):
            launch_btn.configure(bg=self.accent_color)
            
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
        
    def launch_script(self, script_name):
        """Lancia lo script specificato"""
        try:
            # Verifica che il file esista
            if not os.path.exists(script_name):
                messagebox.showerror("Errore", f"File {script_name} non trovato!")
                return
            
            # Lancia il script
            if sys.platform.startswith('win'):
                subprocess.Popen([sys.executable, script_name], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, script_name])
                
            messagebox.showinfo("Successo", f"Modulo {script_name} avviato con successo!")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'avvio del modulo:\n{str(e)}")

def main():
    # Windows DPI awareness
    if sys.platform.startswith('win'):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
    
    root = tk.Tk()
    app = SpotifyBotLauncher(root)
    
    # Center the window
    root.update_idletasks()
    width = 650
    height = 750
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
