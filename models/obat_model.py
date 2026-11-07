import mysql.connector
from config.database import Database


def get_db_connection():
    """Wrapper untuk kompatibilitas unit test."""
    return Database.get_connection()


class ObatModel:
    @staticmethod
    def get_all_obat():
        """Mengambil seluruh data obat sesuai skema tabel obat."""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id_obat, nama_obat, jenis_obat, satuan, stok FROM obat ORDER BY id_obat DESC"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as err:
            print(f"[Error Database - get_all_obat]: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def get_by_id(id_obat):
        """Mengambil satu obat berdasarkan id_obat."""
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id_obat, nama_obat, jenis_obat, satuan, stok FROM obat WHERE id_obat = %s"
            cursor.execute(query, (id_obat,))
            return cursor.fetchone()
        except Exception as err:
            print(f"[Error Database - get_by_id]: {err}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def tambah_obat(nama_obat, jenis_obat, satuan, stok):
        """Menambahkan obat baru."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = "INSERT INTO obat (nama_obat, jenis_obat, satuan, stok) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nama_obat, jenis_obat, satuan, int(stok)))
            conn.commit()
            return True
        except Exception as err:
            print(f"[Error Database - tambah_obat]: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_obat(id_obat, nama_obat, jenis_obat, satuan, stok):
        """Memperbarui data obat berdasarkan id_obat."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = """
                UPDATE obat 
                SET nama_obat = %s, jenis_obat = %s, satuan = %s, stok = %s 
                WHERE id_obat = %s
            """
            cursor.execute(query, (nama_obat, jenis_obat, satuan, int(stok), id_obat))
            conn.commit()
            return True
        except Exception as err:
            print(f"[Error Database - update_obat]: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def hapus_obat(id_obat):
        """Menghapus obat berdasarkan id_obat."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM obat WHERE id_obat = %s"
            cursor.execute(query, (id_obat,))
            conn.commit()
            return True
        except Exception as err:
            print(f"[Error Database - hapus_obat]: {err}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def cari_obat(keyword):
        """Mencari obat berdasarkan nama_obat atau jenis_obat."""
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id_obat, nama_obat, jenis_obat, satuan, stok 
                FROM obat 
                WHERE nama_obat LIKE %s OR jenis_obat LIKE %s 
                ORDER BY id_obat DESC
            """
            pattern = f"%{keyword}%"
            cursor.execute(query, (pattern, pattern))
            return cursor.fetchall()
        except Exception as err:
            print(f"[Error Database - cari_obat]: {err}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

