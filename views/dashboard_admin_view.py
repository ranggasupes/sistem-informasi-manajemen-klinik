import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.admin_controller import AdminController

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

    def __init__(
        self,
        parent,
        username="Apoteker",
        id_user=None,
        on_logout=None
    ):
        super().__init__(parent, fg_color=WARNA_BG)

        self.username = username
        self.id_user = id_user
        self.on_logout = on_logout

        self.controller = AdminController()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()
        self.buat_konten()
        self.tampilkan_dashboard()

    # SIDEBAR
    def buat_sidebar(self):
        sidebar = ctk.CTkFrame(
            self,
            width=190,
            corner_radius=0,
            fg_color=WARNA_BIRU_TUA
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="KLINIK SEHAT",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(30, 5))

        ctk.CTkLabel(
            sidebar,
            text="DASHBOARD ADMIN",
            font=("Arial", 9),
            text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 30))

        menu = [
            ("Dashboard", self.tampilkan_dashboard),
            ("Antrean Resep", self.tampilkan_antrean_resep),
            ("Kelola Obat", self.tampilkan_kelola_obat),
            ("Riwayat Penyerahan", self.tampilkan_riwayat)
        ]

        for teks, fungsi in menu:
            ctk.CTkButton(
                sidebar,
                text=teks,
                command=fungsi,
                height=40,
                anchor="w",
                fg_color="transparent",
                hover_color="#35658F",
                text_color="white"
            ).pack(fill="x", padx=12, pady=3)

        buat_tombol(
            sidebar,
            "Logout",
            self.logout,
            warna=WARNA_MERAH,
            hover="#A83A3A",
            lebar=150
        ).pack(side="bottom", padx=15, pady=15)

        ctk.CTkLabel(
            sidebar,
            text=f"Login sebagai:\n{self.username}",
            text_color="white",
            font=("Arial", 11),
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=5)

    # KONTEN UTAMA
    def buat_konten(self):
        content = ctk.CTkFrame(
            self,
            fg_color=WARNA_BG
        )
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            content,
            fg_color=WARNA_PUTIH,
            corner_radius=0,
            height=70
        )
        header.grid(row=0, column=0, sticky="ew")

        buat_judul(
            header,
            "Sistem Informasi Klinik",
            20
        ).pack(side="left", padx=25, pady=20)

        ctk.CTkLabel(
            header,
            text=f"Selamat datang, {self.username}",
            text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        self.area = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        self.area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=25
        )
        self.area.grid_columnconfigure(0, weight=1)

    # KOMPONEN
    def bersihkan_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def buat_tabel(self, parent, kolom, lebar=None):
        tabel = ttk.Treeview(
            parent,
            columns=kolom,
            show="headings",
            height=14
        )

        for i, nama in enumerate(kolom):
            tabel.heading(
                nama,
                text=nama.replace("_", " ").title()
            )

            ukuran = (
                lebar[i]
                if lebar and i < len(lebar)
                else 120
            )

            tabel.column(
                nama,
                width=ukuran,
                minwidth=70,
                anchor="center"
            )

        tabel.pack(
            fill="both",
            expand=True,
            pady=10
        )

        return tabel

    def buat_halaman(self, judul):
        self.bersihkan_area()

        buat_judul(
            self.area,
            judul,
            22
        ).pack(anchor="w", pady=(0, 10))

    def buat_frame_tabel(self):
        frame = ctk.CTkFrame(
            self.area,
            fg_color=WARNA_PUTIH
        )
        frame.pack(
            fill="both",
            expand=True,
            pady=10
        )
        return frame

    # DASHBOARD
    def tampilkan_dashboard(self):
        self.bersihkan_area()

        data = self.controller.get_dashboard_data()

        buat_judul(
            self.area,
            "Dashboard Admin Apoteker",
            22
        ).pack(anchor="w", pady=(0, 20))

        frame = ctk.CTkFrame(
            self.area,
            fg_color="transparent"
        )
        frame.pack(fill="x")
        frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        daftar_kartu = [
            (
                "Antrean Resep",
                data["jumlah_antrean"],
                WARNA_BIRU
            ),
            (
                "Jenis Obat",
                data["jumlah_obat"],
                WARNA_HIJAU
            ),
            (
                "Riwayat Penyerahan",
                data["jumlah_riwayat"],
                WARNA_BIRU_TUA
            )
        ]

        for i, (judul, nilai, warna) in enumerate(daftar_kartu):
            kartu = ctk.CTkFrame(
                frame,
                fg_color=WARNA_PUTIH
            )
            kartu.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=7,
                pady=7
            )

            ctk.CTkLabel(
                kartu,
                text=judul,
                text_color=WARNA_ABU
            ).pack(
                anchor="w",
                padx=15,
                pady=(15, 5)
            )

            ctk.CTkLabel(
                kartu,
                text=str(nilai),
                font=("Arial", 26, "bold"),
                text_color=warna
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 15)
            )

        ctk.CTkLabel(
            self.area,
            text="Pilih menu Antrean Resep untuk menyerahkan obat.",
            text_color=WARNA_ABU
        ).pack(anchor="w", pady=20)

        buat_tombol(
            self.area,
            "Lihat Antrean Resep",
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
            (
                "nomor_antrian",
                "nama_pasien",
                "nama_dokter",
                "nama_obat",
                "dosis",
                "jumlah",
                "status_penyerahan"
            ),
            [90, 160, 140, 150, 100, 70, 120]
        )

        self.data_antrean = {}

        daftar = self.controller.get_antrean_resep()

        for item in daftar:
            iid = str(item["id_resep"])

            tabel.insert(
                "",
                "end",
                iid=iid,
                values=(
                    item["nomor_antrian"],
                    item["nama_pasien"],
                    item["nama_dokter"] or "-",
                    item["nama_obat"],
                    item["dosis"] or "-",
                    item["jumlah"],
                    item["status_penyerahan"]
                )
            )

            self.data_antrean[iid] = item

        if not daftar:
            ctk.CTkLabel(
                self.area,
                text="Belum ada resep yang menunggu.",
                text_color=WARNA_ABU
            ).pack(anchor="w")

        self.tabel_antrean = tabel

        tombol = ctk.CTkFrame(
            self.area,
            fg_color="transparent"
        )
        tombol.pack(anchor="w", pady=10)

        buat_tombol(
            tombol,
            "Serahkan Obat",
            self.proses_penyerahan,
            warna=WARNA_HIJAU,
            hover="#2E704A"
        ).pack(side="left", padx=(0, 10))

        buat_tombol(
            tombol,
            "Refresh",
            self.tampilkan_antrean_resep
        ).pack(side="left")

    # PROSES PENYERAHAN OBAT
    def proses_penyerahan(self):
        pilihan = self.tabel_antrean.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih resep terlebih dahulu."
            )
            return

        if self.id_user is None:
            messagebox.showerror(
                "Gagal",
                "ID petugas tidak ditemukan. Silakan login kembali."
            )
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

        berhasil, pesan = self.controller.serahkan_obat(
            item["id_kunjungan"],
            self.id_user
        )

        if berhasil:
            messagebox.showinfo("Berhasil", pesan)
            self.tampilkan_antrean_resep()
        else:
            messagebox.showerror("Gagal", pesan)

    # DATA OBAT

    def tampilkan_kelola_obat(self):
        self.buat_halaman("Kelola Data Obat")

        # Tombol tambah
        buat_tombol(
            self.area,
            " + Tambah Obat",
            self.form_tambah_obat,
            warna=WARNA_HIJAU,
            hover="#2E704A"
        ).pack(anchor="w", pady=5)

        # Tabel obat
        tabel = self.buat_tabel(
            self.buat_frame_tabel(),
            (
                "id_obat",
                "nama_obat",
                "jenis_obat",
                "satuan",
                "stok"
            ),
            [80, 220, 160, 120, 100]
        )

        daftar = self.controller.get_data_obat()

        for obat in daftar:
            tabel.insert(
                "",
                "end",
                iid=str(obat["id_obat"]),
                values=(
                    obat["id_obat"],
                    obat["nama_obat"],
                    obat["jenis_obat"],
                    obat["satuan"],
                    obat["stok"]
                )
            )

        if not daftar:
            ctk.CTkLabel(
                self.area,
                text="Belum ada data obat.",
                text_color=WARNA_ABU
            ).pack(anchor="w")

        self.tabel_obat = tabel

        # Tombol edit dan hapus
        tombol = ctk.CTkFrame(
            self.area,
            fg_color="transparent"
        )
        tombol.pack(anchor="w", pady=10)

        buat_tombol(
            tombol,
            "Edit Obat",
            self.form_edit_obat,
            warna=WARNA_BIRU
        ).pack(side="left", padx=(0, 10))

        buat_tombol(
            tombol,
            "Hapus Obat",
            self.hapus_obat,
            warna=WARNA_MERAH,
            hover="#A83A3A"
        ).pack(side="left", padx=(0, 10))

        buat_tombol(
            tombol,
            "Refresh",
            self.tampilkan_kelola_obat
        ).pack(side="left")


    # FORM TAMBAH OBAT
    def form_tambah_obat(self):
        self.form_obat("Tambah Obat")


    # FORM EDIT OBAT
    def form_edit_obat(self):
        pilihan = self.tabel_obat.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih obat yang ingin diedit terlebih dahulu."
            )
            return

        id_obat = int(pilihan[0])

        data = self.controller.get_data_obat()

        obat = next(
            (item for item in data if item["id_obat"] == id_obat),
            None
        )

        if not obat:
            messagebox.showerror(
                "Gagal",
                "Data obat tidak ditemukan."
            )
            return

        self.form_obat("Edit Obat", obat)


    # FORM INPUT OBAT
    def form_obat(self, judul, obat=None):
        popup = ctk.CTkToplevel(self)
        popup.title(judul)
        popup.geometry("400x470")
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        popup.update_idletasks()

        x = (
            popup.winfo_screenwidth() // 2
            - 200
        )
        y = (
            popup.winfo_screenheight() // 2
            - 235
        )

        popup.geometry(f"400x470+{x}+{y}")

        frame = ctk.CTkFrame(
            popup,
            fg_color=WARNA_BG
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        buat_judul(
            frame,
            judul,
            22
        ).pack(anchor="w", padx=15, pady=(15, 20))

        # Input nama obat
        ctk.CTkLabel(
            frame,
            text="Nama Obat"
        ).pack(anchor="w", padx=15)

        input_nama = ctk.CTkEntry(
            frame,
            placeholder_text="Masukkan nama obat",
            height=35
        )
        input_nama.pack(fill="x", padx=15, pady=(5, 12))

        # Input jenis obat
        ctk.CTkLabel(
            frame,
            text="Jenis Obat"
        ).pack(anchor="w", padx=15)

        input_jenis = ctk.CTkEntry(
            frame,
            placeholder_text="Contoh: Tablet, Kapsul, Sirup",
            height=35
        )
        input_jenis.pack(fill="x", padx=15, pady=(5, 12))

        # Input satuan
        ctk.CTkLabel(
            frame,
            text="Satuan"
        ).pack(anchor="w", padx=15)

        input_satuan = ctk.CTkEntry(
            frame,
            placeholder_text="Contoh: Strip, Botol, Box",
            height=35
        )
        input_satuan.pack(fill="x", padx=15, pady=(5, 12))

        # Input stok
        ctk.CTkLabel(
            frame,
            text="Stok"
        ).pack(anchor="w", padx=15)

        input_stok = ctk.CTkEntry(
            frame,
            placeholder_text="Masukkan jumlah stok",
            height=35
        )
        input_stok.pack(fill="x", padx=15, pady=(5, 15))

        # Isi otomatis jika edit
        if obat:
            input_nama.insert(0, obat["nama_obat"])
            input_jenis.insert(0, obat["jenis_obat"])
            input_satuan.insert(0, obat["satuan"])
            input_stok.insert(0, str(obat["stok"]))

        def simpan():
            nama = input_nama.get().strip()
            jenis = input_jenis.get().strip()
            satuan = input_satuan.get().strip()
            stok = input_stok.get().strip()

            if not nama or not jenis or not satuan or not stok:
                messagebox.showwarning(
                    "Peringatan",
                    "Semua kolom wajib diisi.",
                    parent=popup
                )
                return

            try:
                stok = int(stok)

                if stok < 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Peringatan",
                    "Stok harus berupa bilangan bulat minimal 0.",
                    parent=popup
                )
                return

            if obat:
                berhasil = self.controller.update_obat(
                    obat["id_obat"],
                    nama,
                    jenis,
                    satuan,
                    stok
                )
                pesan = "Data obat berhasil diperbarui."
            else:
                berhasil = self.controller.tambah_obat(
                    nama,
                    jenis,
                    satuan,
                    stok
                )
                pesan = "Obat berhasil ditambahkan."

            if berhasil:
                messagebox.showinfo(
                    "Berhasil",
                    pesan,
                    parent=popup
                )
                popup.destroy()
                self.tampilkan_kelola_obat()
            else:
                messagebox.showerror(
                    "Gagal",
                    "Data obat gagal disimpan. Periksa koneksi database atau data yang dimasukkan.",
                    parent=popup
                )

        buat_tombol(
            frame,
            "Simpan",
            simpan,
            warna=WARNA_HIJAU,
            hover="#2E704A"
        ).pack(fill="x", padx=15, pady=(5, 15))


    # HAPUS OBAT
    def hapus_obat(self):
        pilihan = self.tabel_obat.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih obat yang ingin dihapus terlebih dahulu."
            )
            return

        id_obat = int(pilihan[0])

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            "Apakah kamu yakin ingin menghapus obat ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.controller.hapus_obat(id_obat)

        if berhasil:
            messagebox.showinfo(
                "Berhasil",
                "Data obat berhasil dihapus."
            )
            self.tampilkan_kelola_obat()
        else:
            messagebox.showerror(
                "Gagal",
                "Obat tidak dapat dihapus. Bisa jadi obat sudah digunakan dalam resep."
            )

    # RIWAYAT PENYERAHAN
    def tampilkan_riwayat(self):
        self.buat_halaman("Riwayat Penyerahan Obat")

        tabel = self.buat_tabel(
            self.buat_frame_tabel(),
            (
                "nomor_antrian",
                "nama_pasien",
                "nama_obat",
                "jumlah",
                "nama_petugas",
                "waktu_selesai"
            ),
            [90, 160, 170, 80, 130, 170]
        )

        daftar = self.controller.get_riwayat_penyerahan()

        for item in daftar:
            tabel.insert(
                "",
                "end",
                values=(
                    item["nomor_antrian"],
                    item["nama_pasien"],
                    item["nama_obat"],
                    item["jumlah"],
                    item["nama_petugas"] or "-",
                    str(item["waktu_selesai"])
                    if item["waktu_selesai"]
                    else "-"
                )
            )

        if not daftar:
            ctk.CTkLabel(
                self.area,
                text="Belum ada riwayat penyerahan obat.",
                text_color=WARNA_ABU
            ).pack(anchor="w")

        buat_tombol(
            self.area,
            "Refresh",
            self.tampilkan_riwayat
        ).pack(anchor="w", pady=5)

    # LOGOUT
    def logout(self):
        if self.on_logout:
            self.on_logout()
