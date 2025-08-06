import socket
import threading

#create TCP socket
server_socket = socket.socket()
print("Socket created")

#Bind to localhost and port 4444
server_socket.bind(('localhost', 4444))
server_socket.listen(5)
print("Server is listening on port 4444...")

#Track Connected Clients
clients = []

# Brodcast message to all clients
def broadcast(message, sender_socket= None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

# Handle each client in a separate thread
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    client_socket.send(b"Welcome to the server!\nEnter your name: ")
    try:
        name = client_socket.recv(1024).decode().strip()
        welcome_msg = f"{name} has joined the chat!\n".encode()
        broadcast(welcome_msg, client_socket)

        while True:
            msg= client_socket.recv(1024)
            if not msg:
                break
            full_msg = f"{name}: ".encode() + msg
            broadcast(full_msg, client_socket)
        
    except:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        print(f"{address} disconnected")
        broadcast(f"{name} left the chat!\n".encode())


    
# Accept clients forever
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()