import json
import os

work = True
with open('usersDB.txt', 'r+') as f:  # Чтение базы пользователей
    usersDB = json.loads(f.read())


def addUser():
    print('Enter username')
    username = input()
    if username in usersDB:
        print('User already created')
        return
    print('Enter password')
    password = input()
    usersDB[username] = password
    with open(username+'.txt', 'w') as f:
        f.write(json.dumps([]))
    return


def removeUser():
    print('Enter username')
    username = input()
    if username not in usersDB:
        print('User does not exist')
        return
    del usersDB[username]
    os.remove(username+'.txt')
    return


def changePass():
    print('Enter username')
    username = input()
    if username not in usersDB:
        print('User does not exist')
        return
    print('Enter new password')
    password = input()
    usersDB[username] = password
    return


def wrongId():
    print('Wrong input.')
    return


def exitProg():
    global work
    work = False
    return


while work:
    print('Select operation: 1 - add, 2 - remove, 3 - change password, 4 - exit program')
    operationId = input()
    operation = {'1': addUser, '2': removeUser, '3': changePass, '4': exitProg}
    operation.get(operationId, wrongId)()

with open('usersDB.txt', 'w') as f:
    f.write(json.dumps(usersDB))
