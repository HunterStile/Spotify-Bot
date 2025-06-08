#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAC Address Changer - Modulo automatico per il cambio MAC address
Basato sul test script funzionante con fallback automatico
"""

import os
import subprocess
import time
import random
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MacChanger:
    """Classe per il cambio automatico del MAC address"""
    
    def __init__(self):
        self.vendor_prefixes_colon = ["00:1B:44", "00:15:5D", "08:00:27", "00:0C:29"]
        self.vendor_prefixes_no_colon = ["001B44", "00155D", "080027", "000C29"]
        self.current_mac = None
        self.new_mac = None
    
    def get_current_mac_simple(self):
        """Ottiene il MAC address attuale in modo semplice"""
        try:
            result = subprocess.run(['getmac', '/fo', 'csv'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # Prende la prima interfaccia di rete non loopback
                for line in lines[1:]:
                    if '"' in line:
                        mac = line.split(',')[0].strip('"')
                        if mac and mac != "N/A" and not mac.startswith("00-00-00"):
                            return mac
            return "Non rilevato"
        except Exception as e:
            logger.error(f"Errore nel rilevare MAC: {e}")
            return "Errore"
    
    def check_admin_privileges(self):
        """Verifica se lo script ha privilegi admin"""
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            logger.info(f"Privilegi amministratore: {'SÌ' if is_admin else 'NO'}")
            return is_admin
        except Exception as e:
            logger.warning(f"Impossibile verificare privilegi: {e}")
            return False
    
    def change_mac_powershell_only(self):
        """Cambio MAC usando solo PowerShell (non richiede TMAC)"""
        try:
            logger.info("Tentativo cambio MAC con PowerShell...")
            
            # 1. Ottieni lista adattatori attivi
            cmd_adapters = [
                'powershell', '-Command', 
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up" -and $_.Virtual -eq $false} | Select-Object -First 1 | ForEach-Object {$_.Name}'
            ]
            
            result = subprocess.run(cmd_adapters, capture_output=True, text=True)
            adapter_name = result.stdout.strip()
            
            if not adapter_name:
                logger.error("Nessun adattatore fisico attivo trovato")
                return False
            
            logger.info(f"Adattatore trovato: {adapter_name}")
            
            # 2. Genera nuovo MAC
            prefix = random.choice(self.vendor_prefixes_colon)
            suffix = ":".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
            self.new_mac = f"{prefix}:{suffix}"
            mac_no_colons = self.new_mac.replace(':', '')
            
            logger.info(f"Nuovo MAC: {self.new_mac}")
            
            # 3. Prova a cambiare MAC tramite proprietà avanzate
            cmd_change = [
                'powershell', '-Command', f'''
                try {{
                    $adapter = Get-NetAdapter -Name "{adapter_name}"
                    if ($adapter) {{
                        Disable-NetAdapter -Name "{adapter_name}" -Confirm:$false
                        Start-Sleep -Seconds 2
                        Set-NetAdapterAdvancedProperty -Name "{adapter_name}" -DisplayName "Network Address" -DisplayValue "{mac_no_colons}" -ErrorAction SilentlyContinue
                        Enable-NetAdapter -Name "{adapter_name}" -Confirm:$false
                        Start-Sleep -Seconds 3
                        Write-Output "SUCCESS"
                    }} else {{
                        Write-Output "ADAPTER_NOT_FOUND"
                    }}
                }} catch {{
                    Write-Output "ERROR: $($_.Exception.Message)"
                }}
                '''
            ]
            
            result = subprocess.run(cmd_change, capture_output=True, text=True)
            output = result.stdout.strip()
            
            if "SUCCESS" in output:
                logger.info("Cambio MAC PowerShell completato!")
                return True
            else:
                logger.error(f"Errore PowerShell: {output}")
                return False
                
        except Exception as e:
            logger.error(f"Errore generale PowerShell: {e}")
            return False
    
    def change_mac_netsh_method(self):
        """Metodo alternativo usando netsh"""
        try:
            logger.info("Tentativo cambio MAC con netsh...")
            
            # Genera nuovo MAC
            prefix = random.choice(self.vendor_prefixes_no_colon)
            suffix = "".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
            self.new_mac = f"{prefix}{suffix}"
            
            logger.info(f"Nuovo MAC (netsh): {self.new_mac}")
            
            # Trova interfaccia di rete
            cmd_interfaces = ['netsh', 'interface', 'show', 'interface']
            result = subprocess.run(cmd_interfaces, capture_output=True, text=True)
            
            # Prova a impostare su interfaccia Ethernet principale
            interfaces = ["Ethernet", "Ethernet 1", "Local Area Connection", "Wi-Fi"]
            
            for interface in interfaces:
                try:
                    cmd_set = ['netsh', 'interface', 'set', 'interface', interface, 'admin=disable']
                    subprocess.run(cmd_set, capture_output=True, text=True, timeout=10)
                    time.sleep(1)
                    
                    cmd_set = ['netsh', 'interface', 'set', 'interface', interface, 'admin=enable']
                    subprocess.run(cmd_set, capture_output=True, text=True, timeout=10)
                    time.sleep(2)
                    
                    logger.info(f"Operazione netsh completata su {interface}")
                    return True
                    
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
            
            logger.error("Metodo netsh non riuscito")
            return False
            
        except Exception as e:
            logger.error(f"Errore netsh: {e}")
            return False
    
    def change_mac_automatic(self):
        """Cambio MAC automatico con fallback tra metodi"""
        logger.info("AVVIO CAMBIO MAC AUTOMATICO")
        logger.info("=" * 50)
        
        # Verifica privilegi
        has_admin = self.check_admin_privileges()
        if not has_admin:
            logger.warning("Script senza privilegi amministratore - alcuni metodi potrebbero fallire")
        
        # MAC iniziale
        self.current_mac = self.get_current_mac_simple()
        logger.info(f"MAC prima del cambio: {self.current_mac}")
        
        # Metodi da provare in ordine
        methods = [
            ("PowerShell", self.change_mac_powershell_only),
            ("Netsh", self.change_mac_netsh_method)
        ]
        
        success = False
        for method_name, method_func in methods:
            logger.info(f"Provo metodo: {method_name}")
            
            try:
                if method_func():
                    success = True
                    logger.info(f"Successo con {method_name}!")
                    break
                else:
                    logger.warning(f"{method_name} fallito, provo il prossimo...")
            except Exception as e:
                logger.error(f"Errore con {method_name}: {e}")
        
        # Verifica finale
        logger.info("VERIFICA FINALE:")
        time.sleep(3)
        final_mac = self.get_current_mac_simple()
        logger.info(f"MAC dopo il cambio: {final_mac}")
        
        if success and self.current_mac != final_mac:
            logger.info("🎉 CAMBIO MAC RIUSCITO!")
            return True
        else:
            logger.warning("⚠️ Cambio MAC non confermato")
            logger.info("💡 Suggerimenti:")
            logger.info("   - Esegui come Amministratore")
            logger.info("   - Installa TMAC da: https://technitium.com/tmac/")
            logger.info("   - Verifica che l'adattatore supporti il cambio MAC")
            return False
    
    def get_mac_info(self):
        """Restituisce informazioni sui MAC address"""
        return {
            'current_mac': self.current_mac or self.get_current_mac_simple(),
            'new_mac': self.new_mac,
            'has_admin': self.check_admin_privileges()
        }

# Funzioni di compatibilità per il resto del progetto
def change_mac():
    """Funzione principale per il cambio MAC - compatibilità"""
    changer = MacChanger()
    return changer.change_mac_automatic()

def get_current_mac():
    """Ottiene il MAC address attuale - compatibilità"""
    changer = MacChanger()
    return changer.get_current_mac_simple()

def main():
    """Funzione principale - eseguita quando il modulo viene avviato direttamente"""
    changer = MacChanger()
    success = changer.change_mac_automatic()
    
    # Mostra informazioni finali
    info = changer.get_mac_info()
    print(f"\n📊 RIEPILOGO:")
    print(f"MAC iniziale: {info['current_mac']}")
    print(f"MAC finale: {changer.get_current_mac_simple()}")
    print(f"Privilegi admin: {'✅' if info['has_admin'] else '❌'}")
    print(f"Risultato: {'✅ SUCCESSO' if success else '❌ FALLITO'}")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Cambio MAC interrotto dall'utente")
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        print(f"❌ Errore fatale: {e}")