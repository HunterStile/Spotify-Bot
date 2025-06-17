"""
Test script per il Contact Finder
"""

from contact_finder import ContactFinder, get_contact_finder_config
import os

def test_contact_finder():
    """Test base del Contact Finder"""
    print("🧪 Test Contact Finder")
    
    # Verifica se il file CSV esiste
    csv_file = "artisti-emergenti.csv"
    if not os.path.exists(csv_file):
        print(f"❌ File {csv_file} non trovato per il test")
        return False
    
    # Configurazione test
    config = get_contact_finder_config()
    config['max_results_per_search'] = 2  # Limita per test veloce
    config['delay_between_searches'] = (1, 2)  # Delay ridotto per test
    config['verify_social_profiles'] = False  # Disabilita verifica per velocità
    
    print(f"📊 Configurazione test: {config}")
    
    # Crea Contact Finder
    finder = ContactFinder(config)
    
    # Test delle regex
    print("\n🔍 Test estrazione contatti da testo:")
    test_text = "Seguitemi su instagram.com/test_artist e facebook.com/testartist oppure scrivetemi a booking@testartist.com"
    contacts = finder.extract_contacts_from_text(test_text)
    print(f"Contatti estratti: {contacts}")
    
    # Test del sistema completo (commenta se non vuoi eseguire)
    # print("\n🚀 Test sistema completo...")
    # success = finder.process_csv()
    # return success
    
    return True

if __name__ == "__main__":
    test_contact_finder()
