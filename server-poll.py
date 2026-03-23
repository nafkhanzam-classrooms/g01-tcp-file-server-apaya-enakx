import socket
import select
import os

HOST = '127.0.0.1'
PORT = 5003

BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)

poll = select.poll()
poll.register(server, select.POLLIN)

connections = {}

print("[Poll Server Running]")

while True:
    events = poll.poll()

    for fd, flag in events:
        if fd == server.fileno():
            conn, addr = server.accept()
            conn.setblocking(False)
            poll.register(conn, select.POLLIN)
            connections[conn.fileno()] = conn
        else:
            conn = connections[fd]
            try:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    poll.unregister(fd)
                    conn.close()
                    continue

                msg = data.decode(errors='ignore')

                if msg.startswith('/list'):
                    conn.send(str(os.listdir('.')).encode())
                else:
                    for c in connections.values():
                        if c != conn:
                            c.send(data)
            except:
                poll.unregister(fd)
                conn.close()