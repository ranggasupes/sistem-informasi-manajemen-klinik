from datetime import date

from models.pasien_model import PasienModel
from models.profil_kesehatan_model import ProfilKesehatanModel
from models.kunjungan_model import KunjunganModel
from models.rekam_medis_model import RekamMedisModel


class PasienDashboardController:

    def __init__(self):
        self.pasien_model = PasienModel()
        self.profil_model = ProfilKesehatanModel()
        self.kunjungan_model = KunjunganModel()
        self.rekam_medis_model = RekamMedisModel()

    def get_dashboard_data(self, id_user):
        pasien = self.pasien_model.get_pasien_by_user_id(id_user)

        if pasien is None:
            return None, None

        profil = self.profil_model.get_by_pasien_id(
            pasien["id_pasien"]
        )

        return pasien, profil

    def get_antrean_aktif(self, id_user):
        return self.kunjungan_model.get_active_by_user_id(id_user)

    def get_riwayat_medis(self, id_user):
        return self.rekam_medis_model.get_history_by_user_id(id_user)

    def tentukan_poli(self, tanggal_lahir):
        if not tanggal_lahir:
            return None, "Tanggal lahir pasien belum tersedia."

        hari_ini = date.today()

        umur = hari_ini.year - tanggal_lahir.year

        if (hari_ini.month, hari_ini.day) < (
            tanggal_lahir.month,
            tanggal_lahir.day
        ):
            umur -= 1

        if umur < 0:
            return None, "Tanggal lahir tidak valid."

        if umur < 18:
            return 1, "Poli Anak"

        elif umur < 60:
            return 2, "Poli Umum"

        return 3, "Poli Lansia"

    def daftar_kunjungan(self, id_user, keluhan_awal):
        pasien = self.pasien_model.get_pasien_by_user_id(id_user)

        if pasien is None:
            return False, "Data pasien tidak ditemukan.", None

        if not keluhan_awal.strip():
            return False, "Keluhan awal harus diisi.", None

        id_poli, nama_poli = self.tentukan_poli(
            pasien["tanggal_lahir"]
        )

        if id_poli is None:
            return False, nama_poli, None

        kunjungan_aktif = self.kunjungan_model.get_active_by_user_id(
            id_user
        )

        if kunjungan_aktif:
            return (
                False,
                "Anda masih memiliki kunjungan aktif. Selesaikan kunjungan sebelumnya terlebih dahulu.",
                kunjungan_aktif
            )

        tanggal_kunjungan = date.today()

        hasil = self.kunjungan_model.create_kunjungan(
            id_pasien=pasien["id_pasien"],
            id_poli=id_poli,
            id_dokter=None,
            tanggal_kunjungan=tanggal_kunjungan,
            keluhan_awal=keluhan_awal.strip()
        )

        if not hasil:
            return (
                False,
                "Pendaftaran gagal. Silakan periksa koneksi atau coba kembali.",
                None
            )

        hasil["nama_poli"] = nama_poli
        hasil["tanggal_kunjungan"] = tanggal_kunjungan
        hasil["status"] = "Menunggu"

        return True, "Pendaftaran kunjungan berhasil.", hasil