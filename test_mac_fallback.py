#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test MAC address con fallback automatico senza privilegi TMAC
"""

import os
import sys
import subprocess
import time
import random

# Aggiungi la cartella funzioni al path
current_dir = os.path.dirname(os.path.abspath(__file__))
funzioni_dir = os.path.join(current_dir, 'funzioni')
sys.path.append(funzioni_dir)

def get_current_mac_simple():
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
    except:
        return "Errore"

def change_mac_powershell_only():
    """Cambio MAC usando solo PowerShell (non richiede TMAC)"""
    try:
        print("🔧 Tentativo cambio MAC con PowerShell...")
        
        # 1. Ottieni lista adattatori attivi
        cmd_adapters = [
            'powershell', '-Command', 
            'Get-NetAdapter | Where-Object {$_.Status -eq "Up" -and $_.Virtual -eq $false} | Select-Object -First 1 | ForEach-Object {$_.Name}'
        ]
        
        result = subprocess.run(cmd_adapters, capture_output=True, text=True)
        adapter_name = result.stdout.strip()
        
        if not adapter_name:
            print("❌ Nessun adattatore fisico attivo trovato")
            return False
        
        print(f"📡 Adattatore trovato: {adapter_name}")
        
        # 2. Genera nuovo MAC
        vendor_prefixes = ["00:1B:44", "00:15:5D", "08:00:27", "00:0C:29"]
        prefix = random.choice(vendor_prefixes)
        suffix = ":".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
        new_mac = f"{prefix}:{suffix}"
        mac_no_colons = new_mac.replace(':', '')
        
        print(f"🎯 Nuovo MAC: {new_mac}")
        
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
            print("✅ Cambio MAC completato!")
            return True
        else:
            print(f"❌ Errore PowerShell: {output}")
            return False
            
    except Exception as e:
        print(f"❌ Errore generale: {e}")
        return False

def change_mac_netsh_method():
    """Metodo alternativo usando netsh"""
    try:
        print("🔧 Tentativo cambio MAC con netsh...")
        
        # Genera nuovo MAC
        vendor_prefixes = ["001B44", "00155D", "080027", "000C29"]
        prefix = random.choice(vendor_prefixes)
        suffix = "".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
        new_mac = f"{prefix}{suffix}"
        
        print(f"🎯 Nuovo MAC (netsh): {new_mac}")
        
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
                
                print(f"✅ Operazione netsh completata su {interface}")
                return True
                
            except subprocess.TimeoutExpired:
                continue
            except Exception:
                continue
        
        print("❌ Metodo netsh non riuscito")
        return False
        
    except Exception as e:
        print(f"❌ Errore netsh: {e}")
        return False

def test_mac_fallback():
    """Test con fallback automatico tra metodi"""
    print("🧪 TEST MAC CON FALLBACK AUTOMATICO")
    print("=" * 50)
    
    # MAC iniziale
    print("📡 MAC prima del cambio:")
    initial_mac = get_current_mac_simple()
    print(f"   {initial_mac}")
    
    methods = [
        ("PowerShell", change_mac_powershell_only),
        ("Netsh", change_mac_netsh_method)
    ]
    
    success = False
    for method_name, method_func in methods:
        print(f"\n🔄 Provo metodo: {method_name}")
        
        try:
            if method_func():
                success = True
                print(f"✅ Successo con {method_name}!")
                break
            else:
                print(f"❌ {method_name} fallito, provo il prossimo...")
        except Exception as e:
            print(f"❌ Errore con {method_name}: {e}")
    
    # Verifica finale
    print("\n📊 VERIFICA FINALE:")
    time.sleep(3)
    final_mac = get_current_mac_simple()
    print(f"📡 MAC dopo il cambio: {final_mac}")
    
    if success and initial_mac != final_mac:
        print("🎉 CAMBIO MAC RIUSCITO!")
    else:
        print("⚠️ Cambio MAC non confermato")
        print("💡 Suggerimenti:")
        print("   - Esegui come Amministratore")
        print("   - Installa TMAC da: https://technitium.com/tmac/")
        print("   - Verifica che l'adattatore supporti il cambio MAC")
    
    return success

def test_admin_check():
    """Verifica se lo script ha privilegi admin"""
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"🔐 Privilegi amministratore: {'✅ SÌ' if is_admin else '❌ NO'}")
        return is_admin
    except:
        print("🔐 Impossibile verificare privilegi")
        return False

if __name__ == "__main__":
    print("🛠️ TEST MAC ALTERNATIVO (SENZA TMAC)")
    print("=" * 50)
    
    # Verifica privilegi
    test_admin_check()
    
    print("\nScegli test:")
    print("1. Test cambio MAC con fallback")
    print("2. Solo verifica MAC attuale")
    print("3. Test metodo PowerShell")
    print("4. Test metodo Netsh")
    
    try:
        choice = input("\nScelta (1-4): ").strip()
        
        if choice == "1":
            test_mac_fallback()
        elif choice == "2":
            mac = get_current_mac_simple()
            print(f"📡 MAC attuale: {mac}")
        elif choice == "3":
            change_mac_powershell_only()
        elif choice == "4":
            change_mac_netsh_method()
        else:
            print("❌ Scelta non valida")
    
    except KeyboardInterrupt:
        print("\n👋 Test interrotto")
