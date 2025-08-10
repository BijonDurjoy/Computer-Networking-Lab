import socket
import threading
import os

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4444

def receive_messages(sock):
    # Receive thread message from server
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[Disconnected from server]")
                break
            print(data.decode(), end="")
        except:
            break


def send_file(sock, filename):
    # File upload
    if not os.path.exists(filename):
        print(f"[Client] File '{filename}' not found!")
        return
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            sock.sendall(bytes_read)
    sock.sendall(b"<<END>>")


def download_file(sock,filename):
    # File Download
    with open(filename, "wb") as f:
        while True:
            data = sock.recv(1024)
            if b"<<END>>" in data:
                f.write(data.replace(b"<<END>>", b""))
                break
            f.write(data)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    # Receive Thread
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # send username first
    username = input(sock.recv(1024).decode())
    sock.send(username.encode())

    # Message loop
    while True:
        msg = input()
        if msg.strip() == "":
            continue

        if msg.startswith("/upload "):
            sock.send(msg.encode())  # send command
            parts = msg.split(maxsplit=1)
            if len(parts) > 1:
                filename = parts[1]
                send_file(sock, filename)

        elif msg.startswith("/download "):
            sock.send(msg.encode())  # send command
            parts = msg.split(maxsplit=1)
            if len(parts) > 1:
                filename = parts[1]
                download_file(sock, filename)

        else:
            sock.send(msg.encode())

if __name__ == "__main__":
    main()