
from config.database import Database


class KunjunganModel:

    def get_all_kunjungan(self):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    k.id_kunjungan,
                    k.tanggal_kunjungan,
                    k.nomor_antrian,
                    k.keluhan_awal,
                    k.status,
                    p.nama_pasien,
                    po.nama_poli,
                    d.nama_dokter
                FROM kunjungan k
                JOIN pasien p
                    ON k.id_pasien = p.id_pasien
                JOIN poli po
                    ON k.id_poli = po.id_poli
                LEFT JOIN dokter d
                    ON k.id_dokter = d.id_dokter
                ORDER BY
                    k.tanggal_kunjungan DESC,
                    k.id_poli,
                    k.nomor_antrian
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil data kunjungan: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def create_kunjungan(
        self,
        id_pasien,
        id_poli,
        id_dokter,
        tanggal_kunjungan,
        keluhan_awal
    ):
        connection = Database.get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            # Membuat nomor antrean berdasarkan poli dan tanggal
            query_antrian = """
                SELECT COALESCE(MAX(nomor_antrian), 0) + 1
                FROM kunjungan
                WHERE id_poli = %s
                  AND tanggal_kunjungan = %s
            """

            cursor.execute(
                query_antrian,
                (id_poli, tanggal_kunjungan)
            )

            nomor_antrian = cursor.fetchone()[0]

            # Menyimpan kunjungan baru
            query_insert = """
                INSERT INTO kunjungan (
                    id_pasien,
                    id_poli,
                    id_dokter,
                    nomor_antrian,
                    tanggal_kunjungan,
                    keluhan_awal
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                id_pasien,
                id_poli,
                id_dokter,
                nomor_antrian,
                tanggal_kunjungan,
                keluhan_awal
            )

            cursor.execute(query_insert, values)
            connection.commit()

            return True

        except Exception as e:
            print(f"Error menyimpan kunjungan: {e}")
            connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            connection.close()
