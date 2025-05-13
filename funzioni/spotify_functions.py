#librerie
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random
from random import randint
from time import time
from time import sleep
import csv 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  
from selenium import webdriver
import string
from faker import Faker
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
import subprocess
import pyautogui
from dotenv import load_dotenv
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from twocaptcha import TwoCaptcha
import re  # Aggiungiamo l'importazione di re

# Ottieni il percorso assoluto della directory corrente (dove si trova il file eseguibile)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Directory superiore
sys.path.append(parent_dir)  # Aggiungi al sys.path
# Costruisci il percorso assoluto della cartella "Setup"
setup_dir = os.path.join(current_dir, 'Setup')
# Costruisci i percorsi assoluti dei file di testo
path_chrome = os.path.join(setup_dir, 'path_chrome.txt')
path_driver = os.path.join(setup_dir, 'path_driver.txt')

from config import *

#Variabili per il funzionamento
file = os.path.join(parent_dir, 'account_spotify.csv')       #CSV per eseguire gli accessi agli account              
a = 1                              #tempo minimo di attesa negli slepp 
b = 2                              #tempo massimo di attesa negli slepp
count = 0                          #sommattore generico

#XPATH dei bottoni spotify
menu_canzone = '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div[]/div/div[5]/button[2]'
aggiungi_playlist = '//*[@id="tippy-2"]/ul/div/li[{}]/button'

posizione_brano = '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[{}]/div'
posizione_brano2 = '//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/div/div[{}]/div/div[1]'
posizione_seguo_playlist = '[data-testid="add-button"]'

                            

# Carica le variabili d'ambiente dal file .env
load_dotenv()


# FUNZIONI BASE #

# Funzione per terminare connessioni precedenti
def reset_network_connections():
    print("Terminazione delle connessioni di rete in corso...")
    try:
        subprocess.run('netsh interface ip reset', shell=True, check=True)
        print("Connessioni di rete resettate con successo.")
    except subprocess.CalledProcessError:
        print("Errore nel reset delle connessioni di rete.")

# Funzione per configurare il proxy
def change_proxy(config_file_name):
    #reset_network_connections()  # Da capire

    proxifier_exe_path = "C:\\Program Files (x86)\\Proxifier\\proxifier.exe"
    config_file_path = f"C:\\Users\\Luigi\\AppData\\Roaming\\Proxifier4\\Profiles\\{config_file_name}"
    command = f'"{proxifier_exe_path}" -load "{config_file_path}"'

    print("Configurazione del nuovo proxy...")
    try:
        subprocess.Popen(command, shell=True)
        sleep(2)  # Aspetta che il comando venga eseguito
        pyautogui.press('enter')
        sleep(2)
        pyautogui.press('enter')
        sleep(10)  # Tempo aggiuntivo per completare l'operazione
        print(f"Proxy configurato: {config_file_name}")
    except Exception as e:
        print(f"Errore durante la configurazione del proxy: {e}")

#Configurazione del browser
def configurazione_browser(user_agent, disable_stealth=False):
    chrome_driver_path = leggi_txt(path_driver)  # Path di ChromeDriver dal tuo file
    chrome_binary_path = leggi_txt(path_chrome)  # Path di Chrome.exe dal tuo file

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_binary_path

    # Imposta User-Agent personalizzato se non disabilitato
    if not disable_stealth:
        chrome_options.add_argument(f"user-agent={user_agent}")
        print("[BOT] Utilizzando user agent personalizzato")
    else:
        print("[BOT] User agent personalizzato disabilitato")

    # Disabilita automazioni visibili se non in modalità semplice
    if not disable_stealth:
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        print("[BOT] Modalità stealth attivata")
    else:
        print("[BOT] Modalità stealth disattivata - usando configurazione browser semplice")
    
    # Altri parametri utili
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Clean session options (nuovi parametri per avvio pulito)
    chrome_options.add_argument("--incognito")  # Usa modalità incognito per evitare conflitti di sessione
    chrome_options.add_argument("--disable-application-cache")  # Disabilita cache
    chrome_options.add_argument("--disable-session-crashed-bubble")  # Disabilita segnalazione crash
    chrome_options.add_argument("--disable-restore-session-state")  # Previene ripristino sessione
    
    # Imposta la posizione della finestra se vuoi su secondo monitor
    chrome_options.add_argument("window-position=1920,0")
    chrome_options.add_argument("start-maximized")

    try:
        # Inizializza il driver
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
        
        # Applica stealth per evitare detection (solo se non disabilitato)
        if not disable_stealth:
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
            )
            
            # Nasconde proprietà webdriver
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("[BOT] Stealth configurato")
    
        print("[BOT] Browser configurato e pronto")
        return driver
    except Exception as e:
        print(f"Errore durante la configurazione del browser: {str(e)}")
        # In caso di errore, prova una configurazione più semplice
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
        print("[BOT] Browser configurato con opzioni di fallback")
        return driver

# Funzione per scegliere user-agent random
def get_random_user_agent():
    with open("user_agents.txt", "r") as file:
        agents = file.readlines()
    return random.choice(agents).strip()

#Genero l'indirizzo completo
def generate_xpath(base_xpath, n):
    return base_xpath.format(n)

#Genero una random string
def generate_random_string(length):
    # definisce i caratteri alfanumerici possibili
    characters = string.ascii_letters + string.digits
    # genera una stringa casuale di lunghezza data
    return ''.join(random.choice(characters) for i in range(length))

#Rimuove duplicati da un csv
def rimuovi_duplicati(file_input, file_output):
    with open(file_input, newline='') as csvfile_input, \
            open(file_output, 'w', newline='') as csvfile_output:
        reader = csv.reader(csvfile_input)
        writer = csv.writer(csvfile_output)
        # set per tenere traccia delle righe già lette
        seen = set()
        for row in reader:
            # trasforma la riga in una tupla di stringhe, in modo che sia hashabile
            row_tuple = tuple(str(cell) for cell in row)
            if row_tuple not in seen:
                writer.writerow(row)
                seen.add(row_tuple)

#Ritorna il body della pagina 
def check_conferma(driver): 
    try:
        # Aspetta che il corpo della pagina sia presente prima di estrarre il testo
        body_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
        page_text = body_element.text
        
    except Exception as e:
        print(f"Errore durante l'estrazione del testo: {str(e)}")
    return page_text

#Legge un txt
def leggi_txt(nome_file):
    try:
        with open(nome_file, 'r') as file:
            prima_riga = file.readline().strip()  # Legge la prima riga e rimuove eventuali spazi bianchi iniziali/finali
            return prima_riga
    except FileNotFoundError:
        print(f"Errore: Il file '{nome_file}' non è stato trovato.")
        return None
    except Exception as e:
        print(f"Errore durante la lettura del file '{nome_file}': {e}")
        return None
    
def reset_router_tim(driver):
    link_accesso = 'http://192.168.1.1/'
    driver.get(link_accesso)

    # Massimizzare la finestra del driver immediatamente
    driver.maximize_window()
    
    page_text = check_conferma(driver)
    blocco = "privata" in page_text
    if blocco == True:
        driver.find_element(By.XPATH,'//*[@id="details-button"]').click()
        sleep(randint(a,b))
        driver.find_element(By.XPATH,'//*[@id="proceed-link"]').click()
        sleep(randint(a,b))
        
    utente = os.getenv('ROUTER_USER')
    password = os.getenv('ROUTER_PASSWORD')
    sleep(randint(2,3))
    driver.find_element(By.XPATH,'//*[@id="Frm_Username"]').send_keys(utente)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="Frm_Password"]').send_keys(password)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="LoginId"]').click()
     # Wait esplicito per il caricamento della pagina dopo il login
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mgrAndDiag"]'))
        )
    except TimeoutException:
        print("Timeout durante il caricamento della pagina dopo il login")
        return
    driver.find_element(By.XPATH,'//*[@id="mgrAndDiag"]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="devMgr"]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*//*[@id="Btn_restart"]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="confirmOK"]').click()
    sleep(randint(a,b))
    
    print("Router Riavviato")
    
def reset_router_vodafone(driver):
    link_accesso = 'http://192.168.1.1/'
    driver.get(link_accesso)
    
    # Massimizzare la finestra del driver immediatamente
    driver.maximize_window()
    
    page_text = check_conferma(driver)
    blocco = "privata" in page_text
    if blocco == True:
        driver.find_element(By.XPATH,'//*[@id="details-button"]').click()
        sleep(randint(a,b))
        driver.find_element(By.XPATH,'//*[@id="proceed-link"]').click()
        sleep(randint(a,b))
    
    utente = os.getenv('ROUTER_USER')
    password = os.getenv('ROUTER_PASSWORD')
    
    sleep(randint(2,3))
    driver.find_element(By.XPATH,'//*[@id="activation-content-right"]/div[2]/div/input').send_keys(utente)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="activation-content-right"]/div[3]/div[1]/input').send_keys(password)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="activation-content-right"]/div[3]/div[2]/input').click()
    
    # Wait esplicito per il caricamento della pagina dopo il login
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="navigation"]/ul/li[6]/a'))
        )
    except TimeoutException:
        print("Timeout durante il caricamento della pagina dopo il login")
        return
    
    driver.find_element(By.XPATH,'//*[@id="navigation"]/ul/li[6]/a').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="41"]/a').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="restartB"]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="applyButton"]').click()
    sleep(randint(a,b))
    
    print("Router Riavviato")
    
# FUNZIONI SPOTIFY #

#Crea un account spotify
def crea_account(driver, proxy, stop_for_robot, proxy_list=None, proxy_list_first=None, use_captcha_service=False, captcha_service='2captcha'):
    #variabili - logiche
    robot2 = False
    robot = False
    creato = False
    
    # Configurazione servizio CAPTCHA
    captcha_enabled = use_captcha_service
    
    #variabili 
    fake = Faker('it_IT')
    nomi = []
    for i in range(1000):
        nome = fake.first_name()
        nomi.append(nome)
    mesi = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre''novembre''dicembre']
    nickname = random.choice(nomi)
    anno=randint(1996,2005)
    mese=random.choice(mesi)
    giorno=randint(1,29)
    password = 'Napoli10!!'
    sceltasesso = ['M','F','F']
    sesso = random.choice(sceltasesso)
    link='https://www.spotify.com/it/signup'
    tempmail_all=['gmail','hotmail','outlook','virgilio','alice']
    tempstring = [10,11,12]
    tempmail_scelto= random.choice(tempmail_all)
    tempstring_scelto = random.choice(tempstring)
    
    #scelta del temp mail
    if tempmail_scelto == 'gmail':
        email = generate_random_string(tempstring_scelto)
        email +="@gmail.com"
    if tempmail_scelto == 'hotmail':
        email = generate_random_string(tempstring_scelto)
        email +="@hotmail.com"
    if tempmail_scelto == 'outlook':
        email = generate_random_string(tempstring_scelto)
        email +="@outlook.com"
    if tempmail_scelto == 'virgilio':
        email = generate_random_string(tempstring_scelto)
        email +="@virgilio.it"
    if tempmail_scelto == 'alice':
        email = generate_random_string(tempstring_scelto)
        email +="@alicie.it"
    
    #CREAZIONE ACCOUNT
    driver.get(link)
    print("Account in creazione...")
    sleep(randint(5,6))             
    try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            ).click()
    except (NoSuchElementException, TimeoutException):
            print("Pulsante cookie non trovato o non cliccabile. Continuo.")
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(email)
    sleep(randint(a,b))           
    driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/button').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="new-password"]').send_keys(password)
    sleep(randint(a,b))           
    driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[2]/button').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="displayName"]').send_keys(nickname)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="year"]').send_keys(anno)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="month"]').send_keys(mese)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="day"]').send_keys(giorno)
    sleep(randint(a,b))
                
    if sesso == 'M':                  
        driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[1]/div[2]/div/section/div[3]/fieldset/div/div/div[1]/label/span[1]').click()
        sleep(randint(a,b))
    else:                             
        driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[1]/div[2]/div/section/div[3]/fieldset/div/div/div[2]/label/span[1]').click()
        sleep(randint(a,b))
        
    driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[2]/button/span[1]').click()
    sleep(randint(a,b))           
    driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[1]/div[2]/div/section/div[4]/div[1]/div/div/label/span[1]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[1]/div[2]/div/section/div[4]/div[3]/div/div/label/span[1]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="__next"]/main/main/section/div/form/div[2]/button/span[1]').click()
    sleep(randint(6,7))
    if proxy == True:
        # Usa sempre la lista proxy standard in questa funzione
        if proxy_list and len(proxy_list) > 0:
            config_file_name = random.choice(proxy_list)
            print("Usando proxy dalla lista standard:", config_file_name)
            change_proxy(config_file_name)
        else:
            print("Attenzione: Lista proxy vuota!")
            return None
      
    #FINE CREAZIONE ACCCOUNT    #CHECK ROBOT
    page_text = check_conferma(driver)
    robot  = "Crea" in page_text
    sleep(randint(2,3))
    if robot==True:
       driver.find_element(By.XPATH,'//*[@id="encore-web-main-content"]/div/div/div/div/div/button/span[1]').click()
       sleep(randint(4,5))
    robot2 = "Continua" in page_text
    
    while robot2==True:
       if stop_for_robot==True and not captcha_enabled:
           print("Richiesta robot - interruzione configurata")
           return True
       print("richiesta robot...")
       url = driver.current_url
       
       # Prova a risolvere il CAPTCHA se l'opzione è abilitata
       if captcha_enabled:
           print(f"Tentativo di risoluzione automatica del CAPTCHA usando {captcha_service}...")
           
           # Attendi che il frame del CAPTCHA sia completamente caricato
           sleep(3)
           
           # Prova a risolvere il CAPTCHA con la nuova logica migliorata
           captcha_risolto = risolvi_captcha(driver, url)
           
           if captcha_risolto:
               print("CAPTCHA risolto, ora cerco di inviare il modulo...")
               
               # Cerca di cliccare su pulsanti di conferma o invio tipici di Spotify
               try:
                   # Tenta di trovare e cliccare sul pulsante "Avanti" o "Continua"
                   buttons = driver.find_elements(By.XPATH, 
                       "//button[contains(.,'Avanti') or contains(.,'Continua') or " + 
                       "contains(.,'Next') or contains(.,'Continue') or " + 
                       "contains(.,'Verifica') or contains(.,'Verify')]")
                   
                   if buttons:
                       print(f"Trovato pulsante di navigazione: {buttons[0].text}")
                       buttons[0].click()
                       sleep(3)  # Attendi un po' di più per elaborare la risposta
                   
                   # Se il pulsante precedente non funziona, cerca altri pulsanti
                   submit_buttons = driver.find_elements(By.XPATH, "//button[@type='submit']")
                   if submit_buttons:
                       print("Trovato pulsante di invio")
                       submit_buttons[0].click()
                       sleep(3)
                   
                   # Prova anche con qualsiasi link che contenga testo di conferma
                   links = driver.find_elements(By.XPATH, 
                       "//a[contains(.,'Avanti') or contains(.,'Continua') or " +
                       "contains(.,'Next') or contains(.,'Continue')]")
                   if links:
                       print(f"Trovato link di navigazione: {links[0].text}")
                       links[0].click()
                       sleep(3)
                       
                   # Infine, prova a premere Enter sulla tastiera
                   try:
                       active_element = driver.switch_to.active_element
                       active_element.send_keys(Keys.RETURN)
                       print("Invio tasto ENTER")
                       sleep(2)
                   except:
                       pass
                       
               except Exception as e:
                   print(f"Errore durante l'interazione con i pulsanti: {str(e)}")
           
           if not captcha_risolto and stop_for_robot:
               print("Impossibile risolvere il CAPTCHA - interruzione configurata")
               return True
       else:
           print("Risoluzione automatica CAPTCHA disabilitata")
       
       # Attendi più tempo per vedere se il CAPTCHA è stato accettato
       for i in range(10):  # Controllo più frequente
           print(f"Attesa verifica CAPTCHA: {i+1}/10")
           sleep(2)
           
           # Verifica se siamo passati oltre il CAPTCHA
           page_text = check_conferma(driver)
           if "Continua" not in page_text and "robot" not in page_text.lower():
               print("Verificato passaggio oltre la schermata CAPTCHA")
               break
               
       # Prendi uno screenshot per debug
       try:
           driver.save_screenshot('captcha_risolto.png')
           print("Screenshot salvato come 'captcha_risolto.png'")
       except:
           print("Impossibile salvare lo screenshot")
           
       # Verifica se siamo passati oltre il CAPTCHA
       page_text = check_conferma(driver)
       creato = "Scarica" in page_text
       if creato == True:
            robot2=False

    sleep(randint(a,b))
    page_text = check_conferma(driver)
    creato = "Scarica" in page_text
    if creato == True:
        print("Account Creato!")

        # Dati da inserire nel file CSV
        new_rows = [
            [email, password]
        ]

        # Apri il file CSV in modalità append
        with open('account_spotify_creati.csv', 'a', newline='') as csvfile:
            # Scrivi i dati nel file CSV
            csvwriter = csv.writer(csvfile, delimiter=',')
            for row in new_rows:
                csvwriter.writerow(row)
    else:
        print('Account non creato.., riprovo.')

    return email,password,driver

#Seguo la playlist
def seguo_playlist(driver, link):
    try:
        driver.get(link)
        sleep(randint(4,5))                     
        driver.find_element(By.CSS_SELECTOR, posizione_seguo_playlist).click()
        print("Playlist seguita!")
        sleep(randint(2,3))
    except Exception as e:
        print(f"Errore durante il clic: {str(e)}")
        sleep(randint(4,5))
        
#Accedi ad un account spotify
def Accesso_spotify(driver,email,password):
    try:
        print(f"Tentativo di accesso con: {email}")
        link_accesso = 'https://open.spotify.com/'
        driver.get(link_accesso)
        sleep(randint(2,3))
        
        # Accetta i cookie se presenti
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
            )
            cookie_button.click()
            print("Cookie accettati")
        except (NoSuchElementException, TimeoutException):
            print("Pulsante cookie non trovato o non cliccabile. Continuo.")
        
        sleep(randint(a,b))
        
        # Clicca sul bottone di login
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="global-nav-bar"]/div[3]/div[1]/div[2]/button[2]'))
            )
            login_button.click()
            print("Cliccato su login")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Errore nel trovare il pulsante di login: {str(e)}")
            # Prova un XPath alternativo
            try:
                alternative_login = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accedi") or contains(text(), "Log in")]'))
                )
                alternative_login.click()
                print("Cliccato su login alternativo")
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Anche il login alternativo non funziona: {str(e)}")
                # Cattura screenshot per debug
                driver.save_screenshot('login_error.png')
                return True  # Segnala errore
        
        sleep(randint(a,b))
        
        # Inserisci email
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="login-username"]'))
            )
            username_field.clear()
            username_field.send_keys(email)
            print("Email inserita")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Errore nel trovare il campo email: {str(e)}")
            driver.save_screenshot('email_field_error.png')
            return True
        
        driver.find_element(By.XPATH,'//*[@id="login-button"]').click()
        sleep(randint(a,b))
        
        
        
        # Inserisci password
        try:
            password_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="login-password"]'))
            )
            password_field.clear()
            password_field.send_keys(password)
            print("Password inserita")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Errore nel trovare il campo password: {str(e)}")
            driver.save_screenshot('password_field_error.png')
            return True
        
        sleep(randint(a,b))
        
        # Clicca sul bottone di login finale
        try:
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="login-button"]'))
            )
            submit_button.click()
            print("Cliccato su pulsante di invio login")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Errore nel trovare il pulsante di invio: {str(e)}")
            driver.save_screenshot('submit_button_error.png')
            return True
        
        sleep(randint(4,5))
        
        # Verifica se l'accesso è riuscito
        page_text = check_conferma(driver)
        errore = "errati" in page_text or "incorrect" in page_text.lower()
        
        if not errore:
            print("Accesso eseguito correttamente!")
        else:
            print("Errore, dati non corretti.")
            driver.save_screenshot('login_failed.png')
        
        return errore
    
    except Exception as e:
        print(f"Errore generale durante l'accesso: {str(e)}")
        driver.save_screenshot('general_error.png')
        return True

#Ascolto una specifica canzone in una playlit
def Sento_canzone(driver,posizione):
    print("Ascolto la canzone..")
    try:
        # Prova prima con il primo formato XPath
        xpath = generate_xpath(posizione_brano,posizione)
        print(f"Tentativo layout 1, posizione: {posizione}")
        
        # Verifica se l'elemento esiste prima di procedere
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        posizione_scelta(driver, xpath)
    except (NoSuchElementException, TimeoutException):
        # Se il primo formato fallisce, prova con il secondo
        try:
            xpath = generate_xpath(posizione_brano2,posizione)
            print(f"Tentativo layout 2, posizione: {posizione}")
            posizione_scelta(driver, xpath)
        except (NoSuchElementException, TimeoutException):
            print("Nessun elemento trovato con entrambi i layout. Verifica gli XPath.")
            # Aggiungere qui logica di fallback se necessario

#Carico la pagina web di una playlist
def scegli_playlist(driver,playlist_scelta):
    print("Vado sulla playlist..")
    driver.get(playlist_scelta)
    sleep(randint(3,4))

#Elimino un brano dalla playlist
def elimina_brano(driver, posizione):
    print("Elimino la canzone..")     
    sleep(randint(2,3))
    xpath = generate_xpath(menu_canzone,posizione)
    driver.find_element(By.XPATH,xpath).click()
    sleep(randint(2,3))
    driver.find_element(By.XPATH,'//*[@id="context-menu"]/ul/li[2]/button').click()
    sleep(randint(a,b))
    print("Canzone eliminata!")

#Aggiungo uyn brano dalla playlist
def aggiungi_brano(driver, posizione, playlist_target,posizione_playlist):
    print("Vado sulla playlist..")
    driver.get(playlist_target)
    sleep(randint(3,4))   
    print("Aggiungo la canzone..")     
    sleep(randint(2,3))
    xpath = generate_xpath(menu_canzone,posizione)
    driver.find_element(By.XPATH,xpath).click()
    sleep(randint(2,3))
    driver.find_element(By.XPATH,'//*[@id="context-menu"]/ul/li[1]/button').click()
    sleep(randint(a,b))
    xpath = generate_xpath(aggiungi_playlist,posizione_playlist)
    driver.find_element(By.XPATH,xpath).click() 
    print("Canzone aggiunta!")

#Clicco il punto di una canzone
def posizione_scelta(driver,posizione):
    sleep(randint(2,3))
    try:
    # Aspetta che l'elemento sia cliccabile
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, posizione))
    )
        # Registra l'inizio dell'attesa
        start_time = time()

        actions = ActionChains(driver)
        actions.double_click(element).perform()

        # Attendi un periodo di tempo casuale
        sleep(randint(120, 160))
        # Registra la fine dell'attesa
        end_time = time()
        # Calcola la differenza di tempo
        tempo_attesa = end_time - start_time
        print(f"Tempo effettivo di attesa: {tempo_attesa:.2f} secondi")

    except Exception as e:
        print(f"Errore durante il clic: {str(e)}")
        sleep(randint(120, 160))

# Funzione per risolvere i CAPTCHA utilizzando servizi esterni
def risolvi_captcha(driver, url=None):
    """
    Risolve i CAPTCHA utilizzando il servizio 2captcha.
    
    Parametri:
    - driver: l'istanza di Selenium WebDriver
    - url: URL opzionale della pagina con il CAPTCHA
    
    Ritorna:
    - True se il CAPTCHA è stato risolto con successo
    - False altrimenti
    """
    try:
        print("Rilevato CAPTCHA, tentativo di risoluzione automatica...")
        
        # Carica le variabili di ambiente
        load_dotenv()
        api_key = os.getenv('TWOCAPTCHA_API_KEY')
        
        if not api_key:
            print("ERRORE: Chiave API 2captcha non trovata nel file .env")
            print("Aggiungi la tua chiave API nel file .env: TWOCAPTCHA_API_KEY=tua_chiave_qui")
            return False
            
        # Fai uno screenshot iniziale per debug
        try:
            driver.save_screenshot('captcha_iniziale.png')
            print("Screenshot salvato come 'captcha_iniziale.png'")
        except:
            pass
        
        # Controlla prima se c'è una checkbox del reCAPTCHA visibile che può essere cliccata direttamente
        checkbox_clicked = False
        try:
            recaptcha_frames = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            
            # Se ci sono iframe, prova a cliccare sulla checkbox in ogni iframe
            for frame in recaptcha_frames:
                try:
                    driver.switch_to.frame(frame)
                    checkboxes = driver.find_elements(By.XPATH, "//*[contains(@class, 'recaptcha-checkbox')]")
                    
                    if checkboxes and checkboxes[0].is_displayed() and checkboxes[0].is_enabled():
                        print("Trovata checkbox reCAPTCHA, tentativo di click manuale")
                        checkboxes[0].click()
                        sleep(2)
                        checkbox_clicked = True
                        
                    # Torna al contesto principale
                    driver.switch_to.default_content()
                    
                    if checkbox_clicked:
                        print("Checkbox reCAPTCHA cliccata manualmente")
                        break
                        
                except Exception as frame_error:
                    print(f"Errore con frame: {str(frame_error)}")
                    driver.switch_to.default_content()
        except Exception as checkbox_error:
            print(f"Errore tentando click manuale checkbox: {str(checkbox_error)}")
            driver.switch_to.default_content()
        
        # Prima prova con il rilevatore specifico per Spotify
        try:
            print("Tentativo con rilevatore specifico per Spotify...")
            return gestisci_captcha_spotify(driver, api_key)
        except Exception as spotify_error:
            print(f"Errore nella gestione specifica per Spotify: {str(spotify_error)}")
            print("Procedendo con rilevamento CAPTCHA generico...")
            
        # Verifica il tipo di CAPTCHA presente (metodo classico)
        try:
            # Controlla se è presente un reCAPTCHA v2
            if len(driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")) > 0:
                return risolvi_recaptcha_v2(driver, api_key)
                
            # Controlla se è presente un reCAPTCHA v3 
            elif len(driver.find_elements(By.XPATH, "//script[contains(@src, 'recaptcha')]")) > 0:
                return risolvi_recaptcha_v3(driver, api_key)
                
            # Controlla hCaptcha
            elif len(driver.find_elements(By.XPATH, "//iframe[contains(@src, 'hcaptcha')]")) > 0:
                return risolvi_hcaptcha(driver, api_key)
                
            else:
                print("Tipo di CAPTCHA non riconosciuto, tentativo con reCAPTCHA v2 generico")
                return risolvi_recaptcha_v2(driver, api_key)
                
        except Exception as e:
            print(f"Errore nell'identificazione del tipo di CAPTCHA: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Errore nella risoluzione del CAPTCHA: {str(e)}")
        return False

def risolvi_recaptcha_v2(driver, api_key):
    """
    Risolve un reCAPTCHA v2 utilizzando 2captcha
    """
    try:
        # Trova il sitekey del reCAPTCHA
        site_key = None
        
        # Cerca il sitekey nell'HTML della pagina
        page_source = driver.page_source
        import re
        site_key_match = re.search(r'sitekey=["\']([^"\']+)["\']', page_source) or re.search(r'data-sitekey=["\']([^"\']+)["\']', page_source)
        if site_key_match:
            site_key = site_key_match.group(1)
        else:
            # Alternativa: cerca il sitekey nell'attributo data-sitekey
            recaptcha_elements = driver.find_elements(By.CSS_SELECTOR, "[data-sitekey]")
            if recaptcha_elements:
                site_key = recaptcha_elements[0].get_attribute("data-sitekey")
            
            # Se ancora non lo trova, cerca negli iframe
            if not site_key:
                try:
                    # Passa a tutti gli iframe e cerca il sitekey
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    for iframe in iframes:
                        if "recaptcha" in iframe.get_attribute("src"):
                            iframe_src = iframe.get_attribute("src")
                            site_key_match = re.search(r'k=([^&]+)', iframe_src)
                            if site_key_match:
                                site_key = site_key_match.group(1)
                                break
                except:
                    pass
        
        if not site_key:
            print("Impossibile trovare il sitekey del reCAPTCHA")
            return False
            
        # Ottieni l'URL corrente
        url = driver.current_url
        
        # FASE 1: Prima prova a cliccare sulla casella del reCAPTCHA per attivare l'interfaccia
        try:
            # Trova tutti gli iframe del reCAPTCHA
            recaptcha_frames = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            recaptcha_checkbox_clicked = False
            
            for frame in recaptcha_frames:
                try:
                    # Passa all'iframe
                    driver.switch_to.frame(frame)
                    
                    # Cerca la casella di controllo o elementi cliccabili all'interno dell'iframe
                    checkboxes = driver.find_elements(By.XPATH, "//*[contains(@class, 'recaptcha-checkbox') or contains(@class, 'recaptcha-anchor')]")
                    if checkboxes:
                        for checkbox in checkboxes:
                            if checkbox.is_displayed() and checkbox.is_enabled():
                                # Usa JavaScript per un click più affidabile
                                print("Casella di reCAPTCHA trovata, tentativo di click con JS")
                                driver.execute_script("arguments[0].click();", checkbox)
                                recaptcha_checkbox_clicked = True
                                sleep(3)  # Attendi più tempo per l'animazione e la richiesta di sfida
                                break
                    
                    # Torna al contesto principale
                    driver.switch_to.default_content()
                    
                    if recaptcha_checkbox_clicked:
                        break
                        
                except Exception as frame_error:
                    print(f"Errore durante l'interazione con il frame: {str(frame_error)}")
                    driver.switch_to.default_content()  # Assicurati di tornare al contesto principale
            
            if recaptcha_checkbox_clicked:
                print("Casella del reCAPTCHA cliccata con successo")
                # Dai più tempo al reCAPTCHA per caricare la sfida
                sleep(5)
                
                # Verifica se è apparso un frame di sfida con immagini
                challenge_frames = driver.find_elements(By.XPATH, 
                    "//iframe[contains(@title, 'recaptcha challenge') or contains(@title, 'sfida reCAPTCHA')]")
                
                if challenge_frames:
                    print("Rilevata sfida reCAPTCHA con immagini, passaggio a modalità image challenge")
                    # Abbiamo una sfida con immagini, facciamo uno screenshot e passiamo alla risoluzione
                    driver.save_screenshot('recaptcha_image_challenge.png')
                    
                    # Qui utilizzeremo il servizio 2captcha per risolvere la sfida con immagini
                    return risolvi_recaptcha_image_challenge(driver, api_key, site_key)
        except Exception as checkbox_error:
            print(f"Errore durante il tentativo di cliccare sulla casella reCAPTCHA: {str(checkbox_error)}")
        
        # FASE 2: Se non abbiamo una sfida con immagini o il click fallisce, procediamo con la risoluzione via API
        # Inizializza il solutore 2captcha
        solver = TwoCaptcha(api_key)
        
        print(f"Invio del reCAPTCHA a 2captcha (sitekey: {site_key})")
        result = solver.recaptcha(
            sitekey=site_key,
            url=url
        )
        
        # Ottieni il g-recaptcha-response
        code = result.get('code')
        
        print("Risposta CAPTCHA ricevuta, applicazione in corso...")
        
        # Debug info
        print(f"Risposta ottenuta dal servizio (primi 20 caratteri): {code[:20]}...")
        
        # Metodo 1: Tenta di inserire direttamente tramite JavaScript standard
        try:
            # Cerca tutte le possibili textarea di risposta reCAPTCHA
            script = f"""
            // Trova e compila tutte le possibili textarea di risposta reCAPTCHA
            var responses = document.querySelectorAll('textarea[name="g-recaptcha-response"]');
            if (responses.length > 0) {{
                for (var i = 0; i < responses.length; i++) {{
                    responses[i].innerHTML = "{code}";
                    responses[i].value = "{code}";
                    // Simula eventi per attivare gli handler
                    responses[i].dispatchEvent(new Event('change', {{ 'bubbles': true }}));
                    responses[i].dispatchEvent(new Event('input', {{ 'bubbles': true }}));
                }}
                console.log("Risposta reCAPTCHA applicata a " + responses.length + " elementi");
                return responses.length;
            }} else {{
                console.log("Nessun elemento g-recaptcha-response trovato");
                // Cerca di creare l'elemento se non esiste
                var textareas = document.createElement('textarea');
                textareas.id = 'g-recaptcha-response';
                textareas.name = 'g-recaptcha-response';
                textareas.innerHTML = "{code}";
                textareas.value = "{code}";
                textareas.style = "display: none";
                document.body.appendChild(textareas);
                console.log("Creato nuovo elemento g-recaptcha-response");
                return 1;
            }}
            """
            elements_found = driver.execute_script(script)
            print(f"Elementi reCAPTCHA trovati e compilati: {elements_found}")
        except Exception as e:
            print(f"Errore nell'applicare risposta reCAPTCHA con metodo 1: {str(e)}")
        
        # Metodo 2: Usando l'oggetto grecaptcha
        try:
            script = f"""
            if (typeof(___grecaptcha_cfg) !== 'undefined') {{
                console.log("Oggetto grecaptcha trovato, tentativo di hack...");
                try {{
                    // Metodo per recaptcha più recenti
                    var recaptchaKeys = Object.keys(___grecaptcha_cfg.clients).filter(function(key) {{
                        return typeof(___grecaptcha_cfg.clients[key]) === 'object';
                    }});
                    
                    var callbacks = [];
                    for (var i = 0; i < recaptchaKeys.length; i++) {{
                        var client = ___grecaptcha_cfg.clients[recaptchaKeys[i]];
                        // Cerca nelle diverse strutture possibili (A compatibilità con varie versioni)
                        if (client.hasOwnProperty('callback')) {{
                            callbacks.push(client.callback);
                        }} else if (client.hasOwnProperty('l')) {{
                            if (client.l.hasOwnProperty('callback')) {{
                                callbacks.push(client.l.callback);
                            }}
                        }} else if (client.hasOwnProperty('L')) {{
                            if (client.L.hasOwnProperty('L')) {{
                                if (client.L.L.hasOwnProperty('callback')) {{
                                    callbacks.push(client.L.L.callback);
                                }}
                            }}
                        }}
                        // Aggiungi qui altri pattern se necessario
                    }}
                    
                    var callbacksExecuted = 0;
                    for (var j = 0; j < callbacks.length; j++) {{
                        if (typeof(callbacks[j]) === 'function') {{
                            console.log("Chiamata callback reCAPTCHA #" + j);
                            callbacks[j]('{code}');
                            callbacksExecuted++;
                        }}
                    }}
                    
                    console.log("Callback eseguite: " + callbacksExecuted);
                    return callbacksExecuted > 0;
                    
                }} catch (e) {{
                    console.log("Errore nell'accesso a grecaptcha: " + e.message);
                }}
            }}
            return false;
            """
            success = driver.execute_script(script)
            if success:
                print("Risposta reCAPTCHA applicata usando il metodo grecaptcha")
        except Exception as e:
            print(f"Errore nell'applicare risposta reCAPTCHA con metodo 2: {str(e)}")
        
        # NUOVO: Verifica se esistono checkbox non cliccate e prova a cliccarle anche dopo
        try:
            # Cerca in tutti gli iframe visibili dopo l'applicazione della soluzione
            recaptcha_frames = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            for frame in recaptcha_frames:
                try:
                    driver.switch_to.frame(frame)
                    checkboxes = driver.find_elements(By.XPATH, "//*[contains(@class, 'recaptcha-checkbox') and not(contains(@class, 'recaptcha-checkbox-checked'))]")
                    if checkboxes and checkboxes[0].is_displayed() and checkboxes[0].is_enabled():
                        print("Trovata checkbox non cliccata, tentativo di click manuale")
                        # Usa JavaScript per essere sicuri
                        driver.execute_script("arguments[0].click();", checkboxes[0])
                        sleep(2)
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()
        except Exception as checkbox_error:
            print(f"Errore durante il tentativo aggiuntivo di cliccare sulla casella: {str(checkbox_error)}")
            driver.switch_to.default_content()
        
        # NUOVO: Cerca e clicca sui pulsanti rilevanti dopo la risoluzione
        try:
            # Cerca pulsanti usando un XPath più inclusivo
            buttons = driver.find_elements(By.XPATH, 
                "//button[contains(., 'Continua') or contains(., 'Continue') or contains(., 'Verifica') or contains(., 'Verify') or contains(., 'Submit') or contains(., 'Avanti') or contains(., 'Next')]")
            
            if buttons:
                print(f"Trovato pulsante post-CAPTCHA: {buttons[0].text}")
                driver.execute_script("arguments[0].click();", buttons[0])
                sleep(2)
        except Exception as button_error:
            print(f"Errore nel cliccare il pulsante post-CAPTCHA: {str(button_error)}")
        
        # Attendi che la risposta sia processata
        sleep(5)
        
        print("reCAPTCHA risolto con successo!")
        return True
        
    except Exception as e:
        print(f"Errore nella risoluzione del reCAPTCHA v2: {str(e)}")
        return False

def risolvi_hcaptcha(driver, api_key):
    """
    Risolve un hCaptcha utilizzando 2captcha
    """
    try:
        # Trova il sitekey dell'hCaptcha
        site_key = None
        
        # Cerca il sitekey nell'HTML della pagina
        page_source = driver.page_source
        import re
        site_key_match = re.search(r'data-sitekey=["\']([^"\']+)["\']', page_source)
        if site_key_match:
            site_key = site_key_match.group(1)
        else:
            # Alternativa: cerca il sitekey nell'attributo data-sitekey
            hcaptcha_elements = driver.find_elements(By.CSS_SELECTOR, "[data-sitekey]")
            if hcaptcha_elements:
                site_key = hcaptcha_elements[0].get_attribute("data-sitekey")
        
        if not site_key:
            print("Impossibile trovare il sitekey dell'hCaptcha")
            return False
            
        # Ottieni l'URL corrente
        url = driver.current_url
        
        # Inizializza il solutore 2captcha
        solver = TwoCaptcha(api_key)
        
        print(f"Invio dell'hCaptcha a 2captcha (sitekey: {site_key})")
        result = solver.hcaptcha(
            sitekey=site_key,
            url=url
        )
        
        # Ottieni la risposta hcaptcha
        code = result.get('code')
        
        # Esegui JavaScript per impostare la risposta
        script = f"""
        document.querySelector('[name="h-captcha-response"]').innerHTML = "{code}";
        document.querySelector('[name="h-captcha-response"]').dispatchEvent(new Event('change'));
        """
        driver.execute_script(script)
        
        # Attendi che la risposta sia processata
        sleep(2)
        
        # Cerca e clicca sul pulsante di invio
        try:
            submit_buttons = driver.find_elements(By.XPATH, "//button[@type='submit']")
            if submit_buttons:
                submit_buttons[0].click()
        except Exception as e:
            print(f"Errore nel cliccare il pulsante di invio: {str(e)}")
        
        print("hCaptcha risolto con successo!")
        return True
        
    except Exception as e:
        print(f"Errore nella risoluzione dell'hCaptcha: {str(e)}")
        return False

def risolvi_recaptcha_v3(driver, api_key):
    """
    Risolve un reCAPTCHA v3 utilizzando 2captcha
    """
    try:
        # Trova il sitekey del reCAPTCHA v3
        site_key = None
        
        # Cerca il sitekey nell'HTML della pagina
        page_source = driver.page_source
        import re
        site_key_match = re.search(r'reCAPTCHA.*?["\']([^"\']+)["\']', page_source) or re.search(r'grecaptcha.execute["\']([^"\']+)["\']', page_source)
        if site_key_match:
            site_key = site_key_match.group(1)
        
        if not site_key:
            print("Impossibile trovare il sitekey del reCAPTCHA v3")
            return False
            
        # Ottieni l'URL corrente
        url = driver.current_url
        
        # Inizializza il solutore 2captcha
        solver = TwoCaptcha(api_key)
        
        print(f"Invio del reCAPTCHA v3 a 2captcha (sitekey: {site_key})")
        result = solver.recaptcha(
            sitekey=site_key,
            url=url,
            version='v3',
            action='verify',  # Azione tipica per reCAPTCHA v3
            score=0.7  # Punteggio minimo richiesto
        )
        
        # Ottieni il g-recaptcha-response 
        code = result.get('code')
        
        # Trova l'ID del token element o usa un ID predefinito
        token_element_id = 'g-recaptcha-response'
        try:
            token_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='g-recaptcha-response']")
            if token_elements:
                token_element_id = token_elements[0].get_attribute('id')
        except:
            pass
        
        # Esegui JavaScript per impostare la risposta
        script = f"""
        document.getElementById('{token_element_id}').innerHTML = "{code}";
        """
        driver.execute_script(script)
        
        # Attendi che la risposta sia processata
        sleep(2)
        
        print("reCAPTCHA v3 risolto con successo!")
        return True
        
    except Exception as e:
        print(f"Errore nella risoluzione del reCAPTCHA v3: {str(e)}")
        return False

def rileva_tipo_captcha_spotify(driver):
    """
    Funzione specifica per rilevare i tipi di CAPTCHA presenti su Spotify
    e determinare la strategia migliore per la risoluzione
    
    Restituisce:
    - tipo: stringa che indica il tipo di CAPTCHA ("recaptcha_v2", "recaptcha_v2_image", "recaptcha_v3", "hcaptcha", "spotify_custom", "sconosciuto")
    - elementi: elementi rilevanti del CAPTCHA (pulsanti, iframe, ecc.)
    """
    try:
        # Salva uno screenshot per debug
        try:
            driver.save_screenshot('captcha_detected.png')
            print("Screenshot del CAPTCHA salvato")
        except:
            pass
            
        # Controlla se è un reCAPTCHA v2 standard
        recaptcha_frames = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
        if recaptcha_frames:
            print("Rilevato reCAPTCHA v2")
            # Verifica se è presente anche una sfida con immagini (reCAPTCHA v2 con challenge)
            # Cerca frame interni o elementi dell'interfaccia del challenge
            image_challenge_frames = driver.find_elements(By.XPATH, "//iframe[contains(@title, 'recaptcha challenge') or contains(@title, 'sfida reCAPTCHA')]")
            
            if image_challenge_frames:
                print("Rilevata sfida reCAPTCHA con immagini")
                # Se c'è una sfida di immagini, restituisci il tipo specifico
                # Cerca il sitekey
                page_source = driver.page_source
                site_key_match = re.search(r'(?:data-sitekey|sitekey)=["\']([^"\']+)["\']', page_source)
                sitekey = None
                if site_key_match:
                    sitekey = site_key_match.group(1)
                else:
                    # Estrai il sitekey dall'URL dell'iframe
                    for frame in recaptcha_frames:
                        frame_src = frame.get_attribute("src")
                        k_match = re.search(r'k=([^&]+)', frame_src)
                        if k_match:
                            sitekey = k_match.group(1)
                            break
                
                return "recaptcha_v2_image", {
                    "main_frame": recaptcha_frames[0], 
                    "challenge_frame": image_challenge_frames[0],
                    "sitekey": sitekey
                }
            
            # Se non è una sfida con immagini, è un reCAPTCHA v2 standard
            # Cerca il sitekey
            page_source = driver.page_source
            site_key_match = re.search(r'(?:data-sitekey|sitekey)=["\']([^"\']+)["\']', page_source)
            if site_key_match:
                return "recaptcha_v2", {"frame": recaptcha_frames[0], "sitekey": site_key_match.group(1)}
            else:
                # Estrai il sitekey dall'URL dell'iframe
                for frame in recaptcha_frames:
                    frame_src = frame.get_attribute("src")
                    k_match = re.search(r'k=([^&]+)', frame_src)
                    if k_match:
                        return "recaptcha_v2", {"frame": frame, "sitekey": k_match.group(1)}
            
            # Se non troviamo il sitekey, restituisci comunque il frame
            return "recaptcha_v2", {"frame": recaptcha_frames[0]}
            
        # Controlla se è un hCaptcha
        hcaptcha_frames = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'hcaptcha')]")
        if hcaptcha_frames:
            print("Rilevato hCaptcha")
            return "hcaptcha", {"frame": hcaptcha_frames[0]}
            
        # Controlla se è un CAPTCHA personalizzato di Spotify (checkmark o immagine)
        spotify_captcha_elements = driver.find_elements(By.XPATH, 
            "//*[contains(@class, 'captcha') or contains(@id, 'captcha') or contains(@aria-labelledby, 'captcha')]")
        if spotify_captcha_elements:
            print("Rilevato possibile CAPTCHA personalizzato di Spotify")
            return "spotify_custom", {"elements": spotify_captcha_elements}
            
        # Controlla se ci sono indicazioni di robot check nel testo della pagina
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        if "robot" in body_text or "captcha" in body_text or "verifica" in body_text or "seleziona" in body_text:
            print("Rilevato testo indicativo di verifica robot")
            # Cerca pulsanti specifici per la verifica
            button_elements = driver.find_elements(By.XPATH, 
                "//button[contains(., 'Verifica') or contains(., 'Verify') or contains(., 'Continua') or contains(., 'Continue') or contains(@id, 'recaptcha')]")
            
            # Cerca anche elementi di selezione immagini tipici dei CAPTCHA visivi
            image_grid = driver.find_elements(By.XPATH, 
                "//*[contains(@class, 'rc-imageselect-table') or contains(@class, 'imageselect')]")
            
            if image_grid:
                print("Rilevata griglia di selezione immagini")
                return "image_challenge", {"grid": image_grid[0]}
            
            return "spotify_challenge", {"buttons": button_elements}
        
        return "sconosciuto", {}
    except Exception as e:
        print(f"Errore nel rilevamento del CAPTCHA: {str(e)}")
        return "errore", {"error": str(e)}

def gestisci_captcha_spotify(driver, api_key):
    """
    Gestione specifica per i CAPTCHA di Spotify
    """
    print("Avvio rilevamento CAPTCHA specifico per Spotify...")
    captcha_type, elements = rileva_tipo_captcha_spotify(driver)
    
    print(f"Tipo di CAPTCHA rilevato: {captcha_type}")
    
    if captcha_type == "recaptcha_v2":
        # Se abbiamo già il sitekey lo utilizziamo, altrimenti lo troviamo
        sitekey = elements.get("sitekey")
        if not sitekey:
            # Cerca di trovare il sitekey
            frame = elements.get("frame")
            if frame:
                try:
                    # Passa all'iframe del reCAPTCHA
                    driver.switch_to.frame(frame)
                    # Cerca elementi nel frame che possono contenere il sitekey
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()
        
        # NUOVO: Prima di risolvere con 2captcha, tenta di cliccare direttamente sulla checkbox
        try:
            frame = elements.get("frame")
            if frame:
                driver.switch_to.frame(frame)
                # Cerca la checkbox del reCAPTCHA
                try:
                    checkbox = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-border"))
                    )
                    if checkbox.is_displayed() and checkbox.is_enabled():
                        print("Trovata checkbox reCAPTCHA in Spotify, tentativo di click diretto")
                        # Uso ActionChains per un click più preciso
                        ActionChains(driver).move_to_element(checkbox).click().perform()
                        sleep(2)
                except Exception as box_error:
                    print(f"Errore nel click diretto della checkbox: {str(box_error)}")
                driver.switch_to.default_content()
        except Exception as frame_error:
            print(f"Errore nell'interazione con il frame reCAPTCHA: {str(frame_error)}")
            driver.switch_to.default_content()
        
        return risolvi_recaptcha_v2(driver, api_key)
        
    elif captcha_type == "hcaptcha":
        return risolvi_hcaptcha(driver, api_key)
        
    elif captcha_type == "spotify_custom" or captcha_type == "spotify_challenge":
        # Per i CAPTCHA personalizzati di Spotify, prova a cliccare sui pulsanti rilevanti
        try:
            if captcha_type == "spotify_challenge" and elements.get("buttons"):
                for button in elements.get("buttons"):
                    print(f"Tentativo di cliccare sul pulsante: {button.text}")
                    # Usa ActionChains per un click più affidabile
                    ActionChains(driver).move_to_element(button).click().perform()
                    sleep(2)
                    # Verifica se siamo andati oltre
                    if "robot" not in driver.find_element(By.TAG_NAME, "body").text.lower():
                        return True
            
            # Se abbiamo trovato elementi specifici del CAPTCHA
            if captcha_type == "spotify_custom" and elements.get("elements"):
                for element in elements.get("elements"):
                    try:
                        # Tenta di interagire con l'elemento usando ActionChains
                        ActionChains(driver).move_to_element(element).click().perform()
                        sleep(1)
                    except:
                        pass
                
                # Cerca pulsanti di conferma/verifica con un XPath più ampio
                buttons = driver.find_elements(By.XPATH, 
                    "//button[contains(., 'Verifica') or contains(., 'Verify') or contains(., 'Continua') or contains(., 'Continue') or contains(., 'Submit') or contains(., 'Invia')]")
                for button in buttons:
                    try:
                        # Scorri in vista e clicca usando ActionChains
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        sleep(0.5)
                        ActionChains(driver).move_to_element(button).click().perform()
                        sleep(2)
                    except:
                        pass
                        
                # Cerca anche elementi <a> che potrebbero essere usati come pulsanti
                link_buttons = driver.find_elements(By.XPATH, 
                    "//a[contains(., 'Verifica') or contains(., 'Verify') or contains(., 'Continua') or contains(., 'Continue')]")
                for link in link_buttons:
                    try:
                        link.click()
                        sleep(2)
                    except:
                        pass
        except Exception as e:
            print(f"Errore nella gestione del CAPTCHA personalizzato: {str(e)}")
            
        # NUOVO: Dopo tutte le interazioni, premi INVIO come ultima risorsa
        try:
            active_element = driver.switch_to.active_element
            active_element.send_keys(Keys.RETURN)
            sleep(2)
            print("Inviato tasto INVIO come ultima risorsa")
        except:
            pass
            
        # Anche se non possiamo risolvere completamente, ritorniamo True per far continuare il flusso
        return True
        
    # Se è sconosciuto, prova a risolvere come reCAPTCHA v2 come fallback
    return risolvi_recaptcha_v2(driver, api_key)

def debug_captcha_screenshot(driver, name="captcha"):
    """
    Scatta uno screenshot dettagliato del CAPTCHA e della pagina
    per facilitare il debug e l'analisi delle problematiche
    """
    try:
        timestamp = int(time())
        filename = f"{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        print(f"Screenshot salvato come '{filename}'")
        
        # Cerca di fotografare anche eventuali iframe del CAPTCHA
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                # Verifica se è un iframe di CAPTCHA
                src = iframe.get_attribute("src")
                if "recaptcha" in src or "hcaptcha" in src:
                    # Passa all'iframe
                    driver.switch_to.frame(iframe)
                    driver.save_screenshot(f"{name}_frame_{i}_{timestamp}.png")
                    print(f"Screenshot dell'iframe {i} salvato")
                    # Torna al contenuto principale
                    driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                continue
        return True
    except Exception as e:
        print(f"Errore nel salvare gli screenshot di debug: {str(e)}")
        return False






