import customtkinter as ctk
from tkinter import ttk, messagebox

from models.dokter_model import DokterModel
from models.kunjungan_model import KunjunganModel
from models.rekam_medis_model import RekamMedisModel
from controllers.obat_controller import ObatController

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


class DashboardDokterFrame(ctk.CTkFrame):

    def __init__(self, parent, username="Dokter", id_user=None, on_logout=None):
        super().__init__(parent, fg_color=WARNA_BG)

        self.username = username
        self.id_user = id_user
        self.on_logout = on_logout

        self.dokter_model = DokterModel()
        self.kunjungan_model = KunjunganModel()
        self.rekam_medis_model = RekamMedisModel()

        self.profil_dokter = (
            self.dokter_model.get_by_user_id(id_user)
            if id_user else None
        )

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()
        self.buat_konten()
        self.refresh_dashboard()

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
            font=("Arial", 20, "bold"), text_color="white"
        ).pack(anchor="w", padx=20, pady=(30, 5))

        ctk.CTkLabel(
            sidebar, text="DASHBOARD DOKTER",
            font=("Arial", 9), text_color="#D5E4F2"
        ).pack(anchor="w", padx=20, pady=(0, 30))

        menu = [
            ("Dashboard", self.refresh_dashboard),
            ("Antrean Pasien", self.fokus_antrean),
            ("Rekam Medis", self.mulai_pemeriksaan)
        ]

        for teks, fungsi in menu:
            ctk.CTkButton(
                sidebar, text=teks, command=fungsi,
                height=40, anchor="w",
                fg_color="transparent",
                hover_color="#35658F",
                text_color="white"
            ).pack(fill="x", padx=12, pady=3)

        ctk.CTkLabel(
            sidebar, text=f"Dokter:\n{self.username}",
            text_color="white", justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=10)

        buat_tombol(
            sidebar, "Logout", self.logout,
            warna=WARNA_MERAH, hover="#A83A3A", lebar=150
        ).pack(side="bottom", padx=15, pady=15)

    def fokus_antrean(self):
        self.tabel.focus_set()

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
            header, "Dashboard Dokter", 20
        ).pack(side="left", padx=25, pady=20)

        nama = (
            self.profil_dokter["nama_dokter"]
            if self.profil_dokter else self.username
        )

        ctk.CTkLabel(
            header, text=f"Dr. {nama}",
            text_color=WARNA_ABU
        ).pack(side="right", padx=25)

        area = ctk.CTkFrame(content, fg_color="transparent")
        area.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(1, weight=1)

        buat_judul(
            area, "Daftar Antrean Pasien", 18
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        frame = ctk.CTkFrame(
            area, fg_color=WARNA_PUTIH,
            border_width=1, border_color=WARNA_GARIS
        )
        frame.grid(row=1, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32, font=("Arial", 10))
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#E8EFF6",
            foreground=WARNA_BIRU_TUA
        )

        self.tabel = ttk.Treeview(
            frame,
            columns=("nomor", "pasien", "keluhan", "status"),
            show="headings"
        )

        kolom = {
            "nomor": ("No. Antrean", 100),
            "pasien": ("Nama Pasien", 200),
            "keluhan": ("Keluhan", 350),
            "status": ("Status", 130)
        }

        for nama_kolom, (judul, lebar) in kolom.items():
            self.tabel.heading(nama_kolom, text=judul)
            self.tabel.column(
                nama_kolom, width=lebar,
                anchor="center" if nama_kolom in ("nomor", "status") else "w"
            )

        self.tabel.grid(
            row=0, column=0, sticky="nsew",
            padx=12, pady=12
        )

        tombol = ctk.CTkFrame(area, fg_color="transparent")
        tombol.grid(row=2, column=0, sticky="w", pady=15)

        buat_tombol(
            tombol, "Refresh Antrean", self.refresh_dashboard
        ).pack(side="left")

        buat_tombol(
            tombol, "Panggil Pasien", self.panggil_pasien,
            warna=WARNA_BIRU, hover=WARNA_BIRU_TUA, lebar=150
        ).pack(side="left", padx=10)

        buat_tombol(
            tombol, "Mulai Pemeriksaan", self.mulai_pemeriksaan,
            warna=WARNA_HIJAU, hover="#2D704B", lebar=170
        ).pack(side="left")

    # ANTREAN PASIEN
    def refresh_dashboard(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        if not self.id_user or not self.profil_dokter:
            messagebox.showerror(
                "Data Dokter",
                "Profil dokter tidak ditemukan. Hubungi administrator."
            )
            return

        daftar = self.kunjungan_model.get_antrean_dokter(self.id_user)

        for row in daftar:
            self.tabel.insert(
                "", "end",
                iid=str(row["id_kunjungan"]),
                values=(
                    row["nomor_antrian"],
                    row["nama_pasien"],
                    row["keluhan_awal"] or "-",
                    row["status"]
                )
            )

    def ambil_pasien(self):
        pilihan = self.tabel.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan", "Pilih pasien terlebih dahulu."
            )
            return None

        return int(pilihan[0])

    def panggil_pasien(self):
        id_kunjungan = self.ambil_pasien()

        if id_kunjungan is None:
            return

        berhasil = self.kunjungan_model.panggil_pasien(
            id_kunjungan, self.id_user
        )

        if berhasil:
            messagebox.showinfo("Berhasil", "Pasien berhasil dipanggil.")
            self.refresh_dashboard()
        else:
            messagebox.showwarning(
                "Gagal", "Pasien tidak dapat dipanggil. Periksa status kunjungan."
            )

    def mulai_pemeriksaan(self):
        id_kunjungan = self.ambil_pasien()

        if id_kunjungan is None:
            return

        data = self.kunjungan_model.mulai_pemeriksaan(
            id_kunjungan, self.id_user
        )

        if not data:
            messagebox.showwarning(
                "Pemeriksaan",
                "Pasien belum dipanggil atau tidak dapat diperiksa."
            )
            self.refresh_dashboard()
            return

        self.buka_form_pemeriksaan(data)

    # KOMPONEN FORM
    def buat_jendela(self, judul, ukuran):
        window = ctk.CTkToplevel(self)
        window.title(judul)
        window.geometry(ukuran)
        window.configure(fg_color=WARNA_BG)
        window.transient(self.winfo_toplevel())
        window.grab_set()

        header = ctk.CTkFrame(
            window, fg_color=WARNA_BIRU_TUA, corner_radius=0
        )
        header.pack(fill="x")

        ctk.CTkLabel(
            header, text=judul.upper(),
            font=("Arial", 19, "bold"), text_color="white"
        ).pack(anchor="w", padx=22, pady=20)

        konten = ctk.CTkScrollableFrame(
            window, fg_color=WARNA_BG
        )
        konten.pack(fill="both", expand=True, padx=12, pady=10)

        return window, konten

    def buat_input(self, parent, label, placeholder):
        ctk.CTkLabel(
            parent, text=label,
            font=("Arial", 11, "bold"),
            text_color=WARNA_TEKS
        ).pack(anchor="w", padx=18, pady=(9, 3))

        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder, height=35
        )
        entry.pack(fill="x", padx=18)
        return entry

    def tampilkan_informasi(self, parent, judul, data):
        frame = buat_kartu(parent, judul)
        frame.pack(fill="x", padx=8, pady=8)

        for label, nilai in data:
            ctk.CTkLabel(
                frame,
                text=f"{label}: {nilai}",
                font=("Arial", 11),
                text_color=WARNA_TEKS,
                anchor="w",
                justify="left",
                wraplength=520
            ).pack(anchor="w", padx=18, pady=4)

        return frame

    # FORM PEMERIKSAAN
    def buka_form_pemeriksaan(self, data):
        window, konten = self.buat_jendela(
            "Form Pemeriksaan Pasien", "650x720"
        )

        self.tampilkan_informasi(konten, "INFORMASI PASIEN", [
            ("Nama Pasien", data["nama_pasien"]),
            ("Nomor Antrean", data["nomor_antrian"]),
            ("Poli", data["nama_poli"]),
            ("Tanggal", data["tanggal_kunjungan"]),
            ("Keluhan", data["keluhan_awal"] or "-")
        ])

        self.tampilkan_informasi(konten, "PROFIL KESEHATAN", [
            ("Alergi", data.get("alergi") or "Tidak ada data"),
            ("Penyakit Bawaan", data.get("penyakit_bawaan") or "Tidak ada data"),
            ("Riwayat Penyakit", data.get("riwayat_penyakit") or "Tidak ada data"),
            ("Catatan", data.get("catatan_kesehatan") or "Tidak ada data"),
            ("Sumber Data", data.get("sumber_data") or "Tidak diketahui"),
            ("Terakhir Diperbarui", data.get("tanggal_sinkronisasi") or "-")
        ])

        form = buat_kartu(konten, "HASIL PEMERIKSAAN")
        form.pack(fill="x", padx=8, pady=8)

        tekanan = self.buat_input(form, "Tekanan Darah", "Contoh: 120/80 mmHg")
        suhu = self.buat_input(form, "Suhu Tubuh (°C)", "Masukkan suhu")
        berat = self.buat_input(form, "Berat Badan (kg)", "Masukkan berat badan")
        diagnosis = self.buat_input(form, "Diagnosis", "Masukkan diagnosis")

        ctk.CTkLabel(
            form, text="Catatan Pemeriksaan",
            font=("Arial", 11, "bold"), text_color=WARNA_TEKS
        ).pack(anchor="w", padx=18, pady=(10, 3))

        catatan = ctk.CTkTextbox(form, height=100)
        catatan.pack(fill="x", padx=18, pady=(0, 15))

        def simpan():
            if not diagnosis.get().strip():
                messagebox.showwarning(
                    "Validasi", "Diagnosis wajib diisi.", parent=window
                )
                return

            try:
                nilai_suhu = float(suhu.get()) if suhu.get().strip() else None
                nilai_berat = float(berat.get()) if berat.get().strip() else None

                if nilai_suhu is not None and not 0 < nilai_suhu < 100:
                    raise ValueError

                if nilai_berat is not None and not 0 < nilai_berat < 1000:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Validasi", "Suhu atau berat badan tidak valid.",
                    parent=window
                )
                return

            id_rekam = self.rekam_medis_model.create_rekam_medis_dokter(
                id_kunjungan=data["id_kunjungan"],
                id_user=self.id_user,
                tekanan_darah=tekanan.get().strip(),
                suhu_tubuh=nilai_suhu,
                berat_badan=nilai_berat,
                diagnosis=diagnosis.get().strip(),
                catatan=catatan.get("1.0", "end").strip()
            )

            if not id_rekam:
                messagebox.showerror(
                    "Gagal", "Hasil pemeriksaan gagal disimpan.",
                    parent=window
                )
                return

            messagebox.showinfo(
                "Berhasil", "Hasil pemeriksaan berhasil disimpan.",
                parent=window
            )

            window.destroy()
            self.buka_form_resep(id_rekam, data)

        tombol = ctk.CTkFrame(konten, fg_color="transparent")
        tombol.pack(fill="x", padx=8, pady=12)

        buat_tombol(
            tombol, "Simpan Pemeriksaan", simpan,
            warna=WARNA_HIJAU, hover="#2D704B", lebar=190
        ).pack(side="right")

        buat_tombol(
            tombol, "Batal", window.destroy,
            warna=WARNA_MERAH, hover="#A83A3A", lebar=100
        ).pack(side="right", padx=8)

    # FORM RESEP
    def buka_form_resep(self, id_rekam_medis, data):
        window, konten = self.buat_jendela(
            "Form Resep Obat", "650x750"
        )

        self.tampilkan_informasi(konten, "INFORMASI PASIEN", [
            ("Nama", data["nama_pasien"]),
            ("Nomor Antrean", data["nomor_antrian"]),
            ("ID Rekam Medis", id_rekam_medis)
        ])

        form = buat_kartu(konten, "TAMBAH OBAT")
        form.pack(fill="x", padx=8, pady=8)

        semua_obat = ObatController.get_all_obat() or []
        pilihan_obat = {
            f"{o['id_obat']} - {o['nama_obat']} (Stok: {o['stok']} {o['satuan']})": o
            for o in semua_obat if int(o.get("stok") or 0) > 0
        }

        ctk.CTkLabel(
            form, text="Pilih Obat",
            font=("Arial", 11, "bold"), text_color=WARNA_TEKS
        ).pack(anchor="w", padx=18, pady=(12, 4))

        obat_combo = None

        if pilihan_obat:
            obat_combo = ctk.CTkComboBox(
                form, values=list(pilihan_obat.keys()),
                state="readonly", height=35
            )
            obat_combo.pack(fill="x", padx=18)
            obat_combo.set(list(pilihan_obat.keys())[0])
        else:
            ctk.CTkLabel(
                form, text="Belum ada obat dengan stok tersedia.",
                text_color=WARNA_MERAH
            ).pack(anchor="w", padx=18, pady=8)

        dosis = self.buat_input(form, "Dosis", "Isi dosis obat")
        jumlah = self.buat_input(form, "Jumlah", "Masukkan jumlah")
        aturan = self.buat_input(form, "Aturan Pakai", "Isi aturan pakai")

        daftar_resep = []

        daftar_frame = buat_kartu(konten, "DAFTAR RESEP")
        daftar_frame.pack(fill="x", padx=8, pady=8)

        daftar_text = ctk.CTkTextbox(
            daftar_frame, height=150, state="disabled"
        )
        daftar_text.pack(fill="x", padx=15, pady=10)

        def refresh_daftar():
            daftar_text.configure(state="normal")
            daftar_text.delete("1.0", "end")

            if not daftar_resep:
                daftar_text.insert("end", "Belum ada obat yang ditambahkan.")
            else:
                for i, resep in enumerate(daftar_resep, 1):
                    daftar_text.insert(
                        "end",
                        f"{i}. {resep['nama_obat']}\n"
                        f"   Dosis: {resep['dosis']}\n"
                        f"   Jumlah: {resep['jumlah']} {resep['satuan']}\n"
                        f"   Aturan: {resep['aturan_pakai']}\n\n"
                    )

            daftar_text.configure(state="disabled")

        def tambah_resep():
            if not obat_combo:
                messagebox.showwarning(
                    "Resep", "Tidak ada obat yang tersedia.", parent=window
                )
                return

            obat = pilihan_obat.get(obat_combo.get())
            nilai_dosis = dosis.get().strip()
            nilai_jumlah = jumlah.get().strip()
            nilai_aturan = aturan.get().strip()

            if not obat:
                return

            if not nilai_dosis or not nilai_jumlah or not nilai_aturan:
                messagebox.showwarning(
                    "Validasi", "Semua data resep wajib diisi.",
                    parent=window
                )
                return

            try:
                nilai_jumlah = int(nilai_jumlah)
                if nilai_jumlah <= 0 or nilai_jumlah > int(obat["stok"]):
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Validasi", "Jumlah tidak valid atau melebihi stok.",
                    parent=window
                )
                return

            if any(r["id_obat"] == obat["id_obat"] for r in daftar_resep):
                messagebox.showwarning(
                    "Resep", "Obat tersebut sudah ditambahkan.",
                    parent=window
                )
                return

            daftar_resep.append({
                "id_obat": obat["id_obat"],
                "nama_obat": obat["nama_obat"],
                "satuan": obat["satuan"],
                "dosis": nilai_dosis,
                "jumlah": nilai_jumlah,
                "aturan_pakai": nilai_aturan
            })

            refresh_daftar()

            dosis.delete(0, "end")
            jumlah.delete(0, "end")
            aturan.delete(0, "end")

        def hapus_resep():
            if daftar_resep:
                daftar_resep.pop()
                refresh_daftar()
            else:
                messagebox.showwarning(
                    "Resep", "Belum ada obat yang ditambahkan.",
                    parent=window
                )

        tombol_obat = ctk.CTkFrame(form, fg_color="transparent")
        tombol_obat.pack(fill="x", padx=18, pady=15)

        buat_tombol(
            tombol_obat, "Tambah Obat", tambah_resep,
            warna=WARNA_BIRU, hover=WARNA_BIRU_TUA
        ).pack(side="left")

        buat_tombol(
            tombol_obat, "Hapus Terakhir", hapus_resep,
            warna=WARNA_MERAH, hover="#A83A3A"
        ).pack(side="left", padx=8)

        refresh_daftar()

        tombol_akhir = ctk.CTkFrame(konten, fg_color="transparent")
        tombol_akhir.pack(fill="x", padx=8, pady=15)

        def simpan_resep():
            if not daftar_resep:
                messagebox.showwarning(
                    "Resep", "Tambahkan minimal satu obat.", parent=window
                )
                return

            berhasil = self.rekam_medis_model.create_resep_dokter(
                id_rekam_medis, self.id_user, daftar_resep
            )

            if not berhasil:
                messagebox.showerror(
                    "Gagal", "Resep gagal disimpan. Periksa stok dan database.",
                    parent=window
                )
                return

            messagebox.showinfo(
                "Berhasil", "Resep masuk ke antrean apoteker.",
                parent=window
            )
            window.destroy()
            self.refresh_dashboard()

        def tanpa_resep():
            if not messagebox.askyesno(
                "Konfirmasi",
                "Selesaikan kunjungan tanpa resep obat?",
                parent=window
            ):
                return

            berhasil = self.rekam_medis_model.selesaikan_tanpa_resep(
                id_rekam_medis, self.id_user
            )

            if berhasil:
                messagebox.showinfo(
                    "Berhasil", "Kunjungan selesai tanpa resep.",
                    parent=window
                )
                window.destroy()
                self.refresh_dashboard()
            else:
                messagebox.showerror(
                    "Gagal", "Kunjungan gagal diselesaikan.", parent=window
                )

        buat_tombol(
            tombol_akhir, "Simpan Resep", simpan_resep,
            warna=WARNA_HIJAU, hover="#2D704B", lebar=150
        ).pack(side="right")

        buat_tombol(
            tombol_akhir, "Tanpa Resep", tanpa_resep,
            warna=WARNA_BIRU, hover=WARNA_BIRU_TUA, lebar=130
        ).pack(side="right", padx=8)

    def logout(self):
        if self.on_logout:
            self.on_logout()
