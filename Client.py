import socket
import json

buffer = 1024  # Конфиг
port = 9090
addres = 'localhost'
try:
    sock = socket.socket()  # Соединение
    sock.connect((addres, port))
    while True:
        sock.send(input('Enter login:').encode())  # Логин
        status = sock.recv(buffer).decode()
        print(status)
        if status == 'OK':
            break

    while True:
        sock.send(input('Enter password:').encode())  # Пароль
        status = sock.recv(buffer).decode()
        print(status)
        if status == 'OK':
            break

    print('Login and password accepted.')
    msgDB = sock.recv(buffer).decode()  # Получение архива сообщений
    msgDB = json.loads(msgDB)
    for m in msgDB:
        print(m)

    while True:
        msg = input()
        sock.send(msg.encode())  # Отправка сообщений
        if msg == 'exit':
            break

    sock.close()
except:
    print('Oops, something went wrong')