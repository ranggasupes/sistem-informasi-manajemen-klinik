
import customtkinter as ctk
from tkinter import messagebox

from controllers.auth_controller import AuthController
from views.dashboard_view import (
    DashboardAdminFrame,
    DashboardDokterFrame,
    DashboardPasienFrame
)


class LoginView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.auth_controller = AuthController()
        self.current_user = None

        self.title("Sistem Informasi Manajemen Klinik")
        self.geometry("900x550")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.tampilkan_form_login()

    def tampilkan_form_login(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.current_user = None
        self.geometry("900x550")
        self.resizable(False, False)

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

        ctk.CTkLabel(
            self.frame_login,
            text="KLINIK SEHAT",
            font=("Arial", 26, "bold")
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.frame_login,
            text="Sistem Informasi Manajemen Klinik",
            font=("Arial", 13)
        ).pack(pady=(0, 25))

        self.entry_username = ctk.CTkEntry(
            self.frame_login,
            width=300,
            height=40,
            placeholder_text="Masukkan username"
        )
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            self.frame_login,
            width=300,
            height=40,
            placeholder_text="Masukkan password",
            show="*"
        )
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(
            self.frame_login,
            text="LOGIN",
            width=300,
            height=40,
            command=self.proses_login
        )
        self.btn_login.pack(pady=25)

        ctk.CTkLabel(
            self.frame_login,
            text="Sistem Informasi Manajemen Klinik",
            font=("Arial", 11)
        ).pack(pady=5)

        self.entry_username.focus()

    def proses_login(self):

        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        berhasil, hasil = self.auth_controller.login(
            username,
            password
        )

        if not berhasil:
            messagebox.showerror("Login Gagal", hasil)
            return

        self.tampilkan_dashboard(username, hasil)

    def tampilkan_dashboard(self, username, user):

        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("1100x650")
        self.resizable(True, True)

        self.current_user = user
        role = user["role"]

        if role == "pasien":

            dashboard = DashboardPasienFrame(
                self,
                username=username,
                id_user=user["id_user"],
                on_logout=self.logout
            )

        elif role == "dokter":

            dashboard = DashboardDokterFrame(
                self,
                username=username,
                id_user=user["id_user"],
                on_logout=self.logout
            )

        elif role == "apoteker_admin":

            dashboard = DashboardAdminFrame(
                self,
                username=username,
                id_user=user["id_user"],
                on_logout=self.logout
            )

        else:
            messagebox.showerror(
                "Role Tidak Dikenali",
                f"Role {role} tidak tersedia."
            )
            self.tampilkan_form_login()
            return

        dashboard.pack(fill="both", expand=True)

    def logout(self):

        konfirmasi = messagebox.askyesno(
            "Logout",
            "Apakah Anda yakin ingin keluar?"
        )

        if konfirmasi:
            self.tampilkan_form_login()


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
