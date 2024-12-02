import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import sys
import os
import importlib.util
import ctypes

# Import the existing bot configuration and execution function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("config", "config.py")
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)

from Main import *
from config import *

class SpotifyBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Spotify Bot Control Panel")
        master.geometry("600x700")
        
        # Bot Configuration Variables
        self.crea_account_var = tk.BooleanVar(value=config_module.CREAZIONE)
        self.proxy_var = tk.BooleanVar(value=config_module.PROXY)
        self.segui_playlist_var = tk.BooleanVar(value=config_module.SEGUI_PLAYLIST)
        self.ascolta_canzoni_var = tk.BooleanVar(value=config_module.ASCOLTA_CANZONI)
        
        self.max_iterazioni_var = tk.IntVar(value=50)
        self.modalita_posizioni_var = tk.StringVar(value=config_module.MODALITA_POSIZIONI)
        
        # Proxy List
        self.proxy_list_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
        
        # Playlist URLs
        self.playlist_urls_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_URLS))
        
        # Bot Thread
        self.bot_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()
        
    def create_widgets(self):
        # Main Configuration Frame
        config_frame = ttk.LabelFrame(self.master, text="Bot Configuration")
        config_frame.pack(padx=10, pady=10, fill='x')
        
        # Checkboxes
        ttk.Checkbutton(config_frame, text="Create New Account", variable=self.crea_account_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Use Proxy", variable=self.proxy_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Follow Playlists", variable=self.segui_playlist_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Listen to Songs", variable=self.ascolta_canzoni_var).pack(anchor='w')
        
        # Max Iterations
        max_iter_frame = ttk.Frame(config_frame)
        max_iter_frame.pack(fill='x', pady=5)
        ttk.Label(max_iter_frame, text="Max Iterations:").pack(side='left')
        ttk.Entry(max_iter_frame, textvariable=self.max_iterazioni_var, width=10).pack(side='left', padx=5)
        
        # Modalità Posizioni
        modalita_frame = ttk.LabelFrame(self.master, text="Position Selection Mode")
        modalita_frame.pack(padx=10, pady=10, fill='x')
        
        random_radio = ttk.Radiobutton(modalita_frame, text="Random", variable=self.modalita_posizioni_var, value='random')
        random_radio.pack(side='left', padx=10)
        
        statico_radio = ttk.Radiobutton(modalita_frame, text="Static", variable=self.modalita_posizioni_var, value='statico')
        statico_radio.pack(side='left', padx=10)
        
        # Proxy List
        proxy_frame = ttk.LabelFrame(self.master, text="Proxy List (one per line)")
        proxy_frame.pack(padx=10, pady=10, fill='both', expand=True)
        proxy_text = tk.Text(proxy_frame, height=5)
        proxy_text.insert(tk.END, self.proxy_list_var.get())
        proxy_text.pack(padx=5, pady=5, fill='both', expand=True)
        proxy_text.bind('<KeyRelease>', lambda e: self.proxy_list_var.set(proxy_text.get("1.0", tk.END).strip()))
        
        # Playlist URLs
        playlist_urls_frame = ttk.LabelFrame(self.master, text="Playlist URLs (format: url:pos1,pos2,pos3)")
        playlist_urls_frame.pack(padx=10, pady=10, fill='both', expand=True)
        playlist_urls_text = tk.Text(playlist_urls_frame, height=10)
        playlist_urls_text.insert(tk.END, self.playlist_urls_var.get())
        playlist_urls_text.pack(padx=5, pady=5, fill='both', expand=True)
        playlist_urls_text.bind('<KeyRelease>', lambda e: self.playlist_urls_var.set(playlist_urls_text.get("1.0", tk.END).strip()))
        
        # Buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Bot", command=self.start_bot)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Bot", command=self.stop_bot, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        # Console Output
        console_frame = ttk.LabelFrame(self.master, text="Console Output")
        console_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.console_text = tk.Text(console_frame, height=10, state='disabled')
        self.console_text.pack(padx=5, pady=5, fill='both', expand=True)
        
    def start_bot(self):
        # Prepare configuration dictionary
        configurazione_bot = {
            'crea_account': self.crea_account_var.get(),
            'max_iterazioni': self.max_iterazioni_var.get(),
            'input_utente': False,
            'ripetizione': False,
            
            'usa_proxy': self.proxy_var.get(),
            'proxy_list': self.proxy_list_var.get().split('\n'),
            'proxy_list_first': self.proxy_list_var.get().split('\n'),
            
            'segui_playlist': self.segui_playlist_var.get(),
            'playlist_urls': self.playlist_urls_var.get().split('\n'),
            
            'modalita_posizioni': self.modalita_posizioni_var.get(),
            
            'ascolta_canzoni': self.ascolta_canzoni_var.get(),
        }
        
        # Start Bot in a Separate Thread
        self.stop_event.clear()
        self.bot_thread = threading.Thread(target=self.run_bot, args=(configurazione_bot,))
        self.bot_thread.start()
        
        # Update Button States
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
    
    def run_bot(self, configurazione_bot):
        try:
            # Redirect stdout to console text widget
            class TextRedirector:
                def __init__(self, widget, tag="stdout"):
                    self.widget = widget
                    self.tag = tag
                
                def write(self, str):
                    self.widget.configure(state='normal')
                    self.widget.insert(tk.END, str)
                    self.widget.see(tk.END)
                    self.widget.configure(state='disabled')
                
                def flush(self):
                    pass
            
            sys.stdout = TextRedirector(self.console_text)
            sys.stderr = TextRedirector(self.console_text, "stderr")
            
            # Run the bot
            esegui_bot_spotify(configurazione_bot)
        
        except Exception as e:
            messagebox.showerror("Bot Error", str(e))
        finally:
            # Reset UI
            self.master.after(0, self.reset_ui)
    
    def stop_bot(self):
        # Implement graceful shutdown mechanism
        self.stop_event.set()
        messagebox.showinfo("Bot Stopped", "Bot execution has been stopped.")
        
        # Reset UI
        self.reset_ui()
    
    def reset_ui(self):
        # Reset button states
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def main():
    if sys.platform.startswith('win'):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    root = tk.Tk()
    app = SpotifyBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()