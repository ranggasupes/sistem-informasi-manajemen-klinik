import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.pasien_controller import PasienController


class DashboardPasienFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Pasien", id_user=None, on_logout=None):
        super().__init__(parent)

        self.id_user = id_user
        self.on_logout = on_logout
        self.controller = PasienController()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        menu = ctk.CTkFrame(self, width=150)
        menu.grid(row=0, column=0, sticky="ns")
        menu.grid_propagate(False)

        ctk.CTkLabel(
            menu, 
            text="MENU PASIEN", 
            font=("Arial", 15, "bold") 
        ).pack(pady=20)

        for teks, fungsi in [
            ("Dashboard", self.refresh_data),
            ("Daftar Kunjungan", self.buka_form_pendaftaran),
            ("Riwayat Medis", self.buka_riwayat)
        ]:
            ctk.CTkButton(menu, text=teks, command=fungsi).pack(
                fill="x", padx=10, pady=5
            )

        ctk.CTkButton(
            menu, text="Logout", command=self.logout, fg_color="#d9534f", hover_color="#c9302c"
        ).pack(side="bottom", fill="x", padx=10, pady=15)

        self.konten = ctk.CTkScrollableFrame(self)
        self.konten.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        self.refresh_data()

    def judul(self, teks):
        ctk.CTkLabel(
            self.konten, text=teks, font=("Arial", 20, "bold"), justify="center"
        ).pack(anchor="center", pady=(15, 10))

    def refresh_data(self):
        for widget in self.konten.winfo_children():
            widget.destroy()

        self.judul("Dashboard Pasien")

        if not self.id_user:
            ctk.CTkLabel(self.konten, text="Identitas pasien tidak ditemukan.").pack(anchor="center", pady=20)
            return

        try:
            pasien, profil = self.controller.get_dashboard_data(self.id_user)

            if not pasien:
                ctk.CTkLabel(
                    self.konten, text="Data pasien belum tersedia. Hubungi admin."
                ).pack(anchor="center", pady=20)
                return

            tanggal = pasien["tanggal_lahir"]
            tanggal = tanggal.strftime("%d-%m-%Y") if tanggal else "-"

            # --- CARD 1: IDENTITAS PASIEN ---
            card_identitas = ctk.CTkFrame(self.konten, corner_radius=10)
            card_identitas.pack(fill="x", padx=30, pady=10)

            ctk.CTkLabel(
                card_identitas, text="Identitas Pasien", font=("Arial", 16, "bold")
            ).pack(anchor="center", pady=(10, 5))

            identitas = (
                f"Nama: {pasien['nama_pasien']}\n"
                f"NIK: {pasien['nik'] or '-'} | No. BPJS: {pasien['nomor_bpjs'] or '-'}\n"
                f"Jenis Kelamin: {pasien['jenis_kelamin'] or '-'} | Tgl Lahir: {tanggal}\n"
                f"Alamat: {pasien['alamat'] or '-'}\n"
                f"No. Telepon: {pasien['no_telepon'] or '-'}"
            )
            ctk.CTkLabel(
                card_identitas, text=identitas, justify="center"
            ).pack(anchor="center", padx=15, pady=(0, 15))

            # --- CARD 2: PROFIL KESEHATAN ---
            card_profil = ctk.CTkFrame(self.konten, corner_radius=10)
            card_profil.pack(fill="x", padx=30, pady=10)

            ctk.CTkLabel(
                card_profil, text="Profil Kesehatan", font=("Arial", 16, "bold")
            ).pack(anchor="center", pady=(10, 5))

            if profil:
                kesehatan = (
                    f"Alergi: {profil['alergi'] or '-'}\n"
                    f"Penyakit Bawaan: {profil['penyakit_bawaan'] or '-'}\n"
                    f"Riwayat Penyakit: {profil['riwayat_penyakit'] or '-'}\n"
                    f"Catatan: {profil['catatan_kesehatan'] or '-'}\n"
                    f"Sumber Data: {profil['sumber_data'] or '-'}"
                )
            else:
                kesehatan = "Profil kesehatan belum tersedia."

            ctk.CTkLabel(
                card_profil, text=kesehatan, justify="center"
            ).pack(anchor="center", padx=15, pady=(0, 15))

            # --- CARD 3: ANTREAN KUNJUNGAN ---
            card_antrean = ctk.CTkFrame(self.konten, corner_radius=10)
            card_antrean.pack(fill="x", padx=30, pady=10)

            ctk.CTkLabel(
                card_antrean, text="Antrean Kunjungan", font=("Arial", 16, "bold")
            ).pack(anchor="center", pady=(10, 5))

            self.frame_antrean_konten = ctk.CTkLabel(card_antrean, text="", justify="center")
            self.frame_antrean_konten.pack(anchor="center", padx=15, pady=(0, 10))
            self.refresh_antrean()

            # --- TOMBOL DAFTAR KUNJUNGAN ---
            ctk.CTkButton(
                self.konten, text="Daftar Kunjungan",
                command=self.buka_form_pendaftaran, width=220, height=35
            ).pack(anchor="center", pady=20)

        except Exception as e:
            messagebox.showerror("Gagal Memuat Data", str(e))

    def refresh_antrean(self):
        kunjungan = self.controller.get_antrean_aktif(self.id_user)

        if not kunjungan:
            teks = "Belum ada kunjungan aktif."
        else:
            tanggal = kunjungan["tanggal_kunjungan"]
            tanggal = tanggal.strftime("%d-%m-%Y") if tanggal else "-"

            teks = (
                f"Nomor Antrean: {kunjungan['nomor_antrian']}\n"
                f"Poli: {kunjungan['nama_poli']} | Tanggal: {tanggal}\n"
                f"Status: {kunjungan['status']}\n"
                f"Dokter: {kunjungan['nama_dokter'] or 'Belum ditentukan'}"
            )

        if hasattr(self, 'frame_antrean_konten') and self.frame_antrean_konten.winfo_exists():
            self.frame_antrean_konten.configure(text=teks)

    def buka_form_pendaftaran(self):
        if not self.id_user:
            messagebox.showwarning("Peringatan", "Identitas pasien tidak ditemukan.")
            return

        window = ctk.CTkToplevel(self)
        window.title("Daftar Kunjungan")
        window.geometry("400x350")
        window.grab_set()

        ctk.CTkLabel(
            window, text="Pendaftaran Kunjungan",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(
            window, text="Poli ditentukan otomatis berdasarkan usia."
        ).pack(pady=5)

        ctk.CTkLabel(window, text="Keluhan Awal").pack(anchor="w", padx=20)

        entry = ctk.CTkTextbox(window, width=350, height=120)
        entry.pack(padx=20, pady=10)

        def simpan():
            keluhan = entry.get("1.0", "end").strip()

            try:
                berhasil, pesan, hasil = self.controller.daftar_kunjungan(
                    self.id_user, keluhan
                )

                if not berhasil:
                    messagebox.showwarning("Pendaftaran", pesan, parent=window)
                    return

                messagebox.showinfo(
                    "Berhasil",
                    f"{pesan}\n"
                    f"Nomor Antrean: {hasil['nomor_antrian']}\n"
                    f"Poli: {hasil['nama_poli']}\n"
                    f"Status: {hasil['status']}",
                    parent=window
                )

                window.destroy()
                self.refresh_data()

            except Exception as e:
                messagebox.showerror("Error", str(e), parent=window)

        ctk.CTkButton(
            window, text="Simpan Pendaftaran", command=simpan
        ).pack(pady=10)

    def buka_riwayat(self):
        try:
            data = self.controller.get_riwayat_medis(self.id_user)

            window = ctk.CTkToplevel(self)
            window.title("Riwayat Medis")
            window.geometry("950x500")
            window.grab_set()

            ctk.CTkLabel(
                window, text="Riwayat Rekam Medis",
                font=("Arial", 18, "bold")
            ).pack(pady=15)

            if not data:
                ctk.CTkLabel(
                    window, text="Belum ada riwayat pemeriksaan.",
                    font=("Arial", 14)
                ).pack(pady=20)
                return

            kolom = (
                "tanggal", "poli", "dokter",
                "tekanan", "suhu", "berat", "diagnosis"
            )

            tabel = ttk.Treeview(
                window, columns=kolom, show="headings"
            )

            judul = [
                "Tanggal", "Poli", "Dokter",
                "Tekanan Darah", "Suhu", "Berat", "Diagnosis"
            ]

            for nama, teks in zip(kolom, judul):
                tabel.heading(nama, text=teks)
                tabel.column(nama, width=120, anchor="center")

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

        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def logout(self):
        if self.on_logout and messagebox.askyesno("Logout", "Yakin ingin keluar?"):
            self.on_logout()