import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 5000

clients = []

def handle_client(conn, addr):
    print("Connected:", addr)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode()

            if msg.startswith("/list"):
                files = os.listdir()
                conn.send(("\n".join(files)).encode())

            elif msg.startswith("/upload"):
                _, filename = msg.split()
                with open(filename, "wb") as f:
                    while True:
                        chunk = conn.recv(4096)
                        if b"EOF" in chunk:
                            f.write(chunk.replace(b"EOF", b""))
                            break
                        f.write(chunk)
                conn.send(b"Upload selesai!\n")

            elif msg.startswith("/download"):
                _, filename = msg.split()
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        conn.sendall(f.read())
                    conn.send(b"EOF")
                else:
                    conn.send(b"File tidak ada\n")

            else:
                # broadcast
                for c in clients:
                    if c != conn:
                        c.send((f"[{addr}] {msg}\n").encode())

        except:
            break

    clients.remove(conn)
    conn.close()
    print("Disconnected:", addr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Server THREAD running...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr)).start()



