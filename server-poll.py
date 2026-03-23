import socket
import select
import os

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)

poll = select.poll()
poll.register(server.fileno(), select.POLLIN)

fd_map = {server.fileno(): server}
clients = []

print("Server POLL running...")

while True:
    events = poll.poll()

    for fd, event in events:
        sock = fd_map[fd]

        if sock == server:
            conn, addr = server.accept()
            conn.setblocking(False)
            fd_map[conn.fileno()] = conn
            poll.register(conn.fileno(), select.POLLIN)
            clients.append(conn)
            print("Connected:", addr)

        elif event & select.POLLIN:
            data = sock.recv(1024)

            if not data:
                poll.unregister(fd)
                clients.remove(sock)
                del fd_map[fd]
                sock.close()
                continue

            msg = data.decode()

            if msg.startswith("/list"):
                files = os.listdir()
                sock.send(("\n".join(files)).encode())

            else:
                for c in clients:
                    if c != sock:
                        c.send(msg.encode())

