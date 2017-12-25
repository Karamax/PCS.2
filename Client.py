import socket
import json
from tkinter import *
import tkinter.simpledialog
import hmac, hashlib
from datetime import datetime

root = Tk()


def sayTest(event):
    print(inputField.get())
    now = str(datetime.now())
    msg = now + ':  ' + inputField.get()
    sock.send(msg.encode())
    textb.insert('end', '\n' + msg)
    inputField.delete(0, 'end')
    if msg == 'exit':
        root.destroy()

buffer = 1024  # Конфиг
port = 9090
addres = 'localhost'
try:
    sock = socket.socket()  # Соединениe
    sock.connect((addres, port))
    while True:
        var = tkinter.simpledialog.askstring("Name prompt", "enter your name")
        sock.send(var.encode())  # Логин
        status = sock.recv(buffer).decode()
        print(status)
        if status == 'OK':
            break

    while True:
        var = tkinter.simpledialog.askstring("Name prompt", "enter your pass")
        var = hmac.new(bytearray('signature', 'utf-8'), bytearray(var, 'utf-8'), hashlib.sha256).hexdigest()
        sock.send(var.encode())  # Пароль
        status = sock.recv(buffer).decode()
        print(status)
        if status == 'OK':
            break


    print('Login and password accepted.')
    msgDB = sock.recv(buffer).decode()  # Получение архива сообqщений
    msgDB = json.loads(msgDB)

    textb = tkinter.Text(root)
    textb.pack()

    inputField = tkinter.Entry(root)
    # self.inputField["command"] = self.sayTest
    inputField.pack()
    root.bind('<Return>', sayTest)

    for m in msgDB:
        textb.insert('end', '\n' + m)

    root.mainloop()
    sock.send(b'exit')
    sock.close()
except Exception as e:
    print('Oops, something went wrong' + e)
