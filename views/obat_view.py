import os
import sys
from tkinter import ttk, messagebox
import customtkinter as ctk

# Menyesuaikan sys.path agar impor modul controllers aman
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.obat_controller import ObatController

# 1. Atur mode tampilan ke Terang (Light Mode)
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class ObatView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SIM Klinik - Kelola Data Obat")
        self.geometry("1000x600")
        self.resizable(True, True)

        # 2. Latar belakang utama window (putih abu-abu terang)
        self.configure(fg_color="#f4f5f7")

        self.selected_id = None

        # Layout Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.setup_form_ui()
        self.setup_table_ui()
        self.load_data()

    def setup_form_ui(self):
        """Form Input (Panel Kiri) dengan latar kartu abu-abu terang"""
        # 3. fg_color="#d9d9d9" disesuaikan dengan kartu abu-abu pada gambar referensi
        self.form_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#d9d9d9")
        self.form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        lbl_title = ctk.CTkLabel(
            self.form_frame, 
            text="Form Data Obat", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1a1a1a"
        )
        lbl_title.pack(pady=(20, 15), padx=20, anchor="w")

        # 4. Entry input berlatar belakang putih dengan teks hitam
        self.ent_nama = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Nama Obat",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_nama.pack(fill="x", padx=20, pady=6)

        self.opt_kategori = ctk.CTkOptionMenu(
            self.form_frame, 
            values=["Obat Bebas", "Obat Keras", "Sirup", "Tablet/Kapsul", "Salep", "Alkes"],
            fg_color="#3b82f6",
            button_color="#2563eb",
            text_color="#ffffff"
        )
        self.opt_kategori.pack(fill="x", padx=20, pady=6)

        self.ent_satuan = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Satuan (Strip/Botol/Pcs)",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_satuan.pack(fill="x", padx=20, pady=6)

        self.ent_stok = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Jumlah Stok",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_stok.pack(fill="x", padx=20, pady=6)

        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(15, 20))

        # Warna tombol tetap asli
        btn_tambah = ctk.CTkButton(btn_frame, text="Tambah Data", command=self.tambah_data, fg_color="#28a745", hover_color="#218838")
        btn_tambah.pack(fill="x", pady=4)

        btn_update = ctk.CTkButton(btn_frame, text="Update Data", command=self.update_data, fg_color="#ffc107", text_color="black", hover_color="#e0a800")
        btn_update.pack(fill="x", pady=4)

        btn_hapus = ctk.CTkButton(btn_frame, text="Hapus Data", command=self.hapus_data, fg_color="#dc3545", hover_color="#c82333")
        btn_hapus.pack(fill="x", pady=4)

        btn_clear = ctk.CTkButton(btn_frame, text="Reset Form", command=self.clear_form, fg_color="#6c757d", hover_color="#5a6268")
        btn_clear.pack(fill="x", pady=4)

    def setup_table_ui(self):
        """Tabel Data & Search (Panel Kanan)"""
        self.table_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#d9d9d9")
        self.table_frame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        search_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=15)

        self.ent_search = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Cari Obat...", 
            width=250,
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_search.pack(side="left", padx=(0, 10))

        btn_search = ctk.CTkButton(search_frame, text="Cari", command=self.cari_data, width=80)
        btn_search.pack(side="left", padx=4)

        btn_reset = ctk.CTkButton(search_frame, text="Refresh", command=self.load_data, width=80, fg_color="#17a2b8")
        btn_reset.pack(side="left")

        # 5. Style Treeview disesuaikan untuk Mode Terang
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", 
            background="#ffffff", 
            foreground="#000000", 
            fieldbackground="#ffffff", 
            rowheight=28,
            gridcolor="#e5e7eb"
        )
        style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "#ffffff")])
        style.configure(
            "Treeview.Heading", 
            background="#2563eb", 
            foreground="#ffffff", 
            font=('Arial', 10, 'bold')
        )

        columns = ("id", "nama", "kategori", "satuan", "stok")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama Obat")
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("satuan", text="Satuan")
        self.tree.heading("stok", text="Stok")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nama", width=200)
        self.tree.column("kategori", width=120)
        self.tree.column("satuan", width=100)
        self.tree.column("stok", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            data = ObatController.get_all_obat()
            if data is None:
                messagebox.showerror("Koneksi Gagal", "Gagal terhubung ke MySQL! Pastikan XAMPP/MySQL sudah dinyalakan.")
                return

            for row in data:
                if isinstance(row, dict):
                    values = (row.get('id'), row.get('nama_obat'), row.get('kategori'), row.get('satuan', '-'), row.get('stok'))
                else:
                    values = row
                self.tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")

    def tambah_data(self):
        nama = self.ent_nama.get().strip()
        kategori = self.opt_kategori.get()
        satuan = self.ent_satuan.get().strip()
        stok = self.ent_stok.get().strip()

        if not (nama and stok):
            messagebox.showwarning("Peringatan", "Nama Obat dan Stok wajib diisi!")
            return

        success = ObatController.tambah_obat(nama, kategori, satuan, int(stok))
        if success:
            messagebox.showinfo("Sukses", "Data obat berhasil ditambahkan!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Gagal menambahkan data obat! Cek koneksi MySQL.")

    def update_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data obat dari tabel terlebih dahulu!")
            return

        nama = self.ent_nama.get().strip()
        kategori = self.opt_kategori.get()
        satuan = self.ent_satuan.get().strip()
        stok = self.ent_stok.get().strip()

        success = ObatController.update_obat(self.selected_id, nama, kategori, satuan, int(stok))
        if success:
            messagebox.showinfo("Sukses", "Data obat berhasil diperbarui!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Gagal mengupdate data obat!")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data obat dari tabel yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            success = ObatController.hapus_obat(self.selected_id)
            if success:
                messagebox.showinfo("Sukses", "Data obat berhasil dihapus!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Gagal menghapus data obat!")

    def cari_data(self):
        keyword = self.ent_search.get().strip()
        if not keyword:
            self.load_data()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        results = ObatController.cari_obat(keyword)
        for row in results:
            if isinstance(row, dict):
                values = (row.get('id'), row.get('nama_obat'), row.get('kategori'), row.get('satuan', '-'), row.get('stok'))
            else:
                values = row
            self.tree.insert("", "end", values=values)

    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        self.selected_id = values[0]
        self.clear_form(reset_selection=False)

        self.ent_nama.insert(0, values[1])
        self.opt_kategori.set(values[2])
        self.ent_satuan.insert(0, values[3])
        self.ent_stok.insert(0, values[4])

    def clear_form(self, reset_selection=True):
        if reset_selection:
            self.selected_id = None
        self.ent_nama.delete(0, "end")
        self.ent_satuan.delete(0, "end")
        self.ent_stok.delete(0, "end")
        self.opt_kategori.set("Obat Bebas")


