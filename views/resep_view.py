import os
import sys
from tkinter import ttk, messagebox
import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.resep_controller import ResepController

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class ResepView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SIM Klinik - Kelola Data Resep")
        self.geometry("1050x620")
        self.resizable(True, True)
        self.configure(fg_color="#f4f5f7")

        self.selected_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.setup_form_ui()
        self.setup_table_ui()
        self.load_data()

    def setup_form_ui(self):
        """Form Input murni sesuai skema tabel 'resep'"""
        self.form_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#d9d9d9")
        self.form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        lbl_title = ctk.CTkLabel(
            self.form_frame, 
            text="Form Data Resep", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1a1a1a"
        )
        lbl_title.pack(pady=(20, 15), padx=20, anchor="w")

        # Field 1: id_rekam_medis
        self.ent_rekam_medis = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="ID Rekam Medis (Angka)",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_rekam_medis.pack(fill="x", padx=20, pady=6)

        # Field 2: id_obat
        self.ent_obat = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="ID Obat (Angka)",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_obat.pack(fill="x", padx=20, pady=6)

        # Field 3: dosis
        self.ent_dosis = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Dosis (e.g. 500mg)",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_dosis.pack(fill="x", padx=20, pady=6)

        # Field 4: jumlah
        self.ent_jumlah = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Jumlah (Angka)",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_jumlah.pack(fill="x", padx=20, pady=6)

        # Field 5: aturan_pakai
        self.ent_aturan = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="Aturan Pakai (e.g. 3x1 sesudah makan)",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#6c757d"
        )
        self.ent_aturan.pack(fill="x", padx=20, pady=6)

        # Field 6: status_penyerahan (ENUM: Menunggu, Diserahkan)
        self.opt_status = ctk.CTkOptionMenu(
            self.form_frame, 
            values=["Menunggu", "Diserahkan"],
            fg_color="#3b82f6",
            button_color="#2563eb",
            text_color="#ffffff"
        )
        self.opt_status.pack(fill="x", padx=20, pady=6)

        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(15, 20))

        btn_tambah = ctk.CTkButton(btn_frame, text="Tambah Data", command=self.tambah_data, fg_color="#28a745", hover_color="#218838")
        btn_tambah.pack(fill="x", pady=4)

        btn_update = ctk.CTkButton(btn_frame, text="Update Data", command=self.update_data, fg_color="#ffc107", text_color="black", hover_color="#e0a800")
        btn_update.pack(fill="x", pady=4)

        btn_hapus = ctk.CTkButton(btn_frame, text="Hapus Data", command=self.hapus_data, fg_color="#dc3545", hover_color="#c82333")
        btn_hapus.pack(fill="x", pady=4)

        btn_clear = ctk.CTkButton(btn_frame, text="Reset Form", command=self.clear_form, fg_color="#6c757d", hover_color="#5a6268")
        btn_clear.pack(fill="x", pady=4)

    def setup_table_ui(self):
        """Tabel Data Resep"""
        self.table_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#d9d9d9")
        self.table_frame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        search_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=15)

        self.ent_search = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Cari Resep...", 
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

        # Style Treeview Mode Terang
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

        columns = ("id_resep", "id_rekam_medis", "id_obat", "dosis", "jumlah", "aturan_pakai", "status_penyerahan")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        self.tree.heading("id_resep", text="ID Resep")
        self.tree.heading("id_rekam_medis", text="ID Rekam Medis")
        self.tree.heading("id_obat", text="ID Obat")
        self.tree.heading("dosis", text="Dosis")
        self.tree.heading("jumlah", text="Jumlah")
        self.tree.heading("aturan_pakai", text="Aturan Pakai")
        self.tree.heading("status_penyerahan", text="Status")

        self.tree.column("id_resep", width=60, anchor="center")
        self.tree.column("id_rekam_medis", width=90, anchor="center")
        self.tree.column("id_obat", width=70, anchor="center")
        self.tree.column("dosis", width=80)
        self.tree.column("jumlah", width=60, anchor="center")
        self.tree.column("aturan_pakai", width=140)
        self.tree.column("status_penyerahan", width=90, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            data = ResepController.get_all_resep()
            for row in data:
                if isinstance(row, dict):
                    values = (
                        row.get('id_resep'), 
                        row.get('id_rekam_medis'), 
                        row.get('id_obat'), 
                        row.get('dosis'), 
                        row.get('jumlah'),
                        row.get('aturan_pakai'),
                        row.get('status_penyerahan')
                    )
                else:
                    values = row
                self.tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")

    def tambah_data(self):
        id_rekam_medis = self.ent_rekam_medis.get().strip()
        id_obat = self.ent_obat.get().strip()
        dosis = self.ent_dosis.get().strip()
        jumlah = self.ent_jumlah.get().strip()
        aturan_pakai = self.ent_aturan.get().strip()
        status_penyerahan = self.opt_status.get()

        if not (id_rekam_medis and id_obat and jumlah):
            messagebox.showwarning("Peringatan", "ID Rekam Medis, ID Obat, dan Jumlah wajib diisi!")
            return

        try:
            success = ResepController.tambah_resep(id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan)
            if success:
                messagebox.showinfo("Sukses", "Data resep berhasil ditambahkan!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Gagal menambahkan resep! Pastikan ID Rekam Medis & ID Obat terdaftar di database.")
        except ValueError:
            messagebox.showerror("Error", "ID Rekam Medis, ID Obat, dan Jumlah harus berupa angka!")

    def update_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data resep dari tabel terlebih dahulu!")
            return

        id_rekam_medis = self.ent_rekam_medis.get().strip()
        id_obat = self.ent_obat.get().strip()
        dosis = self.ent_dosis.get().strip()
        jumlah = self.ent_jumlah.get().strip()
        aturan_pakai = self.ent_aturan.get().strip()
        status_penyerahan = self.opt_status.get()

        try:
            success = ResepController.update_resep(
                self.selected_id, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan
            )
            if success:
                messagebox.showinfo("Sukses", "Data resep berhasil diperbarui!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Gagal mengupdate data resep!")
        except ValueError:
            messagebox.showerror("Error", "ID Rekam Medis, ID Obat, dan Jumlah harus berupa angka!")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data resep dari tabel yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data resep ini?"):
            success = ResepController.hapus_resep(self.selected_id)
            if success:
                messagebox.showinfo("Sukses", "Data resep berhasil dihapus!")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Gagal menghapus data resep!")

    def cari_data(self):
        keyword = self.ent_search.get().strip()
        if not keyword:
            self.load_data()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        results = ResepController.cari_resep(keyword)
        for row in results:
            if isinstance(row, dict):
                values = (
                    row.get('id_resep'), 
                    row.get('id_rekam_medis'), 
                    row.get('id_obat'), 
                    row.get('dosis'), 
                    row.get('jumlah'),
                    row.get('aturan_pakai'),
                    row.get('status_penyerahan')
                )
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

        self.ent_rekam_medis.insert(0, values[1])
        self.ent_obat.insert(0, values[2])
        self.ent_dosis.insert(0, values[3])
        self.ent_jumlah.insert(0, values[4])
        self.ent_aturan.insert(0, values[5])
        self.opt_status.set(values[6])

    def clear_form(self, reset_selection=True):
        if reset_selection:
            self.selected_id = None
        self.ent_rekam_medis.delete(0, "end")
        self.ent_obat.delete(0, "end")
        self.ent_dosis.delete(0, "end")
        self.ent_jumlah.delete(0, "end")
        self.ent_aturan.delete(0, "end")
        self.opt_status.set("Menunggu")


