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

        ctk.CTkLabel(menu, text="MENU PASIEN").pack(pady=20)

        for teks, fungsi in [
            ("Dashboard", self.refresh_data),
            ("Daftar Kunjungan", self.buka_form_pendaftaran),
            ("Riwayat Medis", self.buka_riwayat)
        ]:
            ctk.CTkButton(menu, text=teks, command=fungsi).pack(
                fill="x", padx=10, pady=5
            )

        ctk.CTkButton(
            menu, text="Logout", command=self.logout
        ).pack(side="bottom", fill="x", padx=10, pady=15)

        self.konten = ctk.CTkScrollableFrame(self)
        self.konten.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        self.refresh_data()

    def judul(self, teks):
        ctk.CTkLabel(
            self.konten, text=teks, font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=8)

    def refresh_data(self):
        for widget in self.konten.winfo_children():
            widget.destroy()

        self.judul("Dashboard Pasien")

        if not self.id_user:
            ctk.CTkLabel(self.konten, text="Identitas pasien tidak ditemukan.").pack(anchor="w")
            return

        try:
            pasien, profil = self.controller.get_dashboard_data(self.id_user)

            if not pasien:
                ctk.CTkLabel(
                    self.konten, text="Data pasien belum tersedia. Hubungi admin."
                ).pack(anchor="w")
                return

            tanggal = pasien["tanggal_lahir"]
            tanggal = tanggal.strftime("%d-%m-%Y") if tanggal else "-"

            identitas = (
                f"Nama: {pasien['nama_pasien']}\n"
                f"NIK: {pasien['nik'] or '-'}\n"
                f"No. BPJS: {pasien['nomor_bpjs'] or '-'}\n"
                f"Jenis Kelamin: {pasien['jenis_kelamin'] or '-'}\n"
                f"Tanggal Lahir: {tanggal}\n"
                f"Alamat: {pasien['alamat'] or '-'}\n"
                f"No. Telepon: {pasien['no_telepon'] or '-'}"
            )

            self.judul("Identitas Pasien")
            ctk.CTkLabel(
                self.konten, text=identitas, justify="left"
            ).pack(anchor="w", padx=10)

            self.judul("Profil Kesehatan")

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
                self.konten, text=kesehatan, justify="left"
            ).pack(anchor="w", padx=10)

            self.judul("Antrean Kunjungan")
            self.refresh_antrean()

            ctk.CTkButton(
                self.konten, text="Daftar Kunjungan",
                command=self.buka_form_pendaftaran
            ).pack(anchor="w", pady=10)

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
                f"Poli: {kunjungan['nama_poli']}\n"
                f"Tanggal: {tanggal}\n"
                f"Status: {kunjungan['status']}\n"
                f"Dokter: {kunjungan['nama_dokter'] or 'Belum ditentukan'}"
            )

        ctk.CTkLabel(
            self.konten, text=teks, justify="left"
        ).pack(anchor="w", padx=10)

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

            ctk.CTkLabel(
                window, text="Riwayat Rekam Medis",
                font=("Arial", 18, "bold")
            ).pack(pady=15)

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

            if not data:
                ctk.CTkLabel(
                    window, text="Belum ada riwayat pemeriksaan."
                ).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Gagal", str(e))

    def logout(self):
        if self.on_logout and messagebox.askyesno("Logout", "Yakin ingin keluar?"):
            self.on_logout()