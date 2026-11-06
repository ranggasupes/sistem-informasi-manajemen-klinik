import customtkinter as ctk
from tkinter import ttk

class PasienView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Klinik - Data Pasien")
        self.geometry("950x500")
        
        # Mengubah latar belakang jendela utama menjadi putih
        self.configure(fg_color="white")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------
        # FRAME KIRI: FORMULIR INPUT DATA PASIEN (Abu-abu Terang)
        # ---------------------------------------------
        self.frame_kiri = ctk.CTkFrame(self, fg_color="#e0e0e0")
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Pasien", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=15)

        # Kolom Isian (Entry) Putih
        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Nama Lengkap Pasien", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_nama.pack(pady=10, padx=15, fill="x")

        self.entry_nik = ctk.CTkEntry(self.frame_kiri, placeholder_text="NIK Pasien", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_nik.pack(pady=10, padx=15, fill="x")

        self.entry_alamat = ctk.CTkEntry(self.frame_kiri, placeholder_text="Alamat", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")

        self.entry_tanggal_lahir = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tanggal Lahir (YYYY-MM-DD)", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_tanggal_lahir.pack(pady=10, padx=15, fill="x")

        self.entry_telepon = ctk.CTkEntry(self.frame_kiri, placeholder_text="No Telepon", fg_color="#ffffff", text_color="#000000", placeholder_text_color="gray")
        self.entry_telepon.pack(pady=10, padx=15, fill="x")

        # Tombol Aksi di Form (Warna Biru)
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data Pasien", fg_color="#3b82f6", hover_color="#2563eb", text_color="#ffffff")
        self.btn_simpan.pack(pady=20, padx=15, fill="x")

        # ---------------------------------------------
        # FRAME KANAN: TABEL DAFTAR PASIEN
        # ---------------------------------------------
        self.frame_kanan = ctk.CTkFrame(self, fg_color="#e0e0e0")
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Pasien Klinik", font=("Arial", 16, "bold"), text_color="#333333").pack(pady=15)

        # Komponen Tabel Visual (Treeview)
        kolom = ("id", "nama", "nik", "alamat", "telepon")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("nama", text="Nama Pasien")
        self.tabel.heading("nik", text="NIK")
        self.tabel.heading("alamat", text="Alamat")
        self.tabel.heading("telepon", text="No Telepon")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=30, anchor="center")
        self.tabel.column("nama", width=130)
        self.tabel.column("nik", width=100)
        self.tabel.column("alamat", width=120)
        self.tabel.column("telepon", width=90)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

if __name__ == "__main__":
    app = PasienView()
    app.mainloop()