import socket
import select
import os

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

clients = []
sockets = [server]

print("Server SELECT running...")

while True:
    read_ready, _, _ = select.select(sockets, [], [])

    for sock in read_ready:
        if sock == server:
            conn, addr = server.accept()
            sockets.append(conn)
            clients.append(conn)
            print("Connected:", addr)

        else:
            data = sock.recv(1024)

            if not data:
                sockets.remove(sock)
                clients.remove(sock)
                sock.close()
                continue

            msg = data.decode()

            if msg.startswith("/list"):
                files = os.listdir()
                sock.send(("\n".join(files)).encode())

            elif msg.startswith("/upload"):
                _, filename = msg.split()
                with open(filename, "wb") as f:
                    while True:
                        chunk = sock.recv(4096)
                        if b"EOF" in chunk:
                            f.write(chunk.replace(b"EOF", b""))
                            break
                        f.write(chunk)

            elif msg.startswith("/download"):
                _, filename = msg.split()
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        sock.sendall(f.read())
                    sock.send(b"EOF")

            else:
                for c in clients:
                    if c != sock:
                        c.send(msg.encode())






