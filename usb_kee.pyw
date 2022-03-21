import wmi
import hashlib
import os

c = wmi.WMI()

keypass_path = "C:\Program Files (x86)\KeePass Password Safe 2\KeePass.exe"

vaults = [
    { 
        "vault" : "C:\Python39\py\key\Database.kdbx", 
        "hash" : "c3f1b129eee3fa0d9191f6b5995af82cd30b377e8c8dd79fc725dbf457223f06"
    },
    {
        "vault" : "C:\Python39\py\key\Database2.kdbx", 
        "hash" : "b52aaeba4b1a97b1b711046b3621f0fee324bf3b2eb0f16f3de056734ece8edf"
    }
]

def scan():
    while(True):
        search()

def search():
    discovered = []
    for drive in c.Win32_DiskDrive():
        if drive.SerialNumber not in discovered:
            m = hashlib.sha256()
            m.update(bytes(drive.SerialNumber, 'utf-8'))
            for v in vaults:
                if m.hexdigest() == v["hash"]:
                    ascii_serial = ""
                    for i in drive.SerialNumber:
                        ascii_serial += str(ord(i))
                    os.system(r'cmd /C "' + keypass_path + '" ' + v["vault"] + '  -pw:' + str(int(v["hash"], 16) ^ int(ascii_serial, base=10)))
                    return
            discovered += [drive.SerialNumber]

def crack(serial, idx = 0):
    m = hashlib.sha256()
    m.update(bytes(serial, 'utf-8'))
    if m.hexdigest() == vaults[idx]["hash"]:
        ascii_serial = ""
        for i in serial:
            ascii_serial += str(ord(i))
        os.system(r'cmd /C "' + keypass_path + '" ' + vaults[idx]["vault"] + '  -pw:' + str(int(vaults[idx]["hash"], 16) ^ int(ascii_serial, base=10)))

def gen():
    for drive in c.Win32_DiskDrive():
        m = hashlib.sha256()
        m.update(bytes(drive.SerialNumber, 'utf-8'))

        ascii_serial = ""
        for i in drive.SerialNumber:
            ascii_serial += str(ord(i))
        
        print("utf-8 serial: " + drive.SerialNumber)
        print("hash: " + m.hexdigest())
        print("ascii serial: " + ascii_serial)
        print("master password: " + str(int(m.hexdigest(), 16) ^ int(ascii_serial, base=10)))

scan()
