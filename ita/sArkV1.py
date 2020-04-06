
import os
import time
from datetime import datetime

def separa():
    print("-----------------------------------------------------------------------")

def cartella(salvataggi, mappa):
    cartella = os.path.split(salvataggi)
    salvataggi = cartella[0] + mappa + cartella[1]
    return salvataggi

def creaConfigFile(percorso, cartella):
    file = open(os.path.join(percorso, "sArk.config"), "a")
    file.write(cartella + "\n")
    file.close()

def errore(cartella, mappa):
    if mappa == "TheIsland":
        mappa = "\\"
    cartellaBackup = os.getenv("USERPROFILE") + "\\Desktop\\arkBackups"
    while os.path.exists(cartella) == False or mappa + "SavedArksLocal" not in cartella or len(os.listdir(cartella)) == 0:
        separa()
        print("errore: cartella contenente salvataggi ARK non trovata o eventualmente")
        print("vuota. continuare a giocare perchè il gioco crei automaticamente")
        print("i salvataggi o inserire manualmente il percorso corretto...")
        separa()
        cartella = os.path.abspath(input("> "))
    if os.path.exists(cartellaBackup):
        pass
    else:
        os.mkdir(cartellaBackup)
    creaConfigFile(cartellaBackup, cartella)
    return cartella

def dividi(percorsi):
    sep = "\n"
    return percorsi.split(sep)

def cerca(tmpConfigFile, mappa):
    configFile = dividi(tmpConfigFile)
    for percorso in configFile:
        cartella = os.path.split(percorso)
        if mappa + "SavedArksLocal" == cartella[1]:
            if os.path.exists(percorso):
                configFile = percorso
                return configFile
    for percorso in configFile:
        cartella = os.path.split(percorso)
        if cartella[1] == "SavedArksLocal":
            if os.path.exists(percorso):
                configFile = percorso
                return configFile
    os.remove(os.getenv("USERPROFILE") + "\\Desktop\\arkBackups\\sArk.config")
    errore(percorso, mappa)

def leggiFile(percorso, mappa):
    file = open(os.path.join(percorso, "sArk.config"), "r")
    tmpConfigFile = file.read()
    file.close()
    configFile = cerca(tmpConfigFile, mappa)
    return configFile

def definisciPercorso(alfabeto, salvataggi, mappa):
    for lettera in alfabeto:
        percorso = lettera + ":\\Program Files (x86)" + salvataggi[2:]
        if os.path.exists(percorso):
            salvataggi = percorso
            return salvataggi
        percorso = lettera + salvataggi[1:]
        if os.path.exists(percorso):
            salvataggi = percorso
            return percorso
    salvataggi = errore(percorso, mappa)
    return salvataggi

def esiste(salvataggi, alfabeto, mappa):
    if os.path.exists(salvataggi):
        return salvataggi
    salvataggi = definisciPercorso(alfabeto, salvataggi, mappa)
    return salvataggi

def svuotare(cartella):
    for file in os.listdir(cartella):
        if file == "sArk.config":
            pass
        else:
            os.remove(os.path.join(cartella,file))

def stampaBackups(salvataggi, lista, num):
    for file in os.listdir(salvataggi):
            if "_" in file[11:]:
                percorsoFile = os.path.join(salvataggi, file)
                fileStat = os.stat(percorsoFile)
                fileInfo = datetime.fromtimestamp(fileStat.st_mtime)
                print(str(num) + ".", file, "{}/{}/{} {}:{}".format(fileInfo.day, fileInfo.month, fileInfo.year, fileInfo.hour, fileInfo.minute))
                lista.append(percorsoFile)
                num += 1
    if len(lista) == 0:
        return None
    print(str(num) + ". annullare l'operazione")


cartellaBackup = os.getenv("USERPROFILE") + "\\Desktop\\arkBackups"
salvataggi = "D:\\Steam\\steamapps\\common\\ARK\\ShooterGame\\Saved\\SavedArksLocal"
stringa = "mappa selezionata. " 
mappa = "x"

print("\n-------------------------------------------- sArkV1 By Darkenar94 -----")
print("Con quale mappa si desidera lavorare:")
separa()
print("1. TheIsland\n2. TheCenter\n3. Ragnarok\n4. Valguero")
separa()

while True:
    operazione = input(">>> ")
    separa()
    if operazione == "1":
        print(stringa + "(TheIsland)") 
        mappa = "TheIsland"
        break
    elif operazione == "2":
        salvataggi = cartella(salvataggi, "\\TheCenter")
        print(stringa + "(TheCenter)")
        mappa = "TheCenter"
        break
    elif operazione == "3":
        salvataggi = cartella(salvataggi, "\\Ragnarok")
        print(stringa + "(Ragnarok)")
        mappa = "Ragnarok"
        break
    elif operazione == "4":
        salvataggi = cartella(salvataggi, "\\Valguero")
        print(stringa + "(Valguero)")
        mappa = "Valguero"
        break
    else:
        print("opzione inesistente.")
        separa()

cartellaMappa = os.path.join(cartellaBackup, mappa)

alfabeto = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

if os.path.exists(os.path.join(cartellaBackup, "sArk.config")):
    salvataggi = leggiFile(cartellaBackup, mappa)
else:
    salvataggi = esiste(salvataggi, alfabeto, mappa) 

lista = []
num = 1

separa()
print("scegliere l'operazione da eseguire:")
separa()
print("1. eseguire un backup completo.\n2. sostituire backup completo > salvataggio.\n3. utilizzare backup automatici di ark.\n4. chiudere programma.")
separa()

while True:
    opzione = input(">> ")
    separa()
    if opzione == "1":
        if os.path.exists(cartellaBackup):
            pass
        else:
            os.mkdir(cartellaBackup)
        if esiste(salvataggi, alfabeto, mappa): 
            pass
        print("operazione creazione backup avviata.")
        separa()
        try:
            os.mkdir(cartellaMappa)
        except:
            print("backup già esistente, creazione nuovo backup in corso...")
            separa()
            svuotare(cartellaMappa)
        os.system("copy " + '"' + salvataggi + '"' + " " + '"' + cartellaMappa + '"')
        separa()
        print("backup effettuato.")
        separa()
    elif opzione == "2":
        print("ATTENZIONE:") 
        separa()
        print("si sta per sostituire il salvataggio con il backup.") 
        separa()
        scelta = input("Procedere? S/n: ")
        scelta = scelta.lower()
        if scelta == "s":
            if esiste(salvataggi, alfabeto, mappa): 
                pass
            separa()
            if os.path.exists(cartellaMappa) and len(os.listdir(cartellaMappa)) > 0: 
                print("operazione sostituzione files avviata.")
                percorsoDiviso = os.path.split(salvataggi)
                vecchioSalvataggio = percorsoDiviso[0] + "\\vecchioSalvataggio" + mappa
                try:
                    separa()
                    print("creazione salvavita in corso...")
                    os.mkdir(vecchioSalvataggio)
                except:
                    separa()
                    print("salvavita già presente. creazione nuovo salvavita in corso...")
                    svuotare(vecchioSalvataggio)
                separa()
                if len(os.listdir(salvataggi)) > 0:
                    os.system("copy " + '"' + salvataggi + '"' + " " + '"' + vecchioSalvataggio + '"')
                    separa()
                    print("salvavita creato in:", percorsoDiviso[0])
                else:
                    print("nessun salvataggio trovato impossibile trasferire files in cartella salvavita.")
                separa()
                print("sostituzione files in corso...")
                separa()
                svuotare(salvataggi)
                os.system("copy " + '"' + cartellaMappa + '"' + " " + '"' + salvataggi + '"')
                separa()
                print("sostituzione files affettuata con successo.")
                separa()
            else:
                print("impossibile eseguire l'operazione. Backup non trovato.")
                print("creare nuovo backup o chiudere il programma.")
                separa()
                continue
        elif scelta == "n":
            separa()
            print("operazione annullata.")
            separa()
        else:
            separa()
            print("comando non riconosciuto.")
            separa()
    elif opzione == "3":
        if esiste(salvataggi, alfabeto, mappa):
            pass
        print("backup creati dal gioco:")
        separa()
        stampaBackups(salvataggi, lista, num)
        if len(lista) == 0:
            print("nessun backup creato automaticamente dal gioco.")
            separa()
            continue
        separa()
        print("selezionare il backup che sostituirà il salvataggio.")
        separa()
        while True:
            opzione = input("> ")
            separa()
            try:
                opzione = int(opzione)
            except ValueError:
                print("digitare un numero.")
                separa()
            else:    
                if opzione > 0 and opzione <= len(lista):
                    file = mappa + ".ark"
                    os.rename(os.path.join(salvataggi, file), os.path.join(salvataggi, "delete"))
                    os.remove(os.path.join(salvataggi, "delete"))
                    os.rename(lista[opzione -1], os.path.join(salvataggi, file))
                    print("sostituzione files affettuata con successo.")
                    lista = []
                    separa()
                    break
                elif opzione == len(lista) +1:
                    print("operazione annullata.")
                    lista = []
                    separa()
                    break
                else:
                    print("opzione inesistente.")
                    separa()
    elif opzione == "4":
        print("richiesta arresto programma. arresto automatico tra (3) secondi...")
        separa()
        time.sleep(3)
        break
    else:
        print("opzione inesistente.")
        separa()

