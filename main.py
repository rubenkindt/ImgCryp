import sys
import os
import datetime
from cryptography.fernet import Fernet


def rmFile(path):
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            print("Can't delete none existing file")
    except Exception as e:
        print(e)


def getCurrentTime():
    try:
        import time
        import ntplib
        import datetime

        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        x = time.localtime(response.tx_time)
        a = datetime.datetime(x.tm_year, x.tm_mon, x.tm_mday, x.tm_hour, x.tm_min, x.tm_sec)
        print(a)
        return a
    except:
        print('Could not sync with time server.')


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


def decUntil(path, key=""):
    if not os.path.exists(path):
        raise Exception("Time file does not exist")

    file = open("encDate.txt", 'rt')
    data = file.read()
    file.close()

    startPath = data.find(path)
    nr = startPath + len(path) + 1  # + 1 for the comma
    deadline = datetime.datetime.fromtimestamp(int(data[nr:nr+10]))
    print("epoch : ", int(data[nr:nr+10]))
    print("deadline", deadline)

    current = getCurrentTime()
    if current:
        if current > deadline:
            print("decrypting")
            dec(path)
            newData = data[:startPath - 1] + data[nr + 12:]
            file = open("encDate.txt", 'wt')
            file.write(newData)
            file.close()
            exit()
        raise Exception("deadline not yet reached")
    raise Exception("decyption failed")




def encUntil(path, sec):
    currentT = getCurrentTime()
    if not currentT:
        print(currentT)
        raise Exception("server time none")
    deadline = currentT + datetime.timedelta(seconds=10)

    try:
        if not os.path.exists(path):
            file = open("encDate.txt", 'wt')
        else:
            file = open("encDate.txt", 'at')

        enc(path)

        file.write("\n")
        file.write(path + "," + deadline.timestamp().__str__())
        file.close()

    except Exception as e:
        print(e)


def enc(path):
    if not os.path.exists(path):
        raise Exception("file does not exist")

    (key, fkey) = loadKey()

    try:
        file = open(path, 'rb')
        bytes = file.read()
        file.close()

        encry = fkey.encrypt(bytes)

        rmFile(path)

        newFile = open(path, "wb")
        newFile.write(encry)
        newFile.close()

    except Exception as e:
        print(e)
        exit()


def dec(path, key=""):
    if not os.path.exists(path):
        raise Exception("file does not exist")

    if not key:
        (key, fkey) = loadKey()
    else:
        (key, fkey) = loadKey(key)

    try:
        file = open(path, 'rb')
        bytes = file.read()
        file.close()

        encry = fkey.decrypt(bytes)

        rmFile(path)

        newFile = open(path, "wb")
        newFile.write(encry)
        newFile.close()

    except Exception as e:
        raise Exception("decrypt failed",e)


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
    elif arg1 == "encUntil":
        path = str(sys.argv[2])
        AmountSec = int(sys.argv[3])
        encUntil(path, AmountSec)
    elif arg1 == "dec":
        path = str(sys.argv[2])
        dec(path)
    elif arg1 == "decUntil":
        path = str(sys.argv[2])
        decUntil(path)
    else:
        print("usage: ")
        print("enc C:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png")
        print("encUntil C:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png 12")
        print("dec c:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png")
        print("decUntil c:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png")
