import subprocess


# Comando di installazione del pacchetto pip per le dipendenze del programma
install_command = f"pip install -r requirements.txt"

# Esegui il comando di installazione utilizzando il modulo subprocess
subprocess.run(install_command, shell=True)
print("Dipendenze Installate!")
input()






