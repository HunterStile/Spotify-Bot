from funzioni.spotify_functions import *
from config import *

## >main<
ripetizione = True
count = 0
una_creazione = False

while ripetizione == True:
    count = count + 1
    print(count,"*account in creazione")
    driver = configurazione_browser()
    crea_account(driver)
    if una_creazione == True:
        input("Fai Quello che devi..")
    ripetizione == True













