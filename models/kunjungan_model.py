
from config.database import Database


class KunjunganModel:

    def _koneksi(self, dictionary=True):
        connection = Database.get_connection()
        if connection is None:
            return None, None
        return connection, connection.cursor(dictionary=dictionary)

    def _tutup(self, connection, cursor):
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    def get_all_kunjungan(self):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT k.id_kunjungan, k.tanggal_kunjungan,
                       k.nomor_antrian, k.keluhan_awal, k.status,
                       p.nama_pasien, po.nama_poli, d.nama_dokter
                FROM kunjungan k
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN poli po ON k.id_poli = po.id_poli
                LEFT JOIN dokter d ON k.id_dokter = d.id_dokter
                ORDER BY k.tanggal_kunjungan DESC,
                         k.id_poli, k.nomor_antrian
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error mengambil kunjungan: {e}")
            return []
        finally:
            self._tutup(connection, cursor)

    def create_kunjungan(
        self, id_pasien, id_poli, id_dokter,
        tanggal_kunjungan, keluhan_awal
    ):
        connection, cursor = self._koneksi()
        if not connection:
            return False

        try:
            cursor.execute("""
                SELECT id_kunjungan FROM kunjungan
                WHERE id_pasien = %s AND status <> 'Selesai'
                LIMIT 1
            """, (id_pasien,))

            if cursor.fetchone():
                connection.rollback()
                return False

            cursor.execute("""
                SELECT COALESCE(MAX(nomor_antrian), 0) + 1 AS nomor_baru
                FROM kunjungan
                WHERE id_poli = %s AND tanggal_kunjungan = %s
            """, (id_poli, tanggal_kunjungan))

            nomor = cursor.fetchone()["nomor_baru"]

            cursor.execute("""
                INSERT INTO kunjungan
                (id_pasien, id_poli, id_dokter, nomor_antrian,
                 tanggal_kunjungan, keluhan_awal, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Menunggu')
            """, (
                id_pasien, id_poli, id_dokter, nomor,
                tanggal_kunjungan, keluhan_awal
            ))

            id_kunjungan = cursor.lastrowid
            connection.commit()

            return {
                "id_kunjungan": id_kunjungan,
                "nomor_antrian": nomor
            }

        except Exception as e:
            print(f"Error menyimpan kunjungan: {e}")
            connection.rollback()
            return False
        finally:
            self._tutup(connection, cursor)

    def get_active_by_user_id(self, id_user):
        connection, cursor = self._koneksi()
        if not connection:
            return None

        try:
            cursor.execute("""
                SELECT k.id_kunjungan, k.nomor_antrian,
                       k.tanggal_kunjungan, k.keluhan_awal,
                       k.status, po.nama_poli, d.nama_dokter
                FROM kunjungan k
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN poli po ON k.id_poli = po.id_poli
                LEFT JOIN dokter d ON k.id_dokter = d.id_dokter
                WHERE p.id_user = %s AND k.status <> 'Selesai'
                ORDER BY k.id_kunjungan DESC
                LIMIT 1
            """, (id_user,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error mengambil antrean aktif: {e}")
            return None
        finally:
            self._tutup(connection, cursor)

    def get_antrean_dokter(self, id_user):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT k.id_kunjungan, k.nomor_antrian,
                       k.tanggal_kunjungan, k.keluhan_awal,
                       k.status, p.nama_pasien, po.nama_poli
                FROM kunjungan k
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN poli po ON k.id_poli = po.id_poli
                JOIN dokter d ON k.id_poli = d.id_poli
                WHERE d.id_user = %s
                  AND k.tanggal_kunjungan = CURDATE()
                  AND k.status <> 'Selesai'
                  AND (k.id_dokter IS NULL OR k.id_dokter = d.id_dokter)
                ORDER BY k.nomor_antrian
            """, (id_user,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error mengambil antrean dokter: {e}")
            return []
        finally:
            self._tutup(connection, cursor)

    def panggil_pasien(self, id_kunjungan, id_user):
        connection, cursor = self._koneksi(False)
        if not connection:
            return False

        try:
            cursor.execute("""
                UPDATE kunjungan k
                JOIN dokter d ON d.id_user = %s
                SET k.id_dokter = d.id_dokter, k.status = 'Dipanggil'
                WHERE k.id_kunjungan = %s
                  AND k.id_poli = d.id_poli
                  AND k.tanggal_kunjungan = CURDATE()
                  AND k.status = 'Menunggu'
                  AND (k.id_dokter IS NULL OR k.id_dokter = d.id_dokter)
            """, (id_user, id_kunjungan))

            berhasil = cursor.rowcount == 1
            connection.commit()
            return berhasil
        except Exception as e:
            print(f"Error memanggil pasien: {e}")
            connection.rollback()
            return False
        finally:
            self._tutup(connection, cursor)

    def mulai_pemeriksaan(self, id_kunjungan, id_user):
        connection, cursor = self._koneksi()
        if not connection:
            return None

        try:
            cursor.execute("""
                SELECT k.id_kunjungan, k.nomor_antrian,
                       k.tanggal_kunjungan, k.keluhan_awal, k.status,
                       p.id_pasien, p.nama_pasien, p.jenis_kelamin,
                       p.tanggal_lahir, p.alamat, po.nama_poli,
                       d.nama_dokter, pk.alergi, pk.penyakit_bawaan,
                       pk.riwayat_penyakit, pk.catatan_kesehatan,
                       pk.sumber_data, pk.tanggal_sinkronisasi
                FROM kunjungan k
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN poli po ON k.id_poli = po.id_poli
                JOIN dokter d ON k.id_dokter = d.id_dokter
                LEFT JOIN profil_kesehatan pk
                    ON p.id_pasien = pk.id_pasien
                WHERE k.id_kunjungan = %s
                  AND d.id_user = %s
                  AND k.status IN ('Dipanggil', 'Diperiksa')
                LIMIT 1
            """, (id_kunjungan, id_user))

            data = cursor.fetchone()
            if not data:
                connection.rollback()
                return None

            if data["status"] == "Dipanggil":
                cursor.execute("""
                    UPDATE kunjungan
                    SET status = 'Diperiksa'
                    WHERE id_kunjungan = %s
                      AND status = 'Dipanggil'
                """, (id_kunjungan,))

                if cursor.rowcount != 1:
                    connection.rollback()
                    return None

                data["status"] = "Diperiksa"
                connection.commit()

            return data

        except Exception as e:
            print(f"Error memulai pemeriksaan: {e}")
            connection.rollback()
            return None
        finally:
            self._tutup(connection, cursor)