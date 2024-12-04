from funzioni.spotify_functions import *
from config import *

driver= configurazione_browser()
if TIPO_ROUTER == 'tim':
    reset_router_tim(driver)

elif TIPO_ROUTER == 'vodafone':
    reset_router_vodafone(driver)