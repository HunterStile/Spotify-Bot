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
file = 'account_spotify.csv'       #CSV per eseguire gli accessi agli account              
a = 1                              #tempo minimo di attesa negli slepp 
b = 2                              #tempo massimo di attesa negli slepp
count = 0                          #sommattore generico

#XPATH dei bottoni spotify
menu_canzone = '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div[{}]/div/div[5]/button[2]'
aggiungi_playlist = '//*[@id="tippy-2"]/ul/div/li[{}]/button'

posizione_brano = '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[{}]/div/div[1]/div/button'
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
def configurazione_browser(user_agent):
    chrome_driver_path = leggi_txt(path_driver)  # Path di ChromeDriver dal tuo file
    chrome_binary_path = leggi_txt(path_chrome)  # Path di Chrome.exe dal tuo file

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_binary_path

    # Imposta User-Agent personalizzato
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Disabilita automazioni visibili
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Altri parametri utili
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")

    # Imposta la posizione della finestra se vuoi su secondo monitor
    chrome_options.add_argument("window-position=1920,0")
    chrome_options.add_argument("start-maximized")

    # Inizializza il driver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # Applica stealth per evitare detection
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

    print("[BOT] Browser configurato e pronto")
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
def crea_account(driver,proxy,stop_for_robot):
    #variabili - logiche
    robot2 = False
    robot = False
    creato = False
    
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
    if proxy == True :
        config_file_name = random.choice(PROXYLIST)
        change_proxy(config_file_name)
      
    #FINE CREAZIONE ACCCOUNT
    
    #CHECK ROBOT
    page_text = check_conferma(driver)
    robot  = "Crea" in page_text
    sleep(randint(2,3))
    
    if robot==True:
       driver.find_element(By.XPATH,'//*[@id="encore-web-main-content"]/div/div/div/div/div/button/span[1]').click()
       sleep(randint(4,5))
    robot2 = "Continua" in page_text
    
    while robot2==True:
       if stop_for_robot==True:
        print("Richiesta robot")
        return True
       print("richiesta robot...")
       url = driver.current_url
       #risolvi_captcha(driver,url)
       sleep(5)
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
    link_accesso = 'https://open.spotify.com/'
    driver.get(link_accesso)
    sleep(randint(2,3))
    driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
    sleep(randint(a,b))           
    driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[1]/div[3]/div[1]/button[2]').click()
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="login-username"]').send_keys(email)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="login-password"]').send_keys(password)
    sleep(randint(a,b))
    driver.find_element(By.XPATH,'//*[@id="login-button"]').click()
    sleep(randint(4,5))
    page_text = check_conferma(driver)
    errore  = "errati" in page_text
    if errore == False:
        print("Accesso eseguito correttamente!")
    else:
        print("Errore, dati non corretti.")
    return errore

#Ascolto una specifica canzone in una playlit
def Sento_canzone(driver,posizione):
    print("Ascolto la canzone..")
    xpath = generate_xpath(posizione_brano,posizione)
    print(f"posizione :",posizione)
    posizione_scelta(driver,xpath)

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






