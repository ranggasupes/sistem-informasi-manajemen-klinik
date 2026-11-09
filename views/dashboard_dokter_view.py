
import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.dokter_controller import DokterController


class DashboardDokterFrame(ctk.CTkFrame):
    def __init__(self, parent, username="Dokter", id_user=None, on_logout=None):
        super().__init__(parent)
        self.id_user = id_user
        self.on_logout = on_logout
        self.controller = DokterController()
        self.id_kunjungan = None
        self.id_rekam_medis = None
        self.daftar_resep = []

        menu = ctk.CTkFrame(self, width=150)
        menu.pack(side="left", fill="y")

        for nama, fungsi in [
            ("Dashboard", self.dashboard),
            ("Antrean", self.tampilkan_antrean),
            ("Riwayat", self.tampilkan_riwayat),
            ("Logout", self.logout)
        ]:
            ctk.CTkButton(menu, text=nama, command=fungsi).pack(
                fill="x", padx=10, pady=8
            )

        self.konten = ctk.CTkFrame(self)
        self.konten.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        self.dashboard()

    def bersihkan(self):
        for widget in self.konten.winfo_children():
            widget.destroy()

    def judul(self, teks):
        ctk.CTkLabel(self.konten, text=teks, font=("Arial", 20)).pack(
            anchor="w", pady=10
        )

    def input(self, parent, label):
        ctk.CTkLabel(parent, text=label).pack(anchor="w")
        entry = ctk.CTkEntry(parent, width=280)
        entry.pack(anchor="w", pady=4)
        return entry

    def tabel(self, kolom):
        tabel = ttk.Treeview(self.konten, columns=kolom, show="headings")
        for nama in kolom:
            tabel.heading(nama, text=nama.replace("_", " ").title())
        tabel.pack(fill="both", expand=True, pady=10)
        return tabel

    def dashboard(self):
        self.bersihkan()
        self.judul("Dashboard Dokter")
        ctk.CTkButton(
            self.konten, text="Lihat Antrean", command=self.tampilkan_antrean
        ).pack(anchor="w")

    def tampilkan_antrean(self):
        self.bersihkan()
        self.judul("Antrean Pasien")
        self.tabel_antrean = self.tabel([
            "id_kunjungan", "nomor_antrian", "nama_pasien",
            "tanggal_kunjungan", "status"
        ])

        for item in self.controller.get_antrean(self.id_user):
            self.tabel_antrean.insert("", "end", values=(
                item["id_kunjungan"], item["nomor_antrian"],
                item["nama_pasien"], item["tanggal_kunjungan"], item["status"]
            ))

        ctk.CTkButton(
            self.konten, text="Panggil", command=self.panggil_pasien
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.konten, text="Periksa", command=self.mulai_pemeriksaan
        ).pack(side="left", padx=5)

    def pilihan(self):
        data = self.tabel_antrean.selection()
        if not data:
            messagebox.showwarning("Peringatan", "Pilih pasien dahulu.")
            return None
        return int(self.tabel_antrean.item(data[0], "values")[0])

    def panggil_pasien(self):
        id_kunjungan = self.pilihan()
        if id_kunjungan is None:
            return

        berhasil = self.controller.panggil_pasien(id_kunjungan, self.id_user)
        messagebox.showinfo(
            "Informasi", "Pasien dipanggil." if berhasil else "Gagal memanggil pasien."
        )
        self.tampilkan_antrean()

    def mulai_pemeriksaan(self):
        self.id_kunjungan = self.pilihan()
        if self.id_kunjungan is None:
            return

        data = self.controller.mulai_pemeriksaan(
            self.id_kunjungan, self.id_user
        )
        if not data:
            messagebox.showwarning("Peringatan", "Pasien belum dapat diperiksa.")
            return

        self.bersihkan()
        self.judul("Pemeriksaan - " + data["nama_pasien"])
        ctk.CTkLabel(
            self.konten,
            text=f"Antrean: {data['nomor_antrian']} | Keluhan: {data['keluhan_awal']}"
        ).pack(anchor="w")

        form = ctk.CTkFrame(self.konten)
        form.pack(anchor="w", pady=10)

        self.tekanan = self.input(form, "Tekanan Darah")
        self.suhu = self.input(form, "Suhu Tubuh")
        self.berat = self.input(form, "Berat Badan")
        self.diagnosis = self.input(form, "Diagnosis")
        self.catatan = self.input(form, "Catatan")

        ctk.CTkButton(
            self.konten, text="Simpan Pemeriksaan",
            command=self.simpan_pemeriksaan
        ).pack(anchor="w")

    def simpan_pemeriksaan(self):
        data = {
            "id_kunjungan": self.id_kunjungan,
            "tekanan_darah": self.tekanan.get(),
            "suhu_tubuh": self.suhu.get(),
            "berat_badan": self.berat.get(),
            "diagnosis": self.diagnosis.get(),
            "catatan": self.catatan.get()
        }

        if not all(data[k] for k in (
            "tekanan_darah", "suhu_tubuh", "berat_badan", "diagnosis"
        )):
            messagebox.showwarning("Peringatan", "Lengkapi pemeriksaan.")
            return

        self.id_rekam_medis = self.controller.simpan_pemeriksaan(
            data, self.id_user
        )
        if self.id_rekam_medis:
            self.form_resep()
        else:
            messagebox.showerror("Gagal", "Pemeriksaan gagal disimpan.")

    def form_resep(self):
        self.bersihkan()
        self.judul("Resep Obat")

        obat = self.controller.get_daftar_obat()
        self.obat = {
            f"{x['nama_obat']} (Stok {x['stok']})": x["id_obat"]
            for x in obat
        }

        if not self.obat:
            ctk.CTkLabel(self.konten, text="Tidak ada obat tersedia.").pack()

        else:
            self.pilihan_obat = ctk.CTkComboBox(
                self.konten, values=list(self.obat.keys()), width=280
            )
            self.pilihan_obat.pack(anchor="w", pady=5)
            self.pilihan_obat.set(list(self.obat.keys())[0])

            self.dosis = self.input(self.konten, "Dosis")
            self.jumlah = self.input(self.konten, "Jumlah")
            self.aturan = self.input(self.konten, "Aturan Pakai")

            ctk.CTkButton(
                self.konten, text="Tambah Obat", command=self.tambah_resep
            ).pack(anchor="w", pady=5)

        self.label_resep = ctk.CTkLabel(self.konten, text="")
        self.label_resep.pack(anchor="w", pady=5)
        self.perbarui_resep()

        ctk.CTkButton(
            self.konten, text="Simpan Resep", command=self.simpan_resep
        ).pack(anchor="w", pady=5)

        ctk.CTkButton(
            self.konten, text="Selesaikan Tanpa Resep",
            command=self.selesaikan_tanpa_resep
        ).pack(anchor="w")

    def tambah_resep(self):
        try:
            nama = self.pilihan_obat.get()
            jumlah = int(self.jumlah.get())
            dosis = self.dosis.get().strip()
            aturan = self.aturan.get().strip()

            if nama not in self.obat or jumlah <= 0 or not dosis or not aturan:
                raise ValueError

            id_obat = self.obat[nama]
            if any(x["id_obat"] == id_obat for x in self.daftar_resep):
                messagebox.showwarning("Peringatan", "Obat sudah ditambahkan.")
                return

            self.daftar_resep.append({
                "id_obat": id_obat, "jumlah": jumlah,
                "dosis": dosis, "aturan_pakai": aturan
            })
            self.perbarui_resep()

        except ValueError:
            messagebox.showwarning("Peringatan", "Periksa kembali data resep.")

    def perbarui_resep(self):
        teks = "\n".join(
            f"{i}. {x['id_obat']} - {x['dosis']} - {x['jumlah']} - {x['aturan_pakai']}"
            for i, x in enumerate(self.daftar_resep, 1)
        )
        self.label_resep.configure(text=teks or "Belum ada obat.")

    def simpan_resep(self):
        if not self.daftar_resep:
            messagebox.showwarning("Peringatan", "Tambahkan obat dahulu.")
            return

        berhasil = self.controller.simpan_resep(
            self.id_rekam_medis, self.id_user, self.daftar_resep
        )
        if berhasil:
            messagebox.showinfo("Berhasil", "Resep disimpan.")
            self.tampilkan_antrean()
        else:
            messagebox.showerror("Gagal", "Resep gagal disimpan.")

    def selesaikan_tanpa_resep(self):
        if self.daftar_resep:
            messagebox.showwarning("Peringatan", "Simpan resep terlebih dahulu.")
            return

        berhasil = self.controller.selesaikan_tanpa_resep(
            self.id_rekam_medis, self.id_user
        )
        if berhasil:
            messagebox.showinfo("Berhasil", "Kunjungan selesai.")
            self.tampilkan_antrean()
        else:
            messagebox.showerror("Gagal", "Kunjungan gagal diselesaikan.")

    def tampilkan_riwayat(self):
        self.bersihkan()
        self.judul("Riwayat Pemeriksaan")
        tabel = self.tabel([
            "tanggal_kunjungan", "nomor_antrian", "nama_pasien",
            "diagnosis", "status"
        ])

        for item in self.controller.get_riwayat(self.id_user):
            tabel.insert("", "end", values=(
                item["tanggal_kunjungan"], item["nomor_antrian"],
                item["nama_pasien"], item["diagnosis"], item["status"]
            ))

    def logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin keluar?"):
            if self.on_logout:
                self.on_logout()
