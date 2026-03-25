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

Pada tugas ini dibuat sebuah aplikasi berbasis terminal menggunakan Python dengan konsep client-server. Aplikasi ini memungkinkan beberapa client untuk terhubung ke server dan saling berkomunikasi (chat), serta melakukan transfer file seperti upload dan download.

Dalam program ini digunakan beberapa metode untuk menangani banyak client, yaitu synchronous, select, poll, dan threading. Tujuannya adalah untuk memahami perbedaan cara kerja masing-masing metode tersebut.

### 2. Arsitektur Program

Program ini terdiri dari 1 file client (`client.py`) dan 4 file server (`server-sync.py`, `server-select.py`, `server-poll.py`, dan `server-thread.py`).

Komunikasi dilakukan menggunakan TCP socket dengan alamat `127.0.0.1` dan port `5000`. Setiap server dijalankan secara terpisah karena menggunakan port yang sama.

### 3. Penjelasan Client (`client.py`)

Client digunakan untuk menghubungkan user dengan server.

- Client melakukan koneksi ke server menggunakan socket TCP,
- Digunakan threading agar client bisa menerima pesan sekaligus mengirim input dari user,
- Client memiliki beberapa fitur, yaitu:
  - Chat (broadcast ke client lain),
  - Upload file ke server menggunakan perintah `/upload`,
  - Download file dari server menggunakan perintah `/download`.

### 4. Penjelasan Server

#### 4.1. Server Thread (`server-thread.py`)

Server ini menggunakan threading, dimana setiap client ditangani oleh thread terpisah sehingga server bisa melayani banyak client secara bersamaan.

Fitur :

- Broadcast pesan ke semua client
- `/list` untuk menampilkan file di server
- `/upload` untuk menerima file dari client
- `/download` untuk mengirim file ke client

#### 4.2 Server Sync (server-sync.py)

Server ini bersifat synchronous, hanya melayani satu client dalam satu waktu. Client lain harus menunggu sampai client sebelumnya selesai.

Fitur :

- `/list`
- `/upload`
- `/download`

#### 4.3 Server Select (server-select.py)

Server ini menggunakan fungsi `select()` untuk menangani banyak client tanpa thread. Server akan memantau socket yang aktif dan memproses yang siap digunakan.

Fitur :
- Broadcast
- `/list`
- `/upload`
- `/download`

#### 4.4 Server Poll (`server-poll.py`)

Server ini menggunakan `select.poll()` yang merupakan pengembangan dari select. Lebih efisien untuk jumlah client yang banyak.

Fitur :

- Broadcast
- `/list`

### 5. Mekanisme Transfer File

Transfer file dilakukan dengan cara data dikirim dalam bentuk byte dan menggunakan penanda "EOF" sebagai akhir file. 

### 6. Pengujian Program

Pengujian dilakukan dengan langkah berikut :

1. Menjalankan server
2. Menjalankan beberapa client
3. Menguji :
   - Chat antar client (broadcast)
   - Perintah `/list`
   - Upload file ke server
   - Download file dari server

Hasil menunjukkan bahwa :

- Komunikasi antar client berjalan dengan baik,
- File dapat diupload dan didownload,
- Server thread dapat menangani multi-client secara bersamaan.

### 7. Kesimpulan

Berdasarkan hasil implementasi, dapat disimpulkan bahwa :

- Socket memungkinkan komunikasi secara real-time antara client dan server,
- Metode concurrency mempengaruhi cara server menangani banyak client,
- Threading paling mudah digunakan, sedangkan select dan poll lebih efisien.

## Screenshot Hasil

### 1. Server-sync

#### a. Server Running

Menjalankan server dengan `python3 server-sync.py`.

<img width="319" height="116" alt="image" src="https://github.com/user-attachments/assets/c950fa3b-e5a4-4264-aafd-f11acedbca2c" />

#### b. Broadcast Chat  

<img width="302" height="93" alt="image" src="https://github.com/user-attachments/assets/33775af8-15cb-4a60-94eb-70de59fcfd1f" />

#### c. Upload File

Client upload file `coba.txt` ke server.

<img width="271" height="63" alt="image" src="https://github.com/user-attachments/assets/7f02a84f-9cc9-4ae7-9221-28fac932b9cb" />

#### d. Download File  

Client download file `coba.txt` dari server.
<img width="288" height="42" alt="image" src="https://github.com/user-attachments/assets/cf6be240-f120-4bc6-893e-2676ea159a96" />


#### e. List File  

Client menjalankan perintah `/list` untuk melihat daftar file di server.

<img width="276" height="146" alt="image" src="https://github.com/user-attachments/assets/88692ee9-b489-4ba6-b6c1-6426fc6d7142" />

### 2. Server-thread

#### a. Server Running

Menjalankan server dengan `python3 server-thread.py`.

<img width="355" height="129" alt="Server Running" src="https://github.com/user-attachments/assets/2ce53eb6-865c-4a5d-ae54-2a25af145a0f" /> 

#### b. Broadcast Chat  

Client A mengirim pesan.

<img width="356" height="155" alt="Client A - Kirim Pesan" src="https://github.com/user-attachments/assets/4ce1082c-852e-445c-8e87-56fced400c84" />  

Client B otomatis menerima pesan.

<img width="356" height="125" alt="Client B - Terima Pesan" src="https://github.com/user-attachments/assets/29f3c8f7-ec33-49e8-9bd9-e9a04cbd6030" />

#### c. Upload File

Client A upload file `test.txt` ke server.

<img width="289" height="72" alt="Client A - Upload File" src="https://github.com/user-attachments/assets/03fb8015-aee8-4816-ae43-ad5ef01dc34b" />  

File berhasil tersimpan di folder server :

<img width="363" height="113" alt="Server - File Tersimpan" src="https://github.com/user-attachments/assets/cdb50cb6-bff0-4f7c-be99-9fc1a285a6dc" />

#### d. Download File  

Client B download file `test.txt` dari server.

<img width="361" height="110" alt="Client B - Download File" src="https://github.com/user-attachments/assets/640d1d21-d528-402a-b0b5-bd34482716a2" />

#### e. List File  

Client menjalankan perintah `/list` untuk melihat daftar file di server.

<img width="226" height="79" alt="List File di Server" src="https://github.com/user-attachments/assets/9c7acd03-4f8e-43e3-935b-182d21ee9efe" />

### 3. Server-select

#### a. Server Running

Menjalankan server dengan `python3 server-select.py` atau `py server-select.py`.

<img width="402" height="142" alt="image" src="https://github.com/user-attachments/assets/44720954-3125-4e2b-90b8-76f36e413404" />

<img width="326" height="49" alt="image" src="https://github.com/user-attachments/assets/e325810a-488f-406a-b684-17bbcb17a6f6" />

#### b. Broadcast Chat  

Client A mengirim pesan.

<img width="399" height="103" alt="image" src="https://github.com/user-attachments/assets/ed9203b6-aa1c-4981-9557-92b75f30c016" />

<img width="323" height="54" alt="image" src="https://github.com/user-attachments/assets/56a24f1a-c844-4e75-b68c-041e76b8fd70" />

Client B otomatis menerima pesan.

<img width="402" height="122" alt="image" src="https://github.com/user-attachments/assets/724815c6-09ff-49af-a793-cba6f53a8c4e" />

<img width="319" height="65" alt="image" src="https://github.com/user-attachments/assets/cd520165-fcc4-4b1e-95b0-d55cb6ec6b7e" />

#### c. Upload File

Client A upload file `cblagit.txt` ke server.

<img width="220" height="16" alt="image" src="https://github.com/user-attachments/assets/eaff91b3-9962-4818-bdb4-77f04ad66003" />

#### d. Download File  

Client B download file `cblagi.txt` dari server.

<img width="259" height="25" alt="image" src="https://github.com/user-attachments/assets/0d19f9ff-9f0c-4a74-b991-fabae74f22b1" />


#### e. List File  

Client menjalankan perintah `/list` untuk melihat daftar file di server.

<img width="211" height="143" alt="image" src="https://github.com/user-attachments/assets/efd14b0d-f9bc-4215-be92-9b1479995117" />


### 4. Server-poll

#### a. Server Running

Menjalankan server dengan `python3 server-poll.py` atau `py server-poll.py`.

<img width="348" height="70" alt="image" src="https://github.com/user-attachments/assets/c1ec3057-84e9-464e-ad21-d752682042dd" />

#### b. Broadcast Chat  

Client A mengirim pesan.

<img width="363" height="29" alt="image" src="https://github.com/user-attachments/assets/33a6b47c-e676-4830-821e-4a416acf41c0" />

Client B otomatis menerima pesan.

<img width="264" height="40" alt="image" src="https://github.com/user-attachments/assets/613e76ec-0a6d-43ac-a709-7e850c901b1c" />

#### c. Upload File

Client A upload file `testlg.txt` ke server.

<img width="183" height="31" alt="image" src="https://github.com/user-attachments/assets/ed261a4b-18e6-4bea-b098-c9ca84b43144" />

File berhasil tersimpan di folder server :

<img width="259" height="45" alt="image" src="https://github.com/user-attachments/assets/c6c7bf79-a3d9-496e-bf5c-e6b81222e9f7" />

#### d. Download File  

Client B download file `testlg.txt` dari server.

<img width="206" height="31" alt="image" src="https://github.com/user-attachments/assets/07f029a3-356d-4041-ad42-6ec9d2923fb0" />

#### e. List File  

Client menjalankan perintah `/list` untuk melihat daftar file di server.

<img width="183" height="154" alt="image" src="https://github.com/user-attachments/assets/68508385-c75c-4f6f-8a65-654496d5faf1" />
