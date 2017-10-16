import socket
import json
import threading
import os

logined = []

print('Server started')


def accept_clients():  # Приём новых клиентов
    while True:
        conn, addr = sock.accept()
        print('connected:', addr)
        proc_client_thread = threading.Thread(target=process_client, args=(conn,))
        proc_client_thread.start()

def accept_managers():
    while True:
        conn, addr = sock2.accept()
        print('connected:', addr)
        proc_client_thread = threading.Thread(target=process_mamager, args=(conn,))
        proc_client_thread.start()

def process_mamager(manager):
    while True:
        try:
            data = manager.recv(1024)
            data = json.loads(data)
            response = b'OK'
            if data['Operation'] == 'add':
                print('add op')
                if data['Login'] in usersDB:
                    print('User already created')
                    response = b'ERR'
                else:
                    usersDB[data['Login']] = data['Password']
                    with open(data['Login'] + '.txt', 'w') as f:
                        f.write(json.dumps([]))
            if data['Operation'] == 'remv':
                print('remv op')
                if data['Login'] not in usersDB:
                    print('User does not exist')
                    response = b'ERR'
                else:
                    if data['Login'] in logined:
                        response = b'ERR'
                        print('User logined')
                    else:
                        del usersDB[data['Login']]
                        os.remove(data['Login'] + '.txt')
            if data['Operation'] == 'chan':
                print('add op')
                if data['Login'] not in usersDB:
                    print('User does not exist')
                    response = b'ERR'
                else:
                    usersDB[data['Login']] = data['Password']

            with open('usersDB.txt', 'w') as f:
                f.write(json.dumps(usersDB))

            if data['Operation'] == 'exit':
                manager.close()
                return
            else:
                manager.send(response)
            #manager.close()
        except Exception as e:
            print('Manager thread error' + e)



def process_client(client):  # Обработка соединения
    try:
        while True:
            data = client.recv(1024)  # Логин
            login = data.decode()
            print(login)
            if login in usersDB and login not in logined:
                status = 'OK'
            else:
                status = 'ERR'
            client.send(status.encode())
            if status == 'OK':
                break

        while True:
            data = client.recv(1024)  # Пароль
            password = data.decode()
            print(password)
            if password == usersDB[login]:
                status = 'OK'
            else:
                status = 'ERR'
            client.send(status.encode())
            if status == 'OK':
                break
        logined.append(login)
        with open(login+'.txt', 'r+') as f:  # Отправка архива сообщений
            data = f.read()
            client.send(data.encode())
            msgDB = json.loads(data)

        while True:
            data = client.recv(1024)  # Получение сообщений
            msg = data.decode()
            print(msg)
            msgDB.append(msg)
            with open(login + '.txt', 'r+') as f:
                f.write(json.dumps(msgDB))
            if msg == 'exit':
                break

        with open(login+'.txt', 'r+') as f:
            f.write(json.dumps(msgDB))
        client.close()
        logined.remove(login)
    except Exception as e:
        print('Oops, something went wrong: ' + e)
        logined.remove(login)


try:
    with open('usersDB.txt', 'r+') as f:
        usersDB = json.loads(f.read())

    sock = socket.socket()  # Конфиг
    sock.bind(('', 9090))
    sock.listen(1)

    sock2 = socket.socket()  # Конфиг
    sock2.bind(('', 7070))
    sock2.listen(1)

    client_listen_thread = threading.Thread(target=accept_clients)  # Запуск приёма новых клиентов
    client_listen_thread.start()

    manager_listen_thread = threading.Thread(target=accept_managers)  # Запуск приёма новых managers
    manager_listen_thread.start()

except Exception as e:
    sock.close()
    print('Oops, something went wrong:' + e)
