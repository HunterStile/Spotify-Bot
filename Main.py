from funzioni.spotify_functions import *
import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from config import PROXYLIST, TARGET_SITES, MAX_BOTS, MIN_TIME, MAX_TIME, ENABLE_SCROLL, ENABLE_CLICKS
from utils import change_proxy, get_random_user_agent


# Funzione comportamento umano
def simulate_user_behavior(driver, stay_time):
    start_time = time.time()
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    last_scroll = 0

    while (time.time() - start_time) < stay_time:
        action = random.choice(['scroll', 'move_mouse', 'click', 'idle'])

        if action == 'scroll' and ENABLE_SCROLL:
            scroll_to = random.randint(last_scroll, scroll_height)
            driver.execute_script(f"window.scrollTo(0, {scroll_to});")
            print(f"[INFO] Scrolled to {scroll_to}px")
            last_scroll = scroll_to
            time.sleep(random.uniform(2, 5))

        elif action == 'move_mouse':
            x, y = random.randint(0, 800), random.randint(0, 600)
            driver.execute_script(f"document.elementFromPoint({x}, {y}).scrollIntoView(true);")
            print(f"[INFO] Moved mouse to ({x}, {y})")
            time.sleep(random.uniform(1, 3))

        elif action == 'click' and ENABLE_CLICKS:
            links = driver.find_elements(By.TAG_NAME, 'a')
            if links:
                link = random.choice(links)
                try:
                    link.click()
                    print(f"[INFO] Clicked on a link.")
                    time.sleep(random.uniform(3, 7))
                except:
                    print("[INFO] Failed to click a link.")

        elif action == 'idle':
            print("[INFO] Idle...")
            time.sleep(random.uniform(2, 4))


# Funzione principale per un bot singolo
def start_bot(proxy_profile):
    try:
        print(f"[BOT] Starting bot with proxy profile: {proxy_profile}")

        # Cambia proxy con Proxifier
        change_proxy(proxy_profile)

        # Configura User-Agent
        user_agent = get_random_user_agent()

        # Configura Chrome con stealth + user agent
        driver = configurazione_browser(user_agent)

        # Scegli sito random
        site = random.choice(TARGET_SITES)
        print(f"[BOT] Visiting site: {site}")
        driver.get(site)

        # Resta sul sito e simula comportamento
        stay_time = random.randint(MIN_TIME, MAX_TIME)
        print(f"[BOT] Staying on site for {stay_time} seconds")
        simulate_user_behavior(driver, stay_time)

        print("[BOT] Done. Closing browser.")
        driver.quit()

    except Exception as e:
        print(f"[ERROR] Bot failed: {e}")
        try:
            driver.quit()
        except:
            pass


# Funzione per gestire i bot multipli
def start_bots():
    threads = []
    for i in range(MAX_BOTS if MAX_BOTS > 0 else 1):
        proxy_profile = random.choice(PROXYLIST)
        t = threading.Thread(target=start_bot, args=(proxy_profile,))
        t.start()
        threads.append(t)
        time.sleep(random.uniform(2, 5))  # Piccola pausa per non farli partire tutti insieme

    # Attendere che tutti finiscano
    for t in threads:
        t.join()


if __name__ == "__main__":
    start_bots()
