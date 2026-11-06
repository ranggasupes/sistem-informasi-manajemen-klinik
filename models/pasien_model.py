from config.database import Database

class PasienModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "pasien"

    def get_all_pasien(self):
        """Mengambil seluruh data pasien dari database (Read)"""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_pasien(self, nama, nik, alamat, tanggal_lahir, no_telepon):
        """Menambahkan data pasien baru secara aman menggunakan Parameterized Query (Create)"""
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama, nik, alamat, tanggal_lahir, no_telepon) VALUES (%s, %s, %s, %s, %s)"
            val = (nama, nik, alamat, tanggal_lahir, no_telepon)
            try:
                cursor.execute(query, val)
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error: {e}")
                self.conn.rollback()
                cursor.close()
                return False
        return False