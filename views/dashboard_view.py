
import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.pasien_dashboard_controller import PasienDashboardController


# =====================================================
# PENGATURAN TAMPILAN
# =====================================================

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

WARNA_BG = "#F2F5F8"
WARNA_PUTIH = "#FFFFFF"
WARNA_BIRU = "#367FB5"
WARNA_BIRU_TUA = "#24527A"
WARNA_TEKS = "#333333"
WARNA_ABU = "#777777"
WARNA_GARIS = "#DCE3E9"
WARNA_HIJAU = "#39865B"
WARNA_MERAH = "#C94C4C"


def buat_tombol(parent, teks, command, warna=WARNA_BIRU,
                hover="#286A9D", lebar=150):
    return ctk.CTkButton(
        parent,
        text=teks,
        command=command,
        width=lebar,
        height=38,
        corner_radius=7,
        fg_color=warna,
        hover_color=hover,
        font=("Arial", 12)
    )


def buat_judul(parent, teks, ukuran=20):
    return ctk.CTkLabel(
        parent,
        text=teks,
        font=("Arial", ukuran, "bold"),
        text_color=WARNA_TEKS
    )


def buat_kartu(parent, judul):
    frame = ctk.CTkFrame(
        parent,
        fg_color=WARNA_PUTIH,
        corner_radius=8,
        border_width=1,
        border_color=WARNA_GARIS
    )

    ctk.CTkLabel(
        frame,
        text=judul,
        font=("Arial", 14, "bold"),
        text_color=WARNA_BIRU_TUA
    ).pack(anchor="w", padx=18, pady=(16, 10))

    return frame


def tampilkan_modul_belum_terhubung(nama_modul):
    messagebox.showinfo(
        "Informasi Modul",
        f"Menu {nama_modul} belum dihubungkan dengan controller."
    )


# =====================================================
# DASHBOARD ADMIN / APOTEKER
# =====================================================

class DashboardAdminFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Admin", on_logout=None):
        super().__init__(parent, fg_color=WARNA_BG)

        self.username = username
        self.on_logout = on_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()
        self.buat_konten()

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
            text="SISTEM INFORMASI KLINIK",
            font=("Arial", 9),
            text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 35))

        self.menu_admin(sidebar, "Dashboard", self.refresh_dashboard)
        self.menu_admin(
            sidebar, "Kelola Pasien",
            lambda: tampilkan_modul_belum_terhubung("Pasien")
        )
        self.menu_admin(
            sidebar, "Kelola Dokter & Poli",
            lambda: tampilkan_modul_belum_terhubung("Dokter dan Poli")
        )
        self.menu_admin(
            sidebar, "Kelola Obat",
            lambda: tampilkan_modul_belum_terhubung("Obat")
        )
        self.menu_admin(
            sidebar, "Data Kunjungan",
            lambda: tampilkan_modul_belum_terhubung("Kunjungan")
        )
        self.menu_admin(
            sidebar, "Data Rekam Medis",
            lambda: tampilkan_modul_belum_terhubung("Rekam Medis")
        )

        ctk.CTkLabel(
            sidebar,
            text=f"Login sebagai:\n{self.username}",
            font=("Arial", 11),
            text_color="white",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=(0, 10))

        buat_tombol(
            sidebar,
            "Logout",
            self.logout,
            warna=WARNA_MERAH,
            hover="#A83A3A",
            lebar=150
        ).pack(side="bottom", padx=15, pady=20)

    def menu_admin(self, parent, teks, command):
        ctk.CTkButton(
            parent,
            text=teks,
            height=40,
            corner_radius=6,
            anchor="w",
            fg_color="transparent",
            hover_color="#35658F",
            text_color="white",
            font=("Arial", 12),
            command=command
        ).pack(fill="x", padx=12, pady=3)

    def buat_konten(self):
        content = ctk.CTkFrame(
            self,
            fg_color=WARNA_BG,
            corner_radius=0
        )
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            content,
            fg_color=WARNA_PUTIH,
            corner_radius=0,
            height=70
        )
        header.grid(row=0, column=0, sticky="ew")

        buat_judul(
            header, "Dashboard Admin", 20
        ).pack(side="left", padx=25, pady=20)

        ctk.CTkLabel(
            header,
            text=f"Selamat datang, {self.username}",
            font=("Arial", 12),
            text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        area = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        area.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
        area.grid_columnconfigure((0, 1), weight=1)

        buat_judul(area, "Menu Pengelolaan Klinik", 18).grid(
            row=0, column=0, columnspan=2,
            sticky="w", pady=(0, 15)
        )

        menu_data = [
            ("Data Pasien", "Pengelolaan data pasien klinik."),
            ("Data Dokter dan Poli", "Pengelolaan dokter dan poli."),
            ("Data Obat", "Pengelolaan daftar dan stok obat."),
            ("Data Kunjungan", "Pemantauan kunjungan pasien."),
            ("Data Rekam Medis", "Melihat data rekam medis.")
        ]

        for i, (judul, deskripsi) in enumerate(menu_data):
            row = (i // 2) + 1
            col = i % 2

            kartu = ctk.CTkFrame(
                area,
                fg_color=WARNA_PUTIH,
                corner_radius=8,
                border_width=1,
                border_color=WARNA_GARIS
            )
            kartu.grid(
                row=row, column=col,
                sticky="ew", padx=7, pady=7
            )

            ctk.CTkLabel(
                kartu,
                text=judul,
                font=("Arial", 15, "bold"),
                text_color=WARNA_BIRU_TUA
            ).pack(anchor="w", padx=18, pady=(17, 5))

            ctk.CTkLabel(
                kartu,
                text=deskripsi,
                font=("Arial", 11),
                text_color=WARNA_ABU
            ).pack(anchor="w", padx=18, pady=(0, 15))

        self.info_label = ctk.CTkLabel(
            area,
            text="Pilih menu pada sidebar untuk mengelola data klinik.",
            font=("Arial", 11),
            text_color=WARNA_ABU
        )
        self.info_label.grid(
            row=4, column=0, columnspan=2,
            sticky="w", padx=7, pady=15
        )

    def refresh_dashboard(self):
        messagebox.showinfo(
            "Dashboard",
            "Dashboard admin berhasil diperbarui."
        )

    def logout(self):
        if self.on_logout:
            self.on_logout()


# =====================================================
# DASHBOARD DOKTER
# =====================================================

class DashboardDokterFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Dokter", on_logout=None):
        super().__init__(parent, fg_color=WARNA_BG)

        self.username = username
        self.on_logout = on_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()
        self.buat_konten()

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
            text="DASHBOARD DOKTER",
            font=("Arial", 9),
            text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 35))

        self.menu_dokter(sidebar, "Dashboard", self.refresh_dashboard)
        self.menu_dokter(
            sidebar, "Antrean Pasien",
            lambda: self.tabel.focus_set()
        )
        self.menu_dokter(
            sidebar, "Rekam Medis",
            lambda: tampilkan_modul_belum_terhubung("Rekam Medis")
        )

        ctk.CTkLabel(
            sidebar,
            text=f"Dokter:\n{self.username}",
            font=("Arial", 11),
            text_color="white",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=(0, 10))

        buat_tombol(
            sidebar,
            "Logout",
            self.logout,
            warna=WARNA_MERAH,
            hover="#A83A3A",
            lebar=150
        ).pack(side="bottom", padx=15, pady=20)

    def menu_dokter(self, parent, teks, command):
        ctk.CTkButton(
            parent,
            text=teks,
            height=40,
            corner_radius=6,
            anchor="w",
            fg_color="transparent",
            hover_color="#35658F",
            text_color="white",
            font=("Arial", 12),
            command=command
        ).pack(fill="x", padx=12, pady=3)

    def buat_konten(self):
        content = ctk.CTkFrame(
            self,
            fg_color=WARNA_BG,
            corner_radius=0
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
            header, "Dashboard Dokter", 20
        ).pack(side="left", padx=25, pady=20)

        ctk.CTkLabel(
            header,
            text=f"Dr. {self.username}",
            font=("Arial", 12),
            text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        area = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        area.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(1, weight=1)

        buat_judul(
            area, "Daftar Antrean Pasien", 18
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        tabel_frame = ctk.CTkFrame(
            area,
            fg_color=WARNA_PUTIH,
            corner_radius=8,
            border_width=1,
            border_color=WARNA_GARIS
        )
        tabel_frame.grid(row=1, column=0, sticky="nsew")
        tabel_frame.grid_columnconfigure(0, weight=1)
        tabel_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 10),
            background="white",
            fieldbackground="white"
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#E8EFF6",
            foreground=WARNA_BIRU_TUA,
            padding=8
        )

        columns = (
            "nomor", "pasien", "keluhan", "status"
        )

        self.tabel = ttk.Treeview(
            tabel_frame,
            columns=columns,
            show="headings"
        )

        heading = {
            "nomor": "No. Antrean",
            "pasien": "Nama Pasien",
            "keluhan": "Keluhan",
            "status": "Status"
        }

        widths = {
            "nomor": 100,
            "pasien": 200,
            "keluhan": 350,
            "status": 130
        }

        for kolom in columns:
            self.tabel.heading(kolom, text=heading[kolom])
            self.tabel.column(
                kolom,
                width=widths[kolom],
                anchor="center" if kolom in ("nomor", "status") else "w"
            )

        self.tabel.grid(
            row=0, column=0,
            sticky="nsew", padx=12, pady=12
        )

        tombol = ctk.CTkFrame(
            area,
            fg_color="transparent"
        )
        tombol.grid(row=2, column=0, sticky="ew", pady=15)

        buat_tombol(
            tombol,
            "Refresh Antrean",
            self.refresh_dashboard
        ).pack(side="left")

        buat_tombol(
            tombol,
            "Mulai Pemeriksaan",
            self.mulai_pemeriksaan,
            warna=WARNA_HIJAU,
            hover="#2D704B",
            lebar=170
        ).pack(side="left", padx=10)

    def refresh_dashboard(self):
        messagebox.showinfo(
            "Antrean",
            "Pengambilan data antrean dokter belum dihubungkan."
        )

    def mulai_pemeriksaan(self):
        pilihan = self.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Pemeriksaan",
                "Pilih pasien terlebih dahulu."
            )
            return

        tampilkan_modul_belum_terhubung("Pemeriksaan dan Rekam Medis")

    def logout(self):
        if self.on_logout:
            self.on_logout()


# =====================================================
# DASHBOARD PASIEN
# =====================================================

class DashboardPasienFrame(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        username="Pasien",
        id_user=None,
        on_logout=None
    ):
        super().__init__(parent, fg_color=WARNA_BG)

        self.username = username
        self.id_user = id_user
        self.on_logout = on_logout
        self.controller = PasienDashboardController()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()
        self.buat_konten()

        self.refresh_data()

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
            text="SISTEM INFORMASI KLINIK",
            font=("Arial", 9),
            text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 35))

        self.menu_pasien(sidebar, "Dashboard", self.refresh_data)
        self.menu_pasien(
            sidebar, "Daftar Kunjungan",
            self.buka_form_pendaftaran
        )
        self.menu_pasien(
            sidebar, "Riwayat Medis",
            self.buka_riwayat
        )
        self.menu_pasien(
            sidebar, "Refresh Data",
            self.refresh_data
        )

        ctk.CTkLabel(
            sidebar,
            text=f"Pasien:\n{self.username}",
            font=("Arial", 11),
            text_color="white",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=(0, 10))

        buat_tombol(
            sidebar,
            "Logout",
            self.logout,
            warna=WARNA_MERAH,
            hover="#A83A3A",
            lebar=150
        ).pack(side="bottom", padx=15, pady=20)

    def menu_pasien(self, parent, teks, command):
        ctk.CTkButton(
            parent,
            text=teks,
            height=40,
            corner_radius=6,
            anchor="w",
            fg_color="transparent",
            hover_color="#35658F",
            text_color="white",
            font=("Arial", 12),
            command=command
        ).pack(fill="x", padx=12, pady=3)

    def buat_konten(self):
        content = ctk.CTkFrame(
            self,
            fg_color=WARNA_BG,
            corner_radius=0
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
            header, "Dashboard Pasien", 20
        ).pack(side="left", padx=25, pady=20)

        ctk.CTkLabel(
            header,
            text=f"Selamat datang, {self.username}",
            font=("Arial", 12),
            text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        self.area = ctk.CTkScrollableFrame(
            content,
            fg_color=WARNA_BG,
            corner_radius=0
        )
        self.area.grid(
            row=1, column=0,
            sticky="nsew", padx=25, pady=20
        )
        self.area.grid_columnconfigure((0, 1), weight=1)

        buat_judul(
            self.area, "Informasi Kunjungan", 18
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.antrean_frame = buat_kartu(
            self.area, "ANTREAN KUNJUNGAN AKTIF"
        )
        self.antrean_frame.grid(
            row=1, column=0, columnspan=2,
            sticky="ew", pady=(0, 15)
        )
        self.antrean_frame.grid_columnconfigure(0, weight=1)

        self.antrean_label = ctk.CTkLabel(
            self.antrean_frame,
            text="Memuat antrean...",
            font=("Arial", 12),
            text_color=WARNA_TEKS,
            justify="left",
            anchor="w"
        )
        self.antrean_label.pack(
            anchor="w", padx=18, pady=(0, 15)
        )

        buat_tombol(
            self.antrean_frame,
            "Daftar Kunjungan",
            self.buka_form_pendaftaran,
            lebar=160
        ).pack(anchor="w", padx=18, pady=(0, 18))

        self.profil_frame = buat_kartu(
            self.area, "IDENTITAS PASIEN"
        )
        self.profil_frame.grid(
            row=2, column=0,
            sticky="nsew", padx=(0, 7), pady=5
        )

        self.profil_label = ctk.CTkLabel(
            self.profil_frame,
            text="Memuat data pasien...",
            font=("Arial", 12),
            text_color=WARNA_TEKS,
            justify="left",
            anchor="nw"
        )
        self.profil_label.pack(
            fill="both", expand=True,
            padx=18, pady=(0, 18)
        )

        self.kesehatan_frame = buat_kartu(
            self.area, "INFORMASI KESEHATAN"
        )
        self.kesehatan_frame.grid(
            row=2, column=1,
            sticky="nsew", padx=(7, 0), pady=5
        )

        self.kesehatan_label = ctk.CTkLabel(
            self.kesehatan_frame,
            text="Memuat profil kesehatan...",
            font=("Arial", 12),
            text_color=WARNA_TEKS,
            justify="left",
            anchor="nw"
        )
        self.kesehatan_label.pack(
            fill="both", expand=True,
            padx=18, pady=(0, 18)
        )

    def logout(self):
        if self.on_logout:
            self.on_logout()

    def refresh_data(self):
        if self.id_user is None:
            self.profil_label.configure(
                text="Identitas akun tidak ditemukan."
            )
            self.kesehatan_label.configure(text="-")
            self.antrean_label.configure(text="-")
            return

        pasien, profil = self.controller.get_dashboard_data(
            self.id_user
        )

        if pasien is None:
            self.profil_label.configure(
                text="Data pasien belum tersedia. Hubungi admin."
            )
            self.kesehatan_label.configure(text="-")
            self.antrean_label.configure(text="-")
            return

        tanggal_lahir = pasien["tanggal_lahir"]

        if tanggal_lahir:
            tanggal_lahir = tanggal_lahir.strftime("%d-%m-%Y")
        else:
            tanggal_lahir = "-"

        teks_pasien = (
            f"Nama Lengkap\n{pasien['nama_pasien']}\n\n"
            f"NIK\n{pasien['nik'] or '-'}\n\n"
            f"Nomor BPJS\n{pasien['nomor_bpjs'] or '-'}\n\n"
            f"Jenis Kelamin\n{pasien['jenis_kelamin'] or '-'}\n\n"
            f"Tanggal Lahir\n{tanggal_lahir}\n\n"
            f"Alamat\n{pasien['alamat'] or '-'}\n\n"
            f"No. Telepon\n{pasien['no_telepon'] or '-'}"
        )

        self.profil_label.configure(text=teks_pasien)

        if profil:
            teks_kesehatan = (
                f"Alergi\n{profil['alergi'] or '-'}\n\n"
                f"Penyakit Bawaan\n{profil['penyakit_bawaan'] or '-'}\n\n"
                f"Riwayat Penyakit\n{profil['riwayat_penyakit'] or '-'}\n\n"
                f"Catatan Kesehatan\n{profil['catatan_kesehatan'] or '-'}\n\n"
                f"Sumber Data: {profil['sumber_data'] or '-'}"
            )
        else:
            teks_kesehatan = "Profil kesehatan belum tersedia."

        self.kesehatan_label.configure(text=teks_kesehatan)
        self.refresh_antrean()

    def refresh_antrean(self):
        kunjungan = self.controller.get_antrean_aktif(
            self.id_user
        )

        if kunjungan is None:
            self.antrean_label.configure(
                text="Belum ada kunjungan aktif.\n"
                     "Silakan tekan tombol Daftar Kunjungan."
            )
            return

        tanggal = kunjungan["tanggal_kunjungan"]

        if tanggal:
            tanggal = tanggal.strftime("%d-%m-%Y")

        teks = (
            f"Nomor Antrean: {kunjungan['nomor_antrian']}\n"
            f"Poli: {kunjungan['nama_poli']}\n"
            f"Tanggal: {tanggal}\n"
            f"Status: {kunjungan['status']}\n"
            f"Dokter: {kunjungan['nama_dokter'] or 'Belum ditentukan'}"
        )

        self.antrean_label.configure(text=teks)

    def buka_form_pendaftaran(self):
        window = ctk.CTkToplevel(self)
        window.title("Pendaftaran Kunjungan")
        window.geometry("450x420")
        window.resizable(False, False)
        window.transient(self.winfo_toplevel())
        window.grab_set()
        window.configure(fg_color=WARNA_BG)

        ctk.CTkLabel(
            window,
            text="Pendaftaran Kunjungan",
            font=("Arial", 21, "bold"),
            text_color=WARNA_TEKS
        ).pack(pady=(25, 10))

        form = ctk.CTkFrame(
            window,
            fg_color=WARNA_PUTIH,
            corner_radius=8
        )
        form.pack(fill="both", expand=True, padx=25, pady=10)

        ctk.CTkLabel(
            form,
            text="Tanggal kunjungan: Hari ini",
            font=("Arial", 12),
            text_color=WARNA_TEKS
        ).pack(anchor="w", padx=20, pady=(18, 5))

        ctk.CTkLabel(
            form,
            text="Poli ditentukan otomatis berdasarkan usia pasien.",
            font=("Arial", 11),
            text_color=WARNA_ABU
        ).pack(anchor="w", padx=20, pady=5)

        ctk.CTkLabel(
            form,
            text="Keluhan awal",
            font=("Arial", 12, "bold"),
            text_color=WARNA_TEKS
        ).pack(anchor="w", padx=20, pady=(15, 5))

        entry_keluhan = ctk.CTkTextbox(
            form,
            width=370,
            height=110,
            corner_radius=6
        )
        entry_keluhan.pack(padx=20, pady=5)

        def simpan_pendaftaran():
            keluhan = entry_keluhan.get("1.0", "end").strip()

            berhasil, pesan, hasil = self.controller.daftar_kunjungan(
                self.id_user,
                keluhan
            )

            if not berhasil:
                messagebox.showwarning(
                    "Pendaftaran", pesan, parent=window
                )
                return

            messagebox.showinfo(
                "Pendaftaran Berhasil",
                (
                    f"{pesan}\n\n"
                    f"Nomor Antrean: {hasil['nomor_antrian']}\n"
                    f"Poli: {hasil['nama_poli']}\n"
                    f"Status: {hasil['status']}"
                ),
                parent=window
            )

            window.destroy()
            self.refresh_data()

        buat_tombol(
            form,
            "Konfirmasi Pendaftaran",
            simpan_pendaftaran,
            lebar=370
        ).pack(fill="x", padx=20, pady=18)

    def buka_riwayat(self):
        data = self.controller.get_riwayat_medis(self.id_user)

        window = ctk.CTkToplevel(self)
        window.title("Riwayat Rekam Medis")
        window.geometry("1000x550")
        window.minsize(800, 450)
        window.transient(self.winfo_toplevel())
        window.configure(fg_color=WARNA_BG)

        buat_judul(
            window, "Riwayat Rekam Medis Pasien", 21
        ).pack(anchor="w", padx=25, pady=(20, 5))

        ctk.CTkLabel(
            window,
            text="Daftar pemeriksaan yang pernah dilakukan.",
            font=("Arial", 11),
            text_color=WARNA_ABU
        ).pack(anchor="w", padx=25, pady=(0, 15))

        frame = ctk.CTkFrame(
            window,
            fg_color=WARNA_PUTIH,
            corner_radius=8
        )
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 10),
            background="white",
            fieldbackground="white"
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#E8EFF6",
            foreground=WARNA_BIRU_TUA,
            padding=7
        )

        columns = (
            "tanggal", "poli", "dokter",
            "tekanan", "suhu", "berat", "diagnosis"
        )

        tabel = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headers = {
            "tanggal": "Tanggal Pemeriksaan",
            "poli": "Poli",
            "dokter": "Dokter",
            "tekanan": "Tekanan Darah",
            "suhu": "Suhu Tubuh",
            "berat": "Berat Badan",
            "diagnosis": "Diagnosis"
        }

        widths = {
            "tanggal": 145,
            "poli": 110,
            "dokter": 130,
            "tekanan": 110,
            "suhu": 90,
            "berat": 100,
            "diagnosis": 250
        }

        for kolom, judul in headers.items():
            tabel.heading(kolom, text=judul)
            tabel.column(
                kolom,
                width=widths[kolom],
                anchor="center"
            )

        for row in data:
            tanggal = row["tanggal_pemeriksaan"]

            if tanggal:
                tanggal = tanggal.strftime("%d-%m-%Y %H:%M")

            tabel.insert(
                "",
                "end",
                values=(
                    tanggal or "-",
                    row["nama_poli"] or "-",
                    row["nama_dokter"] or "-",
                    row["tekanan_darah"] or "-",
                    row["suhu_tubuh"] or "-",
                    row["berat_badan"] or "-",
                    row["diagnosis"] or "-"
                )
            )

        tabel.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        if not data:
            ctk.CTkLabel(
                frame,
                text="Belum ada riwayat pemeriksaan.",
                text_color=WARNA_ABU
            ).pack(pady=10)


# =====================================================
# PREVIEW DASHBOARD
# =====================================================

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Sistem Informasi Manajemen Klinik")
    app.geometry("1100x700")
    app.minsize(900, 600)

    # Pilih dashboard untuk preview:
    frame = DashboardAdminFrame(
        app,
        username="Admin Klinik"
    )

    # Untuk preview dashboard dokter:
    # frame = DashboardDokterFrame(app, username="Dokter")

    # Untuk preview dashboard pasien:
    # frame = DashboardPasienFrame(app, username="Pasien", id_user=121)

    frame.pack(fill="both", expand=True)
    app.mainloop()
