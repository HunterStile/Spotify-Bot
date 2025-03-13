import subprocess
import time
import pyautogui
import random

# Funzione per cambiare proxy via Proxifier
def change_proxy(config_file_name):
    proxifier_exe_path = "C:\\Program Files (x86)\\Proxifier\\Proxifier.exe"
    config_file_path = f"C:\\Users\\Luigi\\AppData\\Roaming\\Proxifier4\\Profiles\\{config_file_name}"
    command = f'"{proxifier_exe_path}" -load "{config_file_path}"'
    print("Configurazione del nuovo proxy...")

    try:
        subprocess.Popen(command, shell=True)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(10)
        print(f"Proxy configurato: {config_file_name}")
    except Exception as e:
        print(f"Errore durante la configurazione del proxy: {e}")

# Funzione per scegliere user-agent random
def get_random_user_agent():
    with open("user_agents.txt", "r") as file:
        agents = file.readlines()
    return random.choice(agents).strip()
