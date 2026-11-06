import mysql.connector

class Database:
    def __init__(self):
        # Konfigurasi koneksi database MySQL (Default Laragon: user root, tanpa password)
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = " sistem_informasi_klinik" # Sesuaikan dengan nama database Anda diphpMyAdmin

    def get_connection(self):
        """Membuat dan mengembalikan objek koneksi database"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Koneksi ke database gagal: {err}")
            return None