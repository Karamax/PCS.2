import socket
import json

usrLogin = 'D'
usrPass = 'q'

try:
    with open('usersDB.txt', 'r+') as f:
        usersDB = json.loads(f.read())

    sock = socket.socket()  # Конфиг
    sock.bind(('', 9090))
    sock.listen(1)

    print('Server started')  # Приём соединения
    conn, addr = sock.accept()
    print('connected:', addr)

    while True:
        data = conn.recv(1024)  # Логин
        login = data.decode()
        print(login)
        if login in usersDB:
            status = 'OK'
        else:
            status = 'ERR'
        conn.send(status.encode())
        if status == 'OK':
            break

    while True:
        data = conn.recv(1024)  # Пароль
        password = data.decode()
        print(password)
        if password == usersDB[login]:
            status = 'OK'
        else:
            status = 'ERR'
        conn.send(status.encode())
        if status == 'OK':
            break

    with open(login+'.txt', 'r+') as f:  # Отправка архива сообщений
        data = f.read()
        conn.send(data.encode())
        msgDB = json.loads(data)

    while True:
        data = conn.recv(1024)  # Получение сообщений
        msg = data.decode()
        print(msg)
        msgDB.append(msg)
        if msg == 'exit':
            break

    with open('q', 'r+') as f:
        f.write(json.dumps(msgDB))
    conn.close()
except:
    print('Oops, something went wrong')
