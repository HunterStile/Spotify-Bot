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
import re
import os
import subprocess
import pyautogui
from config import *

# Ottieni il percorso assoluto della directory corrente (dove si trova il file eseguibile)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Costruisci il percorso assoluto della cartella "Setup"
setup_dir = os.path.join(current_dir, 'Setup')
# Costruisci i percorsi assoluti dei file di testo
path_chrome = os.path.join(setup_dir, 'path_chrome.txt')
path_driver = os.path.join(setup_dir, 'path_driver.txt')

#Variabili per il funzionamento
file = 'account_spotify.csv'       #CSV per eseguire gli accessi agli account              
a = 1                              #tempo minimo di attesa negli slepp 
b = 2                              #tempo massimo di attesa negli slepp
count = 0                          #sommattore generico

#XPATH dei bottoni spotify
menu_canzone = '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div[{}]/div/div[5]/button[2]'
aggiungi_playlist = '//*[@id="tippy-2"]/ul/div/li[{}]/button'
posizione_brano = '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[{}]/div/div[1]'
posizione_seguo_playlist = '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[2]/div[2]/div/div/button[1]'
                    

# FUNZIONI BASE #

#Inserisce il proxy dato
def changhe_proxy(config_file_name):
    proxifier_exe_path = "C:\\Program Files (x86)\\Proxifier\\proxifier.exe"
    config_file_path = "C:\\Users\\Luigi\\AppData\\Roaming\\Proxifier4\\Profiles\\" + config_file_name
    command = f'"{proxifier_exe_path}" -load "{config_file_path}"'
    subprocess.Popen(command)
    sleep(2)
    pyautogui.press('enter')
    sleep(2)
    pyautogui.press('enter')
    sleep(10)
    print(f"Proxy configurato: {config_file_name}")   

#Configurazione del browser
def configurazione_browser():
    chrome_driver_path = leggi_txt(path_driver)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = leggi_txt(path_chrome)
    # Imposta la posizione della finestra per il secondo schermo
    chrome_options.add_argument("window-position=1920,0")
    driver =Chrome(service=Service(chrome_driver_path),options=chrome_options)
    sleep(randint(a,b))
    return driver

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
    
# FUNZIONI SPOTIFY #

#Crea un account spotify
def crea_account(driver,proxy):
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
    mesi = ['gennaio','febbraio','marzo','aprile','maggio','giguno','luglio','agosto','settembre','ottobre''novembre''dicembre']
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
        changhe_proxy(config_file_name)
      
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
            print('Playlist seguite!')
    else:
        print('Account non creato.., riprovo.')

    return email,password,driver

#Seguo la playlist
def seguo_playlist(driver,link):
    try:
        driver.get(link)
        sleep(randint(4,5))                     
        driver.find_element(By.XPATH,posizione_seguo_playlist).click()
        sleep(randint(4,5))
        print("Playlist seguita!")
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






