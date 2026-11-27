# Sistem Pengecekan & Pemesanan Kursi Kereta Api

Program berbasis Python (CLI) untuk membantu penumpang, petugas, dan admin dalam mencari jadwal keberangkatan, menyaring harga tiket sesuai anggaran, mengecek ketersediaan kursi, memesan tiket kereta api, serta mengelola dan menganalisis data perjalanan dari file dataset CSV.

---

## 1. Identifikasi Masalah
Berdasarkan latar belakang pengolahan data perjalanan kereta api yang berjumlah banyak (misalnya ratusan baris data dalam satu *dataset*), ditemukan beberapa permasalahan utama jika dilakukan secara manual:
1. **Pencarian Lambat dan Kurang Efisien:** Mencari jadwal dari ratusan data secara manual memakan waktu lama, terutama ketika pengguna harus mempertimbangkan banyak kriteria sekaligus (stasiun asal, tujuan, tanggal, jam, kelas, dan anggaran).
2. **Rentan Kesalahan Pembacaan dan Pencatatan:** Banyaknya variasi data meningkatkan risiko salah baca jadwal maupun ketidakakuratan pembaruan sisa kursi setelah terjadi pemesanan.
3. **Kesulitan Membandingkan Harga dan Ketersediaan:** Perbedaan harga antarkelas serta perubahan jumlah kursi menuntut perbandingan yang teliti agar pengguna tidak melewatkan pilihan kereta yang lebih murah, sesuai jadwal, dan masih memiliki kursi tersedia.

---

## 2. Modul `import` yang Digunakan
Program ini memanfaatkan tiga pustaka standar (*built-in library*) Python:
* **`csv`**: Digunakan untuk membaca data dari file `dataset_tiket_kereta.readable.csv` ke dalam struktur *dictionary* (`csv.DictReader`) serta memperbarui/menulis ulang seluruh data jadwal dan sisa kursi ke dalam file CSV (`csv.DictWriter`).
* **`os`**: Digunakan untuk memeriksa keberadaan file *dataset* di direktori penyimpanan (`os.path.exists`) sebelum program membacanya, sehingga mencegah *error* apabila file tidak ditemukan.
* **`datetime` (`from datetime import datetime`)**: Digunakan untuk memvalidasi format tanggal keberangkatan (`YYYY-MM-DD`) dan format jam keberangkatan (`HH:MM`) melalui `datetime.strptime()` dan `strftime()` saat admin memfilter jadwal yang sudah berlalu maupun saat menambahkan jadwal kereta baru.

---

## 3. Daftar Fungsi dalam Program
Program disusun secara modular ke dalam tujuh fungsi utama:

1. **`muat_data()`**
   * Membaca file `dataset_tiket_kereta.readable.csv`, mengonversi kolom `Harga Tiket` dan `Kursi Tersedia` menjadi bilangan bulat (`int`), serta mencatat `Kursi Awal` sebagai acuan kapasitas kursi sebelum pemesanan.
2. **`simpan_semua_data(data_kereta)`**
   * Menyimpan kembali seluruh perubahan data (seperti pengurangan sisa kursi, perubahan status menjadi `"Penuh"`, atau penambahan jadwal baru) secara permanen ke dalam file CSV.
3. **`pilih_dari_daftar(judul, daftar_pilihan)`**
   * Menampilkan daftar opsi bernomor (stasiun tujuan, jadwal, kelas, atau nama kereta) dan memvalidasi input pengguna agar memilih nomor yang valid.
4. **`tanya_lanjut(pesan)`**
   * Memberikan konfirmasi perulangan (`y/n`) kepada pengguna apakah ingin melanjutkan pencarian, pemesanan, atau melihat ringkasan data lainnya.
5. **`menu_pencarian_kereta(data_kereta, role="PENUMPANG")`**
   * Menjalankan alur pencarian kereta secara bertahap (stasiun asal, tujuan, tanggal & jam, batas harga maksimal, serta pemilihan kereta). Khusus peran **Penumpang**, fungsi ini juga memproses pemesanan kursi, menghitung total harga, dan mengurangi sisa kursi secara otomatis.
6. **`menu_admin(data_kereta)`**
   * Menyediakan panel khusus admin (dilindungi kata sandi `admin123`) untuk melihat 3 jenis ringkasan data kereta serta menambahkan jadwal perjalanan baru dengan validasi tanggal, jam, harga, dan jumlah kursi.
7. **`main()`**
   * Fungsi utama yang memuat data awal dan menampilkan menu login (Penumpang, Petugas, Admin, atau Keluar) secara berulang hingga pengguna memilih keluar.

---

## 4. Alur Proses Program
1. **Inisialisasi Data:** Program memanggil `muat_data()` untuk membaca seluruh jadwal kereta dari `dataset_tiket_kereta.readable.csv` ke memori.
2. **Pemilihan Peran (*Login*):** Pengguna memilih peran pada menu utama (`1` Penumpang, `2` Petugas, `3` Admin, atau `4` Keluar).
3. **Proses Pencarian & Pemesanan (Penumpang & Petugas):**
   * Pengguna memasukkan stasiun asal (sistem otomatis membersihkan karakter non-alfanumerik dan huruf kapital agar pencarian fleksibel).
   * Pengguna memilih stasiun tujuan, tanggal & jam keberangkatan, serta memasukkan batas anggaran harga tiket maksimal.
   * Setelah memilih kereta, sistem menampilkan status ketersediaan kursi. Jika peran adalah **Penumpang** dan kursi tersedia, penumpang dapat menginput jumlah kursi yang dipesan, melihat total biaya, dan sisa kursi langsung diperbarui ke file CSV.
4. **Proses Analisis & Manajemen Data (Admin):**
   * Setelah memasukkan kata sandi (`admin123`), admin dapat melihat:
     1. Ringkasan kereta yang sudah berlalu sebelum tanggal batas tertentu.
     2. Ringkasan kelas dan perbandingan sisa kursi terhadap kursi awal berdasarkan nama kereta.
     3. Ringkasan 5 kereta dengan sisa kursi paling sedikit.
   * Admin juga dapat menambah jadwal kereta baru dengan validasi format tanggal/jam menggunakan `datetime` serta validasi nilai positif untuk harga dan kursi.

---

## 5. Kesimpulan
Penerapan bahasa pemrograman Python dengan modul `csv`, `os`, dan `datetime` terbukti mampu mengotomatisasi pengelolaan dan pencarian data perjalanan kereta api secara efektif. Program ini tidak hanya mempercepat proses penyaringan jadwal berdasarkan rute dan anggaran, tetapi juga menjaga keakuratan data melalui pembaruan sisa kursi secara *real-time* saat pemesanan serta validasi format waktu pada sisi admin. Dengan demikian, risiko kesalahan manual dapat diminimalkan dan pengambilan keputusan pengguna menjadi jauh lebih cepat dan akurat.
