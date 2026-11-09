
import customtkinter as ctk
from tkinter import ttk


class PasienView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Klinik - Data Pasien")
        self.geometry("1150x650")
        self.configure(fg_color="white")

        # Konfigurasi tampilan utama
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # FRAME KIRI: FORM DATA PASIEN
        # ==========================================

        self.frame_kiri = ctk.CTkFrame(
            self,
            fg_color="#e0e0e0"
        )
        self.frame_kiri.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Pasien",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=15)

        # Frame yang dapat di-scroll
        self.form_scroll = ctk.CTkScrollableFrame(
            self.frame_kiri,
            fg_color="transparent"
        )
        self.form_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # ID User
        self.entry_id_user = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="ID User",
            fg_color="white",
            text_color="black"
        )
        self.entry_id_user.pack(
            pady=8,
            fill="x"
        )

        # Nomor BPJS
        self.entry_nomor_bpjs = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Nomor BPJS",
            fg_color="white",
            text_color="black"
        )
        self.entry_nomor_bpjs.pack(
            pady=8,
            fill="x"
        )

        # NIK
        self.entry_nik = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="NIK Pasien",
            fg_color="white",
            text_color="black"
        )
        self.entry_nik.pack(
            pady=8,
            fill="x"
        )

        # Nama Pasien
        self.entry_nama = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Nama Lengkap Pasien",
            fg_color="white",
            text_color="black"
        )
        self.entry_nama.pack(
            pady=8,
            fill="x"
        )

        # Jenis Kelamin
        ctk.CTkLabel(
            self.form_scroll,
            text="Jenis Kelamin",
            text_color="#333333"
        ).pack(
            anchor="w",
            pady=(8, 2)
        )

        self.entry_jenis_kelamin = ctk.CTkComboBox(
            self.form_scroll,
            values=["Laki-laki", "Perempuan"],
            fg_color="white",
            text_color="black"
        )
        self.entry_jenis_kelamin.pack(
            pady=5,
            fill="x"
        )
        self.entry_jenis_kelamin.set("Laki-laki")

        # Tanggal Lahir
        self.entry_tanggal_lahir = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Tanggal Lahir (YYYY-MM-DD)",
            fg_color="white",
            text_color="black"
        )
        self.entry_tanggal_lahir.pack(
            pady=8,
            fill="x"
        )

        # Alamat
        self.entry_alamat = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Alamat",
            fg_color="white",
            text_color="black"
        )
        self.entry_alamat.pack(
            pady=8,
            fill="x"
        )

        # Nomor Telepon
        self.entry_telepon = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Nomor Telepon",
            fg_color="white",
            text_color="black"
        )
        self.entry_telepon.pack(
            pady=8,
            fill="x"
        )

        # Tombol Simpan
        self.btn_simpan = ctk.CTkButton(
            self.form_scroll,
            text="Simpan Data Pasien",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white"
        )
        self.btn_simpan.pack(
            pady=20,
            fill="x"
        )

        # ==========================================
        # FRAME KANAN: TABEL DAFTAR PASIEN
        # ==========================================

        self.frame_kanan = ctk.CTkFrame(
            self,
            fg_color="#e0e0e0"
        )
        self.frame_kanan.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Pasien Klinik",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=15)

        # Frame tabel
        self.frame_tabel = ctk.CTkFrame(
            self.frame_kanan,
            fg_color="white"
        )
        self.frame_tabel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Kolom tabel
        kolom = (
            "id",
            "nama",
            "nik",
            "alamat",
            "telepon"
        )

        self.tabel = ttk.Treeview(
            self.frame_tabel,
            columns=kolom,
            show="headings",
            height=20
        )

        # Header tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("nama", text="Nama Pasien")
        self.tabel.heading("nik", text="NIK")
        self.tabel.heading("alamat", text="Alamat")
        self.tabel.heading("telepon", text="No Telepon")

        # Lebar kolom
        self.tabel.column(
            "id",
            width=50,
            anchor="center"
        )
        self.tabel.column(
            "nama",
            width=160
        )
        self.tabel.column(
            "nik",
            width=130
        )
        self.tabel.column(
            "alamat",
            width=180
        )
        self.tabel.column(
            "telepon",
            width=120
        )

        # Scrollbar tabel
        scrollbar = ttk.Scrollbar(
            self.frame_tabel,
            orient="vertical",
            command=self.tabel.yview
        )

        self.tabel.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabel.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


if __name__ == "__main__":
    app = PasienView()
    app.mainloop()
