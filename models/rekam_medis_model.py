from config.database import Database


class RekamMedisModel:

    def get_all_rekam_medis(self):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    rm.id_rekam_medis,
                    rm.id_kunjungan,
                    rm.tekanan_darah,
                    rm.suhu_tubuh,
                    rm.berat_badan,
                    rm.diagnosis,
                    rm.catatan,
                    rm.tanggal_pemeriksaan,
                    p.nama_pasien
                FROM rekam_medis rm
                JOIN kunjungan k
                    ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p
                    ON k.id_pasien = p.id_pasien
                ORDER BY rm.tanggal_pemeriksaan DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil data rekam medis: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def create_rekam_medis(
        self,
        id_kunjungan,
        tekanan_darah,
        suhu_tubuh,
        berat_badan,
        diagnosis,
        catatan
    ):
        connection = Database.get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO rekam_medis (
                    id_kunjungan,
                    tekanan_darah,
                    suhu_tubuh,
                    berat_badan,
                    diagnosis,
                    catatan
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                id_kunjungan,
                tekanan_darah or None,
                suhu_tubuh or None,
                berat_badan or None,
                diagnosis,
                catatan or None
            )

            cursor.execute(query, values)
            connection.commit()

            return True

        except Exception as e:
            print(f"Error menyimpan rekam medis: {e}")
            connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def get_history_by_user_id(self, id_user):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    rm.id_rekam_medis,
                    rm.id_kunjungan,
                    rm.tekanan_darah,
                    rm.suhu_tubuh,
                    rm.berat_badan,
                    rm.diagnosis,
                    rm.catatan,
                    rm.tanggal_pemeriksaan,
                    k.nomor_antrian,
                    k.tanggal_kunjungan,
                    po.nama_poli,
                    d.nama_dokter
                FROM rekam_medis rm
                JOIN kunjungan k
                    ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p
                    ON k.id_pasien = p.id_pasien
                JOIN poli po
                    ON k.id_poli = po.id_poli
                LEFT JOIN dokter d
                    ON k.id_dokter = d.id_dokter
                WHERE p.id_user = %s
                ORDER BY rm.tanggal_pemeriksaan DESC
            """

            cursor.execute(query, (id_user,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil riwayat medis pasien: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()