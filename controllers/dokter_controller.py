
from models.dokter_model import DokterModel
from models.kunjungan_model import KunjunganModel
from models.rekam_medis_model import RekamMedisModel
from controllers.obat_controller import ObatController


class DokterController:
    def __init__(self):
        self.dokter = DokterModel()
        self.kunjungan = KunjunganModel()
        self.rekam_medis = RekamMedisModel()

    def daftar_dokter(self):
        return self.dokter.get_all_dokter()

    def get_antrean(self, id_user):
        return self.kunjungan.get_antrean_dokter(id_user)

    def panggil_pasien(self, id_kunjungan, id_user):
        return self.kunjungan.panggil_pasien(id_kunjungan, id_user)

    def mulai_pemeriksaan(self, id_kunjungan, id_user):
        return self.kunjungan.mulai_pemeriksaan(id_kunjungan, id_user)

    def get_daftar_obat(self):
        return ObatController.get_all_obat()

    def simpan_pemeriksaan(self, data, id_user):
        return self.rekam_medis.create_rekam_medis_dokter(
            data["id_kunjungan"], id_user,
            data["tekanan_darah"], data["suhu_tubuh"],
            data["berat_badan"], data["diagnosis"], data["catatan"]
        )

    def simpan_resep(self, id_rekam_medis, id_user, daftar_resep):
        return self.rekam_medis.create_resep_dokter(
            id_rekam_medis, id_user, daftar_resep
        )

    def selesaikan_tanpa_resep(self, id_rekam_medis, id_user):
        return self.rekam_medis.selesaikan_tanpa_resep(
            id_rekam_medis, id_user
        )

    def get_riwayat(self, id_user):
        return self.rekam_medis.get_history_by_doctor_id(id_user)
