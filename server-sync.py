import socket
import os

HOST = '0.0.0.0'
PORT = 5000   

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Server sync listening on port", PORT)

def handle_client(conn, addr):
    print("Connected:", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        msg = data.decode().strip()

        # ini list
        if msg == "/list":
            files = os.listdir(".")
            response = "\n".join(files) + "\n"
            conn.send(response.encode())

        # ini upload
        elif msg.startswith("/upload"):
            filename = msg.split()[1]

            conn.send(b"READY") 

            with open(filename, "wb") as f:
                while True:
                    chunk = conn.recv(1024)
                    if chunk == b"EOF":
                        break
                    f.write(chunk)

            conn.send(b"Upload selesai!\n")

        # ini donlot
        elif msg.startswith("/download"):
            filename = msg.split()[1]

            if not os.path.exists(filename):
                conn.send(b"File tidak ada\n")
            else:
                conn.send(b"READY")

                with open(filename, "rb") as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        conn.send(chunk)

                conn.send(b"EOF")

        else:
            conn.send(data)

    conn.close()
    print("Disconnected:", addr)

while True:
    conn, addr = server.accept()
    handle_client(conn, addr)   
