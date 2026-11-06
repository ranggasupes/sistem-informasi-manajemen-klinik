import customtkinter as ctk
from tkinter import ttk

class KunjunganView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Klinik - Data Kunjungan")
        self.geometry("950x500")

        self.configure(fg_color="white")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------
        # FRAME KIRI: FORMULIR INPUT KUNJUNGAN (Latar Belakang Abu-abu)
        # ---------------------------------------------
        self.frame_kiri = ctk.CTkFrame(self, fg_color="#e0e0e0") # Warna latar abu-abu terang
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Kunjungan Pasien", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=15)

        # Kolom Isian (Entry) dengan latar belakang putih
        self.entry_id_pasien = ctk.CTkEntry(self.frame_kiri, placeholder_text="ID Pasien", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_id_pasien.pack(pady=10, padx=15, fill="x")

        self.entry_id_dokter = ctk.CTkEntry(self.frame_kiri, placeholder_text="ID Dokter", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_id_dokter.pack(pady=10, padx=15, fill="x")

        self.entry_tanggal = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tanggal (YYYY-MM-DD)", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_tanggal.pack(pady=10, padx=15, fill="x")

        self.entry_keluhan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Keluhan Pasien", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_keluhan.pack(pady=10, padx=15, fill="x")

        # Tombol Simpan (Warna Biru)
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Kunjungan", fg_color="#3b82f6", hover_color="#2563eb", text_color="#ffffff")
        self.btn_simpan.pack(pady=20, padx=15, fill="x")

        # ---------------------------------------------
        # FRAME KANAN: TABEL DAFTAR KUNJUNGAN
        # ---------------------------------------------
        self.frame_kanan = ctk.CTkFrame(self, fg_color="#e0e0e0") # Disesuaikan senada abu-abu terang
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Kunjungan Pasien", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=15)

        # Komponen Tabel Visual (Treeview)
        kolom = ("id", "tanggal", "pasien", "poli", "dokter", "keluhan")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("tanggal", text="Tanggal")
        self.tabel.heading("pasien", text="Nama Pasien")
        self.tabel.heading("poli", text="Poli")
        self.tabel.heading("dokter", text="Dokter Pemeriksa")
        self.tabel.heading("keluhan", text="Keluhan")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=30, anchor="center")
        self.tabel.column("tanggal", width=80, anchor="center")
        self.tabel.column("pasien", width=100)
        self.tabel.column("poli", width=80)
        self.tabel.column("dokter", width=100)
        self.tabel.column("keluhan", width=120)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)