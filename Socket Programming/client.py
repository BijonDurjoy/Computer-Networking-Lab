import socket
import threading

# Server connection info
HOST = 'localhost'
PORT = 4444

# Create TCP socket
client_socket = socket.socket()
client_socket.connect((HOST,PORT))

#Receive initial message
initial_msg = client_socket.recv(1024).decode()
print(initial_msg, end='')

# Send username to server
name = input()
client_socket.send(name.encode())

# Function to non stop receive message
def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print("\n" + msg.decode())
        except:
            print("Connection lost.")
            client_socket.close()
            break

# Function to send messages to server
def send_messages():
    while True:
        try:
            msg = input()
            if msg.lower() == 'exit':
                client_socket.close()
                break
            client_socket.send(msg.encode())
        except:
            break

# Start receiving thread
recv_thread = threading.Thread(target=receive_messages)
recv_thread.daemon = True
recv_thread.start()

# Start sending in main thread
send_messages()