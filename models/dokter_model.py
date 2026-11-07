from config.database import get_db_connection

class DokterModel:
    def get_all_dokter(self):
        conn = get_db_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dokter")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result