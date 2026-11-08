import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.obat_controller import ObatController
from models.resep_model import ResepModel

from views.dashboard_components import (
    WARNA_BG,
    WARNA_PUTIH,
    WARNA_BIRU,
    WARNA_BIRU_TUA,
    WARNA_ABU,
    WARNA_HIJAU,
    WARNA_MERAH,
    buat_tombol,
    buat_judul
)


class DashboardAdminFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Apoteker", id_user=None, on_logout=None):
        super().__init__(parent, fg_color=WARNA_BG)

        self.username = username
        self.id_user = id_user
        self.on_logout = on_logout
        self.resep_model = ResepModel()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()
        self.buat_konten()
        self.tampilkan_dashboard()

    # SIDEBAR
    def buat_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, width=190, corner_radius=0,
            fg_color=WARNA_BIRU_TUA
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar, text="KLINIK SEHAT",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(30, 5))

        ctk.CTkLabel(
            sidebar, text="DASHBOARD APOTEKER",
            font=("Arial", 9), text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 30))

        menu = [
            ("Dashboard", self.tampilkan_dashboard),
            ("Antrean Resep", self.tampilkan_antrean_resep),
            ("Kelola Obat", self.tampilkan_kelola_obat),
            ("Riwayat Penyerahan", self.tampilkan_riwayat)
        ]

        for teks, fungsi in menu:
            ctk.CTkButton(
                sidebar, text=teks, command=fungsi,
                height=40, anchor="w",
                fg_color="transparent",
                hover_color="#35658F",
                text_color="white"
            ).pack(fill="x", padx=12, pady=3)

        buat_tombol(
            sidebar, "Logout", self.logout,
            warna=WARNA_MERAH, hover="#A83A3A", lebar=150
        ).pack(side="bottom", padx=15, pady=15)

        ctk.CTkLabel(
            sidebar, text=f"Login sebagai:\n{self.username}",
            text_color="white", font=("Arial", 11),
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=5)

    # KONTEN UTAMA
    def buat_konten(self):
        content = ctk.CTkFrame(self, fg_color=WARNA_BG)
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            content, fg_color=WARNA_PUTIH,
            corner_radius=0, height=70
        )
        header.grid(row=0, column=0, sticky="ew")

        buat_judul(
            header, "Sistem Informasi Klinik", 20
        ).pack(side="left", padx=25, pady=20)

        ctk.CTkLabel(
            header, text=f"Selamat datang, {self.username}",
            text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        self.area = ctk.CTkFrame(content, fg_color="transparent")
        self.area.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
        self.area.grid_columnconfigure(0, weight=1)

    def bersihkan_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def buat_tabel(self, parent, kolom, lebar=None):
        tabel = ttk.Treeview(parent, columns=kolom, show="headings", height=14)

        for i, nama in enumerate(kolom):
            tabel.heading(nama, text=nama.replace("_", " ").title())
            ukuran = lebar[i] if lebar and i < len(lebar) else 120
            tabel.column(nama, width=ukuran, minwidth=70, anchor="center")

        tabel.pack(fill="both", expand=True, pady=10)
        return tabel

    def buat_halaman(self, judul):
        self.bersihkan_area()
        buat_judul(self.area, judul, 22).pack(anchor="w", pady=(0, 10))

    def buat_frame_tabel(self):
        frame = ctk.CTkFrame(self.area, fg_color=WARNA_PUTIH)
        frame.pack(fill="both", expand=True, pady=10)
        return frame

    # DASHBOARD
    def tampilkan_dashboard(self):
        self.bersihkan_area()

        antrean = self.resep_model.get_antrean_resep()
        obat = ObatController.get_all_obat()
        riwayat = self.resep_model.get_riwayat_penyerahan()

        jumlah_antrean = len(set(item["id_kunjungan"] for item in antrean))

        buat_judul(
            self.area, "Dashboard Apoteker", 22
        ).pack(anchor="w", pady=(0, 20))

        frame = ctk.CTkFrame(self.area, fg_color="transparent")
        frame.pack(fill="x")
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        data = [
            ("Antrean Resep", jumlah_antrean, WARNA_BIRU),
            ("Jenis Obat", len(obat), WARNA_HIJAU),
            ("Riwayat Penyerahan", len(riwayat), WARNA_BIRU_TUA)
        ]

        for i, (judul, nilai, warna) in enumerate(data):
            kartu = ctk.CTkFrame(frame, fg_color=WARNA_PUTIH)
            kartu.grid(row=0, column=i, sticky="ew", padx=7, pady=7)

            ctk.CTkLabel(
                kartu, text=judul, text_color=WARNA_ABU
            ).pack(anchor="w", padx=15, pady=(15, 5))

            ctk.CTkLabel(
                kartu, text=str(nilai),
                font=("Arial", 26, "bold"), text_color=warna
            ).pack(anchor="w", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            self.area,
            text="Pilih menu Antrean Resep untuk menyerahkan obat.",
            text_color=WARNA_ABU
        ).pack(anchor="w", pady=20)

        buat_tombol(
            self.area, "Lihat Antrean Resep",
            self.tampilkan_antrean_resep
        ).pack(anchor="w")

    # ANTREAN RESEP
    def tampilkan_antrean_resep(self):
        self.buat_halaman("Antrean Resep Pasien")

        ctk.CTkLabel(
            self.area,
            text="Pilih salah satu resep untuk menyerahkan seluruh obat pasien.",
            text_color=WARNA_ABU
        ).pack(anchor="w")

        tabel = self.buat_tabel(
            self.buat_frame_tabel(),
            ("nomor_antrian", "nama_pasien", "nama_dokter",
             "nama_obat", "dosis", "jumlah", "status_penyerahan"),
            [90, 160, 140, 150, 100, 70, 120]
        )

        self.data_antrean = {}
        daftar = self.resep_model.get_antrean_resep()

        for item in daftar:
            iid = str(item["id_resep"])

            tabel.insert("", "end", iid=iid, values=(
                item["nomor_antrian"],
                item["nama_pasien"],
                item["nama_dokter"] or "-",
                item["nama_obat"],
                item["dosis"] or "-",
                item["jumlah"],
                item["status_penyerahan"]
            ))

            self.data_antrean[iid] = item

        if not daftar:
            ctk.CTkLabel(
                self.area, text="Belum ada resep yang menunggu.",
                text_color=WARNA_ABU
            ).pack(anchor="w")

        self.tabel_antrean = tabel

        tombol = ctk.CTkFrame(self.area, fg_color="transparent")
        tombol.pack(anchor="w", pady=10)

        buat_tombol(
            tombol, "Serahkan Obat", self.proses_penyerahan,
            warna=WARNA_HIJAU, hover="#2E704A"
        ).pack(side="left", padx=(0, 10))

        buat_tombol(
            tombol, "Refresh", self.tampilkan_antrean_resep
        ).pack(side="left")

    def proses_penyerahan(self):
        pilihan = self.tabel_antrean.selection()

        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih resep terlebih dahulu.")
            return

        if self.id_user is None:
            messagebox.showerror("Gagal", "ID petugas tidak ditemukan. Silakan login kembali.")
            return

        item = self.data_antrean.get(pilihan[0])

        if not item:
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Serahkan seluruh obat untuk pasien {item['nama_pasien']}?"
        )

        if not konfirmasi:
            return

        berhasil, pesan = self.resep_model.serahkan_obat(
            item["id_kunjungan"], self.id_user
        )

        if berhasil:
            messagebox.showinfo("Berhasil", pesan)
            self.tampilkan_antrean_resep()
        else:
            messagebox.showerror("Gagal", pesan)

    # DATA OBAT
    def tampilkan_kelola_obat(self):
        self.buat_halaman("Data Obat")

        tabel = self.buat_tabel(
            self.buat_frame_tabel(),
            ("id_obat", "nama_obat", "jenis_obat", "satuan", "stok"),
            [80, 200, 150, 100, 100]
        )

        daftar = ObatController.get_all_obat()

        for obat in daftar:
            tabel.insert("", "end", values=(
                obat["id_obat"],
                obat["nama_obat"],
                obat["jenis_obat"],
                obat["satuan"],
                obat["stok"]
            ))

        if not daftar:
            ctk.CTkLabel(
                self.area, text="Belum ada data obat.",
                text_color=WARNA_ABU
            ).pack(anchor="w")

        buat_tombol(
            self.area, "Refresh Data Obat",
            self.tampilkan_kelola_obat
        ).pack(anchor="w", pady=5)

    # RIWAYAT PENYERAHAN
    def tampilkan_riwayat(self):
        self.buat_halaman("Riwayat Penyerahan Obat")

        tabel = self.buat_tabel(
            self.buat_frame_tabel(),
            ("nomor_antrian", "nama_pasien", "nama_obat",
             "jumlah", "nama_petugas", "waktu_selesai"),
            [90, 160, 170, 80, 130, 170]
        )

        daftar = self.resep_model.get_riwayat_penyerahan()

        for item in daftar:
            tabel.insert("", "end", values=(
                item["nomor_antrian"],
                item["nama_pasien"],
                item["nama_obat"],
                item["jumlah"],
                item["nama_petugas"] or "-",
                str(item["waktu_selesai"]) if item["waktu_selesai"] else "-"
            ))

        if not daftar:
            ctk.CTkLabel(
                self.area, text="Belum ada riwayat penyerahan obat.",
                text_color=WARNA_ABU
            ).pack(anchor="w")

        buat_tombol(
            self.area, "Refresh",
            self.tampilkan_riwayat
        ).pack(anchor="w", pady=5)

    def logout(self):
        if self.on_logout:
            self.on_logout()
