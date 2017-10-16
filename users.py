import json
import os
import socket
import json
import  tkinter
from tkinter import simpledialog as sd
from tkinter import  *
root = Tk()

work = True

sock = socket.socket()

sock.connect(('localhost',7070))


def addUser():
    print('Enter username')
    #username = input()
    username = sd.askstring("Enter username:", "Enter username")
    print('Enter password')
    #password = input()
    password = sd.askstring("Enter password:", "Enter password")
    uData = {'Operation': 'add', 'Login': username, 'Password': password}
    sendData(uData)
    return


def removeUser():
    print('Enter username')
    username = sd.askstring("Enter username:", "Enter username")
    uData = {'Operation': 'remv', 'Login': username}
    sendData(uData)
    return


def changePass():
    print('Enter username')
    username = sd.askstring("Enter username:", "Enter username")
    print('Enter new password')
    password = sd.askstring("Enter password:", "Enter password")
    uData = {'Operation': 'chan', 'Login': username, 'Password': password}
    sendData(uData)
    return


def wrongId():
    print('Wrong input.')
    sd.messagebox.showerror('Error', 'Wrong operation id')
    return


def exitProg():
    global work
    work = False
    return

def sendData(data):
    sock.send(json.dumps(data).encode())
    data = sock.recv(1024)
    sd.messagebox.showinfo('Status', data.decode())


while work:
    print('Select operation: 1 - add, 2 - remove, 3 - change password, 4 - exit program')
    operationId = sd.askstring("Select operation:", " 1 - add, 2 - remove, 3 - change password, 4 - exit program")
    operation = {'1': addUser, '2': removeUser, '3': changePass, '4': exitProg}
    operation.get(operationId, wrongId)()

