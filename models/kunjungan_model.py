from config.database import Database

class KunjunganModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "kunjungan"

    def get_all_kunjungan(self):
        """Mengambil data kunjungan lengkap dengan JOIN ke tabel pasien, poli, dan dokter"""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
                SELECT k.id_kunjungan, k.tanggal_kunjungan, k.nomor_antrian, k.keluhan_awal, 
                       p.nama_pasien AS nama_pasien, 
                       po.nama_poli AS nama_poli, 
                       d.nama_dokter AS nama_dokter 
                FROM {self.table_name} k
                JOIN pasien p ON k.id_pasien = p.id_pasien
                JOIN poli po ON k.id_poli = po.id_poli
                LEFT JOIN dokter d ON k.id_dokter = d.id_dokter
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_kunjungan(self, id_pasien, id_poli, id_dokter, nomor_antrian, tanggal_kunjungan, keluhan_awal):
        """Menambahkan data kunjungan baru ke database"""
        if self.conn:
            cursor = self.conn.cursor()
            query = f"""
                INSERT INTO {self.table_name} 
                (id_pasien, id_poli, id_dokter, nomor_antrian, tanggal_kunjungan, keluhan_awal) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (id_pasien, id_poli, id_dokter, nomor_antrian, tanggal_kunjungan, keluhan_awal)
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