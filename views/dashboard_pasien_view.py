
import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.pasien_dashboard_controller import PasienDashboardController

from views.dashboard_components import (
    WARNA_BG,
    WARNA_PUTIH,
    WARNA_BIRU,
    WARNA_BIRU_TUA,
    WARNA_TEKS,
    WARNA_ABU,
    WARNA_GARIS,
    WARNA_HIJAU,
    WARNA_MERAH,
    buat_tombol,
    buat_judul,
    buat_kartu
)


class DashboardPasienFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Pasien", id_user=None, on_logout=None):
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
            sidebar, text="SISTEM INFORMASI KLINIK",
            font=("Arial", 9), text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 35))

        menu = [
            ("Dashboard", self.refresh_data),
            ("Daftar Kunjungan", self.buka_form_pendaftaran),
            ("Riwayat Medis", self.buka_riwayat),
            ("Refresh Data", self.refresh_data)
        ]

        for teks, command in menu:
            ctk.CTkButton(
                sidebar, text=teks, height=40,
                corner_radius=6, anchor="w",
                fg_color="transparent",
                hover_color="#35658F",
                text_color="white",
                command=command
            ).pack(fill="x", padx=12, pady=3)

        ctk.CTkLabel(
            sidebar, text=f"Pasien:\n{self.username}",
            font=("Arial", 11), text_color="white",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=(0, 10))

        buat_tombol(
            sidebar, "Logout", self.logout,
            warna=WARNA_MERAH, hover="#A83A3A",
            lebar=150
        ).pack(side="bottom", padx=15, pady=20)

    # KONTEN DASHBOARD
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

        buat_judul(header, "Dashboard Pasien", 20).pack(
            side="left", padx=25, pady=20
        )

        ctk.CTkLabel(
            header, text=f"Selamat datang, {self.username}",
            font=("Arial", 12), text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        self.area = ctk.CTkScrollableFrame(
            content, fg_color=WARNA_BG
        )
        self.area.grid(
            row=1, column=0, sticky="nsew",
            padx=25, pady=20
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

        self.antrean_label = ctk.CTkLabel(
            self.antrean_frame, text="Memuat antrean...",
            font=("Arial", 12), text_color=WARNA_TEKS,
            justify="left", anchor="w"
        )
        self.antrean_label.pack(anchor="w", padx=18, pady=10)

        buat_tombol(
            self.antrean_frame, "Daftar Kunjungan",
            self.buka_form_pendaftaran, lebar=160
        ).pack(anchor="w", padx=18, pady=(0, 18))

        self.profil_frame = buat_kartu(
            self.area, "IDENTITAS PASIEN"
        )
        self.profil_frame.grid(
            row=2, column=0, sticky="nsew",
            padx=(0, 7), pady=5
        )

        self.profil_label = ctk.CTkLabel(
            self.profil_frame, text="Memuat data pasien...",
            font=("Arial", 12), text_color=WARNA_TEKS,
            justify="left", anchor="nw"
        )
        self.profil_label.pack(
            fill="both", expand=True, padx=18, pady=18
        )

        self.kesehatan_frame = buat_kartu(
            self.area, "INFORMASI KESEHATAN"
        )
        self.kesehatan_frame.grid(
            row=2, column=1, sticky="nsew",
            padx=(7, 0), pady=5
        )

        self.kesehatan_label = ctk.CTkLabel(
            self.kesehatan_frame, text="Memuat profil kesehatan...",
            font=("Arial", 12), text_color=WARNA_TEKS,
            justify="left", anchor="nw"
        )
        self.kesehatan_label.pack(
            fill="both", expand=True, padx=18, pady=18
        )

    # REFRESH DATA
    def refresh_data(self):
        if self.id_user is None:
            self.profil_label.configure(text="Identitas akun tidak ditemukan.")
            self.kesehatan_label.configure(text="-")
            self.antrean_label.configure(text="-")
            return

        pasien, profil = self.controller.get_dashboard_data(self.id_user)

        if not pasien:
            self.profil_label.configure(
                text="Data pasien belum tersedia. Hubungi admin."
            )
            self.kesehatan_label.configure(text="-")
            self.antrean_label.configure(text="-")
            return

        tanggal = pasien["tanggal_lahir"]
        tanggal = tanggal.strftime("%d-%m-%Y") if tanggal else "-"

        self.profil_label.configure(text=(
            f"Nama Lengkap\n{pasien['nama_pasien']}\n\n"
            f"NIK\n{pasien['nik'] or '-'}\n\n"
            f"Nomor BPJS\n{pasien['nomor_bpjs'] or '-'}\n\n"
            f"Jenis Kelamin\n{pasien['jenis_kelamin'] or '-'}\n\n"
            f"Tanggal Lahir\n{tanggal}\n\n"
            f"Alamat\n{pasien['alamat'] or '-'}\n\n"
            f"No. Telepon\n{pasien['no_telepon'] or '-'}"
        ))

        if profil:
            teks = (
                f"Alergi\n{profil['alergi'] or '-'}\n\n"
                f"Penyakit Bawaan\n{profil['penyakit_bawaan'] or '-'}\n\n"
                f"Riwayat Penyakit\n{profil['riwayat_penyakit'] or '-'}\n\n"
                f"Catatan Kesehatan\n{profil['catatan_kesehatan'] or '-'}\n\n"
                f"Sumber Data: {profil['sumber_data'] or '-'}"
            )
        else:
            teks = "Profil kesehatan belum tersedia."

        self.kesehatan_label.configure(text=teks)
        self.refresh_antrean()

    def refresh_antrean(self):
        kunjungan = self.controller.get_antrean_aktif(self.id_user)

        if not kunjungan:
            self.antrean_label.configure(
                text="Belum ada kunjungan aktif.\n"
                     "Silakan tekan tombol Daftar Kunjungan."
            )
            return

        tanggal = kunjungan["tanggal_kunjungan"]
        tanggal = tanggal.strftime("%d-%m-%Y") if tanggal else "-"

        self.antrean_label.configure(text=(
            f"Nomor Antrean: {kunjungan['nomor_antrian']}\n"
            f"Poli: {kunjungan['nama_poli']}\n"
            f"Tanggal: {tanggal}\n"
            f"Status: {kunjungan['status']}\n"
            f"Dokter: {kunjungan['nama_dokter'] or 'Belum ditentukan'}"
        ))

    # PENDAFTARAN KUNJUNGAN
    def buka_form_pendaftaran(self):
        if self.id_user is None:
            messagebox.showwarning("Pendaftaran", "Identitas pasien tidak ditemukan.")
            return

        window = ctk.CTkToplevel(self)
        window.title("Pendaftaran Kunjungan")
        window.geometry("450x420")
        window.resizable(False, False)
        window.transient(self.winfo_toplevel())
        window.grab_set()
        window.configure(fg_color=WARNA_BG)

        ctk.CTkLabel(
            window, text="Pendaftaran Kunjungan",
            font=("Arial", 21, "bold"), text_color=WARNA_TEKS
        ).pack(pady=(25, 10))

        form = ctk.CTkFrame(window, fg_color=WARNA_PUTIH)
        form.pack(fill="both", expand=True, padx=25, pady=10)

        ctk.CTkLabel(
            form, text="Tanggal kunjungan: Hari ini",
            text_color=WARNA_TEKS
        ).pack(anchor="w", padx=20, pady=(18, 5))

        ctk.CTkLabel(
            form, text="Poli ditentukan otomatis berdasarkan usia pasien.",
            font=("Arial", 11), text_color=WARNA_ABU
        ).pack(anchor="w", padx=20, pady=5)

        ctk.CTkLabel(
            form, text="Keluhan awal",
            font=("Arial", 12, "bold"), text_color=WARNA_TEKS
        ).pack(anchor="w", padx=20, pady=(15, 5))

        entry = ctk.CTkTextbox(form, width=370, height=110)
        entry.pack(padx=20, pady=5)

        def simpan():
            keluhan = entry.get("1.0", "end").strip()
            berhasil, pesan, hasil = self.controller.daftar_kunjungan(
                self.id_user, keluhan
            )

            if not berhasil:
                messagebox.showwarning(
                    "Pendaftaran", pesan, parent=window
                )
                return

            messagebox.showinfo(
                "Pendaftaran Berhasil",
                f"{pesan}\n\n"
                f"Nomor Antrean: {hasil['nomor_antrian']}\n"
                f"Poli: {hasil['nama_poli']}\n"
                f"Status: {hasil['status']}",
                parent=window
            )

            window.destroy()
            self.refresh_data()

        buat_tombol(
            form, "Konfirmasi Pendaftaran",
            simpan, lebar=370
        ).pack(fill="x", padx=20, pady=18)

    # RIWAYAT MEDIS
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
            window, text="Daftar pemeriksaan yang pernah dilakukan.",
            font=("Arial", 11), text_color=WARNA_ABU
        ).pack(anchor="w", padx=25, pady=(0, 15))

        frame = ctk.CTkFrame(window, fg_color=WARNA_PUTIH)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "tanggal", "poli", "dokter",
            "tekanan", "suhu", "berat", "diagnosis"
        )

        tabel = ttk.Treeview(frame, columns=columns, show="headings")

        headers = {
            "tanggal": ("Tanggal Pemeriksaan", 145),
            "poli": ("Poli", 110),
            "dokter": ("Dokter", 130),
            "tekanan": ("Tekanan Darah", 110),
            "suhu": ("Suhu Tubuh", 90),
            "berat": ("Berat Badan", 100),
            "diagnosis": ("Diagnosis", 250)
        }

        for kolom, (judul, lebar) in headers.items():
            tabel.heading(kolom, text=judul)
            tabel.column(kolom, width=lebar, anchor="center")

        for row in data:
            tanggal = row["tanggal_pemeriksaan"]
            tanggal = tanggal.strftime("%d-%m-%Y %H:%M") if tanggal else "-"

            tabel.insert("", "end", values=(
                tanggal,
                row["nama_poli"] or "-",
                row["nama_dokter"] or "-",
                row["tekanan_darah"] or "-",
                row["suhu_tubuh"] or "-",
                row["berat_badan"] or "-",
                row["diagnosis"] or "-"
            ))

        tabel.pack(fill="both", expand=True, padx=10, pady=10)

        if not data:
            ctk.CTkLabel(
                frame, text="Belum ada riwayat pemeriksaan.",
                text_color=WARNA_ABU
            ).pack(pady=10)

    # LOGOUT
    def logout(self):
        if self.on_logout:
            self.on_logout()
