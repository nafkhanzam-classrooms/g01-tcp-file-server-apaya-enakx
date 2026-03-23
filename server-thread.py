import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5000
clients = []

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("[Thread Server Running]")


def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def handle_client(conn, addr):
    print(f"Connected: {addr}")

    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break

            msg = data.decode(errors='ignore')

            if msg.startswith('/list'):
                files = os.listdir('.')
                conn.send(("Files: " + str(files)).encode())

            elif msg.startswith('/download'):
                filename = msg.split()[1]
                if os.path.exists(filename):
                    filesize = os.path.getsize(filename)
                    header = f"FILE{SEPARATOR}{filename}{SEPARATOR}{filesize}"
                    conn.send(header.encode())

                    with open(filename, 'rb') as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            conn.sendall(bytes_read)
                else:
                    conn.send(b"File tidak ada")

            elif msg.startswith('UPLOAD'):
                _, filename, filesize = msg.split(SEPARATOR)
                filesize = int(filesize)

                with open(filename, 'wb') as f:
                    remaining = filesize
                    while remaining > 0:
                        chunk = conn.recv(min(BUFFER_SIZE, remaining))
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)

                conn.send(f"Upload {filename} berhasil".encode())

            else:
                print(msg)
                broadcast(data, conn)

        except:
            break

    conn.close()
    clients.remove(conn)


while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr)).start()