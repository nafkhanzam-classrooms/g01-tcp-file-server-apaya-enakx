import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            print("\n" + data.decode(), end="")
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("> ")

    if msg.startswith("/upload"):
        client.send(msg.encode())
        _, filename = msg.split()

        with open(filename, "rb") as f:
            client.sendall(f.read())
        client.send(b"EOF")

        response = client.recv(1024)
        print(response.decode())

    elif msg.startswith("/download"):
        client.send(msg.encode())
        _, filename = msg.split()

        with open("download_" + filename, "wb") as f:
            while True:
                data = client.recv(4096)
                if b"EOF" in data:
                    f.write(data.replace(b"EOF", b""))
                    break
                f.write(data)

        print("Download selesai!")

    else:
        client.send(msg.encode())

