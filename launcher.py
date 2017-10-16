import os
import tkinter
from tkinter import *

root = Tk()

def runClient(event):
    root.destroy()
    os.system('client.bat')


def runUsers(event):
    root.destroy()
    os.system('users.bat')


btnClient = Button(root,text='Client',)
btnClient.bind('<Button-1>', runClient)
btnClient.pack()

btnUsers = Button(root,text='Users')
btnUsers.bind('<Button-1>', runUsers)
btnUsers.pack()

root.mainloop()
