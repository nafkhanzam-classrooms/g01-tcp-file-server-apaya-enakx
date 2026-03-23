import socket
import select
import os

HOST = '127.0.0.1'
PORT = 5002

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

sockets_list = [server]
clients = {}

print("[Select Server Running]")

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for sock in read_sockets:
        if sock == server:
            client_socket, addr = server.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = addr
        else:
            try:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    sockets_list.remove(sock)
                    continue

                msg = data.decode(errors='ignore')

                if msg.startswith('/list'):
                    sock.send(str(os.listdir('.')).encode())

                else:
                    for c in clients:
                        if c != sock:
                            c.send(data)

            except:
                sockets_list.remove(sock)