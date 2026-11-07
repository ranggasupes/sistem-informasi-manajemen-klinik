
from config.database import Database


class PasienModel:

    def get_all_pasien(self):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    id_pasien,
                    id_user,
                    nomor_bpjs,
                    nik,
                    nama_pasien,
                    jenis_kelamin,
                    tanggal_lahir,
                    alamat,
                    no_telepon
                FROM pasien
                ORDER BY id_pasien DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil data pasien: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def create_pasien(
        self,
        id_user,
        nomor_bpjs,
        nik,
        nama_pasien,
        jenis_kelamin,
        tanggal_lahir,
        alamat,
        no_telepon
    ):
        connection = Database.get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO pasien (
                    id_user,
                    nomor_bpjs,
                    nik,
                    nama_pasien,
                    jenis_kelamin,
                    tanggal_lahir,
                    alamat,
                    no_telepon
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                id_user,
                nomor_bpjs,
                nik,
                nama_pasien,
                jenis_kelamin,
                tanggal_lahir,
                alamat,
                no_telepon
            )

            cursor.execute(query, values)
            connection.commit()

            return True

        except Exception as e:
            print(f"Error menyimpan data pasien: {e}")
            connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            connection.close()
