import pykeepass
import wmi
import hashlib
from os import system, listdir
from os.path import isfile, join, splitext
from time import sleep
from pathlib import Path

dir = str(Path(__file__).parent.absolute())

# this only works on windows
clear = lambda: system('cls')
# returns a list of every file name in the vaults folder with a .kdbx extension
hashes = lambda: [splitext(f)[0] for f in listdir(dir + "\\vaults") if isfile(join(dir + "\\vaults", f)) and splitext(f)[1] == ".kdbx"]
c = wmi.WMI()

# runs search on loop
def scan():
    while(True):
        search()

# checks if a connected usb device has a database associated with it
def search():
    discovered = []
    for drive in c.Win32_DiskDrive():
        if drive.SerialNumber not in discovered:
            m = hashlib.sha256()
            m.update(bytes(drive.SerialNumber, 'utf-8'))
            for hash in hashes():
                if m.hexdigest() == hash:
                    system(r'cmd /C KeePass ' + dir + "\\vaults\\" + hash + '.kdbx -pw:' + str(int(hash, 16) ^ int(ascii(drive.SerialNumber), base=10)))
                    return
            discovered += [drive.SerialNumber]

# unlocks a database belonging to the serial number passed in
def crack(serial):
    m = hashlib.sha256()
    m.update(bytes(serial, 'utf-8'))
    for hash in hashes():
        if hash == m.hexdigest():
            system(r'cmd /C KeePass ' + dir + "\\vaults\\" + hash + '.kdbx -pw:' + str(int(hash, 16) ^ int(ascii(serial), base=10)))

# print generated values
def gen():
    connections = capture()
    for drive in connections:
        m = hashlib.sha256()
        m.update(bytes(drive.SerialNumber, 'utf-8'))

        print("utf-8 serial: " + drive.SerialNumber)
        print("hash: " + m.hexdigest())
        print("ascii serial: " + ascii(drive.SerialNumber))
        print("master password: " + str(int(m.hexdigest(), 16) ^ int(ascii(drive.SerialNumber))))


# go through the process of supporting a new usb and creating a database associated with it
def add():
    connections = capture()
    for drive in connections:
        m = hashlib.sha256()
        m.update(bytes(drive.SerialNumber, 'utf-8'))
        new = False
        for hash in hashes():
            if m.hexdigest() == hash:
                new = True
                break
        if not new:
            create(drive.SerialNumber)
            print("success")
        else:
            print("Drive already in use")

# returns a usb drive list that was connected and then disconnected
def capture():

    clear()
    print("Connect the USB device")
    connections = detect_connection(c.Win32_DiskDrive())
    while not len(connections):
        connections = detect_connection(c.Win32_DiskDrive())
    
    clear()
    print("Disconnect the USB device")
    disconnections = detect_disconnection(c.Win32_DiskDrive())
    while not len(disconnections):
        disconnections = detect_disconnection(c.Win32_DiskDrive())
    
    clear()
    if connections == disconnections:
        print("Successly detected USB")
        return connections

# returns a list of usbs that are connected
def detect_connection(start):
    sleep(1)
    now = c.Win32_DiskDrive()
    changes = list(set(start) ^ set(now))
    if len(changes) and len(now) > len(start):
        return changes
    return []

def detect_disconnection(start):
    sleep(1)
    now = c.Win32_DiskDrive()
    changes = list(set(start) ^ set(now))
    if len(changes) and len(start) > len(now):
        return changes
    return []

# creates a new database
def create(serial):
    m = hashlib.sha256()
    m.update(bytes(serial, 'utf-8'))
    p = pykeepass.create_database(dir + "\\vaults\\" + m.hexdigest() + ".kdbx", password = str(int(m.hexdigest(), 16) ^ int(ascii(serial), base=10)))
    p.save()

def ascii(serial):
    return "".join(str(ord(c)) for c in serial)
