
from config.database import Database


class ResepModel:

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

    def get_antrean_resep(self):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT r.id_resep, k.id_kunjungan, k.nomor_antrian,
                       p.nama_pasien, d.nama_dokter, o.nama_obat,
                       o.satuan, r.dosis, r.jumlah, r.aturan_pakai,
                       rm.diagnosis, r.status_penyerahan
                FROM resep r
                JOIN rekam_medis rm ON r.id_rekam_medis = rm.id_rekam_medis
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p ON k.id_pasien = p.id_pasien
                LEFT JOIN dokter d ON k.id_dokter = d.id_dokter
                JOIN obat o ON r.id_obat = o.id_obat
                WHERE k.status = 'Menunggu Obat'
                  AND r.status_penyerahan = 'Menunggu'
                ORDER BY k.waktu_daftar, r.id_resep
            """)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error antrean resep: {e}")
            return []

        finally:
            self._tutup(connection, cursor)

    def get_riwayat_penyerahan(self):
        connection, cursor = self._koneksi()
        if not connection:
            return []

        try:
            cursor.execute("""
                SELECT r.id_resep, k.id_kunjungan, k.nomor_antrian,
                       p.nama_pasien, d.nama_dokter, o.nama_obat,
                       o.satuan, r.dosis, r.jumlah, r.aturan_pakai,
                       k.waktu_selesai, u.username AS nama_petugas
                FROM resep r
                JOIN rekam_medis rm ON r.id_rekam_medis = rm.id_rekam_medis
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p ON k.id_pasien = p.id_pasien
                LEFT JOIN dokter d ON k.id_dokter = d.id_dokter
                JOIN obat o ON r.id_obat = o.id_obat
                LEFT JOIN users u ON k.id_petugas_selesai = u.id_user
                WHERE r.status_penyerahan = 'Diserahkan'
                ORDER BY k.waktu_selesai DESC, r.id_resep DESC
            """)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error riwayat penyerahan: {e}")
            return []

        finally:
            self._tutup(connection, cursor)

    def serahkan_obat(self, id_kunjungan, id_user):
        connection, cursor = self._koneksi()
        if not connection:
            return False, "Koneksi database gagal."

        try:
            connection.start_transaction()

            cursor.execute("""
                SELECT id_kunjungan FROM kunjungan
                WHERE id_kunjungan = %s AND status = 'Menunggu Obat'
                FOR UPDATE
            """, (id_kunjungan,))

            if not cursor.fetchone():
                raise ValueError("Antrean sudah tidak menunggu obat.")

            cursor.execute("""
                SELECT r.id_obat, r.jumlah, r.status_penyerahan
                FROM resep r
                JOIN rekam_medis rm ON r.id_rekam_medis = rm.id_rekam_medis
                WHERE rm.id_kunjungan = %s
                FOR UPDATE
            """, (id_kunjungan,))

            resep = cursor.fetchall()

            if not resep:
                raise ValueError("Resep tidak ditemukan.")

            if any(r["status_penyerahan"] != "Menunggu" for r in resep):
                raise ValueError("Status resep sudah berubah.")

            kebutuhan = {}
            for r in resep:
                id_obat = r["id_obat"]
                kebutuhan[id_obat] = kebutuhan.get(id_obat, 0) + r["jumlah"]

            for id_obat, jumlah in kebutuhan.items():
                cursor.execute("""
                    SELECT nama_obat, stok FROM obat
                    WHERE id_obat = %s FOR UPDATE
                """, (id_obat,))

                obat = cursor.fetchone()

                if not obat:
                    raise ValueError("Data obat tidak ditemukan.")

                if obat["stok"] < jumlah:
                    raise ValueError(
                        f"Stok {obat['nama_obat']} tidak mencukupi. "
                        f"Tersedia {obat['stok']}, dibutuhkan {jumlah}."
                    )

            for id_obat, jumlah in kebutuhan.items():
                cursor.execute("""
                    UPDATE obat SET stok = stok - %s
                    WHERE id_obat = %s AND stok >= %s
                """, (jumlah, id_obat, jumlah))

                if cursor.rowcount != 1:
                    raise ValueError("Gagal memperbarui stok.")

            cursor.execute("""
                UPDATE resep r
                JOIN rekam_medis rm ON r.id_rekam_medis = rm.id_rekam_medis
                SET r.status_penyerahan = 'Diserahkan'
                WHERE rm.id_kunjungan = %s
                  AND r.status_penyerahan = 'Menunggu'
            """, (id_kunjungan,))

            if cursor.rowcount != len(resep):
                raise ValueError("Gagal memperbarui status resep.")

            cursor.execute("""
                UPDATE kunjungan
                SET status = 'Selesai',
                    id_petugas_selesai = %s,
                    waktu_selesai = NOW()
                WHERE id_kunjungan = %s
                  AND status = 'Menunggu Obat'
            """, (id_user, id_kunjungan))

            if cursor.rowcount != 1:
                raise ValueError("Gagal menyelesaikan kunjungan.")

            connection.commit()
            return True, "Obat berhasil diserahkan. Kunjungan selesai."

        except Exception as e:
            connection.rollback()
            print(f"Error penyerahan obat: {e}")

            pesan = str(e)
            if not isinstance(e, ValueError):
                pesan = f"Penyerahan obat gagal: {pesan}"

            return False, pesan

        finally:
            self._tutup(connection, cursor)
