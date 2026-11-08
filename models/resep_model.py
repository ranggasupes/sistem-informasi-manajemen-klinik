
from config.database import Database


class ResepModel:

    def get_antrean_resep(self):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    r.id_resep,
                    k.id_kunjungan,
                    k.nomor_antrian,
                    p.nama_pasien,
                    d.nama_dokter,
                    o.nama_obat,
                    o.satuan,
                    r.dosis,
                    r.jumlah,
                    r.aturan_pakai,
                    rm.diagnosis,
                    r.status_penyerahan
                FROM resep r
                JOIN rekam_medis rm
                    ON r.id_rekam_medis = rm.id_rekam_medis
                JOIN kunjungan k
                    ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p
                    ON k.id_pasien = p.id_pasien
                LEFT JOIN dokter d
                    ON k.id_dokter = d.id_dokter
                JOIN obat o
                    ON r.id_obat = o.id_obat
                WHERE
                    k.status = 'Menunggu Obat'
                    AND r.status_penyerahan = 'Menunggu'
                ORDER BY k.waktu_daftar ASC, r.id_resep ASC
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil antrean resep: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def get_riwayat_penyerahan(self):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    r.id_resep,
                    k.id_kunjungan,
                    k.nomor_antrian,
                    p.nama_pasien,
                    d.nama_dokter,
                    o.nama_obat,
                    o.satuan,
                    r.dosis,
                    r.jumlah,
                    r.aturan_pakai,
                    k.waktu_selesai,
                    u.username AS nama_petugas
                FROM resep r
                JOIN rekam_medis rm
                    ON r.id_rekam_medis = rm.id_rekam_medis
                JOIN kunjungan k
                    ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p
                    ON k.id_pasien = p.id_pasien
                LEFT JOIN dokter d
                    ON k.id_dokter = d.id_dokter
                JOIN obat o
                    ON r.id_obat = o.id_obat
                LEFT JOIN users u
                    ON k.id_petugas_selesai = u.id_user
                WHERE r.status_penyerahan = 'Diserahkan'
                ORDER BY k.waktu_selesai DESC, r.id_resep DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil riwayat penyerahan: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def serahkan_obat(self, id_kunjungan, id_user):
        connection = Database.get_connection()

        if connection is None:
            return False, "Koneksi database gagal."

        cursor = None

        try:
            connection.start_transaction()
            cursor = connection.cursor(dictionary=True)

            # 1. Pastikan kunjungan masih menunggu obat.
            cursor.execute(
                """
                SELECT id_kunjungan
                FROM kunjungan
                WHERE id_kunjungan = %s
                  AND status = 'Menunggu Obat'
                FOR UPDATE
                """,
                (id_kunjungan,)
            )

            kunjungan = cursor.fetchone()

            if not kunjungan:
                connection.rollback()
                return False, "Antrean ini sudah tidak menunggu obat."

            # 2. Ambil seluruh resep dalam kunjungan.
            cursor.execute(
                """
                SELECT
                    r.id_resep,
                    r.id_obat,
                    r.jumlah,
                    r.status_penyerahan
                FROM resep r
                JOIN rekam_medis rm
                    ON r.id_rekam_medis = rm.id_rekam_medis
                WHERE rm.id_kunjungan = %s
                FOR UPDATE
                """,
                (id_kunjungan,)
            )

            daftar_resep = cursor.fetchall()

            if not daftar_resep:
                connection.rollback()
                return False, "Resep tidak ditemukan."

            if any(
                resep["status_penyerahan"] != "Menunggu"
                for resep in daftar_resep
            ):
                connection.rollback()
                return False, "Status resep sudah berubah."

            # 3. Hitung total kebutuhan setiap obat.
            kebutuhan_obat = {}

            for resep in daftar_resep:
                id_obat = resep["id_obat"]
                jumlah = resep["jumlah"]

                kebutuhan_obat[id_obat] = (
                    kebutuhan_obat.get(id_obat, 0) + jumlah
                )

            # 4. Periksa dan kunci stok setiap obat.
            for id_obat, jumlah in kebutuhan_obat.items():

                cursor.execute(
                    """
                    SELECT nama_obat, stok
                    FROM obat
                    WHERE id_obat = %s
                    FOR UPDATE
                    """,
                    (id_obat,)
                )

                obat = cursor.fetchone()

                if not obat:
                    connection.rollback()
                    return False, "Data obat tidak ditemukan."

                if obat["stok"] < jumlah:
                    connection.rollback()
                    return False, (
                        f"Stok {obat['nama_obat']} tidak mencukupi. "
                        f"Stok tersedia: {obat['stok']}, "
                        f"kebutuhan: {jumlah}."
                    )

            # 5. Kurangi stok setelah semua obat lolos pemeriksaan.
            for id_obat, jumlah in kebutuhan_obat.items():

                cursor.execute(
                    """
                    UPDATE obat
                    SET stok = stok - %s
                    WHERE id_obat = %s
                      AND stok >= %s
                    """,
                    (jumlah, id_obat, jumlah)
                )

                if cursor.rowcount != 1:
                    raise Exception("Gagal memperbarui stok obat.")

            # 6. Tandai seluruh resep sebagai diserahkan.
            cursor.execute(
                """
                UPDATE resep r
                JOIN rekam_medis rm
                    ON r.id_rekam_medis = rm.id_rekam_medis
                SET r.status_penyerahan = 'Diserahkan'
                WHERE rm.id_kunjungan = %s
                  AND r.status_penyerahan = 'Menunggu'
                """,
                (id_kunjungan,)
            )

            if cursor.rowcount != len(daftar_resep):
                raise Exception("Gagal memperbarui status resep.")

            # 7. Selesaikan kunjungan dan catat petugas.
            cursor.execute(
                """
                UPDATE kunjungan
                SET
                    status = 'Selesai',
                    id_petugas_selesai = %s,
                    waktu_selesai = NOW()
                WHERE id_kunjungan = %s
                  AND status = 'Menunggu Obat'
                """,
                (id_user, id_kunjungan)
            )

            if cursor.rowcount != 1:
                raise Exception("Gagal menyelesaikan kunjungan.")

            connection.commit()

            return True, "Obat berhasil diserahkan. Kunjungan selesai."

        except Exception as e:
            connection.rollback()
            print(f"Error penyerahan obat: {e}")
            return False, f"Penyerahan obat gagal: {e}"

        finally:
            if cursor:
                cursor.close()
            connection.close()
