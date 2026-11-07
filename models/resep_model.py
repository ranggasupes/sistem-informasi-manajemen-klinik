import mysql.connector
from config.database import Database


def get_db_connection():
    """Wrapper untuk pengujian/mocking."""
    return Database.get_connection()


class ResepModel:
    @staticmethod
    def get_all_resep():
        """Mengambil seluruh data resep."""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan 
                FROM resep 
                ORDER BY id_resep DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as err:
            print(f"[Error Database - get_all_resep]: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_id(id_resep):
        """Mengambil satu data resep berdasarkan id_resep."""
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan 
                FROM resep 
                WHERE id_resep = %s
            """
            cursor.execute(query, (id_resep,))
            return cursor.fetchone()
        except Exception as err:
            print(f"[Error Database - get_by_id]: {err}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def tambah_resep(id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan="Menunggu"):
        """Menambahkan record resep baru ke database."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO resep (id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (int(id_rekam_medis), int(id_obat), dosis, int(jumlah), aturan_pakai, status_penyerahan))
            conn.commit()
            return True
        except Exception as err:
            print(f"[Error Database - tambah_resep]: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_resep(id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan):
        """Memperbarui data resep berdasarkan id_resep."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
                UPDATE resep 
                SET id_rekam_medis = %s, id_obat = %s, dosis = %s, jumlah = %s, aturan_pakai = %s, status_penyerahan = %s 
                WHERE id_resep = %s
            """
            cursor.execute(query, (int(id_rekam_medis), int(id_obat), dosis, int(jumlah), aturan_pakai, status_penyerahan, id_resep))
            conn.commit()
            return True
        except Exception as err:
            print(f"[Error Database - update_resep]: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def hapus_resep(id_resep):
        """Menghapus data resep berdasarkan id_resep."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM resep WHERE id_resep = %s"
            cursor.execute(query, (id_resep,))
            conn.commit()
            return True
        except Exception as err:
            print(f"[Error Database - hapus_resep]: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def cari_resep(keyword):
        """Mencari resep berdasarkan id_rekam_medis, dosis, atau aturan_pakai."""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan 
                FROM resep 
                WHERE id_rekam_medis LIKE %s OR dosis LIKE %s OR aturan_pakai LIKE %s OR status_penyerahan LIKE %s
                ORDER BY id_resep DESC
            """
            pattern = f"%{keyword}%"
            cursor.execute(query, (pattern, pattern, pattern, pattern))
            return cursor.fetchall()
        except Exception as err:
            print(f"[Error Database - cari_resep]: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

