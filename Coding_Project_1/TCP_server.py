from socket import *
import time

in_use_ids = {}  # Dictionary to track in-use connection IDs
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print('The TCP server is ready to receive')

server_start_time = time.time()
timeout_seconds = 5 * 60  # 5 minutes

while True:
    # Check server timeout
    if time.time() - server_start_time > timeout_seconds:
        print("Server timeout reached. Closing socket.")
        serverSocket.close()
        break

    # Remove expired connection IDs (older than 60 seconds)
    current_time = time.time()
    expired_ids = [cid for cid, t in in_use_ids.items() if current_time - t > 60]
    for cid in expired_ids:
        del in_use_ids[cid]

    serverSocket.settimeout(1)
    try:
        connectionSocket, clientAddress = serverSocket.accept()
    except timeout:
        continue

    try:
        message = connectionSocket.recv(2048).decode()
        client_connection_id = message.split()[-1]
        client_ip_address = clientAddress[0]
        client_port = clientAddress[1]

        if client_connection_id in in_use_ids:
            if current_time - in_use_ids[client_connection_id] < 60:
                print(f"Connection ID {client_connection_id} is already in use. Ignoring message from {client_ip_address}:{client_port}")
                modifiedMessage = "RESET " + client_connection_id
                connectionSocket.send(modifiedMessage.encode())
                connectionSocket.close()
                continue
            else:
                del in_use_ids[client_connection_id]
        in_use_ids[client_connection_id] = current_time
        modifiedMessage = "OK " + client_connection_id + " " + client_ip_address + " " + str(client_port)
        connectionSocket.send(modifiedMessage.encode())
        connectionSocket.close()
    except Exception as e:
        connectionSocket.close()
        continue