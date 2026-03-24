import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    """Thread untuk menerima pesan umum dari server (chat, list, konfirmasi)."""
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            print("\n" + data.decode(), end="\n> ")
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("> ")

    # upload
    if msg.startswith("/upload"):
        client.send(msg.encode())
        _, filename = msg.split()

        if not os.path.exists(filename):
            print("File tidak ditemukan:", filename)
            continue

        ready = client.recv(1024).decode()
        print(ready)

        with open(filename, "rb") as f:
            client.sendall(f.read())
        client.send(b"EOF")

        response = client.recv(1024).decode()
        print(response)

    # donlot
    elif msg.startswith("/download"):
        client.send(msg.encode())
        _, filename = msg.split()

        ready = client.recv(1024).decode()
        print(ready)

        with open("download_" + filename, "wb") as f:
            while True:
                data = client.recv(4096)
                if b"EOF" in data:
                    f.write(data.replace(b"EOF", b""))
                    break
                f.write(data)

        print("Download selesai!")

    # LIST
    elif msg.startswith("/list"):
        client.send(msg.encode())
    

    # CHAT / ECHO
    else:
        client.send(msg.encode())
