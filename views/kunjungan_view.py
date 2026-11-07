
import customtkinter as ctk
from tkinter import ttk


class KunjunganView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Klinik - Data Kunjungan")
        self.geometry("1200x650")
        self.configure(fg_color="white")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # FORM KUNJUNGAN
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
            text="Form Kunjungan Pasien",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=15)

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

        self.entry_id_pasien = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="ID Pasien",
            fg_color="white",
            text_color="black"
        )
        self.entry_id_pasien.pack(
            pady=10,
            fill="x"
        )

        self.entry_id_poli = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="ID Poli",
            fg_color="white",
            text_color="black"
        )
        self.entry_id_poli.pack(
            pady=10,
            fill="x"
        )

        self.entry_id_dokter = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="ID Dokter (Opsional)",
            fg_color="white",
            text_color="black"
        )
        self.entry_id_dokter.pack(
            pady=10,
            fill="x"
        )

        self.entry_tanggal = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Tanggal (YYYY-MM-DD)",
            fg_color="white",
            text_color="black"
        )
        self.entry_tanggal.pack(
            pady=10,
            fill="x"
        )

        self.entry_keluhan = ctk.CTkEntry(
            self.form_scroll,
            placeholder_text="Keluhan Pasien",
            fg_color="white",
            text_color="black"
        )
        self.entry_keluhan.pack(
            pady=10,
            fill="x"
        )

        self.btn_simpan = ctk.CTkButton(
            self.form_scroll,
            text="Simpan Kunjungan",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white"
        )
        self.btn_simpan.pack(
            pady=20,
            fill="x"
        )

        # ==========================================
        # TABEL KUNJUNGAN
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
            text="Daftar Kunjungan Pasien",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=15)

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

        kolom = (
            "id",
            "tanggal",
            "antrian",
            "pasien",
            "poli",
            "dokter",
            "keluhan",
            "status"
        )

        self.tabel = ttk.Treeview(
            self.frame_tabel,
            columns=kolom,
            show="headings"
        )

        headers = {
            "id": "ID",
            "tanggal": "Tanggal",
            "antrian": "Antrean",
            "pasien": "Nama Pasien",
            "poli": "Poli",
            "dokter": "Dokter",
            "keluhan": "Keluhan",
            "status": "Status"
        }

        for kolom_id, judul in headers.items():
            self.tabel.heading(kolom_id, text=judul)

        self.tabel.column("id", width=45, anchor="center")
        self.tabel.column("tanggal", width=95, anchor="center")
        self.tabel.column("antrian", width=65, anchor="center")
        self.tabel.column("pasien", width=130)
        self.tabel.column("poli", width=100)
        self.tabel.column("dokter", width=120)
        self.tabel.column("keluhan", width=160)
        self.tabel.column("status", width=110)

        scrollbar_y = ttk.Scrollbar(
            self.frame_tabel,
            orient="vertical",
            command=self.tabel.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.frame_tabel,
            orient="horizontal",
            command=self.tabel.xview
        )

        self.tabel.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tabel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.frame_tabel.grid_rowconfigure(0, weight=1)
        self.frame_tabel.grid_columnconfigure(0, weight=1)


if __name__ == "__main__":
    app = KunjunganView()
    app.mainloop()
