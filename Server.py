import socket
import json
import threading

logined = []

print('Server started')


def accept_clients():  # Приём новых клиентов
    while True:
        conn, addr = sock.accept()
        print('connected:', addr)
        proc_client_thread = threading.Thread(target=process_client, args=(conn,))
        proc_client_thread.start()


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

    client_listen_thread = threading.Thread(target= accept_clients)  # Запуск приёма новых клиентoв
    client_listen_thread.start()

except Exception as e:
    sock.close()
    print('Oops, something went wrong:' + e)
