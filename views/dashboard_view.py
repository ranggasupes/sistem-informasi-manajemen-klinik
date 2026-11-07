import customtkinter as ctk
from tkinter import ttk

# Mengatur tema global CustomTkinter menjadi terang (Light)
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class DashboardAdminFrame(ctk.CTkFrame):
    def __init__(self, parent, username="Admin", on_logout=None):
        super().__init__(parent, fg_color="#FFFFFF")
        self.on_logout = on_logout
        
        self.header_label = ctk.CTkLabel(
            self, 
            text=f"Dashboard Admin - Selamat Datang, {username}", 
            font=("Arial", 22, "bold"),
            text_color="#333333"
        )
        self.header_label.pack(pady=25)
        
        self.menu_frame = ctk.CTkFrame(self, fg_color="#F0F0F0", corner_radius=10)
        self.menu_frame.pack(fill="x", padx=30, pady=10)
        
        self.btn_pasien = ctk.CTkButton(self.menu_frame, text="Kelola Pasien", fg_color="#1F6AA5", font=("Arial", 14, "bold"))
        self.btn_pasien.grid(row=0, column=0, padx=15, pady=15)
        
        self.btn_dokter = ctk.CTkButton(self.menu_frame, text="Kelola Dokter & Poli", fg_color="#1F6AA5", font=("Arial", 14, "bold"))
        self.btn_dokter.grid(row=0, column=1, padx=15, pady=15)
        
        self.btn_obat = ctk.CTkButton(self.menu_frame, text="Kelola Obat & Apotek", fg_color="#1F6AA5", font=("Arial", 14, "bold"))
        self.btn_obat.grid(row=0, column=2, padx=15, pady=15)
        
        self.btn_logout = ctk.CTkButton(
            self.menu_frame, 
            text="Logout", 
            fg_color="#D9534F", 
            hover_color="#C9302C",
            font=("Arial", 14, "bold"),
            command=self.on_logout
        )
        self.btn_logout.grid(row=0, column=3, padx=15, pady=15)
        
        self.content_frame = ctk.CTkFrame(self, fg_color="#FAFAFA", corner_radius=12, border_width=1, border_color="#DDDDDD")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.info_label = ctk.CTkLabel(
            self.content_frame, 
            text="Pilih menu di atas untuk mulai mengelola operasional klinik.", 
            font=("Arial", 15),
            text_color="#666666"
        )
        self.info_label.pack(pady=70)


class DashboardDokterFrame(ctk.CTkFrame):
    def __init__(self, parent, username="Dokter", on_logout=None):
        super().__init__(parent, fg_color="#FFFFFF")
        self.on_logout = on_logout
        
        self.header_label = ctk.CTkLabel(
            self, 
            text=f"Dashboard Dokter - Dr. {username}", 
            font=("Arial", 22, "bold"),
            text_color="#333333"
        )
        self.header_label.pack(pady=25)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="#FAFAFA", corner_radius=12, border_width=1, border_color="#DDDDDD")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(
            self.main_frame, 
            text="Daftar Antrean Pasien Hari Ini", 
            font=("Arial", 18, "bold"),
            text_color="#333333"
        ).pack(pady=15)
        
        columns = ("no_antrean", "nama_pasien", "keluhan", "status")
        self.tabel = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)
        
        self.tabel.heading("no_antrean", text="No. Antrean")
        self.tabel.heading("nama_pasien", text="Nama Pasien")
        self.tabel.heading("keluhan", text="Keluhan Utama")
        self.tabel.heading("status", text="Status")
        
        self.tabel.column("no_antrean", width=90, anchor="center")
        self.tabel.column("nama_pasien", width=200)
        self.tabel.column("keluhan", width=300)
        self.tabel.column("status", width=120, anchor="center")
        
        self.tabel.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=20)

        self.btn_periksa = ctk.CTkButton(
            self.btn_frame, 
            text="Mulai Pemeriksaan / Input Rekam Medis", 
            fg_color="#28A745", 
            hover_color="#218838",
            font=("Arial", 14, "bold")
        )
        self.btn_periksa.pack(side="left")

        self.btn_logout = ctk.CTkButton(
            self.btn_frame, 
            text="Logout", 
            fg_color="#D9534F", 
            hover_color="#C9302C",
            font=("Arial", 14, "bold"),
            command=self.on_logout
        )
        self.btn_logout.pack(side="right")


class DashboardPasienFrame(ctk.CTkFrame):
    def __init__(self, parent, username="Pasien", on_logout=None):
        super().__init__(parent, fg_color="#FFFFFF")
        self.on_logout = on_logout
        
        self.header_label = ctk.CTkLabel(
            self, 
            text=f"Selamat Datang, {username} (Pasien)", 
            font=("Arial", 22, "bold"),
            text_color="#333333"
        )
        self.header_label.pack(pady=25)
        
        self.action_frame = ctk.CTkFrame(self, fg_color="#F0F0F0", corner_radius=10)
        self.action_frame.pack(fill="x", padx=30, pady=10)
        
        self.btn_daftar = ctk.CTkButton(self.action_frame, text="Daftar Kunjungan & Poli", fg_color="#1F6AA5", font=("Arial", 14, "bold"))
        self.btn_daftar.pack(side="left", padx=20, pady=15)
        
        self.btn_riwayat = ctk.CTkButton(self.action_frame, text="Lihat Riwayat Rekam Medis", fg_color="#17A2B8", hover_color="#138496", font=("Arial", 14, "bold"))
        self.btn_riwayat.pack(side="left", padx=20, pady=15)
        
        self.btn_logout = ctk.CTkButton(
            self.action_frame, 
            text="Logout", 
            fg_color="#D9534F", 
            hover_color="#C9302C",
            font=("Arial", 14, "bold"),
            command=self.on_logout
        )
        self.btn_logout.pack(side="right", padx=20, pady=15)
        
        self.info_frame = ctk.CTkFrame(self, fg_color="#FAFAFA", corner_radius=12, border_width=1, border_color="#DDDDDD")
        self.info_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(self.info_frame, text="Status Antrean Anda Saat Ini:", font=("Arial", 18, "bold"), text_color="#333333").pack(pady=25)
        self.status_label = ctk.CTkLabel(
            self.info_frame, 
            text="Belum ada pendaftaran kunjungan aktif.", 
            font=("Arial", 15), 
            text_color="#888888"
        )
        self.status_label.pack(pady=10)

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Preview Dashboard Klinik")
    app.geometry("950x600")
    
    # Ganti dengan DashboardAdminFrame, DashboardDokterFrame, atau DashboardPasienFrame sesuai yang ingin dilihat
    frame = DashboardAdminFrame(app, username="Admin Klinik")
    
    frame.pack(fill="both", expand=True)
    app.mainloop()