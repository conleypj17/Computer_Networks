import sys
import socket
import time
from socket import *

sentence = sys.argv[1]
server_ip = sys.argv[2]
server_port = int(sys.argv[3])
connection_id = sys.argv[4]

max_attempts = 3
attempts = 0
success = False

while attempts < max_attempts and not success:
    full_message = sentence + " " + connection_id
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.settimeout(60)
    try:
        clientSocket.connect((server_ip, server_port))
        start_time = time.time()
        clientSocket.send(full_message.encode())
        reply = clientSocket.recv(2048).decode()
        end_time = time.time()
        if reply.startswith("RESET"):
            print(f"Connection Error {connection_id}")
            attempts += 1
            clientSocket.close()
            if attempts < max_attempts:
                connection_id = input("Enter a new connection ID: ")
            continue
        elif reply.startswith("OK"):
            parts = reply.split()
            if len(parts) == 4:
                print(f"Connection established {parts[1]} {parts[2]} {parts[3]}")
            else:
                print('From Server: ', reply)
            print('Round Trip Time: ', end_time - start_time, 'seconds')
            success = True
        else:
            print('From Server: ', reply)
            print('Round Trip Time: ', end_time - start_time, 'seconds')
            success = True
        clientSocket.close()
    except socket.timeout:
        print(f"Connection Error {connection_id}")
        attempts += 1
        clientSocket.close()
        if attempts < max_attempts:
            connection_id = input("Enter a new connection ID: ")
        continue
    except Exception as e:
        print(f"Connection Error {connection_id}")
        attempts += 1
        clientSocket.close()
        if attempts < max_attempts:
            connection_id = input("Enter a new connection ID: ")
        continue

if not success:
    print("Connection Failure")