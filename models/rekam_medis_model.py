from config.database import Database

class RekamMedisModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "rekam_medis"

    def get_all_rekam_medis(self):
        """Mengambil data rekam medis dengan JOIN ke tabel kunjungan dan pasien"""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
                SELECT rm.id_rekam_medis, rm.id_kunjungan, rm.tekanan_darah, 
                       rm.suhu_tubuh, rm.berat_badan, rm.diagnosis, rm.catatan, 
                       rm.tanggal_pemeriksaan, 
                       p.nama_pasien AS nama_pasien
                FROM {self.table_name} rm
                JOIN kunjungan k ON rm.id_kunjungan = k.id_kunjungan
                JOIN pasien p ON k.id_pasien = p.id_pasien
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_rekam_medis(self, id_kunjungan, diagnosa, tindakan, catatan_dokter):
        """Menyimpan hasil rekam medis baru ke database"""
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (id_kunjungan, diagnosa, tindakan, catatan_dokter) VALUES (%s, %s, %s, %s)"
            val = (id_kunjungan, diagnosa, tindakan, catatan_dokter)
            try:
                cursor.execute(query, val)
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error: {e}")
                self.conn.rollback()
                cursor.close()
                return False
        return False