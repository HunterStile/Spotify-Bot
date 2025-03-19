import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import sys
import os
import json
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
        master.geometry("600x900")  # Made taller to accommodate new controls
        
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
        
        # Load saved configuration or use defaults
        self.load_config()
        
        # Bot Thread
        self.bot_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()
        
    def create_widgets(self):
        # Main Configuration Frame
        config_frame = ttk.LabelFrame(self.master, text="Bot Configuration")
        config_frame.pack(padx=10, pady=10, fill='x')
        
        # Checkboxes in main config
        ttk.Checkbutton(config_frame, text="Create New Account", variable=self.crea_account_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Use Proxy", variable=self.proxy_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Use Double Proxy", variable=self.doppio_proxy_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Follow Playlists", variable=self.segui_playlist_var).pack(anchor='w')
        ttk.Checkbutton(config_frame, text="Listen to Songs", variable=self.ascolta_canzoni_var).pack(anchor='w')
        
        # Robot Detection Frame
        robot_frame = ttk.LabelFrame(self.master, text="Robot Detection Settings")
        robot_frame.pack(padx=10, pady=5, fill='x')
        
        ttk.Checkbutton(robot_frame, text="Stop For Robot", variable=self.stop_for_robot_var).pack(anchor='w')
        
        tempo_frame = ttk.Frame(robot_frame)
        tempo_frame.pack(fill='x', pady=5)
        ttk.Label(tempo_frame, text="Restart Time (seconds):").pack(side='left')
        ttk.Entry(tempo_frame, textvariable=self.tempo_ripartenza_var, width=10).pack(side='left', padx=5)
        
        # Router Reset Frame
        router_frame = ttk.LabelFrame(self.master, text="Router Reset Settings")
        router_frame.pack(padx=10, pady=5, fill='x')
        
        ttk.Checkbutton(router_frame, text="Reset Router", variable=self.reset_router_var).pack(anchor='w')
        
        # Router Type Radio Buttons
        router_type_frame = ttk.Frame(router_frame)
        router_type_frame.pack(fill='x', pady=5)
        ttk.Label(router_type_frame, text="Router Type:").pack(side='left')
        ttk.Radiobutton(router_type_frame, text="TIM", variable=self.tipo_router_var, value='tim').pack(side='left', padx=10)
        ttk.Radiobutton(router_type_frame, text="Vodafone", variable=self.tipo_router_var, value='vodafone').pack(side='left')
        
        # Max Iterations
        max_iter_frame = ttk.Frame(config_frame)
        max_iter_frame.pack(fill='x', pady=5)
        ttk.Label(max_iter_frame, text="Max Iterations:").pack(side='left')
        ttk.Entry(max_iter_frame, textvariable=self.max_iterazioni_var, width=10).pack(side='left', padx=5)
        
        # Modalità Posizioni
        modalita_frame = ttk.LabelFrame(self.master, text="Position Selection Mode")
        modalita_frame.pack(padx=10, pady=5, fill='x')
        
        random_radio = ttk.Radiobutton(modalita_frame, text="Random", variable=self.modalita_posizioni_var, value='random')
        random_radio.pack(side='left', padx=10)
        
        statico_radio = ttk.Radiobutton(modalita_frame, text="Static", variable=self.modalita_posizioni_var, value='statico')
        statico_radio.pack(side='left', padx=10)
        
        # Proxy Lists
        proxy_frame = ttk.LabelFrame(self.master, text="Proxy Lists")
        proxy_frame.pack(padx=10, pady=5, fill='both', expand=True)
        
        # Main Proxy List
        proxy_main_frame = ttk.Frame(proxy_frame)
        proxy_main_frame.pack(fill='x', pady=5)
        ttk.Label(proxy_main_frame, text="Main Proxy List (one per line)").pack(side='top', anchor='w')
        proxy_text = tk.Text(proxy_main_frame, height=4)
        proxy_text.insert(tk.END, self.proxy_list_var.get())
        proxy_text.pack(fill='both', expand=True)
        proxy_text.bind('<KeyRelease>', lambda e: self.proxy_list_var.set(proxy_text.get("1.0", tk.END).strip()))
        
        # First Proxy List (for double proxy)
        proxy_first_frame = ttk.Frame(proxy_frame)
        proxy_first_frame.pack(fill='x', pady=5)
        first_proxy_label = ttk.Label(proxy_first_frame, text="First Proxy List (used when Double Proxy is enabled)")
        first_proxy_label.pack(side='top', anchor='w')
        proxy_first_text = tk.Text(proxy_first_frame, height=4)
        proxy_first_text.insert(tk.END, self.proxy_list_first_var.get())
        proxy_first_text.pack(fill='both', expand=True)
        proxy_first_text.bind('<KeyRelease>', lambda e: self.proxy_list_first_var.set(proxy_first_text.get("1.0", tk.END).strip()))

        # Update proxy text states based on checkbox
        def update_proxy_states(*args):
            proxy_enabled = self.proxy_var.get()
            double_proxy_enabled = self.doppio_proxy_var.get()
            
            proxy_text['state'] = 'normal' if proxy_enabled else 'disabled'
            proxy_first_text['state'] = 'normal' if proxy_enabled and double_proxy_enabled else 'disabled'
            first_proxy_label['state'] = 'normal' if proxy_enabled else 'disabled'
        
        # Bind the update function to the checkboxes
        self.proxy_var.trace('w', update_proxy_states)
        self.doppio_proxy_var.trace('w', update_proxy_states)
        
        # Initial state update
        update_proxy_states()
        
        # Playlist Configuration
        playlist_frame = ttk.LabelFrame(self.master, text="Playlist Configuration")
        playlist_frame.pack(padx=10, pady=5, fill='both', expand=True)
        
        # Playlist URLs for listening
        ttk.Label(playlist_frame, text="Playlist URLs for Listening (format: url;pos1,pos2,pos3)").pack(anchor='w')
        playlist_urls_text = tk.Text(playlist_frame, height=4)
        playlist_urls_text.insert(tk.END, self.playlist_urls_var.get())
        playlist_urls_text.pack(padx=5, pady=5, fill='both')
        playlist_urls_text.bind('<KeyRelease>', lambda e: self.playlist_urls_var.set(playlist_urls_text.get("1.0", tk.END).strip()))
        
        # Playlist URLs for following
        ttk.Label(playlist_frame, text="Playlist URLs for Following (one per line)").pack(anchor='w')
        playlist_follow_text = tk.Text(playlist_frame, height=4)
        playlist_follow_text.insert(tk.END, self.playlist_follow_var.get())
        playlist_follow_text.pack(padx=5, pady=5, fill='both')
        playlist_follow_text.bind('<KeyRelease>', lambda e: self.playlist_follow_var.set(playlist_follow_text.get("1.0", tk.END).strip()))
        
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
                
                print("Configuration loaded successfully from", self.config_file)
            else:
                print("No saved configuration found, using defaults")
                # Use defaults from config module
                self.crea_account_var = tk.BooleanVar(value=config_module.CREAZIONE)
                self.proxy_var = tk.BooleanVar(value=config_module.PROXY)
                self.doppio_proxy_var = tk.BooleanVar(value=config_module.DOPPIOPROXY)
                self.segui_playlist_var = tk.BooleanVar(value=config_module.SEGUI_PLAYLIST)
                self.ascolta_canzoni_var = tk.BooleanVar(value=config_module.ASCOLTA_CANZONI)
                self.stop_for_robot_var = tk.BooleanVar(value=config_module.STOP_FOR_ROBOT)
                self.reset_router_var = tk.BooleanVar(value=config_module.RESET_ROUTER)
                
                self.max_iterazioni_var = tk.IntVar(value=config_module.MAX_ITERAZIONE)
                self.tempo_ripartenza_var = tk.IntVar(value=config_module.TEMPO_RIPARTENZA)
                
                self.modalita_posizioni_var = tk.StringVar(value=config_module.MODALITA_POSIZIONI)
                self.tipo_router_var = tk.StringVar(value=config_module.TIPO_ROUTER)
                
                self.proxy_list_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
                self.proxy_list_first_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
                self.playlist_urls_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_URLS))
                self.playlist_follow_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_FOLLOW))
                
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            messagebox.showerror("Configuration Error", f"Error loading configuration: {str(e)}")
            # Use defaults if there's an error
            self.crea_account_var = tk.BooleanVar(value=config_module.CREAZIONE)
            self.proxy_var = tk.BooleanVar(value=config_module.PROXY)
            self.doppio_proxy_var = tk.BooleanVar(value=config_module.DOPPIOPROXY)
            self.segui_playlist_var = tk.BooleanVar(value=config_module.SEGUI_PLAYLIST)
            self.ascolta_canzoni_var = tk.BooleanVar(value=config_module.ASCOLTA_CANZONI)
            self.stop_for_robot_var = tk.BooleanVar(value=config_module.STOP_FOR_ROBOT)
            self.reset_router_var = tk.BooleanVar(value=config_module.RESET_ROUTER)
            
            self.max_iterazioni_var = tk.IntVar(value=config_module.MAX_ITERAZIONE)
            self.tempo_ripartenza_var = tk.IntVar(value=config_module.TEMPO_RIPARTENZA)
            
            self.modalita_posizioni_var = tk.StringVar(value=config_module.MODALITA_POSIZIONI)
            self.tipo_router_var = tk.StringVar(value=config_module.TIPO_ROUTER)
            
            self.proxy_list_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
            self.proxy_list_first_var = tk.StringVar(value='\n'.join(config_module.PROXYLIST))
            self.playlist_urls_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_URLS))
            self.playlist_follow_var = tk.StringVar(value='\n'.join(config_module.PLAYLIST_FOLLOW))
    
    def save_config(self):
        config_data = {
            'crea_account': self.crea_account_var.get(),
            'usa_proxy': self.proxy_var.get(),
            'doppio_proxy': self.doppio_proxy_var.get(),
            'segui_playlist': self.segui_playlist_var.get(),
            'ascolta_canzoni': self.ascolta_canzoni_var.get(),
            'stop_for_robot': self.stop_for_robot_var.get(),
            'reset_router': self.reset_router_var.get(),
            'max_iterazioni': self.max_iterazioni_var.get(),
            'tempo_ripartenza': self.tempo_ripartenza_var.get(),
            'modalita_posizioni': self.modalita_posizioni_var.get(),
            'tipo_router': self.tipo_router_var.get(),
            'proxy_list': [x for x in self.proxy_list_var.get().split('\n') if x.strip()],
            'proxy_list_first': [x for x in self.proxy_list_first_var.get().split('\n') if x.strip()],
            'playlist_urls': [x for x in self.playlist_urls_var.get().split('\n') if x.strip()],
            'playlist_follow': [x for x in self.playlist_follow_var.get().split('\n') if x.strip()]
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving configuration: {str(e)}")

    def start_bot(self):
        # Save configuration before starting the bot
        self.save_config()
        
        # Prepare configuration dictionary
        configurazione_bot = {
            'crea_account': self.crea_account_var.get(),
            'max_iterazioni': self.max_iterazioni_var.get(),
            'input_utente': INPUT_UTENTE,
            'ripetizione': RIPETIZIONE,
            
            'usa_proxy': self.proxy_var.get(),
            'proxy_list': [x.strip() for x in self.proxy_list_var.get().split('\n') if x.strip()],
            'proxy_list_first': [x.strip() for x in self.proxy_list_first_var.get().split('\n') if x.strip()],
            
            'doppio_proxy': self.doppio_proxy_var.get(),
            'stop_for_robot': self.stop_for_robot_var.get(),
            'tempo_ripartenza': self.tempo_ripartenza_var.get(),
            'reset_router': self.reset_router_var.get(),
            'tipo_router': self.tipo_router_var.get(),
            
            'segui_playlist': self.segui_playlist_var.get(),
            'playlist_urls': [x.strip() for x in self.playlist_urls_var.get().split('\n') if x.strip()],
            'playlist_follow': [x.strip() for x in self.playlist_follow_var.get().split('\n') if x.strip()],
            
            'modalita_posizioni': self.modalita_posizioni_var.get(),
            'ascolta_canzoni': self.ascolta_canzoni_var.get(),
        }
        
        # Validazione delle configurazioni
        if configurazione_bot['usa_proxy'] and configurazione_bot['doppio_proxy']:
            if not configurazione_bot['proxy_list_first']:
                messagebox.showwarning("Configurazione Incompleta", 
                    "Hai attivato il doppio proxy ma la lista proxy primaria è vuota!")
                return
        
        if configurazione_bot['usa_proxy'] and not configurazione_bot['proxy_list']:
            messagebox.showwarning("Configurazione Incompleta", 
                "Hai attivato l'uso dei proxy ma la lista proxy è vuota!")
            return
        
        if configurazione_bot['segui_playlist'] and not configurazione_bot['playlist_follow']:
            messagebox.showwarning("Configurazione Incompleta", 
                "Hai attivato il seguire playlist ma non hai specificato playlist da seguire!")
            return
        
        if configurazione_bot['ascolta_canzoni'] and not configurazione_bot['playlist_urls']:
            messagebox.showwarning("Configurazione Incompleta", 
                "Hai attivato l'ascolto delle canzoni ma non hai specificato playlist da ascoltare!")
            return
        
        # Passa l'evento di stop al bot
        configurazione_bot['stop_event'] = self.stop_event
        
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