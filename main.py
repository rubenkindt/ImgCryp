import sys
import os
from cryptography.fernet import Fernet


def rmFile(path):
    try:
        os.remove(path)
    except Exception as e:
        print(e)


def addENC2File(path, add="ENC"):
    (ocPath, file) = os.path.split(path)
    (name, extension) = file.split('.', 2)
    encFile = ocPath + "\\" + name + add + '.' + extension
    return encFile


def renameFile(path, rename="temp"):
    (ocPath, file) = os.path.split(path)
    (_, extension) = file.split('.', 2)
    encFile = ocPath + "\\" + rename + '.' + extension
    return encFile


def loadKey(key=b'VZPTDBB4K9dVyXUGdQBYC28fiXDbUjVaFEQUnGhOeY8='):
    print(key)
    return key, Fernet(key)


def enc(path):
    if os.path.exists(addENC2File(path)):
        print("file already exist, delete before regenerating new one", addENC2File(path))
        exit()

    (key, fkey) = loadKey()

    try:
        file = open(path, 'rb')
        bytes = file.read()
        file.close()

        encry = fkey.encrypt(bytes)

        newFile = open(addENC2File(path), "wb")
        newFile.write(encry)
        newFile.close()

    except Exception as e:
        print(e)
        exit()


def dec(path, key=b''):
    if not os.path.exists(path):
        print("file does not exist")
        exit()

    if key == b'' :
        (key, fkey) = loadKey()
    else:
        (key, fkey) = loadKey(key)

    try:
        file = open(path, 'rb')
        bytes = file.read()
        file.close()

        encry = fkey.decrypt(bytes)

        newFile = open(renameFile(path, "name"), "wb")
        newFile.write(encry)
        newFile.close()

    except Exception as e:
        print(e)
        exit()


if __name__ == '__main__':
    arg1 = str(sys.argv[1])
    if arg1 == "key":
        loadKey()
    elif arg1 == "del":
        path = str(sys.argv[2])
        rmFile(addENC2File(path))
    elif arg1 == "enc":
        path = str(sys.argv[2])
        enc(path)
    elif arg1 == "dec":
        path = str(sys.argv[2])
        dec(path)
    else:
        print("wrong first arg")
