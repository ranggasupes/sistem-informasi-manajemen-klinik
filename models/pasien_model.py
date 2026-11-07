from ..config.database import get_db_connection

class PasienModel:
    def get_all_pasien(self):
        conn = get_db_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def tambah_pasien(self, nama, nik, alamat, no_telp):
        conn = get_db_connection()
        if not conn: return False
        cursor = conn.cursor()
        query = "INSERT INTO pasien (nama, nik, alamat, no_telp) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (nama, nik, alamat, no_telp))
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = False
        finally:
            cursor.close()
            conn.close()
        return success