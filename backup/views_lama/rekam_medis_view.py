
import customtkinter as ctk
from tkinter import ttk


class RekamMedisView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Klinik - Rekam Medis")
        self.geometry("1250x650")
        self.configure(fg_color="white")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # FRAME KIRI: FORM REKAM MEDIS
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

        self.frame_kiri.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Rekam Medis",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=20)

        self.entry_id_kunjungan = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="ID Kunjungan"
        )
        self.entry_id_kunjungan.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        self.entry_tekanan_darah = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tekanan Darah (contoh: 120/80)"
        )
        self.entry_tekanan_darah.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        self.entry_suhu_tubuh = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Suhu Tubuh (°C)"
        )
        self.entry_suhu_tubuh.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        self.entry_berat_badan = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Berat Badan (kg)"
        )
        self.entry_berat_badan.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        self.entry_diagnosis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Diagnosis"
        )
        self.entry_diagnosis.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Catatan Pemeriksaan",
            text_color="#333333"
        ).pack(
            anchor="w",
            padx=15,
            pady=(8, 2)
        )

        self.entry_catatan = ctk.CTkTextbox(
            self.frame_kiri,
            height=100,
            fg_color="white",
            text_color="black"
        )
        self.entry_catatan.pack(
            pady=5,
            padx=15,
            fill="x"
        )

        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Rekam Medis",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white"
        )
        self.btn_simpan.pack(
            pady=20,
            padx=15,
            fill="x"
        )

        # FRAME KANAN: TABEL REKAM MEDIS
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
            text="Riwayat Rekam Medis Pasien",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=15)

        kolom = (
            "id",
            "kunjungan",
            "tanggal",
            "pasien",
            "tekanan_darah",
            "diagnosis",
            "catatan"
        )

        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
            height=20
        )

        self.tabel.heading("id", text="ID")
        self.tabel.heading("kunjungan", text="ID Kunjungan")
        self.tabel.heading("tanggal", text="Tanggal Pemeriksaan")
        self.tabel.heading("pasien", text="Nama Pasien")
        self.tabel.heading("tekanan_darah", text="Tekanan Darah")
        self.tabel.heading("diagnosis", text="Diagnosis")
        self.tabel.heading("catatan", text="Catatan")

        self.tabel.column("id", width=45, anchor="center")
        self.tabel.column("kunjungan", width=90, anchor="center")
        self.tabel.column("tanggal", width=140, anchor="center")
        self.tabel.column("pasien", width=130)
        self.tabel.column("tekanan_darah", width=110, anchor="center")
        self.tabel.column("diagnosis", width=150)
        self.tabel.column("catatan", width=200)

        scrollbar_y = ttk.Scrollbar(
            self.frame_kanan,
            orient="vertical",
            command=self.tabel.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.frame_kanan,
            orient="horizontal",
            command=self.tabel.xview
        )

        self.tabel.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tabel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 0)
        )

        scrollbar_y.pack(
            side="right",
            fill="y",
            padx=(0, 10)
        )

        scrollbar_x.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )


if __name__ == "__main__":
    app = RekamMedisView()
    app.mainloop()
