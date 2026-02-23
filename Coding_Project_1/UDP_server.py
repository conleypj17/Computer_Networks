from socket import *
import time

in_use_ids = {} # Dictionary to track in-use connection IDs
"""
format of the dictionary

in_use_ids : 
{
    id #: time (both integers)
}
"""
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')

server_start_time = time.time()
timeout_seconds = 5 * 60 # 5 minutes

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

    serverSocket.settimeout(1)  # Non-blocking wait for up to 1 second
    try:
        message, clientAddress = serverSocket.recvfrom(2048)
    except timeout:
        continue  # Loop again to check for server timeout and expired IDs

    client_ip_address = clientAddress[0]
    client_port = clientAddress[1]
    client_connection_id = message.decode().split()[-1] # Extract the connection ID from the message

    # Check if the connection ID is already in use
    if client_connection_id in in_use_ids:
        # If the connection ID is in use, check if it has expired
        if current_time - in_use_ids[client_connection_id] < 60: # Assuming a timeout of 60 seconds
            print(f"Connection ID {client_connection_id} is already in use. Ignoring message from {client_ip_address}:{client_port}")
            modifiedMessage = "RESET " + client_connection_id
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            continue
        else:
            # If the connection ID has expired, remove it from the dictionary
            del in_use_ids[client_connection_id]
    in_use_ids[client_connection_id] = current_time
    modifiedMessage = "OK " + client_connection_id + " " + client_ip_address + " " + str(client_port)
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)