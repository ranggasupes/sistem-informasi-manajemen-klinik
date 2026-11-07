
from config.database import Database


class ProfilKesehatanModel:

    def get_by_pasien_id(self, id_pasien):
        connection = Database.get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    id_profil,
                    id_pasien,
                    alergi,
                    penyakit_bawaan,
                    riwayat_penyakit,
                    catatan_kesehatan,
                    sumber_data,
                    tanggal_sinkronisasi
                FROM profil_kesehatan
                WHERE id_pasien = %s
                LIMIT 1
            """

            cursor.execute(query, (id_pasien,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error mengambil profil kesehatan: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            connection.close()
