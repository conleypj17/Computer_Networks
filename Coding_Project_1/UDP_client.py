
import sys
import socket
import time
from socket import *

serverName = 'hostname'
serverPort = 12000

sentence = sys.argv[1]
server_ip = sys.argv[2]
server_port = int(sys.argv[3])
connection_id = sys.argv[4]

max_attempts = 3
attempts = 0
success = False

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(60)

while attempts < max_attempts and not success:
	full_message = sentence + " " + connection_id
	start_time = time.time()
	clientSocket.sendto(full_message.encode(), (server_ip, server_port))
	try:
		modifiedSentence, serverAddress = clientSocket.recvfrom(2048)
		end_time = time.time()
		reply = modifiedSentence.decode()
		if reply.startswith("RESET"):
			print(f"Connection Error {connection_id}")
			attempts += 1
			if attempts < max_attempts:
				connection_id = input("Enter a new connection ID: ")
			continue
		elif reply.startswith("OK"):
			# reply format: OK <connection_id> <client_ip> <client_port>
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
	except socket.timeout:
		print(f"Connection Error {connection_id}")
		attempts += 1
		if attempts < max_attempts:
			connection_id = input("Enter a new connection ID: ")
		continue

if not success:
	print("Connection Failure")
clientSocket.close()


