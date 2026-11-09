# 🏥 Sistem Informasi Manajemen Klinik

Aplikasi desktop manajemen klinik berbasis **Python** dengan arsitektur **MVC**, antarmuka **CustomTkinter**, dan basis data **MySQL/MariaDB**. Aplikasi ini mengelola alur pelayanan klinik dari pendaftaran kunjungan pasien, pemeriksaan dokter, pembuatan resep, sampai penyerahan obat oleh apoteker/admin.

> Proyek UAS Praktikum Rekayasa Perangkat Lunak, Program Studi S1 Sistem Informasi, Universitas Tadulako (Kelompok 1).

---

## ✨ Fitur

Aplikasi memiliki 3 peran (role). Setelah login, pengguna diarahkan ke dashboard sesuai perannya.

| Peran (`role`)                        | Fitur                                                                                                                                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Pasien** (`pasien`)                 | Melihat profil dan profil kesehatan, mendaftar kunjungan dengan mengisi keluhan, melihat nomor dan status antrean aktif, melihat riwayat rekam medis                                                               |
| **Dokter** (`dokter`)                 | Melihat antrean pasien di poli-nya, memanggil pasien, memulai pemeriksaan, mengisi rekam medis (tekanan darah, suhu, berat badan, diagnosis, catatan), membuat resep obat atau menyelesaikan kunjungan tanpa resep |
| **Apoteker/Admin** (`apoteker_admin`) | Melihat antrean resep, menyerahkan obat (stok berkurang otomatis), CRUD data obat (tambah, ubah, hapus, cari), melihat riwayat penyerahan obat                                                                     |

## 🔄 Alur Status Kunjungan

Setiap kunjungan berpindah status mengikuti alur berikut:

```
Menunggu → Dipanggil → Diperiksa → Menunggu Obat → Selesai
 (pasien     (dokter      (dokter      (resep dibuat,     (admin menyerahkan
  daftar)     memanggil)   memeriksa)   menunggu obat)     obat, stok dikurangi)
```

Jika dokter tidak memberi resep, kunjungan langsung berstatus **Selesai** setelah pemeriksaan.

Beberapa aturan bisnis yang diterapkan di kode:

- Pasien **tidak dapat mendaftar lagi** selama masih punya kunjungan yang belum `Selesai`.
- **Poli ditentukan otomatis dari umur pasien**: di bawah 18 tahun ke Poli Anak (`id_poli = 1`), 18 sampai 59 tahun ke Poli Umum (`id_poli = 2`), dan 60 tahun ke atas ke Poli Lansia (`id_poli = 3`).
- **Nomor antrean** dibuat otomatis per poli per tanggal (nomor terakhir + 1).
- Dokter hanya bisa memanggil pasien **dari poli-nya sendiri dan pada hari yang sama**.
- Penyerahan obat berjalan dalam **satu transaksi database** (`FOR UPDATE`): stok dicek, dikurangi, status resep diubah, lalu kunjungan diselesaikan. Jika salah satu langkah gagal, semuanya di-rollback.

## 🧰 Teknologi

| Komponen | Teknologi                                  |
| -------- | ------------------------------------------ |
| Bahasa   | Python 3.10+                               |
| GUI      | CustomTkinter                              |
| Database | MySQL / MariaDB (`mysql-connector-python`) |
| Testing  | pytest, pytest-cov, `unittest.mock`        |
| CI/CD    | GitHub Actions                             |

## 📂 Struktur Proyek

```
sistem-informasi-manajemen-klinik/
├── main.py                      # Entry point, menjalankan LoginView
├── requirements.txt             # Daftar dependensi
├── config/
│   └── database.py              # Konfigurasi dan koneksi MySQL
├── models/                      # Layer Model: query SQL ke database
│   ├── user_model.py
│   ├── pasien_model.py
│   ├── dokter_model.py
│   ├── profil_kesehatan_model.py
│   ├── kunjungan_model.py
│   ├── rekam_medis_model.py
│   ├── resep_model.py
│   └── obat_model.py
├── controllers/                 # Layer Controller: logika aplikasi
│   ├── auth_controller.py
│   ├── pasien_controller.py
│   ├── dokter_controller.py
│   ├── admin_controller.py
│   └── obat_controller.py
├── views/                       # Layer View: antarmuka CustomTkinter
│   ├── login_view.py
│   ├── dashboard_view.py        # Menggabungkan 3 dashboard
│   ├── dashboard_pasien_view.py
│   ├── dashboard_dokter_view.py
│   ├── dashboard_admin_view.py
│   └── dashboard_components.py  # Warna dan komponen UI yang dipakai ulang
├── tests/                       # Unit test (pytest)
├── backup/                      # Arsip versi lama controller dan view
└── .github/workflows/
    └── ci_pipeline.yml          # Pipeline CI
```

## 🏗️ Arsitektur MVC

```
View (customtkinter)  →  Controller  →  Model  →  MySQL
   login_view.py          auth_controller    user_model
   dashboard_*.py         pasien_controller  pasien_model, kunjungan_model, ...
```

- **View** menampilkan UI dan menerima input pengguna.
- **Controller** memvalidasi input dan menjalankan logika (misalnya menentukan poli dari umur).
- **Model** menjalankan query SQL ke database dan mengembalikan hasilnya.

Setiap model memakai pola yang sama: ambil koneksi dari `Database.get_connection()`, jalankan _parameterized query_ (`%s`) untuk mencegah SQL Injection, tangani error dengan `try/except` (rollback jika gagal), lalu tutup cursor dan koneksi di blok `finally`.

> Catatan: pada `dashboard_dokter_view.py`, view dokter memanggil model secara langsung (`KunjunganModel`, `RekamMedisModel`, `DokterModel`) karena `DokterController` saat ini baru berisi `daftar_dokter()`.

## 🔐 Autentikasi dan RBAC

- Login ditangani `AuthController.login()`: password yang diinput di-hash dengan **SHA-256**, lalu dibandingkan dengan hash di database memakai `hmac.compare_digest` (aman terhadap _timing attack_).
- Jika login berhasil, `LoginView` membaca kolom `role` dan membuka dashboard yang sesuai. Role di luar `pasien`, `dokter`, dan `apoteker_admin` ditolak.
- Otorisasi juga dijaga di level query. Contohnya, dokter hanya bisa memeriksa kunjungan yang `id_dokter`-nya terhubung ke `id_user` dokter yang sedang login.

## 🗄️ Basis Data

Nama database: **`sistem_informasi_klinik`**

| Tabel              | Kolom utama                                                                                                                            |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `users`            | id_user, username, password (hash SHA-256), role                                                                                       |
| `pasien`           | id_pasien, id_user, nomor_bpjs, nik, nama_pasien, jenis_kelamin, tanggal_lahir, alamat, no_telepon                                     |
| `profil_kesehatan` | id_profil, id_pasien, alergi, penyakit_bawaan, riwayat_penyakit, catatan_kesehatan, sumber_data, tanggal_sinkronisasi                  |
| `dokter`           | id_dokter, id_user, id_poli, nama_dokter, spesialisasi, no_telepon                                                                     |
| `poli`             | id_poli, nama_poli                                                                                                                     |
| `kunjungan`        | id_kunjungan, id_pasien, id_poli, id_dokter, nomor_antrian, tanggal_kunjungan, keluhan_awal, status, id_petugas_selesai, waktu_selesai |
| `rekam_medis`      | id_rekam_medis, id_kunjungan, tekanan_darah, suhu_tubuh, berat_badan, diagnosis, catatan                                               |
| `resep`            | id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan                                                      |
| `obat`             | id_obat, nama_obat, jenis_obat, satuan, stok                                                                                           |

## 🚀 Cara Menjalankan

**Prasyarat:** Python 3.10+, MySQL/MariaDB (misalnya lewat XAMPP), dan Git.

```bash
# 1. Clone repository
git clone https://github.com/<username>/sistem-informasi-manajemen-klinik.git
cd sistem-informasi-manajemen-klinik

# 2. Buat dan aktifkan virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

# 3. Install dependensi
pip install -r requirements.txt
```

**4. Siapkan database.** Buat database `sistem_informasi_klinik` di MySQL, lalu buat tabel-tabel di atas. Isi juga data awal: tabel `poli` dengan 3 poli (`id_poli` 1 = Poli Anak, 2 = Poli Umum, 3 = Poli Lansia) dan akun `users` untuk setiap role.

**5. Atur koneksi database** di `config/database.py`:

```python
HOST = "localhost"
USER = "root"
PASSWORD = ""
DATABASE = "sistem_informasi_klinik"
```

**6. Jalankan aplikasi:**

```bash
python main.py
```

## 🧪 Pengujian

Unit test memakai **pytest** dan `unittest.mock`, jadi database dan GUI di-mock dan test **tidak membutuhkan koneksi MySQL**.

```bash
pytest -v                          # jalankan semua test
pytest --cov=models --cov=controllers   # dengan laporan coverage
```

| File test                  | Yang diuji                                                                          |
| -------------------------- | ----------------------------------------------------------------------------------- |
| `test_auth.py`             | Login (berhasil, password salah, user tidak ada), konsistensi hash SHA-256          |
| `test_user.py`             | Model user                                                                          |
| `test_pasien.py`           | Model dan controller pasien, penentuan poli berdasarkan umur, pendaftaran kunjungan |
| `test_dokter.py`           | Model dan controller dokter                                                         |
| `test_profil_kesehatan.py` | Model profil kesehatan                                                              |
| `test_kunjungan.py`        | Nomor antrean, antrean aktif, panggil pasien, mulai pemeriksaan                     |
| `test_rekam_medis.py`      | Rekam medis dan pembuatan resep oleh dokter                                         |
| `test_resep.py`            | Antrean resep dan penyerahan obat                                                   |
| `test_obat.py`             | CRUD dan pencarian obat                                                             |
| `test_admin.py`            | Controller admin                                                                    |

## ⚙️ CI/CD

Workflow `.github/workflows/ci_pipeline.yml` berjalan otomatis pada setiap **push** dan **pull request** ke branch `main`:

1. Checkout repository
2. Setup Python 3.10
3. Install dependensi dari `requirements.txt`
4. Jalankan `pytest -v`

## 👥 Tim Pengembang (Kelompok 1)

| Nama                   | NIM         |
| ---------------------- | ----------- |
| Salwa Shafa Salsabila  | F5212510003 |
| Patimah Azzahra        | F5212510006 |
| Ibnaty Naeela Adjani   | F5212510008 |
| Aditya Eka Kumara      | F5212510019 |
| Rosaria Reflin Gala    | F5212510029 |
| Rangga Ferdi Kurniawan | F5212510032 |
| Moh. Daffa Setiawan    | F5212520039 |

**Asisten Dosen:** Cindy Amelia dan Rut Naomi Ester Sitompul
