from funzioni.spotify_functions import *
from config import *

## >main<
ripetizione = True
count = 0

while ripetizione == True:
    count = count + 1
    print(count,"*account in creazione")
    driver = configurazione_browser()
    crea_account(driver)
    input("Fai Quello che devi..")
    ripetizione == True













