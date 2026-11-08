
from config.database import Database


def get_db_connection():
    """Mengambil koneksi database."""
    return Database.get_connection()


class ObatModel:

    @staticmethod
    def tambah_obat(*args, **kwargs):
        conn = get_db_connection()

        if conn is None:
            return False

        cursor = None

        try:
            cursor = conn.cursor()

            if len(args) >= 4:
                nama, jenis, satuan, stok = args[:4]
            else:
                nama = kwargs.get("nama_obat", "")
                jenis = kwargs.get(
                    "jenis_obat",
                    kwargs.get("kategori", "")
                )
                satuan = kwargs.get("satuan", "")
                stok = kwargs.get("stok", 0)

            query = """
                INSERT INTO obat (
                    nama_obat,
                    jenis_obat,
                    satuan,
                    stok
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (nama, jenis, satuan, stok)
            )

            conn.commit()
            return True

        except Exception as e:
            print(f"Error menambahkan obat: {e}")
            conn.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def update_obat(*args, **kwargs):
        conn = get_db_connection()

        if conn is None:
            return False

        cursor = None

        try:
            cursor = conn.cursor()

            if len(args) >= 5:
                obat_id, nama, jenis, satuan, stok = args[:5]
            else:
                obat_id = kwargs.get("id_obat")
                nama = kwargs.get("nama_obat", "")
                jenis = kwargs.get(
                    "jenis_obat",
                    kwargs.get("kategori", "")
                )
                satuan = kwargs.get("satuan", "")
                stok = kwargs.get("stok", 0)

            query = """
                UPDATE obat
                SET nama_obat = %s,
                    jenis_obat = %s,
                    satuan = %s,
                    stok = %s
                WHERE id_obat = %s
            """

            cursor.execute(
                query,
                (nama, jenis, satuan, stok, obat_id)
            )

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error memperbarui obat: {e}")
            conn.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def hapus_obat(obat_id):
        conn = get_db_connection()

        if conn is None:
            return False

        cursor = None

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM obat WHERE id_obat = %s",
                (obat_id,)
            )

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error menghapus obat: {e}")
            conn.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def get_all_obat():
        conn = get_db_connection()

        if conn is None:
            return []

        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    id_obat,
                    id_obat AS id,
                    nama_obat,
                    jenis_obat,
                    jenis_obat AS kategori,
                    satuan,
                    stok
                FROM obat
                ORDER BY id_obat DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil data obat: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(obat_id):
        conn = get_db_connection()

        if conn is None:
            return None

        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    id_obat,
                    id_obat AS id,
                    nama_obat,
                    jenis_obat,
                    jenis_obat AS kategori,
                    satuan,
                    stok
                FROM obat
                WHERE id_obat = %s
                """,
                (obat_id,)
            )

            return cursor.fetchone()

        except Exception as e:
            print(f"Error mengambil detail obat: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def cari_obat(keyword):
        conn = get_db_connection()

        if conn is None:
            return []

        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            pola = f"%{keyword}%"

            cursor.execute(
                """
                SELECT
                    id_obat,
                    id_obat AS id,
                    nama_obat,
                    jenis_obat,
                    jenis_obat AS kategori,
                    satuan,
                    stok
                FROM obat
                WHERE nama_obat LIKE %s
                   OR jenis_obat LIKE %s
                ORDER BY id_obat DESC
                """,
                (pola, pola)
            )

            return cursor.fetchall()

        except Exception as e:
            print(f"Error mencari obat: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            conn.close()

    # Alias kompatibilitas
    create = tambah_obat
    update = update_obat
    edit_obat = update_obat
    delete = hapus_obat
    delete_obat = hapus_obat
    get_all = get_all_obat
    tampil_obat = get_all_obat
    get_obat = get_all_obat
    search = cari_obat
