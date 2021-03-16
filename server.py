import socket
import threading
import json
import sqlite3
import hashlib
import rsacrypt
import sys
import os

from datetime import datetime
from printy import printy

## Connection Data
host = '127.0.0.1'
port = 44444

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()
print(server)

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

special_words = ['#online']

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(4096)
            dec_message = rsacrypt.decrypt_message(message).decode()
            split_dec_message = dec_message.split()[1]
            if "#online" == split_dec_message:
                str_nicknames = ','.join(nicknames)
                str_nicknames = f'online: [{str_nicknames}]'
                client.send(rsacrypt.encrypt_message(str_nicknames.encode()))
            else:
                broadcast(message)
        except Exception as e:
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # printy(f"File name: {fname}", 'bwU')
            # printy(f"EXC type :{exc_type}", 'bbU')
            # printy(f"Error: {e}", 'brU')
            # printy(f"Line no: {exc_tb.tb_lineno}", 'boU')

            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(rsacrypt.encrypt_message(('{} left!'.format(nickname)).encode()))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    try:
        while True:
            is_present = []
            # Accept Connection
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send(rsacrypt.encrypt_message(b'CLIENT'))
            
            # Receiving Client name
            nickname = client.recv(4096)
            decrypted_nickname = rsacrypt.decrypt_message(nickname).decode()
            print('nickname: ', decrypted_nickname)
            
            # Receiving Client password
            client.send(rsacrypt.encrypt_message(b'PASS'))
            password = client.recv(4096)
            password = rsacrypt.decrypt_message(password)
            
            # checking with database
            conn = sqlite3.connect('pychat.db')
            salt = b'\x15%\xfb\xd1\r\x9d\xd3\xa4\xa9\xfb%\xbd\x14vl\xaa\x1f\xc3q\x86\xf9S\xe5\xe8\x7f\xfd\xd1\xcd\xcf\xca\xfc\xa6'
            key = str(hashlib.pbkdf2_hmac('sha256', password, salt, 100000))
            key = key.replace("\\", "\\")
            sql = "SELECT ID FROM ADMIN WHERE USERNAME = ? AND  KEY = ?"
            cursor2 = conn.execute(sql, (str(decrypted_nickname), str(key)))
            is_present = cursor2.fetchall()
            
            if len(is_present) != 0:
                client.send(rsacrypt.encrypt_message(b'You are invited'))
                nicknames.append(decrypted_nickname)
                clients.append(client)

                # Print And Broadcast Nickname
                print("Nickname is {}".format(decrypted_nickname))
                who_joined = f'{decrypted_nickname} joined!'.encode()
                broadcast(rsacrypt.encrypt_message(who_joined))

                # Start Handling Thread For Client
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            else:
                client.send(rsacrypt.encrypt_message(b'REJECTED'))
                client.send(rsacrypt.encrypt_message(b'Not Invited.'))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # printy(f"File name: {fname}", 'bwU')
        # printy(f"EXC type :{exc_type}", 'bbU')
        printy(f"Error: {e}", 'brU')
        printy(f"Line no: {exc_tb.tb_lineno}", 'boU')

receive()