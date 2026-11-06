
import customtkinter as ctk
from tkinter import messagebox

from controllers.auth_controller import AuthController


class LoginView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.auth_controller = AuthController()

        self.title("Login - Sistem Informasi Klinik")
        self.geometry("900x550")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Frame utama
        self.frame_login = ctk.CTkFrame(
            self,
            width=400,
            height=420,
            corner_radius=15
        )
        self.frame_login.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.frame_login.pack_propagate(False)

        # Judul
        self.label_judul = ctk.CTkLabel(
            self.frame_login,
            text="KLINIK SEHAT",
            font=("Arial", 26, "bold")
        )
        self.label_judul.pack(pady=(35, 5))

        self.label_subjudul = ctk.CTkLabel(
            self.frame_login,
            text="Sistem Informasi Manajemen Klinik",
            font=("Arial", 13)
        )
        self.label_subjudul.pack(pady=(0, 25))

        # Input username
        self.entry_username = ctk.CTkEntry(
            self.frame_login,
            width=300,
            height=40,
            placeholder_text="Masukkan username"
        )
        self.entry_username.pack(pady=10)

        # Input password
        self.entry_password = ctk.CTkEntry(
            self.frame_login,
            width=300,
            height=40,
            placeholder_text="Masukkan password",
            show="*"
        )
        self.entry_password.pack(pady=10)

        # Tombol login
        self.btn_login = ctk.CTkButton(
            self.frame_login,
            text="LOGIN",
            width=300,
            height=40,
            command=self.proses_login
        )
        self.btn_login.pack(pady=25)

        self.label_footer = ctk.CTkLabel(
            self.frame_login,
            text="Sistem Informasi Manajemen Klinik",
            font=("Arial", 11)
        )
        self.label_footer.pack(pady=5)

        self.entry_username.focus()

    def proses_login(self):

        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        berhasil, hasil = self.auth_controller.login(
            username,
            password
        )

        if berhasil:
            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang!\nRole: {hasil}"
            )

            self.tampilkan_halaman_berhasil(username, hasil)

        else:
            messagebox.showerror(
                "Login Gagal",
                hasil
            )

    def tampilkan_halaman_berhasil(self, username, role):

        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("900x550")

        label = ctk.CTkLabel(
            self,
            text=f"Selamat datang, {username}!",
            font=("Arial", 25, "bold")
        )
        label.pack(pady=40)

        label_role = ctk.CTkLabel(
            self,
            text=f"Anda login sebagai: {role}",
            font=("Arial", 16)
        )
        label_role.pack(pady=10)

        label_info = ctk.CTkLabel(
            self,
            text="Login berhasil. Halaman dashboard akan dibuat berikutnya.",
            font=("Arial", 14)
        )
        label_info.pack(pady=20)
