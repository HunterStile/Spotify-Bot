import tkinter as tk
from tkinter import ttk, font
import subprocess
import sys
import os

class SpotifyBotLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Spotify Bot Suite - Launcher")
        master.geometry("600x500")
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
        main_frame = ttk.Frame(self.master, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_font = font.Font(family="Arial", size=24, weight="bold")
        header = tk.Label(main_frame, text="🎵 Spotify Bot Suite", 
                         font=header_font, bg=self.bg_color, fg=self.accent_color)
        header.pack(pady=(0, 10))
        
        subtitle = tk.Label(main_frame, text="Scegli il modulo da avviare", 
                           font=("Arial", 12), bg=self.bg_color, fg=self.text_color)
        subtitle.pack(pady=(0, 30))
        
        # Bot cards container
        cards_frame = ttk.Frame(main_frame)
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # Original Spotify Bot Card
        self.create_bot_card(
            cards_frame,
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
            row=0
        )
        
        # Artist Scraper Card
        self.create_bot_card(
            cards_frame,
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
            row=1
        )
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(30, 0))
        
        version_label = tk.Label(footer_frame, text="Suite v1.3.0 by HunterStile", 
                               bg=self.bg_color, fg=self.text_color, font=("Arial", 10))
        version_label.pack()
        
    def create_bot_card(self, parent, title, features, script_name, row):
        """Crea una card per un bot"""
        # Card frame
        card_frame = tk.Frame(parent, bg=self.secondary_bg, relief=tk.RAISED, bd=2)
        card_frame.grid(row=row, column=0, sticky="ew", pady=10, padx=5, ipady=15, ipadx=15)
        
        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        
        # Title
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(card_frame, text=title, font=title_font,
                              bg=self.secondary_bg, fg=self.accent_color)
        title_label.pack(pady=(0, 10))
        
        # Features list
        features_frame = tk.Frame(card_frame, bg=self.secondary_bg)
        features_frame.pack(fill=tk.X, pady=(0, 15))
        
        for i, feature in enumerate(features):
            feature_label = tk.Label(features_frame, text=feature, 
                                   bg=self.secondary_bg, fg=self.text_color,
                                   font=("Arial", 10), anchor='w')
            feature_label.pack(fill=tk.X, pady=2)
        
        # Launch button
        launch_btn = tk.Button(card_frame, text=f"🚀 Avvia", 
                              command=lambda: self.launch_script(script_name),
                              bg=self.accent_color, fg=self.text_color,
                              font=("Arial", 12, "bold"), relief=tk.FLAT,
                              padx=20, pady=8)
        launch_btn.pack()
        
        # Hover effects
        def on_enter(e):
            launch_btn.configure(bg="#1ed760")  # Lighter green on hover
            
        def on_leave(e):
            launch_btn.configure(bg=self.accent_color)
            
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
        
    def launch_script(self, script_name):
        """Lancia lo script specificato"""
        try:
            # Verifica che il file esista
            if not os.path.exists(script_name):
                tk.messagebox.showerror("Errore", f"File {script_name} non trovato!")
                return
            
            # Lancia il script
            if sys.platform.startswith('win'):
                subprocess.Popen([sys.executable, script_name], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, script_name])
                
            # Opzionalmente chiudi il launcher
            # self.master.destroy()
            
        except Exception as e:
            tk.messagebox.showerror("Errore", f"Errore nell'avvio del modulo:\n{str(e)}")

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
    x = (root.winfo_screenwidth() // 2) - (600 // 2)
    y = (root.winfo_screenheight() // 2) - (500 // 2)
    root.geometry(f"600x500+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
