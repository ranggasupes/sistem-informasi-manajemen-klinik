from models.resep_model import ResepModel


class ResepController:
    @staticmethod
    def get_all_resep():
        return ResepModel.get_all_resep()

    @staticmethod
    def tambah_resep(id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan="Menunggu"):
        return ResepModel.tambah_resep(id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan)

    @staticmethod
    def update_resep(id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan):
        return ResepModel.update_resep(id_resep, id_rekam_medis, id_obat, dosis, jumlah, aturan_pakai, status_penyerahan)

    @staticmethod
    def hapus_resep(id_resep):
        return ResepModel.hapus_resep(id_resep)

    @staticmethod
    def cari_resep(keyword):
        return ResepModel.cari_resep(keyword)


