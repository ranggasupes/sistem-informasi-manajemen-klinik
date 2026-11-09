
from config.database import Database


class RekamMedisModel:

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

    def get_all_rekam_medis(self):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT rm.*, p.nama_pasien
                FROM rekam_medis rm
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p ON k.id_pasien = p.id_pasien
                ORDER BY rm.tanggal_pemeriksaan DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error mengambil rekam medis: {e}")
            return []
        finally:
            self._tutup(connection, cursor)

    def create_rekam_medis(
        self, id_kunjungan, tekanan_darah, suhu_tubuh,
        berat_badan, diagnosis, catatan
    ):
        connection, cursor = self._koneksi(False)
        if not connection:
            return False

        try:
            cursor.execute("""
                INSERT INTO rekam_medis
                (id_kunjungan, tekanan_darah, suhu_tubuh,
                 berat_badan, diagnosis, catatan)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_kunjungan, tekanan_darah or None,
                suhu_tubuh or None, berat_badan or None,
                diagnosis, catatan or None
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error menyimpan rekam medis: {e}")
            connection.rollback()
            return False
        finally:
            self._tutup(connection, cursor)

    def get_history_by_user_id(self, id_user):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT rm.*, k.nomor_antrian, k.tanggal_kunjungan,
                       po.nama_poli, d.nama_dokter
                FROM rekam_medis rm
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN poli po ON k.id_poli = po.id_poli
                LEFT JOIN dokter d ON k.id_dokter = d.id_dokter
                WHERE p.id_user = %s
                ORDER BY rm.tanggal_pemeriksaan DESC
            """, (id_user,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error mengambil riwayat pasien: {e}")
            return []
        finally:
            self._tutup(connection, cursor)

    def create_rekam_medis_dokter(
        self, id_kunjungan, id_user, tekanan_darah,
        suhu_tubuh, berat_badan, diagnosis, catatan
    ):
        connection, cursor = self._koneksi()
        if not connection:
            return None

        try:
            cursor.execute("""
                SELECT k.id_kunjungan
                FROM kunjungan k
                JOIN dokter d ON k.id_dokter = d.id_dokter
                WHERE k.id_kunjungan = %s
                  AND d.id_user = %s
                  AND k.status = 'Diperiksa'
                FOR UPDATE
            """, (id_kunjungan, id_user))

            if not cursor.fetchone():
                connection.rollback()
                return None

            cursor.execute("""
                INSERT INTO rekam_medis
                (id_kunjungan, tekanan_darah, suhu_tubuh,
                 berat_badan, diagnosis, catatan)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_kunjungan, tekanan_darah or None,
                suhu_tubuh or None, berat_badan or None,
                diagnosis, catatan or None
            ))

            id_rekam_medis = cursor.lastrowid
            connection.commit()
            return id_rekam_medis

        except Exception as e:
            print(f"Error menyimpan pemeriksaan: {e}")
            connection.rollback()
            return None
        finally:
            self._tutup(connection, cursor)

    def create_resep_dokter(self, id_rekam_medis, id_user, daftar_resep):
        connection, cursor = self._koneksi()
        if not connection:
            return False

        try:
            if not daftar_resep:
                return False

            cursor.execute("""
                SELECT rm.id_rekam_medis, k.id_kunjungan
                FROM rekam_medis rm
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN dokter d ON k.id_dokter = d.id_dokter
                WHERE rm.id_rekam_medis = %s
                  AND d.id_user = %s
                  AND k.status = 'Diperiksa'
                FOR UPDATE
            """, (id_rekam_medis, id_user))

            rekam_medis = cursor.fetchone()
            if not rekam_medis:
                connection.rollback()
                return False

            obat_dipilih = set()

            for resep in daftar_resep:
                id_obat = int(resep["id_obat"])
                jumlah = int(resep["jumlah"])
                dosis = resep["dosis"].strip()
                aturan = resep["aturan_pakai"].strip()

                if jumlah <= 0 or not dosis or not aturan:
                    raise ValueError("Data resep belum lengkap.")

                if id_obat in obat_dipilih:
                    raise ValueError("Obat tidak boleh duplikat.")
                obat_dipilih.add(id_obat)

                cursor.execute("""
                    SELECT stok FROM obat
                    WHERE id_obat = %s FOR UPDATE
                """, (id_obat,))
                obat = cursor.fetchone()

                if not obat or jumlah > obat["stok"]:
                    raise ValueError("Obat tidak ditemukan atau stok kurang.")

                cursor.execute("""
                    INSERT INTO resep
                    (id_rekam_medis, id_obat, dosis, jumlah,
                     aturan_pakai, status_penyerahan)
                    VALUES (%s, %s, %s, %s, %s, 'Menunggu')
                """, (id_rekam_medis, id_obat, dosis, jumlah, aturan))

            cursor.execute("""
                UPDATE kunjungan
                SET status = 'Menunggu Obat'
                WHERE id_kunjungan = %s AND status = 'Diperiksa'
            """, (rekam_medis["id_kunjungan"],))

            if cursor.rowcount != 1:
                raise ValueError("Status kunjungan gagal diperbarui.")

            connection.commit()
            return True

        except Exception as e:
            print(f"Error menyimpan resep: {e}")
            connection.rollback()
            return False
        finally:
            self._tutup(connection, cursor)

    def selesaikan_tanpa_resep(self, id_rekam_medis, id_user):
        connection, cursor = self._koneksi(False)
        if not connection:
            return False

        try:
            cursor.execute("""
                UPDATE kunjungan k
                JOIN rekam_medis rm ON k.id_kunjungan = rm.id_kunjungan
                JOIN dokter d ON k.id_dokter = d.id_dokter
                SET k.status = 'Selesai'
                WHERE rm.id_rekam_medis = %s
                  AND d.id_user = %s
                  AND k.status = 'Diperiksa'
                  AND NOT EXISTS (
                      SELECT 1 FROM resep r
                      WHERE r.id_rekam_medis = rm.id_rekam_medis
                  )
            """, (id_rekam_medis, id_user))

            berhasil = cursor.rowcount == 1
            connection.commit()
            return berhasil

        except Exception as e:
            print(f"Error menyelesaikan kunjungan: {e}")
            connection.rollback()
            return False
        finally:
            self._tutup(connection, cursor)

    def get_history_by_doctor_id(self, id_user):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT rm.*, k.nomor_antrian, k.tanggal_kunjungan,
                       k.status, p.nama_pasien, po.nama_poli
                FROM rekam_medis rm
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN dokter d ON k.id_dokter = d.id_dokter
                JOIN poli po ON k.id_poli = po.id_poli
                WHERE d.id_user = %s
                ORDER BY rm.tanggal_pemeriksaan DESC
            """, (id_user,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error mengambil riwayat dokter: {e}")
            return []
        finally:
            self._tutup(connection, cursor)
