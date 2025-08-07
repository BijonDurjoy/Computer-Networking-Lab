import socket
import threading
import os

# Server Config
HOST = '0.0.0.0'
PORT = 4444

# Where files will be stored
FILE_DIR = 'server_files'

# Keep all connected clients
clients = []
usernames = {}

# Send message to all except sender
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

# Handle file-related commands
def handle_file_commands(command, client_socket):
    tokens = command.strip().split()
    if tokens[0] == '/list':
        try:
            files = os.listdir(FILE_DIR)
            if not files:
                client_socket.send(b"[Server] No files found.\n")
            else:
                file_list = "\n".join(files) + "\n"
                client_socket.send(f"[Server] Files:\n{file_list}".encode())
        except Exception as e:
            client_socket.send(f"[Server] Error listing files: {e}\n".encode())

    elif tokens[0] == '/upload':
        if len(tokens) < 2:
            client_socket.send(b"[Server] Usage: /upload filename\n")
            return
        filename = tokens[1]
        client_socket.send(b"[Server] Ready to receive file.\n")
        with open(os.path.join(FILE_DIR, filename), 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if data.endswith(b"<<END>>"):
                    f.write(data[:-8])
                    break
                f.write(data)
        client_socket.send(f"[Server] File '{filename}' uploaded successfully.\n".encode())

    elif tokens[0] == '/download':
        if len(tokens) < 2:
            client_socket.send(b"[Server] Usage: /download filename\n")
            return
        filename = tokens[1]
        filepath = os.path.join(FILE_DIR, filename)
        if not os.path.exists(filepath):
            client_socket.send(b"[Server] File not found.\n")
            return
        client_socket.send(b"[Server] Sending file...\n")
        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        client_socket.send(b"<<END>>")
        client_socket.send(f"\n[Server] File '{filename}' sent successfully.\n".encode())

    elif tokens[0] == '/delete':
        if len(tokens) < 2:
            client_socket.send(b"[Server] Usage: /delete filename\n")
            return
        filename = tokens[1]
        filepath = os.path.join(FILE_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            client_socket.send(f"[Server] File '{filename}' deleted.\n".encode())
        else:
            client_socket.send(b"[Server] File not found.\n")
    else:
        client_socket.send(b"[Server] Unknown command.\n")

# Handle each client
def handle_client(client_socket, address):
    try:
        client_socket.send(b"Welcome to the server!\nEnter your name: ")
        username = client_socket.recv(1024).decode().strip()
        usernames[client_socket] = username
        clients.append(client_socket)
        broadcast(f"[+] {username} joined the chat.\n".encode(), client_socket)

        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break

            decoded = msg.decode().strip()
            if decoded.startswith('/'):
                handle_file_commands(decoded, client_socket)
            else:
                full_msg = f"{username}: {decoded}\n".encode()
                broadcast(full_msg, client_socket)

    except:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        broadcast(f"[-] {usernames.get(client_socket, 'A user')} left the chat.\n".encode())
        client_socket.close()

# Start server
def start_server():
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection: {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
