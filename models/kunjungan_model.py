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
            cursor = connection.cursor(dictionary=True)

            # Cegah pendaftaran baru selama masih ada kunjungan aktif.
            cursor.execute(
                """
                SELECT id_kunjungan
                FROM kunjungan
                WHERE id_pasien = %s
                  AND status <> 'Selesai'
                LIMIT 1
                """,
                (id_pasien,)
            )

            kunjungan_aktif = cursor.fetchone()

            if kunjungan_aktif:
                connection.rollback()
                return False

            # Membuat nomor antrean berdasarkan poli dan tanggal.
            cursor.execute(
                """
                SELECT COALESCE(MAX(nomor_antrian), 0) + 1
                    AS nomor_baru
                FROM kunjungan
                WHERE id_poli = %s
                  AND tanggal_kunjungan = %s
                """,
                (id_poli, tanggal_kunjungan)
            )

            nomor_antrian = cursor.fetchone()["nomor_baru"]

            cursor.execute(
                """
                INSERT INTO kunjungan (
                    id_pasien,
                    id_poli,
                    id_dokter,
                    nomor_antrian,
                    tanggal_kunjungan,
                    keluhan_awal,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'Menunggu')
                """,
                (
                    id_pasien,
                    id_poli,
                    id_dokter,
                    nomor_antrian,
                    tanggal_kunjungan,
                    keluhan_awal
                )
            )

            id_kunjungan = cursor.lastrowid
            connection.commit()

            return {
                "id_kunjungan": id_kunjungan,
                "nomor_antrian": nomor_antrian
            }

        except Exception as e:
            print(f"Error menyimpan kunjungan: {e}")
            connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def get_active_by_user_id(self, id_user):
        connection = Database.get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    k.id_kunjungan,
                    k.nomor_antrian,
                    k.tanggal_kunjungan,
                    k.keluhan_awal,
                    k.status,
                    po.nama_poli,
                    d.nama_dokter
                FROM kunjungan k
                JOIN pasien p
                    ON k.id_pasien = p.id_pasien
                JOIN poli po
                    ON k.id_poli = po.id_poli
                LEFT JOIN dokter d
                    ON k.id_dokter = d.id_dokter
                WHERE p.id_user = %s
                  AND k.status <> 'Selesai'
                ORDER BY k.id_kunjungan DESC
                LIMIT 1
            """

            cursor.execute(query, (id_user,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error mengambil antrean aktif: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            connection.close()