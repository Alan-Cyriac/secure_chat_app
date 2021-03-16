# Alan Cyriac
import socket
import threading
import sys
import rsacrypt
from os import system, name
import signal
from printy import printy
import os
from colorama import init
from termcolor import colored

# Choosing alias
nickname = input("Enter your Name: ").encode()
enc_nickname = rsacrypt.encrypt_message(nickname)
password = input("Enter your Password: ").encode()
password = input("Enter your Password: ").encode()

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 44444))


# Listening to Server and Sending username
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(4096)
            # print("Encrypted: ", message)
            message = rsacrypt.decrypt_message(message).decode()
            if message == 'CLIENT':
                client.send(enc_nickname)
            elif message == 'PASS':
                client.send(password)
                _ = clear_screen()
                with open('out.txt', 'r') as aimg:
                    ascii_img = aimg.read()
                printy(ascii_img, 'by')
                print(colored("[Type '#help' for help]", 'green'))
            elif message == 'REJECTED':
                message = client.recv(4096)
                message = rsacrypt.decrypt_message(message).decode()
                print(message)
                client.close()
            elif message == 'You are invited':
                printy(message, 'bm')
            else:
                nic_name = message.split()[0]
                msg = message.replace(nic_name, '')
                print(colored(nic_name, 'yellow'), colored(msg, 'cyan'))
                
        except Exception as e:
            _ = clear_screen()
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # printy(f"EXC type :{exc_type}", 'bbU')
            # printy(f"Error: {e}", 'brU')
            # printy(f"File name: {fname}", 'bwU')
            # printy(f"Line no: {exc_tb.tb_lineno}", 'boU')
            print("Connection Lost!!!\nEnter Ctrl+Enter")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        try:
            data = input('')
            message = '{}: {}'.format(nickname.decode(), data).encode()
            enc_message = rsacrypt.encrypt_message(message)
            # print("Encrypted: ", enc_message)
            if "#clear" == data:
                _ = clear_screen()
            elif "#batman" == data:
                with open('out.txt', 'r') as aimg:
                    ascii_img = aimg.read()
                    printy(ascii_img, 'by')
            elif "#help" == data:
                help = {"#online": "print all online members", "#clear": "clear screen", "#batman": "display batman logo"}
                printy(help)
            else:
                client.send(enc_message)
        except Exception as e:
            _ = clear_screen()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printy(f"EXC type :{exc_type}", 'bbU')
            printy(f"Error: {e}", 'brU')
            printy(f"File name: {fname}", 'bwU')
            printy(f"Line no: {exc_tb.tb_lineno}", 'boU')
            print("Connection Lost!!!\nEnter Ctrl+Enter")
            client.close()
            break


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


# Clear screen
def clear_screen():
    # if windows then cls else unix,mos clear
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    return 0


# Our signal handler
def signal_handler(signum, frame):  
    _ = clear_screen()
    client.close()
    printy("[Exit Strategy Activated]", 'bc')
    printy("Bye.", 'bn')
# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, signal_handler)
