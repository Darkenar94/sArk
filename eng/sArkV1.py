
# COMPILARE IL PROGRAMMA:
# cd C:\Users\Darkenar94\AppData\Local\Programs\Python\Python38-32\scripts
# pyinstaller percorso\File.py

# AGGIUNGERE L'ICONA.

# stampare errori su un file ???
# aggiornamento del programma in caso di nuova versione ???

import os
import time
from datetime import datetime

def separa():
    print("----------------------------------------------------------------------------------------------------------")

def cartella(salvataggi, mappa):
    cartella = os.path.split(salvataggi)
    salvataggi = cartella[0] + mappa + cartella[1]
    return salvataggi

def creaConfigFile(percorso, cartella):
    file = open(os.path.join(percorso, "sArk.config"), "a")
    file.write(cartella + "\n")
    file.close()

def errore(cartella):
    cartellaBackup = os.getenv("USERPROFILE") + "\\Desktop\\arkBackups"
    while os.path.exists(cartella) == False or "SavedArksLocal" not in cartella or len(os.listdir(cartella)) == 0:
        separa()
        print("error: folder containing ARK savings not found or EMPTY. ")
        print("keep playing so that the game automatically creates savings or")
        print("insert the right path manually...")
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
    errore(percorso)

def leggiFile(percorso, mappa):
    file = open(os.path.join(percorso, "sArk.config"), "r")
    tmpConfigFile = file.read()
    file.close()
    configFile = cerca(tmpConfigFile, mappa)
    return configFile

def definisciPercorso(alfabeto, salvataggi):
    for lettera in alfabeto:
        percorso = lettera + ":\\Program Files (x86)" + salvataggi[2:]
        if os.path.exists(percorso):
            salvataggi = percorso
            return salvataggi
        percorso = lettera + salvataggi[1:]
        if os.path.exists(percorso):
            salvataggi = percorso
            return percorso
    salvataggi = errore(percorso)
    return salvataggi

def esiste(salvataggi, alfabeto):
    if os.path.exists(salvataggi):
        return salvataggi
    else:
        salvataggi = definisciPercorso(alfabeto,salvataggi)
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
    else:
        print(str(num) + ". cancel operation")


cartellaBackup = os.getenv("USERPROFILE") + "\\Desktop\\arkBackups"
salvataggi = "D:\\Steam\\steamapps\\common\\ARK\\ShooterGame\\Saved\\SavedArksLocal"
mappa = "x"

print("\n------------------------------------------------------------------------- sArkV1 By Darkenar94 -----------")
print("Select the map you'd like to work with:")
separa()
print("1. TheIsland\n2. TheCenter\n3. Ragnarok\n4. Valguero")
separa()

while True:
    operazione = input(">>> ")
    separa()
    if operazione == "1":
        print("map selected. " + "(TheIsland)")
        mappa = "TheIsland"
        break
    elif operazione == "2":
        salvataggi = cartella(salvataggi, "\\TheCenter")
        print("map selected. " + "(TheCenter)")
        mappa = "TheCenter"
        break
    elif operazione == "3":
        salvataggi = cartella(salvataggi, "\\Ragnarok")
        print("map selected. " + "(Ragnarok)")
        mappa = "Ragnarok"
        break
    elif operazione == "4":
        salvataggi = cartella(salvataggi, "\\Valguero")
        print("map selected. " + "(Valguero)")
        mappa = "Valguero"
        break
    else:
        print("this option does not exist.")
        separa()

cartellaMappa = os.path.join(cartellaBackup, mappa)

alfabeto = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

if os.path.exists(os.path.join(cartellaBackup, "sArk.config")):
    salvataggi = leggiFile(cartellaBackup, mappa)
else:
    salvataggi = esiste(salvataggi, alfabeto)

lista = []
num = 1

separa()
print("choose what operation to perform:")
separa()
print("1. create full backup.\n2. replace full backup > saving.\n3. use ark automatic backups.\n4. close program.")
separa()

while True:
    opzione = input(">> ")
    separa()
    if opzione == "1":
        if os.path.exists(cartellaBackup):
            pass
        else:
            os.mkdir(cartellaBackup)
        if esiste(salvataggi, alfabeto):
            pass
        print("started creating backup.")
        separa()
        try:
            os.mkdir(cartellaMappa)
        except:
            print("a backup already exists, creating new backup...")
            separa()
            svuotare(cartellaMappa)
        os.system("copy " + '"' + salvataggi + '"' + " " + '"' + cartellaMappa + '"')
        separa()
        print("backup completed.")
        separa()
    elif opzione == "2":
        print("WARNING: the option you selected will replace the saving with the backup.")
        separa()
        scelta = input("proceed? Y/n: ")
        scelta = scelta.lower()
        if scelta == "s":
            if esiste(salvataggi, alfabeto):
                pass
            separa()
            listaFiles = os.listdir(os.getenv("USERPROFILE") + "\\Desktop")
            if "arkBackups" in listaFiles and len(os.listdir(cartellaBackup)) > 0:
                print("file substitution in progress.")
                percorsoDiviso = os.path.split(salvataggi)
                vecchioSalvataggio = percorsoDiviso[0] + "\\oldSaving" + mappa
                try:
                    separa()
                    print("failsafe creation in progress...")
                    os.mkdir(vecchioSalvataggio)
                except:
                    separa()
                    print("a failsafe already exists. failsafe creation in progress...")
                    svuotare(vecchioSalvataggio)
                separa()
                if len(os.listdir(salvataggi)) > 0:
                    os.system("copy " + '"' + salvataggi + '"' + " " + '"' + vecchioSalvataggio + '"')
                    separa()
                    print("failsafe created at:", percorsoDiviso[0])
                else:
                    print("no savings found impossible to transfer files to failsafe folder.")
                separa()
                print("file substitution in progress...")
                separa()
                svuotare(salvataggi)
                os.system("copy " + '"' + cartellaMappa + '"' + " " + '"' + salvataggi + '"')
                separa()
                print("file substitution successfully completed.")
                separa()
            else:
                print("operation impossible to perform. Backup not found.")
                print("create new backup or close program.")
                separa()
                continue
        elif scelta == "n":
            separa()
            print("operation aborted.")
            separa()
        else:
            separa()
            print("command not found.")
            separa()
    elif opzione == "3":
        if esiste(salvataggi, alfabeto):
            pass
        print("backup created by the game:")
        separa()
        stampaBackups(salvataggi, lista, num)
        if len(lista) == 0:
            print("no backup automatically created by the game.")
            separa()
            continue
        separa()
        print("select backup to use to substitute the saving.")
        separa()
        while True:
            opzione = input("> ")
            separa()
            try:
                opzione = int(opzione)
            except ValueError:
                print("select a number.")
                separa()
            else:
                if opzione > 0 and opzione <= len(lista):
                    file = mappa + ".ark"
                    os.rename(os.path.join(salvataggi, file), os.path.join(salvataggi, "delete"))
                    os.remove(os.path.join(salvataggi, "delete"))
                    os.rename(lista[opzione -1], os.path.join(salvataggi, file))
                    print("file substitution successfully completed.")
                    lista = []
                    separa()
                    break
                elif opzione == len(lista) +1:
                    print("operation aborted.")
                    lista = []
                    separa()
                    break
                else:
                    print("this option does not exist.")
                    separa()
    elif opzione == "4":
        print("quitting automatically in (3) seconds...")
        separa()
        time.sleep(3)
        quit()
    else:
        print("this option does not exist.")
        separa()
