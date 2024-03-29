
import os
import time
from datetime import datetime

def ridimensiona_finestra():
    os.system('mode con: cols=114 lines=26')

def separa():
    print("-----------------------------------------------------------------------")

def opzioni_scelta_mappa():
    print("Con quale mappa si desidera lavorare:")
    separa()
    print("1. TheIsland\n2. TheCenter\n3. Ragnarok\n4. Valguero\n5. Extinction\n6. CrystalIsles")
    separa()

def ottieni_settaggi(mappa, salvataggi):
    salvataggi = cartella(salvataggi, "\\" + mappa)
    print("mappa selezionata. " + "(" + mappa + ")")
    return salvataggi, mappa

def scelta(mappe, salvataggi):
    operazione = input(">>> ")
    separa()
    if operazione == "1":
        print("mappa selezionata. " + "(" + mappe[0] + ")") 
        mappa = mappe[0]
    elif operazione == "2":
        salvataggi, mappa = ottieni_settaggi(mappe[1], salvataggi)
    elif operazione == "3":
        salvataggi, mappa = ottieni_settaggi(mappe[2], salvataggi)
    elif operazione == "4":
        salvataggi, mappa = ottieni_settaggi(mappe[3], salvataggi)
    elif operazione == "5":
        salvataggi, mappa = ottieni_settaggi(mappe[4], salvataggi)
    elif operazione == "6":
        salvataggi, mappa = ottieni_settaggi(mappe[5], salvataggi)
    else:
        print("opzione inesistente.")
        separa()
        return scelta(mappe, salvataggi)
    return salvataggi, mappa

def controllo_salvataggio(cartellaBackup, mappa, salvataggi, alfabeto):
    if os.path.exists(os.path.join(cartellaBackup, "sArk.config")):
        salvataggi = leggiFile(cartellaBackup, mappa)
    else:
        salvataggi = definisciPercorso(alfabeto, salvataggi, mappa)
    return salvataggi

def opzioni_salvataggi():
    separa()
    print("scegliere l'operazione da eseguire:")
    separa()
    print("1. eseguire un backup completo.\n2. sostituire backup completo > salvataggio.\n3. utilizzare backup automatici di ark.\n4. richiesta cambio mappa.\n5. chiudere programma.")
    separa()

def cartella(salvataggi, mappa):
    cartella = os.path.split(salvataggi)
    salvataggi = cartella[0] + mappa + cartella[1]
    return salvataggi

def creaConfigFile(percorso, cartella):
    file = open(os.path.join(percorso, "sArk.config"), "a")
    file.write(cartella + "\n")
    file.close()

def avvertimento():
    separa()
    print("errore: cartella contenente salvataggi ARK non trovata o eventualmente")
    print("vuota. continuare a giocare perchè il gioco crei automaticamente")
    print("i salvataggi o inserire manualmente il percorso corretto...")
    separa()
    
def errore(cartella, mappa):
    if mappa == "TheIsland":
        mappa = "\\"
    cartellaBackup = os.getenv("USERPROFILE") + "\\Desktop\\arkBackups"
    while not os.path.exists(cartella) or mappa + "SavedArksLocal" not in cartella or len(os.listdir(cartella)) == 0:
        avvertimento()
        cartella = os.path.abspath(input("> "))
    controllo(cartellaBackup)
    creaConfigFile(cartellaBackup, cartella)
    return cartella

def dividi(percorsi):
    return percorsi.split("\n")

def cerca(nome_mappa, testo):
    configFile = dividi(testo)
    cartella = nome_mappa + "SavedArksLocal"
    if nome_mappa == "TheIsland":
        cartella = "SavedArksLocal"
    for percorso in configFile:
        percorso_diviso = os.path.split(percorso)
        if cartella == percorso_diviso[1]:
            if os.path.exists(percorso):
                configFile = percorso
                return configFile
    salvataggi = errore(percorso, nome_mappa)
    return salvataggi

def leggiFile(percorso, nome_mappa):
    file = open(os.path.join(percorso, "sArk.config"), "r")
    testo = file.read()
    file.close()
    configFile = cerca(nome_mappa, testo)
    return configFile

def definisciPercorso(alfabeto, salvataggi, mappa):
    for lettera in alfabeto:
        percorsi = [lettera + ":\\Program Files (x86)" + salvataggi[2:], lettera + salvataggi[1:]]
        for percorso in percorsi:
            if os.path.exists(percorso):
                salvataggi = percorso
                return salvataggi
    salvataggi = errore(percorso, mappa)
    return salvataggi

def controllo(cartellaBackup):
    if os.path.exists(cartellaBackup):
        pass
    else:
        os.mkdir(cartellaBackup)

def gestione_esistenza(cartellaMappa):
    try:
        os.mkdir(cartellaMappa)
    except:
        print("backup già esistente, creazione nuovo backup in corso...")
        separa()
        svuotare(cartellaMappa)

def esecuzione_backup(salvataggi, alfabeto, mappa, cartellaMappa):
    if not esiste(salvataggi):
        salvataggi = definisciPercorso(alfabeto, salvataggi, mappa)
    controllo(cartellaBackup)
    print("operazione creazione backup avviata.")
    separa()
    gestione_esistenza(cartellaMappa)
    os.system("copy " + '"' + salvataggi + '"' + " " + '"' + cartellaMappa + '"')
    separa()
    print("backup effettuato.")
    separa()

def gestione_salvavita(vecchioSalvataggio):
    try:
        separa()
        print("creazione salvavita in corso...")
        os.mkdir(vecchioSalvataggio)
    except:
        separa()
        print("salvavita già presente. creazione nuovo salvavita in corso...")
        svuotare(vecchioSalvataggio)

def gestione_trasferimento_files(salvataggi, vecchioSalvataggio, percorsoDiviso):
    if len(os.listdir(salvataggi)) > 0:
        os.system("copy " + '"' + salvataggi + '"' + " " + '"' + vecchioSalvataggio + '"')
        separa()
        print("salvavita creato in:", percorsoDiviso)
    else:
        print("nessun salvataggio trovato impossibile trasferire files in cartella salvavita.")

def gestione_sostituzione(cartellaMappa, salvataggi, mappa):
    if not esiste(salvataggi):
        salvataggi = definisciPercorso(alfabeto, salvataggi, mappa)
    separa()
    if os.path.exists(cartellaMappa) and len(os.listdir(cartellaMappa)) > 0:
        print("operazione sostituzione files avviata.")
        percorsoDiviso = os.path.split(salvataggi)
        vecchioSalvataggio = percorsoDiviso[0] + "\\vecchioSalvataggio" + mappa
        gestione_salvavita(vecchioSalvataggio)
        separa()
        gestione_trasferimento_files(salvataggi, vecchioSalvataggio, percorsoDiviso[0])
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

def sostituzione_salvataggio(cartellaMappa, salvataggi, mappa):
    print("ATTENZIONE:") 
    separa()
    print("si sta per sostituire il salvataggio con il backup.") 
    separa()
    scelta = input("Procedere? S/n: ").lower()
    if scelta == "s":
        gestione_sostituzione(cartellaMappa, salvataggi, mappa)
    elif scelta == "n":
        separa()
        print("operazione annullata.")
        separa()
    else:
        separa()
        print("comando non riconosciuto.")
        separa()

def gestione_stampa_backups(salvataggi, lista, num):
    print("backup creati dal gioco:")
    separa()
    stampaBackups(salvataggi, lista, num)
    if len(lista) == 0:
        print("nessun backup creato automaticamente dal gioco.")
        separa()
        return False
    return True

def gestione_rimpiazzamento(lista, mappa, salvataggi):
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

def utilizzo_backup_automatici(salvataggi, alfabeto, mappa, lista, num):
    if not esiste(salvataggi):
        salvataggi = definisciPercorso(alfabeto, salvataggi, mappa)
    if not gestione_stampa_backups(salvataggi, lista, num):
        return
    separa()
    gestione_rimpiazzamento(lista, mappa, salvataggi)

def esiste(salvataggi):
    if os.path.exists(salvataggi):
        return True
    return False

def svuotare(cartella):
    for file in os.listdir(cartella):
        if file == "sArk.config" or file.lower() == "serverpaintingscache":
            continue
        os.remove(os.path.join(cartella, file))

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

def arresto_programma():
    print("richiesta arresto programma. arresto automatico tra (3) secondi...")
    separa()
    time.sleep(3)
    
def reset():
    scelta = input("si desidera cambiare mappa? S/n: ").lower()
    if scelta == "n":
        opzioni_salvataggi()
        return False
    elif scelta == "s":
        return True
    separa()
    return reset()

def richiesta_resettaggio(salvataggi, mappa, cartellaMappa, cartellaBackup):
    if reset():
        separa()
        opzioni_scelta_mappa()
        salvataggi, mappa = scelta(mappe, os.path.join(os.path.split(salvataggi)[0], "SavedArksLocal"))
        cartellaMappa = os.path.join(cartellaBackup, mappa)
        salvataggi = controllo_salvataggio(cartellaBackup, mappa, salvataggi, alfabeto)
        opzioni_salvataggi()
    return salvataggi, mappa, cartellaMappa

print("\n"*20, r"""
                                                    ____
                                                  .\    /
                                                  |\\  //\
                                                 /  \\//  \
                                                /   /  \   \
                                               /   /    \   \
                                              /   /      \   \  
                                             /   /______^ \   \
                                            /    ________\ \   \
                                           /   /            \   \
                                         /\\  /              \  //\
                                        /__\\_\     sArk     /_//__\
                                                byDarkenar94
""")

print("\n"*5)
time.sleep(2)

ridimensiona_finestra()

mappe = ["TheIsland", "TheCenter", "Ragnarok", "Valguero", "Extinction", "CrystalIsles"]
cartellaBackup = os.getenv("USERPROFILE") + "\\Desktop\\arkBackups"
salvataggi = "D:\\Steam\\steamapps\\common\\ARK\\ShooterGame\\Saved\\SavedArksLocal"
mappa = "x"

separa()

opzioni_scelta_mappa()

salvataggi, mappa = scelta(mappe, salvataggi)

cartellaMappa = os.path.join(cartellaBackup, mappa)

alfabeto = list("abcdefghijklmnopqrstuvwxyz".upper())

salvataggi = controllo_salvataggio(cartellaBackup, mappa, salvataggi, alfabeto)

lista = []
num = 1

opzioni_salvataggi()

while True:
    opzione = input(">> ")
    separa()
    if opzione == "1":
        esecuzione_backup(salvataggi, alfabeto, mappa, cartellaMappa)
        salvataggi, mappa, cartellaMappa = richiesta_resettaggio(salvataggi, mappa, cartellaMappa, cartellaBackup)
    elif opzione == "2":
        sostituzione_salvataggio(cartellaMappa, salvataggi, mappa)
        salvataggi, mappa, cartellaMappa = richiesta_resettaggio(salvataggi, mappa, cartellaMappa, cartellaBackup)
    elif opzione == "3":
        utilizzo_backup_automatici(salvataggi, alfabeto, mappa, lista, num)
        salvataggi, mappa, cartellaMappa = richiesta_resettaggio(salvataggi, mappa, cartellaMappa, cartellaBackup)
    elif opzione == "4":
        salvataggi, mappa, cartellaMappa = richiesta_resettaggio(salvataggi, mappa, cartellaMappa, cartellaBackup)
    elif opzione == "5":
        arresto_programma()
        break
    else:
        print("opzione inesistente.")
        separa()
