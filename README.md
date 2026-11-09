# Sistem Informasi Manajemen Klinik

Aplikasi desktop berbasis Python untuk membantu pengelolaan pelayanan klinik, mulai dari pendaftaran kunjungan pasien, pengelolaan antrean, pemeriksaan dokter, pencatatan rekam medis, hingga penyerahan obat oleh apoteker.

## Fitur Aplikasi

### Pasien

- Login menggunakan akun yang telah disediakan.
- Mendaftarkan kunjungan ke klinik.
- Mendapatkan nomor antrean berdasarkan poli dan tanggal kunjungan.
- Melihat status antrean.
- Melihat profil kesehatan.
- Melihat riwayat rekam medis.

### Dokter

- Melihat antrean pasien sesuai poli.
- Memanggil pasien dan memulai pemeriksaan.
- Mencatat hasil pemeriksaan dan diagnosis.
- Menyimpan rekam medis.
- Membuat resep obat.
- Menyelesaikan kunjungan tanpa resep.

### Apoteker/Admin

- Melihat resep yang menunggu penyerahan.
- Memeriksa informasi resep.
- Mengonfirmasi penyerahan obat.
- Memperbarui stok obat setelah penyerahan dikonfirmasi.

## Alur Pelayanan

1. Pasien login dan mendaftarkan kunjungan.
2. Sistem menentukan poli dan nomor antrean.
3. Dokter memanggil pasien dan melakukan pemeriksaan.
4. Dokter mencatat hasil pemeriksaan ke dalam rekam medis.
5. Jika terdapat resep, kunjungan masuk ke status Menunggu Obat.
6. Apoteker menyerahkan obat dan mengonfirmasi penyerahan.
7. Sistem memperbarui stok obat dan status kunjungan menjadi Selesai.

Jika tidak terdapat resep, dokter dapat menyelesaikan kunjungan secara langsung.

## Teknologi

- Python 3.10
- CustomTkinter
- MySQL
- MySQL Connector/Python
- Pytest
- PyInstaller
- GitHub Actions

## Persyaratan

Untuk menjalankan aplikasi dari source code:

- Windows 10 atau Windows 11
- Python 3.10
- MySQL Server

Untuk menjalankan versi EXE:

- Windows 10 atau Windows 11
- MySQL
