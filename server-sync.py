import socket
import os

HOST = '127.0.0.1'
PORT = 5001

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("[Sync Server Running]")

while True:
    conn, addr = server.accept()
    print("Connected:", addr)

    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        msg = data.decode(errors='ignore')

        if msg.startswith('/list'):
            conn.send(str(os.listdir('.')).encode())

        elif msg.startswith('/download'):
            filename = msg.split()[1]
            if os.path.exists(filename):
                filesize = os.path.getsize(filename)
                header = f"FILE{SEPARATOR}{filename}{SEPARATOR}{filesize}"
                conn.send(header.encode())

                with open(filename, 'rb') as f:
                    while True:
                        chunk = f.read(BUFFER_SIZE)
                        if not chunk:
                            break
                        conn.sendall(chunk)
            else:
                conn.send(b"File tidak ada")

        elif msg.startswith('UPLOAD'):
            _, filename, filesize = msg.split(SEPARATOR)
            filesize = int(filesize)

            with open(filename, 'wb') as f:
                remaining = filesize
                while remaining > 0:
                    chunk = conn.recv(min(BUFFER_SIZE, remaining))
                    f.write(chunk)
                    remaining -= len(chunk)

            conn.send(b"Upload berhasil")

        else:
            conn.send(data)

    conn.close()