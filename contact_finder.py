"""
🔍 CONTACT FINDER MODULE
Modulo per la ricerca automatica di contatti degli artisti emergenti
Analizza i CSV generati dall'Artist Scraper e cerca:
- Instagram
- Facebook  
- Email
- TikTok
- YouTube
- Twitter/X
- Siti web ufficiali
"""

import csv
import time
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import json
import os
from datetime import datetime
from urllib.parse import quote_plus, urljoin

# Importa le funzioni esistenti
from funzioni.spotify_functions import (
    configurazione_browser, 
    get_random_user_agent
)

class ContactFinder:
    """Classe principale per la ricerca contatti artisti"""
    
    def __init__(self, config=None):
        self.config = config or self.get_default_config()
        self.driver = None
        self.found_contacts = []
        
        # Pattern per riconoscere diversi social
        self.social_patterns = {
            'instagram': [
                r'instagram\.com/([a-zA-Z0-9_.]+)',
                r'@([a-zA-Z0-9_.]+)',
                r'ig\.me/([a-zA-Z0-9_.]+)'
            ],
            'facebook': [
                r'facebook\.com/([a-zA-Z0-9_.]+)',
                r'fb\.me/([a-zA-Z0-9_.]+)',
                r'fb\.com/([a-zA-Z0-9_.]+)'
            ],
            'tiktok': [
                r'tiktok\.com/@([a-zA-Z0-9_.]+)',
                r'tiktok\.com/([a-zA-Z0-9_.]+)',
                r'@([a-zA-Z0-9_.]+)'
            ],
            'twitter': [
                r'twitter\.com/([a-zA-Z0-9_.]+)',
                r'x\.com/([a-zA-Z0-9_.]+)',
                r'@([a-zA-Z0-9_.]+)'
            ],
            'youtube': [
                r'youtube\.com/channel/([a-zA-Z0-9_-]+)',
                r'youtube\.com/c/([a-zA-Z0-9_-]+)',
                r'youtube\.com/user/([a-zA-Z0-9_-]+)',
                r'youtu\.be/([a-zA-Z0-9_-]+)'
            ],
            'email': [
                r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                r'([a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,})',
                r'mail\s*:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
            ]
        }
        
    def get_default_config(self):
        """Configurazione di default per il Contact Finder"""
        return {
            'csv_input_file': 'artisti-emergenti.csv',
            'csv_output_file': 'artisti-con-contatti.csv',
            'search_engines': ['google', 'bing'],
            'max_results_per_search': 5,
            'delay_between_searches': (2, 5),
            'use_stealth_mode': True,
            'timeout': 10,
            'user_agent_rotation': True,
            'search_social_networks': ['instagram', 'facebook', 'tiktok', 'twitter', 'youtube'],
            'search_emails': True,
            'search_websites': True,
            'verify_social_profiles': True
        }
    
    def init_browser(self):
        """Inizializza il browser con configurazioni stealth"""
        try:
            chrome_options = Options()
            
            if self.config.get('use_stealth_mode', True):
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
            if self.config.get('user_agent_rotation', True):
                user_agent = get_random_user_agent()
                chrome_options.add_argument(f"--user-agent={user_agent}")
            
            # Headless opzionale
            if self.config.get('headless', False):
                chrome_options.add_argument("--headless")
                
            self.driver = webdriver.Chrome(options=chrome_options)
            
            if self.config.get('use_stealth_mode', True):
                # Rimuove proprietà webdriver
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            print("🌐 Browser inizializzato con successo")
            return True
            
        except Exception as e:
            print(f"❌ Errore inizializzazione browser: {str(e)}")
            return False
    
    def search_google(self, query, max_results=5):
        """Esegue ricerca su Google"""
        try:
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            self.driver.get(search_url)
            
            # Attendi il caricamento
            time.sleep(random.uniform(2, 4))
            
            # Cerca i risultati
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for i, result in enumerate(search_results[:max_results]):
                try:
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    
                    title = title_element.text
                    url = link_element.get_attribute("href")
                    
                    # Estrai snippet se presente
                    snippet = ""
                    try:
                        snippet_element = result.find_element(By.CSS_SELECTOR, "span[data-testid='snippet']")
                        snippet = snippet_element.text
                    except:
                        try:
                            snippet_element = result.find_element(By.CSS_SELECTOR, ".VwiC3b")
                            snippet = snippet_element.text
                        except:
                            pass
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'source': 'google'
                    })
                    
                except Exception as e:
                    continue
                    
            return results
            
        except Exception as e:
            print(f"⚠️ Errore ricerca Google: {str(e)}")
            return []
    
    def search_bing(self, query, max_results=5):
        """Esegue ricerca su Bing"""
        try:
            search_url = f"https://www.bing.com/search?q={quote_plus(query)}"
            self.driver.get(search_url)
            
            time.sleep(random.uniform(2, 4))
            
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, ".b_algo")
            
            for i, result in enumerate(search_results[:max_results]):
                try:
                    title_element = result.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_element.text
                    url = title_element.get_attribute("href")
                    
                    snippet = ""
                    try:
                        snippet_element = result.find_element(By.CSS_SELECTOR, ".b_caption p")
                        snippet = snippet_element.text
                    except:
                        pass
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'source': 'bing'
                    })
                    
                except Exception as e:
                    continue
                    
            return results
            
        except Exception as e:
            print(f"⚠️ Errore ricerca Bing: {str(e)}")
            return []
    
    def extract_contacts_from_text(self, text):
        """Estrae contatti social ed email da un testo"""
        contacts = {
            'instagram': [],
            'facebook': [],
            'tiktok': [],
            'twitter': [],
            'youtube': [],
            'email': [],
            'website': []
        }
        
        if not text:
            return contacts
            
        # Pulisci il testo
        text = text.lower().replace(' ', '')
        
        # Cerca ogni tipo di social
        for social_type, patterns in self.social_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    
                    # Pulisci e valida il match
                    clean_match = self.clean_social_handle(match, social_type)
                    if clean_match and clean_match not in contacts[social_type]:
                        contacts[social_type].append(clean_match)
        
        return contacts
    
    def clean_social_handle(self, handle, social_type):
        """Pulisce e valida un handle social"""
        if not handle:
            return None
            
        # Rimuovi caratteri non validi
        handle = re.sub(r'[^\w\.\-@]', '', handle)
        
        # Validazioni specifiche per tipo
        if social_type == 'email':
            if '@' in handle and '.' in handle:
                return handle
        elif social_type in ['instagram', 'facebook', 'tiktok', 'twitter']:
            # Rimuovi @ se presente
            handle = handle.lstrip('@')
            if len(handle) >= 3 and len(handle) <= 30:
                return handle
        elif social_type == 'youtube':
            if len(handle) >= 5:
                return handle
                
        return None
    
    def verify_social_profile(self, handle, social_type):
        """Verifica se un profilo social esiste effettivamente"""
        if not self.config.get('verify_social_profiles', True):
            return True
            
        try:
            if social_type == 'instagram':
                url = f"https://www.instagram.com/{handle}/"
            elif social_type == 'facebook':
                url = f"https://www.facebook.com/{handle}/"
            elif social_type == 'tiktok':
                url = f"https://www.tiktok.com/@{handle}"
            elif social_type == 'twitter':
                url = f"https://twitter.com/{handle}"
            elif social_type == 'youtube':
                url = f"https://www.youtube.com/c/{handle}"
            else:
                return True
                
            # Fai una richiesta HEAD per verificare l'esistenza
            response = requests.head(url, timeout=5, allow_redirects=True)
            return response.status_code == 200
            
        except:
            return True  # In caso di errore, assumiamo che esista
    
    def search_artist_contacts(self, artist_name):
        """Cerca contatti per un singolo artista"""
        print(f"🔍 Cercando contatti per: {artist_name}")
        
        all_contacts = {
            'instagram': [],
            'facebook': [],
            'tiktok': [],
            'twitter': [],
            'youtube': [],
            'email': [],
            'website': []
        }
        
        # Query di ricerca diverse
        search_queries = [
            f'"{artist_name}" instagram contact',
            f'"{artist_name}" facebook page',
            f'"{artist_name}" email booking',
            f'"{artist_name}" social media',
            f'"{artist_name}" official website',
            f'"{artist_name}" tiktok',
            f'"{artist_name}" twitter',
            f'"{artist_name}" youtube channel'
        ]
        
        # Esegui ricerche
        for query in search_queries:
            print(f"  📝 Query: {query}")
            
            # Ricerca su motori configurati
            for engine in self.config.get('search_engines', ['google']):
                if engine == 'google':
                    results = self.search_google(query, self.config.get('max_results_per_search', 5))
                elif engine == 'bing':
                    results = self.search_bing(query, self.config.get('max_results_per_search', 5))
                else:
                    continue
                
                # Analizza i risultati
                for result in results:
                    # Estrai contatti dal titolo, URL e snippet
                    text_to_analyze = f"{result['title']} {result['url']} {result['snippet']}"
                    contacts = self.extract_contacts_from_text(text_to_analyze)
                    
                    # Aggiungi contatti trovati
                    for contact_type, contact_list in contacts.items():
                        for contact in contact_list:
                            if contact not in all_contacts[contact_type]:
                                # Verifica se il profilo esiste
                                if self.verify_social_profile(contact, contact_type):
                                    all_contacts[contact_type].append(contact)
                                    print(f"    ✅ {contact_type.title()}: {contact}")
                
                # Delay tra ricerche
                delay = random.uniform(*self.config.get('delay_between_searches', (2, 5)))
                time.sleep(delay)
        
        return all_contacts
    
    def process_csv(self, input_file=None, output_file=None):
        """Processa il CSV degli artisti emergenti e aggiunge contatti"""
        input_file = input_file or self.config.get('csv_input_file', 'artisti-emergenti.csv')
        output_file = output_file or self.config.get('csv_output_file', 'artisti-con-contatti.csv')
        
        if not os.path.exists(input_file):
            print(f"❌ File CSV non trovato: {input_file}")
            return False
        
        # Inizializza browser
        if not self.init_browser():
            return False
        
        try:
            # Leggi CSV input
            with open(input_file, 'r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                artists = list(reader)
            
            print(f"📊 Trovati {len(artists)} artisti da analizzare")
            
            # Processa ogni artista
            processed_artists = []
            
            for i, artist in enumerate(artists, 1):
                print(f"\n🎤 [{i}/{len(artists)}] Processando: {artist.get('Nome Artista', 'N/A')}")
                
                # Cerca contatti
                contacts = self.search_artist_contacts(artist.get('Nome Artista', ''))
                
                # Crea record arricchito
                enriched_artist = dict(artist)
                enriched_artist.update({
                    'Instagram': ', '.join(contacts.get('instagram', [])),
                    'Facebook': ', '.join(contacts.get('facebook', [])),
                    'TikTok': ', '.join(contacts.get('tiktok', [])),
                    'Twitter': ', '.join(contacts.get('twitter', [])),
                    'YouTube': ', '.join(contacts.get('youtube', [])),
                    'Email': ', '.join(contacts.get('email', [])),
                    'Sito Web': ', '.join(contacts.get('website', [])),
                    'Data Ricerca Contatti': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                processed_artists.append(enriched_artist)
                
                # Salvataggio incrementale ogni 5 artisti
                if i % 5 == 0:
                    self.save_to_csv(processed_artists, output_file)
                    print(f"💾 Salvato progresso ({i}/{len(artists)})")
            
            # Salvataggio finale
            self.save_to_csv(processed_artists, output_file)
            
            print(f"\n🎯 COMPLETATO!")
            print(f"📊 Artisti processati: {len(processed_artists)}")
            print(f"💾 File salvato: {output_file}")
            
            # Statistiche
            self.print_statistics(processed_artists)
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante il processamento: {str(e)}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_to_csv(self, artists_data, output_file):
        """Salva i dati arricchiti in CSV"""
        try:
            if not artists_data:
                return
                
            # Headers per il CSV arricchito
            headers = list(artists_data[0].keys())
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(artists_data)
                
        except Exception as e:
            print(f"⚠️ Errore salvataggio CSV: {str(e)}")
    
    def print_statistics(self, processed_artists):
        """Stampa statistiche sui contatti trovati"""
        print(f"\n📈 STATISTICHE CONTATTI:")
        
        stats = {
            'Instagram': 0,
            'Facebook': 0,
            'TikTok': 0,
            'Twitter': 0,
            'YouTube': 0,
            'Email': 0,
            'Sito Web': 0
        }
        
        for artist in processed_artists:
            for platform in stats.keys():
                if artist.get(platform) and artist.get(platform).strip():
                    stats[platform] += 1
        
        total_artists = len(processed_artists)
        for platform, count in stats.items():
            percentage = (count / total_artists * 100) if total_artists > 0 else 0
            print(f"  📱 {platform}: {count}/{total_artists} ({percentage:.1f}%)")


def get_contact_finder_config():
    """Configurazione di default per il Contact Finder"""
    return {
        'csv_input_file': 'artisti-emergenti.csv',
        'csv_output_file': 'artisti-con-contatti.csv',
        'search_engines': ['google'],
        'max_results_per_search': 3,
        'delay_between_searches': (3, 7),
        'use_stealth_mode': True,
        'timeout': 10,
        'user_agent_rotation': True,
        'search_social_networks': ['instagram', 'facebook', 'tiktok', 'twitter', 'youtube'],
        'search_emails': True,
        'search_websites': True,
        'verify_social_profiles': False,  # Disabilita verifica per velocità
        'headless': False
    }


def main():
    """Funzione principale per test"""
    print("🔍 CONTACT FINDER - Test Mode")
    
    config = get_contact_finder_config()
    finder = ContactFinder(config)
    
    # Test con il CSV esistente
    success = finder.process_csv()
    
    if success:
        print("✅ Test completato con successo!")
    else:
        print("❌ Test fallito!")


if __name__ == "__main__":
    main()
