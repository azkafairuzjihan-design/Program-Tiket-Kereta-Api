# Sistem Pengecekan Kursi dan Jadwal Kereta Api

Program berbasis Python (CLI) untuk membantu penumpang, petugas, dan admin dalam mencari jadwal keberangkatan, menyaring harga tiket sesuai anggaran, mengecek ketersediaan kursi kereta api, serta mengelola data perjalanan dari file dataset CSV.

---

## 1. Identifikasi Masalah
Berdasarkan latar belakang pengolahan data perjalanan kereta api yang berjumlah banyak (misalnya ratusan baris data dalam satu *dataset*), ditemukan beberapa permasalahan utama jika dilakukan secara manual:
1. **Pencarian Lambat dan Kurang Efisien:** Mencari jadwal dari ratusan data secara manual memakan waktu lama, terutama ketika pengguna harus mempertimbangkan banyak kriteria sekaligus (stasiun asal, tujuan, tanggal, jam, kelas, dan anggaran).
2. **Rentan Kesalahan Pembacaan:** Banyaknya variasi data meningkatkan risiko salah baca informasi jadwal maupun status kursi.
3. **Kesulitan Membandingkan Harga dan Ketersediaan:** Perbedaan harga antarkelas serta perubahan jumlah kursi menuntut perbandingan yang teliti agar pengguna tidak melewatkan pilihan kereta yang lebih murah, sesuai jadwal, dan masih memiliki kursi tersedia.

---

## 2. Modul `import` yang Digunakan
Program ini memanfaatkan dua pustaka standar (*built-in library*) Python:
* **`csv`**: Digunakan untuk membaca data dari file `dataset_tiket_kereta.readable.csv` ke dalam struktur *dictionary* (`csv.DictReader`) serta menambahkan baris data jadwal baru ke dalam file CSV (`csv.DictWriter`).
* **`os`**: Digunakan untuk memeriksa keberadaan file *dataset* di direktori penyimpanan (`os.path.exists`) sebelum program membacanya, sehingga mencegah *error* jika file tidak ditemukan.

---

## 3. Daftar Fungsi dalam Program
Program dibagi menjadi beberapa fungsi modular agar kode rapi dan mudah dikelola:

1. **`muat_data()`**
   * Membaca file `dataset_tiket_kereta.readable.csv` dan mengonversi kolom `Harga Tiket` serta `Kursi Tersedia` menjadi tipe data bilangan bulat (`int`), lalu menyimpannya ke dalam *list*.
2. **`pilih_dari_daftar(judul, daftar_pilihan)`**
   * Menampilkan daftar opsi bernomor (seperti stasiun tujuan atau jadwal) dan memvalidasi input pengguna agar memilih nomor yang sesuai.
3. **`menu_pencarian_kereta(data_kereta, role="PENUMPANG")`**
   * Menjalankan alur pencarian kereta secara bertahap mulai dari memilih stasiun asal, stasiun tujuan, tanggal & jam keberangkatan, filter batas harga maksimal, pemilihan kereta, hingga menampilkan hasil status ketersediaan kursi.
4. **`menu_admin(data_kereta)`**
   * Menyediakan panel khusus admin (dilindungi kata sandi) untuk melihat ringkasan total data kereta serta menambahkan jadwal kereta baru langsung ke file CSV.
5. **`main()`**
   * Fungsi utama yang memuat data awal dan menampilkan menu login (Penumpang, Petugas, Admin, atau Keluar) dalam perulangan (*loop*) hingga pengguna memilih keluar.

---

## 4. Alur Proses Program
1. **Inisialisasi Data:** Saat program dijalankan, fungsi `main()` memanggil `muat_data()` untuk memuat seluruh isi file CSV ke memori.
2. **Pemilihan Peran (*Login*):** Pengguna memilih peran pada menu utama (`1` Penumpang, `2` Petugas, `3` Admin, atau `4` Keluar).
3. **Proses Pencarian (Penumpang & Petugas):**
   * Sistem menampilkan daftar stasiun asal yang unik dan meminta input pengguna.
   * Sistem menyaring data dan menampilkan pilihan stasiun tujuan yang tersedia untuk rute tersebut.
   * Pengguna memilih tanggal dan jam keberangkatan.
   * Pengguna memasukkan batas harga tiket maksimal (dalam Rupiah).
   * Sistem menampilkan kereta yang sesuai kriteria dan anggaran. Setelah pengguna memilih salah satu kereta, sistem menampilkan detail lengkap beserta status kursi (**TERSEDIA** beserta sisa kursi, atau **TIDAK TERSEDIA / PENUH**).
4. **Proses Pengelolaan Data (Admin):**
   * Admin memasukkan kata sandi (`admin123`).
   * Admin dapat melihat total jumlah jadwal yang tersimpan atau menginput data perjalanan baru yang otomatis tersimpan ke file `dataset_tiket_kereta.readable.csv`.

---

## 5. Kesimpulan
Penerapan bahasa pemrograman Python dengan modul `csv` dan `os` terbukti mampu menyederhanakan pengolahan data perjalanan kereta api secara otomatis. Program ini berhasil mengatasi kendala pencarian manual dengan menghadirkan fitur penyaringan bertingkat berdasarkan rute, waktu keberangkatan, dan batas anggaran harga. Dengan demikian, informasi ketersediaan kursi dan perbandingan harga tiket dapat diperoleh dengan jauh lebih cepat, akurat, dan efisien.
