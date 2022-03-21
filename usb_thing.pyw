import wmi
import hashlib
import os

c = wmi.WMI()

def search():
    hash = "c3f1b129eee3fa0d9191f6b5995af82cd30b377e8c8dd79fc725dbf457223f06"
    discovered = []
    while(True):
        for drive in c.Win32_DiskDrive():
            if drive.SerialNumber not in discovered:
                m = hashlib.sha256()
                m.update(bytes(drive.SerialNumber, 'utf-8'))
                if m.hexdigest() == hash:
                    ascii_serial = ""
                    for i in drive.SerialNumber:
                        ascii_serial += str(ord(i))
                    os.system(r'cmd /C "C:\Program Files (x86)\KeePass Password Safe 2\KeePass.exe" C:\Python39\py\key\Database.kdbx  -pw:' + str(int(hash, 16) ^ int(ascii_serial, base=10)))
                else:
                    discovered += [drive.SerialNumber]
search()
