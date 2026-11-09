import mysql.connector
from mysql.connector import Error


class Database:

    HOST = "localhost"
    USER = "root"
    PASSWORD = ""
    DATABASE = "sistem_informasi_klinik"

    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host=Database.HOST,
                user=Database.USER,
                password=Database.PASSWORD,
                database=Database.DATABASE,
                use_pure=True
            )

            return connection

        except Error as e:
            print(f"Koneksi database gagal: {e}")
            return None