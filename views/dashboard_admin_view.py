import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.admin_controller import AdminController


class DashboardAdminFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Apoteker", id_user=None, on_logout=None):
        super().__init__(parent)

        self.username = username
        self.id_user = id_user
        self.on_logout = on_logout
        self.controller = AdminController()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar()
        self.konten()
        self.dashboard()

    def sidebar(self):
        menu = ctk.CTkFrame(self, width=180)
        menu.grid(row=0, column=0, sticky="ns")
        menu.grid_propagate(False)

        ctk.CTkLabel(menu, text="ADMIN APOTEKER",
                     font=("Arial", 14, "bold")).pack(pady=25)

        for teks, fungsi in [
            ("Dashboard", self.dashboard),
            ("Antrean Resep", self.antrean),
            ("Kelola Obat", self.obat),
            ("Riwayat", self.riwayat)
        ]:
            ctk.CTkButton(menu, text=teks, command=fungsi).pack(
                fill="x", padx=10, pady=5
            )

        ctk.CTkButton(
            menu, text="Logout", fg_color="red", command=self.logout
        ).pack(side="bottom", fill="x", padx=10, pady=15)

    def konten(self):
        self.area = ctk.CTkFrame(self)
        self.area.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

    def bersihkan(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def judul(self, teks):
        self.bersihkan()
        ctk.CTkLabel(
            self.area, text=teks, font=("Arial", 22, "bold")
        ).pack(anchor="center", padx=10, pady=10)

    def buat_tabel(self, kolom):
        tabel = ttk.Treeview(
            self.area, columns=kolom, show="headings", height=15
        )

        for kolom_nama in kolom:
            tabel.heading(kolom_nama, text=kolom_nama.replace("_", " ").title())
            tabel.column(kolom_nama, width=130, anchor="center")

        tabel.pack(fill="both", expand=True, padx=10, pady=10)
        return tabel

    # DASHBOARD

    def dashboard(self):
        self.judul("Dashboard Admin")

        ctk.CTkLabel(
            self.area,
            text=f"Selamat datang, {self.username}"
        ).pack(anchor="center", padx=10, pady=10)

        ctk.CTkButton(
            self.area, text="Lihat Antrean Resep",
            command=self.antrean
        ).pack(anchor="center", padx=10, pady=10)

    # ANTREAN RESEP

    def antrean(self):
        self.judul("Antrean Resep")

        kolom = (
            "nomor_antrian", "nama_pasien", "nama_dokter",
            "nama_obat", "dosis", "jumlah", "status_penyerahan"
        )

        self.tabel_antrean = self.buat_tabel(kolom)
        self.data_antrean = {}

        for item in self.controller.get_antrean_resep():
            iid = str(item["id_resep"])

            self.tabel_antrean.insert("", "end", iid=iid, values=(
                item["nomor_antrian"],
                item["nama_pasien"],
                item["nama_dokter"] or "-",
                item["nama_obat"],
                item["dosis"] or "-",
                item["jumlah"],
                item["status_penyerahan"]
            ))

            self.data_antrean[iid] = item

        ctk.CTkButton(
            self.area, text="Serahkan Obat",
            command=self.serahkan_obat
        ).pack(anchor="center", padx=10, pady=10)

    def serahkan_obat(self):
        pilihan = self.tabel_antrean.selection()

        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih resep terlebih dahulu.")
            return

        if self.id_user is None:
            messagebox.showerror("Gagal", "ID petugas tidak ditemukan.")
            return

        item = self.data_antrean.get(pilihan[0])

        if not messagebox.askyesno(
            "Konfirmasi",
            f"Serahkan obat untuk pasien {item['nama_pasien']}?"
        ):
            return

        berhasil, pesan = self.controller.serahkan_obat(
            item["id_kunjungan"], self.id_user
        )

        if berhasil:
            messagebox.showinfo("Berhasil", pesan)
            self.antrean()
        else:
            messagebox.showerror("Gagal", pesan)

    # KELOLA OBAT

    def obat(self):
        self.judul("Kelola Obat")

        self.tabel_obat = self.buat_tabel(
            ("id_obat", "nama_obat", "jenis_obat", "satuan", "stok")
        )

        for item in self.controller.get_data_obat():
            self.tabel_obat.insert("", "end", iid=str(item["id_obat"]), values=(
                item["id_obat"], item["nama_obat"],
                item["jenis_obat"], item["satuan"], item["stok"]
            ))

        tombol = ctk.CTkFrame(self.area)
        tombol.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            tombol, text="Tambah", command=self.tambah_obat
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            tombol, text="Edit", command=self.edit_obat
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            tombol, text="Hapus", fg_color="red",
            command=self.hapus_obat
        ).pack(side="left", padx=5)

    def tambah_obat(self):
        self.form_obat()

    def edit_obat(self):
        pilihan = self.tabel_obat.selection()

        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih obat terlebih dahulu.")
            return

        id_obat = int(pilihan[0])
        data = self.controller.get_data_obat()
        obat = next((x for x in data if x["id_obat"] == id_obat), None)

        if obat:
            self.form_obat(obat)

    def form_obat(self, obat=None):
        popup = ctk.CTkToplevel(self)
        popup.title("Data Obat")
        popup.geometry("350x400")
        popup.grab_set()

        inputan = {}

        for label in ["nama_obat", "jenis_obat", "satuan", "stok"]:
            ctk.CTkLabel(popup, text=label.replace("_", " ").title()).pack(pady=5)

            entry = ctk.CTkEntry(popup, width=250)
            entry.pack(pady=5)

            if obat:
                entry.insert(0, str(obat[label]))

            inputan[label] = entry

        def simpan():
            nama = inputan["nama_obat"].get().strip()
            jenis = inputan["jenis_obat"].get().strip()
            satuan = inputan["satuan"].get().strip()
            stok = inputan["stok"].get().strip()

            if not all([nama, jenis, satuan, stok]):
                messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
                return

            try:
                stok = int(stok)
                if stok < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Peringatan", "Stok harus angka minimal 0.")
                return

            if obat:
                berhasil = self.controller.update_obat(
                    obat["id_obat"], nama, jenis, satuan, stok
                )
            else:
                berhasil = self.controller.tambah_obat(
                    nama, jenis, satuan, stok
                )

            if berhasil:
                messagebox.showinfo("Berhasil", "Data obat berhasil disimpan.")
                popup.destroy()
                self.obat()
            else:
                messagebox.showerror("Gagal", "Data obat gagal disimpan.")

        ctk.CTkButton(popup, text="Simpan", command=simpan).pack(pady=20)

    def hapus_obat(self):
        pilihan = self.tabel_obat.selection()

        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih obat terlebih dahulu.")
            return

        id_obat = int(pilihan[0])

        if messagebox.askyesno("Konfirmasi", "Hapus obat ini?"):
            if self.controller.hapus_obat(id_obat):
                messagebox.showinfo("Berhasil", "Obat berhasil dihapus.")
                self.obat()
            else:
                messagebox.showerror("Gagal", "Obat tidak dapat dihapus.")

    # RIWAYAT

    def riwayat(self):
        self.judul("Riwayat Penyerahan Obat")

        tabel = self.buat_tabel((
            "nomor_antrian", "nama_pasien", "nama_obat",
            "jumlah", "nama_petugas", "waktu_selesai"
        ))

        for item in self.controller.get_riwayat_penyerahan():
            tabel.insert("", "end", values=(
                item["nomor_antrian"],
                item["nama_pasien"],
                item["nama_obat"],
                item["jumlah"],
                item["nama_petugas"] or "-",
                item["waktu_selesai"] or "-"
            ))

    # LOGOUT

    def logout(self):
        if self.on_logout:
            self.on_logout()