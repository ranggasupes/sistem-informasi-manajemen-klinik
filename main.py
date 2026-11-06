
import customtkinter as ctk
from config.database import Database


class KlinikApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Informasi Manajemen Klinik")
        self.geometry("900x600")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Judul aplikasi
        self.label_judul = ctk.CTkLabel(
            self,
            text="SISTEM INFORMASI MANAJEMEN KLINIK",
            font=("Arial", 22, "bold")
        )
        self.label_judul.pack(pady=30)

        # Tombol tes koneksi database
        self.btn_database = ctk.CTkButton(
            self,
            text="Tes Koneksi Database",
            command=self.test_database
        )
        self.btn_database.pack(pady=15)

        # Label status
        self.label_status = ctk.CTkLabel(
            self,
            text="Status: Belum diperiksa",
            font=("Arial", 14)
        )
        self.label_status.pack(pady=10)

    def test_database(self):
        connection = Database.get_connection()

        if connection:
            self.label_status.configure(
                text="Status: Database berhasil terhubung!"
            )
            connection.close()
        else:
            self.label_status.configure(
                text="Status: Koneksi database gagal!"
            )


if __name__ == "__main__":
    app = KlinikApp()
    app.mainloop()
