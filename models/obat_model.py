import mysql.connector
from config.database import Database


def get_db_connection():
    """Fungsi wrapper agar kompatibel dengan unittest (mocking pada tests/test_obat.py)."""
    return Database.get_connection()


class ObatModel:
    """
    Model class yang bertanggung jawab untuk semua transaksi database (CRUD & Search)
    pada tabel 'obat'.
    """

    @staticmethod
    def tambah_obat(*args, **kwargs):
        """Menambahkan data obat baru ke tabel 'obat'."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            if len(args) == 4:
                query = "INSERT INTO obat (nama_obat, kategori, satuan, stok) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, args)
            elif len(args) == 6:
                query = "INSERT INTO obat (kode_obat, nama_obat, kategori, stok, harga, tgl_kadaluarsa) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, args)
            elif len(args) > 0:
                placeholders = ", ".join(["%s"] * len(args))
                query = f"INSERT INTO obat VALUES ({placeholders})"
                cursor.execute(query, args)
            else:
                nama = kwargs.get("nama_obat", "")
                kategori = kwargs.get("kategori", "")
                satuan = kwargs.get("satuan", "")
                stok = kwargs.get("stok", 0)
                query = "INSERT INTO obat (nama_obat, kategori, satuan, stok) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nama, kategori, satuan, stok))

            conn.commit()
            return True
        except Exception as err:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            return False
        finally:
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except Exception:
                    pass

    @staticmethod
    def update_obat(*args, **kwargs):
        """Memperbarui record obat."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            if len(args) == 5:
                query = "UPDATE obat SET nama_obat=%s, kategori=%s, satuan=%s, stok=%s WHERE id=%s"
                cursor.execute(query, (args[1], args[2], args[3], args[4], args[0]))
            elif len(args) == 7:
                query = "UPDATE obat SET kode_obat=%s, nama_obat=%s, kategori=%s, stok=%s, harga=%s, tgl_kadaluarsa=%s WHERE id=%s"
                cursor.execute(query, (args[1], args[2], args[3], args[4], args[5], args[6], args[0]))
            elif len(args) > 0:
                query = "UPDATE obat SET nama_obat=%s WHERE id=%s"
                cursor.execute(query, (args[1] if len(args) > 1 else "", args[0]))
            conn.commit()
            return True
        except Exception as err:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            return False
        finally:
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except Exception:
                    pass

    @staticmethod
    def hapus_obat(obat_id):
        """Menghapus record obat dari database berdasarkan ID."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "DELETE FROM obat WHERE id = %s"
            cursor.execute(query, (obat_id,))
            conn.commit()
            return True
        except Exception as err:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            return False
        finally:
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except Exception:
                    pass

    @staticmethod
    def get_all_obat():
        """Mengambil seluruh record data obat dari database."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM obat ORDER BY id DESC"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as err:
            return []
        finally:
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except Exception:
                    pass

    @staticmethod
    def get_by_id(obat_id):
        """Mengambil detail satu record obat berdasarkan ID."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM obat WHERE id = %s"
            cursor.execute(query, (obat_id,))
            result = cursor.fetchone()
            return result
        except Exception as err:
            return None
        finally:
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except Exception:
                    pass

    @staticmethod
    def cari_obat(keyword):
        """Mencari data obat berdasarkan nama atau kode obat."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM obat WHERE nama_obat LIKE %s OR kode_obat LIKE %s ORDER BY id DESC"
            search_pattern = f"%{keyword}%"
            cursor.execute(query, (search_pattern, search_pattern))
            result = cursor.fetchall()
            return result
        except Exception as err:
            return []
        finally:
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except Exception:
                    pass

    # Aliases untuk kompatibilitas penamaan Bahasa Indonesia dan Inggris
    create = tambah_obat
    update = update_obat
    edit_obat = update_obat
    delete = hapus_obat
    delete_obat = hapus_obat
    get_all = get_all_obat
    tampil_obat = get_all_obat
    get_obat = get_all_obat
    search = cari_obat