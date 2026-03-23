import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


def receive():
    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            if not data:
                break

            msg = data.decode(errors='ignore')

            if msg.startswith("FILE"):
                _, filename, filesize = msg.split(SEPARATOR)
                filename = "download_" + filename
                filesize = int(filesize)

                with open(filename, 'wb') as f:
                    remaining = filesize
                    while remaining > 0:
                        chunk = client.recv(min(BUFFER_SIZE, remaining))
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)

                print(f"[Download selesai] {filename}")
            else:
                print(msg)
        except:
            break


def send():
    while True:
        msg = input()

        if msg.startswith('/upload'):
            try:
                filename = msg.split()[1]
                if os.path.exists(filename):
                    filesize = os.path.getsize(filename)
                    header = f"UPLOAD{SEPARATOR}{filename}{SEPARATOR}{filesize}"
                    client.send(header.encode())

                    with open(filename, 'rb') as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            client.sendall(bytes_read)
                else:
                    print("File tidak ditemukan")
            except:
                print("Format salah. Gunakan: /upload namafile")

        else:
            client.send(msg.encode())


threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send, daemon=True).start()