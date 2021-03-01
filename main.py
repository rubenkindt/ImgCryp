import sys
import os
import datetime
from cryptography.fernet import Fernet

#removes file
def rmFile(path):
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            print("Can't delete none existing file")
    except Exception as e:
        print(e)

#gets timeData from a server
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

#outdated code
#adds "enc" to a file name
def addENC2File(path, add="ENC"):
    (ocPath, file) = os.path.split(path)
    (name, extension) = file.split('.', 2)
    encFile = ocPath + "\\" + name + add + '.' + extension
    return encFile

#renames file
def renameFile(path, rename="temp"):
    (ocPath, file) = os.path.split(path)
    (_, extension) = file.split('.', 2)
    encFile = ocPath + "\\" + rename + '.' + extension
    return encFile

#get key
def getKey(key=b'VZPTDBB4K9dVyXUGdQBYC28fiXDbUjVaFEQUnGhOeY8='):
    print(key)
    return key, Fernet(key)

#returns the timeDate gotten fom the enc txt file
#If Path does not exist in that file raises exception
def checkPathEpoch(path):
    decrData = decTxtData()

    startPath = decrData.find(path)
    if startPath==-1:
        raise Exception("path is not in text file")
    nr = startPath + len(path) + 1  # + 1 for the comma
    deadline = datetime.datetime.fromtimestamp(int(decrData[nr:nr + 10]))
    return deadline

#decode txt file with deadlines
def decTxtData():
    file = open("encDate.txt", 'rb')
    data = file.read()
    file.close()

    if not data:
        return ""

    (_, fkey) = getKey()
    decrData = fkey.decrypt(data)
    return decrData.decode('utf-8')

#encode txt file with deadlines
def encTxtData(Data):
    (_, fkey) = getKey()
    encData = fkey.encrypt(Data.encode('ascii'))

    file = open("encDate.txt", 'wb')

    file.write(encData)
    file.close()

#removes used path from encoded txt file with deadlines
def rmPathAndEpoch(path):
    decrData = decTxtData()

    startPath = decrData.find(path)
    if startPath == -1:
        raise Exception("path is not in text file")

    nr = startPath + len(path) + 1  # + 1 for the comma
    newData = decrData[:startPath - 1] + decrData[nr + 12:]

    encTxtData(newData)

#decodes img if deadline is reached
def decUntil(path, key=""):
    if not os.path.exists(path):
        raise Exception("Time file does not exist")

    data = decTxtData()
    if data.find(path)==-1:
        raise Exception("path is not in txt file")

    deadline=checkPathEpoch(path)
    print("deadline", deadline)

    current = getCurrentTime()
    if current:
        if current > deadline:
            print("decrypting")
            dec(path)
            rmPathAndEpoch(path)

            exit()
        raise Exception("deadline not yet reached")
    raise Exception("decyption failed")

#encodes img with deadline
def encUntil(path, sec):
    currentT = getCurrentTime()
    if not currentT:
        print(currentT)
        raise Exception("server time none")
    deadline = currentT + datetime.timedelta(seconds=10)

    try:

        enc(path)

        txtData = decTxtData()
        txtData += "\n"
        txtData += path + "," + deadline.timestamp().__str__()
        encTxtData(txtData)

    except Exception as e:
        print(e)

#encodes img
def enc(path):
    if not os.path.exists(path):
        raise Exception("file does not exist")

    (key, fkey) = getKey()

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

#decrypt img
def dec(path, key=""):
    if not os.path.exists(path):
        raise Exception("file does not exist")

    if not key:
        (key, fkey) = getKey()
    else:
        (key, fkey) = getKey(key)

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
        getKey()
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
    elif arg1 == "decTxtData":
        print(decTxtData())
    else:
        print("usage: ")
        print("enc C:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png")
        print("encUntil C:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png 12")
        print("dec c:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png")
        print("decUntil c:\\Users\\ruben\\Desktop\\ImgCryp\\genericImag.png")
