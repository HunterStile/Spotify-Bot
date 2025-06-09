#librerie
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import randint
import re
import requests
import json
import csv
import os
from datetime import datetime

# Importa le funzioni esistenti
from funzioni.spotify_functions import (
    configurazione_browser, 
    get_random_user_agent, 
    check_conferma,
    get_resource_path
)

#Variabili globali
a = 1
b = 3

# FUNZIONI PER ARTIST SCRAPING #

def scraping_artisti_da_playlist(driver, playlist_url, max_artisti=50, soglia_ascoltatori=100000):
    """
    Estrae gli artisti da una playlist Spotify con filtro su ascoltatori mensili
    
    Args:
        driver: WebDriver Selenium
        playlist_url: URL della playlist Spotify
        max_artisti: Numero massimo di artisti da estrarre
        soglia_ascoltatori: Soglia massima di ascoltatori mensili (default 100k)
    
    Returns:
        List[dict]: Lista di artisti con informazioni base
    """
    print(f"🎵 Analizzando playlist: {playlist_url}")
    artisti_emergenti = []
    
    try:
        # Naviga alla playlist
        driver.get(playlist_url)
        sleep(randint(3, 5))
        
        # Accetta cookie se presenti
        try:
            cookie_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
            )
            cookie_button.click()
            print("Cookie accettati")
        except (NoSuchElementException, TimeoutException):
            pass
        
        # Scroll per caricare più brani
        scroll_playlist(driver)
        artisti_processati = set()  # Per evitare duplicati
        tracks_processed = 0
          # Loop per processare artisti senza riferimenti stale
        while len(artisti_emergenti) < max_artisti and tracks_processed < max_artisti * 2:
            try:
                # Re-trova i brani ogni volta per evitare stale element reference
                brani_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
                
                if tracks_processed >= len(brani_elements):
                    print("📋 Fine brani disponibili nella playlist")
                    break
                
                brano = brani_elements[tracks_processed]
                
                # Estrai nome artista dal brano corrente
                artist_link = brano.find_element(By.CSS_SELECTOR, 'a[href*="/artist/"]')
                artist_name = artist_link.text.strip()
                artist_url = artist_link.get_attribute('href')
                
                tracks_processed += 1
                
                # Evita duplicati
                if artist_name in artisti_processati:
                    print(f"⏭️ Artista già processato: {artist_name}")
                    continue
                    
                artisti_processati.add(artist_name)
                
                print(f"🎤 Analizzando artista {tracks_processed}/{len(brani_elements)}: {artist_name}")
                
                # Vai alla pagina dell'artista per ottenere dettagli
                dettagli_artista = get_artist_details(driver, artist_url, soglia_ascoltatori)
                
                if dettagli_artista:
                    artisti_emergenti.append(dettagli_artista)
                    print(f"✅ Artista emergente aggiunto: {artist_name} ({len(artisti_emergenti)}/{max_artisti})")
                else:
                    print(f"❌ Artista scartato (troppi ascoltatori): {artist_name}")
                    
                # Torna alla playlist con retry logic
                print("🔙 Tornando alla playlist...")
                retry_count = 0
                max_retries = 3
                
                while retry_count < max_retries:
                    try:
                        driver.back()
                        sleep(randint(2, 4))
                        
                        # Aspetta che la playlist sia caricata
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tracklist-row"]'))
                        )
                        break  # Successo, esci dal retry loop
                        
                    except Exception as retry_error:
                        retry_count += 1
                        print(f"⚠️ Retry {retry_count}/{max_retries} per tornare alla playlist: {str(retry_error)}")
                        if retry_count >= max_retries:
                            print("❌ Impossibile tornare alla playlist dopo 3 tentativi")
                            raise retry_error
                        sleep(2)
                
            except Exception as e:
                print(f"⚠️ Errore processing artista {tracks_processed}: {str(e)}")
                tracks_processed += 1
                
                # Se errore critico, prova a tornare alla playlist
                try:
                    driver.get(playlist_url)
                    sleep(randint(3, 5))
                except:
                    pass
                    
                continue
                
    except Exception as e:
        print(f"❌ Errore durante scraping playlist: {str(e)}")
    
    print(f"🎯 Trovati {len(artisti_emergenti)} artisti emergenti!")
    return artisti_emergenti

def scroll_playlist(driver, max_scrolls=5):
    """
    Effettua scroll sulla playlist per caricare più contenuti
    """
    print("📜 Caricamento contenuti playlist...")
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(randint(1, 2))
    
    # Torna in alto
    driver.execute_script("window.scrollTo(0, 0);")
    sleep(1)

def get_artist_details(driver, artist_url, soglia_ascoltatori):
    """
    Ottiene dettagli di un artista dalla sua pagina Spotify
    
    Args:
        driver: WebDriver Selenium
        artist_url: URL della pagina dell'artista
        soglia_ascoltatori: Soglia massima ascoltatori mensili
    
    Returns:
        dict: Dettagli artista se emergente, None altrimenti
    """
    try:
        driver.get(artist_url)
        sleep(randint(2, 4))
          # Estrai nome artista - selettori aggiornati dal tuo HTML
        try:
            # Nuovo selettore basato sul tuo HTML: span con classe "rEN7ncpaUeSGL9z0NGQR"
            selectors_name = [
                'span.rEN7ncpaUeSGL9z0NGQR span[data-encore-id="adaptiveTitle"]',  # Dal tuo HTML
                'span[data-testid="adaptiveEntityTitle"] span[data-encore-id="adaptiveTitle"]',
                'h1[data-testid="entityTitle"]',  # Fallback precedente
                'h1[class*="encore-text-headline"]',
                'span[class*="encore-text-headline"]'
            ]
            
            artist_name = "Nome non trovato"
            for selector in selectors_name:
                try:
                    artist_name_element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    artist_name = artist_name_element.text.strip()
                    if artist_name:
                        print(f"[DEBUG] Nome artista trovato: '{artist_name}'")
                        break
                except:
                    continue
        except:
            artist_name = "Nome non trovato"
        
        # Estrai ascoltatori mensili
        ascoltatori_mensili = extract_monthly_listeners(driver)
        
        # Filtra per soglia ascoltatori
        if ascoltatori_mensili and ascoltatori_mensili > soglia_ascoltatori:
            return None
        
        # Estrai generi musicali
        generi = extract_genres(driver)
        
        # Estrai biografia
        biografia = extract_biography(driver)
          # Estrai link social dalla biografia E dalla pagina
        social_links = extract_social_links_comprehensive(driver, biografia)
        
        # Estrai data ultima release
        data_ultima_release = extract_career_span(driver)
        
        return {
            'nome': artist_name,
            'spotify_url': artist_url,
            'ascoltatori_mensili': ascoltatori_mensili,
            'generi': generi,
            'biografia': biografia,
            'social_links': social_links,
            'data_uscita': data_ultima_release,
            'data_scraping': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        print(f"⚠️ Errore dettagli artista: {str(e)}")
        return None

def extract_monthly_listeners(driver):
    """
    Estrae il numero di ascoltatori mensili dall'artista
    """
    try:
        # Nuovi selettori aggiornati basati sull'HTML fornito
        selectors = [
            'span.Ydwa1P5GkCggtLlSvphs',  # Nuovo selettore dal tuo HTML
            'span[class*="Ydwa1P"]',      # Fallback per variazioni di classe
            '[data-testid="monthly-listeners"]',
            'span:contains("ascoltatori mensili")',
            'div:contains("ascoltatori mensili")',
            'span:contains("monthly listeners")',
            'div:contains("monthly listeners")'
        ]
        
        for selector in selectors:
            try:
                if ':contains(' in selector:
                    # Per selettori con :contains, usiamo XPath
                    if 'ascoltatori mensili' in selector:
                        xpath = f"//span[contains(text(), 'ascoltatori mensili')]"
                    else:
                        xpath = f"//span[contains(text(), 'monthly listeners')]"
                    listener_element = driver.find_element(By.XPATH, xpath)
                else:
                    listener_element = driver.find_element(By.CSS_SELECTOR, selector)
                    text = listener_element.text
                print(f"[DEBUG] Testo trovato per ascoltatori: '{text}'")                # Estrai numero dagli ascoltatori mensili
                # Spotify Italia formato: "24.363", "1.551.379", "69.467.427" 
                # Punto = separatore migliaia (mai decimali)
                numbers = re.findall(r'[\d\.]+', text)
                if numbers:
                    num_str = numbers[0]
                    print(f"[DEBUG] Numero estratto: '{num_str}'")
                    
                    # In Spotify Italia il punto è SEMPRE separatore migliaia
                    # Esempi: "24.363" = 24363, "69.467.427" = 69467427
                    clean_num = num_str.replace('.', '')
                    print(f"[DEBUG] Formato Spotify Italia: {num_str} -> {clean_num}")
                    
                    try:
                        result = int(clean_num)
                        print(f"[DEBUG] Ascoltatori convertiti: {result:,}")
                        return result
                    except ValueError:
                        print(f"[DEBUG] Errore conversione: {clean_num}")
                        continue
            except:
                continue
                
        # Se non trovato tramite selettori specifici, cerca nel testo della pagina
        page_text = driver.find_element(By.TAG_NAME, 'body').text.lower()
        monthly_matches = re.findall(r'(\d+[,\.]?\d*)\s*[km]?\s*monthly\s*listeners', page_text)
        
        if monthly_matches:
            num_str = monthly_matches[0].replace(',', '').replace('.', '')
            if 'k' in page_text:
                return int(float(num_str) * 1000)
            elif 'm' in page_text:
                return int(float(num_str) * 1000000)
            else:
                return int(num_str) if num_str.isdigit() else None
                
        return None
        
    except Exception as e:
        print(f"⚠️ Errore estrazione ascoltatori: {str(e)}")
        return None

def extract_genres(driver):
    """
    Estrae i generi musicali dell'artista
    """
    try:
        generi = []
        # Cerca elementi che potrebbero contenere generi
        genre_selectors = [
            'a[href*="/genre/"]',
            'span[class*="genre"]',
            'div[class*="genre"]'
        ]
        
        for selector in genre_selectors:
            try:
                genre_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in genre_elements:
                    genre_text = element.text.strip()
                    if genre_text and genre_text not in generi:
                        generi.append(genre_text)
            except:
                continue
                
        return generi[:5]  # Limita a 5 generi
    except:
        return []

def extract_biography(driver):
    """
    Estrae la biografia dell'artista dalla sezione "Informazioni su"
    """
    try:
        # Scroll per cercare la sezione biografia
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        sleep(2)
        
        # Cerca diversi selettori per la biografia
        bio_selectors = [
            '[data-testid="about"]',
            'div[class*="about"]',
            'section[class*="about"]',
            'div[class*="biography"]',
            'p[class*="bio"]'
        ]
        
        for selector in bio_selectors:
            try:
                bio_element = driver.find_element(By.CSS_SELECTOR, selector)
                bio_text = bio_element.text.strip()
                if len(bio_text) > 50:  # Solo biografie significative
                    return bio_text
            except:
                continue
                
        return "Biografia non disponibile"
        
    except Exception as e:
        print(f"⚠️ Errore estrazione biografia: {str(e)}")
        return "Biografia non disponibile"

def extract_social_links_comprehensive(driver, biografia):
    """
    Estrae link social sia dalla biografia che dalla pagina artista (pulsanti social)
    """
    social_links = {
        'instagram': [],
        'email': [],
        'facebook': [],
        'twitter': [],
        'youtube': [],
        'altri_link': []
    }
    
    try:
        # 1. Estrai dalla biografia (metodo esistente)
        bio_links = extract_social_links_from_bio(biografia)
        
        # Unisci i risultati dalla biografia
        for platform in social_links:
            social_links[platform].extend(bio_links.get(platform, []))
        
        # 2. Cerca pulsanti social nella pagina artista
        print("🔍 Cercando pulsanti social nella pagina...")
        
        # Selettori per pulsanti social di Spotify
        social_selectors = {
            'instagram': [
                'a[href*="instagram.com"]',
                'a[aria-label*="Instagram"]',
                '[data-testid*="instagram"]'
            ],
            'facebook': [
                'a[href*="facebook.com"]',
                'a[aria-label*="Facebook"]',
                '[data-testid*="facebook"]'
            ],
            'twitter': [
                'a[href*="twitter.com"]',
                'a[href*="x.com"]',
                'a[aria-label*="Twitter"]',
                '[data-testid*="twitter"]'
            ],
            'youtube': [
                'a[href*="youtube.com"]',
                'a[href*="youtu.be"]',
                'a[aria-label*="YouTube"]',
                '[data-testid*="youtube"]'
            ]
        }
        
        # Cerca i link social
        for platform, selectors in social_selectors.items():
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute('href')
                        if href and platform not in href.lower():
                            continue
                        if href and href not in social_links[platform]:
                            # Estrai username dal link
                            if platform == 'instagram':
                                username = extract_instagram_username(href)
                                if username and username not in social_links[platform]:
                                    social_links[platform].append(username)
                            elif platform == 'facebook':
                                username = extract_facebook_username(href)
                                if username and username not in social_links[platform]:
                                    social_links[platform].append(username)
                            elif platform == 'twitter':
                                username = extract_twitter_username(href)
                                if username and username not in social_links[platform]:
                                    social_links[platform].append(username)
                            elif platform == 'youtube':
                                username = extract_youtube_username(href)
                                if username and username not in social_links[platform]:
                                    social_links[platform].append(username)
                            
                            print(f"📱 Trovato {platform}: {href}")
                except Exception as e:
                    continue
        
        # 3. Cerca nella sezione "About" se presente
        try:
            about_section = driver.find_element(By.CSS_SELECTOR, '[data-testid="about"]')
            about_text = about_section.text.lower()
            
            # Estrai contatti dalla sezione about
            email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            emails = re.findall(email_pattern, about_text)
            for email in emails:
                if email not in social_links['email']:
                    social_links['email'].append(email)
                    print(f"📧 Email trovata in About: {email}")
        except:
            pass
        
        # 4. Cerca link esterni generici
        try:
            external_links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="http"]:not([href*="spotify.com"])')
            for link in external_links[:5]:  # Limite per performance
                href = link.get_attribute('href')
                if href and not any(platform in href.lower() for platform in ['instagram', 'facebook', 'twitter', 'youtube']):
                    if href not in social_links['altri_link']:
                        social_links['altri_link'].append(href)
        except:
            pass
            
    except Exception as e:
        print(f"⚠️ Errore estrazione social completa: {str(e)}")
    
    return social_links

def extract_instagram_username(url):
    """Estrae username Instagram da URL"""
    try:
        match = re.search(r'instagram\.com/([a-zA-Z0-9._]+)', url)
        return match.group(1) if match else None
    except:
        return None

def extract_facebook_username(url):
    """Estrae username Facebook da URL"""
    try:
        match = re.search(r'facebook\.com/([a-zA-Z0-9._]+)', url)
        return match.group(1) if match else None
    except:
        return None

def extract_twitter_username(url):
    """Estrae username Twitter da URL"""
    try:
        match = re.search(r'(?:twitter\.com|x\.com)/([a-zA-Z0-9._]+)', url)
        return match.group(1) if match else None
    except:
        return None

def extract_youtube_username(url):
    """Estrae username YouTube da URL"""
    try:
        match = re.search(r'youtube\.com/(?:c/|channel/|user/)?([a-zA-Z0-9._-]+)', url)
        return match.group(1) if match else None
    except:
        return None

def extract_social_links_from_bio(biografia):
    """
    Estrae link social e email dalla biografia usando regex
    """
    social_links = {
        'instagram': [],
        'email': [],
        'facebook': [],
        'twitter': [],
        'youtube': [],
        'altri_link': []
    }
    
    try:
        if not biografia or biografia == "Biografia non disponibile":
            return social_links
            
        text = biografia.lower()
        
        # Regex patterns per diversi tipi di contatti
        patterns = {
            'instagram': [
                r'@([a-zA-Z0-9._]+)',
                r'instagram\.com/([a-zA-Z0-9._]+)',
                r'ig:\s*([a-zA-Z0-9._]+)'
            ],
            'email': [
                r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ],
            'facebook': [
                r'facebook\.com/([a-zA-Z0-9._]+)',
                r'fb\.com/([a-zA-Z0-9._]+)'
            ],
            'twitter': [
                r'twitter\.com/([a-zA-Z0-9._]+)',
                r'@([a-zA-Z0-9._]+).*twitter'
            ],
            'youtube': [
                r'youtube\.com/([a-zA-Z0-9._]+)',
                r'youtu\.be/([a-zA-Z0-9._]+)'
            ]
        }
        
        # Applica i pattern
        for platform, platform_patterns in patterns.items():
            for pattern in platform_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if match and match not in social_links[platform]:
                        social_links[platform].append(match)
        
        # Cerca altri link generici
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, biografia)
        for url in urls:
            if not any(platform in url.lower() for platform in ['instagram', 'facebook', 'twitter', 'youtube']):
                if url not in social_links['altri_link']:
                    social_links['altri_link'].append(url)
        
    except Exception as e:
        print(f"⚠️ Errore estrazione social links: {str(e)}")
    
    return social_links

def scrape_artist_contacts_web(artist_name, num_results=5):
    """
    Cerca contatti aggiuntivi dell'artista sul web usando Google Search
    (Questa funzione richiede cautela per non violare ToS)
    """
    contacts = {
        'email_trovate': [],
        'social_trovati': [],
        'siti_ufficiali': []
    }
    
    try:
        # Search query per l'artista
        search_queries = [
            f'"{artist_name}" contact email music',
            f'"{artist_name}" instagram music artist',
            f'"{artist_name}" official website'
        ]
        
        print(f"🔍 Ricerca web per: {artist_name}")
        
        # Qui puoi implementare una ricerca web più sofisticata
        # Per ora restituisce un placeholder
        print("⚠️ Ricerca web non implementata in questa versione")
        
    except Exception as e:
        print(f"⚠️ Errore ricerca web: {str(e)}")
    
    return contacts

def save_artists_to_csv(artisti_list, filename="artisti_emergenti.csv"):
    """
    Salva la lista degli artisti in un file CSV
    """
    try:
        filepath = os.path.join(os.getcwd(), filename)        # Headers per il CSV - Solo dati utili
        headers = [
            'Nome Artista',
            'Spotify URL', 
            'Ascoltatori Mensili',
            'Data Scraping',
            'Periodo Carriera'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for artista in artisti_list:
                # Prepara i dati per il CSV - Solo dati utili
                row = [
                    artista.get('nome', ''),
                    artista.get('spotify_url', ''),
                    artista.get('ascoltatori_mensili', ''),
                    artista.get('data_scraping', ''),
                    artista.get('data_uscita', '')
                ]
                writer.writerow(row)
        
        print(f"💾 Dati salvati in: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Errore salvataggio CSV: {str(e)}")
        return None

def analizza_multiple_playlists(driver, playlist_urls, max_artisti_per_playlist=20, soglia_ascoltatori=100000):
    """
    Analizza multiple playlist per trovare artisti emergenti
    """
    tutti_artisti = []
    artisti_unici = set()
    
    print(f"🎵 Analizzando {len(playlist_urls)} playlist...")
    
    for idx, playlist_url in enumerate(playlist_urls):
        print(f"\n📋 Playlist {idx+1}/{len(playlist_urls)}")
        
        try:
            artisti_playlist = scraping_artisti_da_playlist(
                driver, 
                playlist_url, 
                max_artisti_per_playlist, 
                soglia_ascoltatori
            )
            
            # Evita duplicati globali
            for artista in artisti_playlist:
                nome = artista.get('nome', '')
                if nome not in artisti_unici:
                    artisti_unici.add(nome)
                    tutti_artisti.append(artista)
            
            print(f"✅ Playlist completata. Artisti unici totali: {len(tutti_artisti)}")
            
            # Pausa tra playlist
            sleep(randint(3, 6))
            
        except Exception as e:
            print(f"❌ Errore playlist {idx+1}: {str(e)}")
            continue
    
    return tutti_artisti

# FUNZIONI DI CONFIGURAZIONE #

def get_artist_scraper_config():
    """
    Configurazione di default per l'artist scraper
    """
    return {
        'max_artisti_per_playlist': 30,
        'soglia_ascoltatori_max': 100000,  # 100k ascoltatori mensili
        'usa_proxy': False,
        'enable_web_search': False,
        'output_filename': 'artisti_emergenti.csv',
        'playlist_curatori': [
            'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',  # Today's Top Hits
            'https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd',  # Global Top 50
            'https://open.spotify.com/playlist/37i9dQZF1DXarRatq9Oe86',  # New Music Friday
        ]
    }

def esegui_artist_scraper(config):
    """
    Funzione principale per eseguire l'artist scraper
    """
    print("🎤 SPOTIFY ARTIST SCRAPER AVVIATO")
    print("="*50)
    
    driver = None
    
    try:
        # Configurazione browser
        user_agent = get_random_user_agent()
        driver = configurazione_browser(user_agent, 
                                       disable_stealth=not config.get('usa_stealth', True), 
                                       secondo_schermo=config.get('secondo_schermo', False))
        
        if not driver:
            print("❌ Errore configurazione browser")
            return
        
        # Ottieni lista playlist da analizzare
        playlist_urls = config.get('playlist_curatori', [])
        
        if not playlist_urls:
            print("❌ Nessuna playlist specificata")
            return
        
        # Analizza le playlist
        artisti_emergenti = analizza_multiple_playlists(
            driver,
            playlist_urls,
            config.get('max_artisti_per_playlist', 30),
            config.get('soglia_ascoltatori_max', 100000)
        )
        
        if not artisti_emergenti:
            print("❌ Nessun artista emergente trovato")
            return
        
        # Salva risultati
        output_file = save_artists_to_csv(artisti_emergenti, config.get('output_filename', 'artisti_emergenti.csv'))
        
        if output_file:
            print(f"\n🎯 RISULTATI FINALI:")
            print(f"📊 Artisti emergenti trovati: {len(artisti_emergenti)}")
            print(f"💾 File salvato: {output_file}")
            
            # Statistiche
            print(f"\n📈 STATISTICHE:")
            artisti_con_instagram = sum(1 for a in artisti_emergenti if a.get('social_links', {}).get('instagram'))
            artisti_con_email = sum(1 for a in artisti_emergenti if a.get('social_links', {}).get('email'))
            
            print(f"📱 Artisti con Instagram: {artisti_con_instagram}")
            print(f"📧 Artisti con Email: {artisti_con_email}")
        
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {str(e)}")
    
    finally:
        if driver:
            try:
                driver.quit()
                print("🔒 Browser chiuso")
            except:
                pass

def extract_career_span(driver):
    """
    Estrae il range di anni della carriera dell'artista (primo-ultimo)
    dalla discografia dell'artista (Spotify mostra solo gli anni, non date precise)
    """
    try:
        # Scroll down per vedere la sezione discografia
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        sleep(2)
        
        # Cerca il pulsante "Mostra tutto" della discografia
        try:
            show_all_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Mostra tutto')]"))
            )
            driver.execute_script("arguments[0].click();", show_all_button)
            sleep(2)
            print("[DEBUG] Cliccato su 'Mostra tutto' discografia")
        except:
            print("[DEBUG] Pulsante 'Mostra tutto' non trovato, procedo con la vista attuale")
        
        # Cerca gli anni nella discografia (Spotify mostra solo anni)
        found_years = []
        
        # Cerca tutti gli elementi che potrebbero contenere anni
        year_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'w1TBi3o5CTM7zW1EB3Bm') or contains(@class, 'encore-text') or contains(@class, 'blfR_YJUsKUvdgTejBSb')]")
        
        # Pattern per anni (espanso per includere più anni possibili)
        year_pattern = r'\b(20[0-2][0-9])\b'
        
        for element in year_elements:
            try:
                text = element.text.strip()
                if not text:
                    continue
                
                # Cerca anni nel testo
                years = re.findall(year_pattern, text)
                for year in years:
                    if year not in found_years:
                        found_years.append(year)
                        print(f"[DEBUG] Trovato anno: {year}")
                        
            except:
                continue
        
        # Se abbiamo trovato anni, restituisci il range
        if found_years:
            # Converti in interi e ordina
            years_int = [int(year) for year in found_years]
            years_int.sort()
            
            first_year = min(years_int)
            last_year = max(years_int)
            
            # Se l'artista ha solo un anno di uscite
            if first_year == last_year:
                career_span = str(first_year)
            else:
                career_span = f"{first_year}-{last_year}"
            
            print(f"[DEBUG] Range carriera: {career_span}")
            return career_span
        
        # Fallback: cerca anni specifici dal più recente al meno recente
        for year in range(2025, 2010, -1):
            try:
                year_xpath = f"//*[contains(text(), '{year}')]"
                year_elements = driver.find_elements(By.XPATH, year_xpath)
                if year_elements:
                    print(f"[DEBUG] Trovato anno fallback: {year}")
                    return str(year)
            except:
                continue
        
        return "Non trovato"
        
    except Exception as e:
        print(f"⚠️ Errore estrazione range carriera: {str(e)}")
        return "Non trovato"

if __name__ == "__main__":
    # Test della funzione
    config = get_artist_scraper_config()
    esegui_artist_scraper(config)
