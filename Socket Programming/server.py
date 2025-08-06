import socket

s= socket.socket()
print("Socket created")

s.bind(('localhost', 4444))
s.listen(2)
print("Waiting for connections...")

while True:
    c, addr = s.accept()
    print("Connected with", addr)
    c.send("Welcome to the server!")

    c.close()