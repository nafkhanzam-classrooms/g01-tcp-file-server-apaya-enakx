[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mRmkZGKe)
# Network Programming - Assignment G01

## Anggota Kelompok
| Nama                     | NRP        | Kelas |
|--------------------------|------------|-------|
| Shifa Alya Dewi          | 5025241176 | D     |
| Dyah Utami Kesuma Dewi   | 5025241186 | D     |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```

```

## Penjelasan Program

### 1. Pendahuluan

Pada tugas ini, dibuat sebuah aplikasi berbasis terminal menggunakan bahasa Python dengan konsep client-server. Aplikasi ini memungkinkan beberapa client terhubung ke server dan saling berkomunikasi (chat) serta melakukan transfer file seperti upload dan download,

Program ini mengimplementasikan beberapa metode, yaitu:
- Synchronous
- Select
- Poll
- Threading

### 2. Arsitektur Program

Program ini terdiri dari :
- 1 file client : `client.py`
- 4 file server : `server-sync.py`, `server-select.py`, `server-poll.py`, dan `server-thread.py`

Komunikasi dilakukan menggunakan TCP socket dengan alamat `127.0.0.1` dan port `5000`.

### 3. Penjelasan Client (`client.py`)

Client berfungsi sebagai penghubung antara user dengan server.

a. Koneksi ke server
```
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
```
Client membuat socket TCP dan melakukan koneksi ke server.

b. Thread untuk menerima pesan
```
threading.Thread(target=receive, daemon=True).start()
```
Digunakan thread agar client bisa menerima pesan dari server dan tetap bisa input dari user secara bersamaan.

c. Fitur yang tersedia

1. Chat biasa (broadcast)
```
client.send(msg.encode())
```
Pesan dikirim ke server lalu disebarkan ke client lain.

2. Upload file
```
if msg.startswith("/upload"):
```
Client membaca file dari lokal, mengirim isi file ke server, menggunakan "EOF" sebagai akhir file.

3. Download file
```
elif msg.startswith("/download"):
```
CLient menerima data file dari server dan disimpan dengan nama `download_<filename>`.

### 4. Penjelasan Server

#### 4.1. Server Thread (`server-thread.py`)

Server ini menggunakan threading, dimana setiap client ditangani oleh thread terpisah.
```
threading.Thread(target=handle_client, args=(conn, addr)).start()
```
Fitur :

- Broadcast pesan ke semua client
- `/list` untuk menampilkan file di server
- `/upload` untuk menerima file dari client
- `/download` untuk mengirim file ke client

Kelebihan : Bisa melayani banyak client secara paralel

Kekurangan : Menggunakan banyak resource jika client banyak

#### 4.2 Server Sync (server-sync.py)

Server ini bersifat synchronous, hanya melayani satu client dalam satu waktu.

Cara kerja : Server menerima satu koneksi, melayani sampai selesai, baru kemudian menerima client berikutnya.

Fitur :

- `/list`
- `/upload`
- `/download`
 
Kelebihan : Sederhana dan mudah dipahami

Kekurangan : Tidak bisa multi-client secara bersamaan

#### 4.3 Server Select (server-select.py)

Server ini menggunakan fungsi `select()` untuk menangani banyak client tanpa thread.
```
read_ready, _, _ = select.select(sockets, [], [])
```

Cara kerja : Memantau banyak socket sekaligus, menentukan socket mana yang siap dibaca.

Fitur :
- Broadcast
- `/list`
- `/upload`
- `/download`

Kelebihan : Lebih efisien dibanding threading untuk jumlah client sedang

#### 4.4 Server Poll (`server-poll.py`)

Server ini menggunakan `select.poll()` yang merupakan pengembangan dari select.
```
events = poll.poll()
```
Cara kerja : Menggunakan file descriptor

Fitur :

- Broadcast
- `/list`

Kelebihan : Lebih efisien untuk banyak koneksi

Kekurangan : Implementasi lebih kompleks dan fitur file transfer belum selengkap server lain

### 5. Mekanisme Transfer File

Transfer file dilakukan dengan cara data dikirim dalam bentuk byte dan menggunakan penanda "EOF" sebagai akhir file

Contoh :
```
client.send(b"EOF")
```
Server membaca sampai menemukan "EOF".

### 6. Pengujian Program

Pengujian dilakukan dengan langkah berikut :

1. Menjalankan server
2. Menjalankan beberapa client
3. Menguji :
   - Chat antar client (broadcast)
   - Perintah /list
   - Upload file ke server
   - Download file dari server

Hasil menunjukkan bahwa :

- Komunikasi antar client berjalan dengan baik,
- File dapat diupload dan didownload,
- Server thread dapat menangani multi-client secara bersamaan.

### 7. Kesimpulan

Berdasarkan hasil implementasi, dapat disimpulkan bahwa :

- Socket programming memungkinkan komunikasi client-server secara real-time,
- Metode concurrency mempengaruhi performa server,
- Threading paling mudah digunakan untuk multi-client,
- Select dan poll lebih efisien namun lebih kompleks.

## Screenshot Hasil

1. Server Running  
Menjalankan server dengan `python3 server-thread.py`  

<img width="355" height="129" alt="Server Running" src="https://github.com/user-attachments/assets/2ce53eb6-865c-4a5d-ae54-2a25af145a0f" /> 

2. Broadcast Chat  
Client A mengirim pesan  

<img width="356" height="155" alt="Client A - Kirim Pesan" src="https://github.com/user-attachments/assets/4ce1082c-852e-445c-8e87-56fced400c84" />  

Client B otomatis menerima pesan  

<img width="356" height="125" alt="Client B - Terima Pesan" src="https://github.com/user-attachments/assets/29f3c8f7-ec33-49e8-9bd9-e9a04cbd6030" />

3. Upload File  
Client A upload file `test.txt` ke server  

<img width="289" height="72" alt="Client A - Upload File" src="https://github.com/user-attachments/assets/03fb8015-aee8-4816-ae43-ad5ef01dc34b" />  

File berhasil tersimpan di folder server:  

<img width="363" height="113" alt="Server - File Tersimpan" src="https://github.com/user-attachments/assets/cdb50cb6-bff0-4f7c-be99-9fc1a285a6dc" />

4. Download File  
Client B download file `test.txt` dari server  

<img width="361" height="110" alt="Client B - Download File" src="https://github.com/user-attachments/assets/640d1d21-d528-402a-b0b5-bd34482716a2" />

5. List File  
Client menjalankan perintah `/list` untuk melihat daftar file di server  

<img width="226" height="79" alt="List File di Server" src="https://github.com/user-attachments/assets/9c7acd03-4f8e-43e3-935b-182d21ee9efe" />
