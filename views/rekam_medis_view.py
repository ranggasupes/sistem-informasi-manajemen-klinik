import customtkinter as ctk
from tkinter import ttk

class RekamMedisView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Klinik - Rekam Medis")
        self.geometry("950x500")
        
        # Mengubah latar belakang jendela utama menjadi putih
        self.configure(fg_color="white")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------
        # FRAME KIRI: FORMULIR INPUT REKAM MEDIS (Abu-abu Terang)
        # ---------------------------------------------
        self.frame_kiri = ctk.CTkFrame(self, fg_color="#e0e0e0")
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Rekam Medis", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=15)

        # Kolom Isian (Entry) Putih
        self.entry_id_kunjungan = ctk.CTkEntry(self.frame_kiri, placeholder_text="ID Kunjungan", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_id_kunjungan.pack(pady=10, padx=15, fill="x")

        self.entry_diagnosis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Diagnosis Penyakit", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_diagnosis.pack(pady=10, padx=15, fill="x")

        self.entry_tindakan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tindakan Medis", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_tindakan.pack(pady=10, padx=15, fill="x")

        self.entry_catatan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Catatan Dokter", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_catatan.pack(pady=10, padx=15, fill="x")

        # Tombol Simpan (Biru)
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Rekam Medis", fg_color="#3b82f6", hover_color="#2563eb", text_color="#ffffff")
        self.btn_simpan.pack(pady=20, padx=15, fill="x")

        # ---------------------------------------------
        # FRAME KANAN: TABEL DAFTAR REKAM MEDIS
        # ---------------------------------------------
        self.frame_kanan = ctk.CTkFrame(self, fg_color="#e0e0e0")
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Riwayat Rekam Medis Pasien", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=15)

        # Komponen Tabel Visual (Treeview)
        kolom = ("id", "tanggal", "pasien", "diagnosis", "tindakan", "catatan")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("tanggal", text="Tanggal")
        self.tabel.heading("pasien", text="Nama Pasien")
        self.tabel.heading("diagnosis", text="Diagnosis")
        self.tabel.heading("tindakan", text="Tindakan")
        self.tabel.heading("catatan", text="Catatan")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=30, anchor="center")
        self.tabel.column("tanggal", width=75, anchor="center")
        self.tabel.column("pasien", width=100)
        self.tabel.column("diagnosis", width=100)
        self.tabel.column("tindakan", width=90)
        self.tabel.column("catatan", width=100)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

if __name__ == "__main__":
    app = RekamMedisView()
    app.mainloop()