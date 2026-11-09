
from models.resep_model import ResepModel
from controllers.obat_controller import ObatController


class AdminController:

    def __init__(self):
        self.resep_model = ResepModel()

    # DASHBOARD
    def get_dashboard_data(self):
        antrean = self.get_antrean_resep()
        obat = self.get_data_obat()
        riwayat = self.get_riwayat_penyerahan()

        jumlah_antrean = len(
            set(item["id_kunjungan"] for item in antrean)
        )

        return {
            "jumlah_antrean": jumlah_antrean,
            "jumlah_obat": len(obat),
            "jumlah_riwayat": len(riwayat)
        }

    # ANTREAN RESEP
    def get_antrean_resep(self):
        return self.resep_model.get_antrean_resep()

    def serahkan_obat(self, id_kunjungan, id_user):
        return self.resep_model.serahkan_obat(
            id_kunjungan, id_user
        )

    # CRUD OBAT
    def get_data_obat(self):
        return ObatController.get_all_obat()

    def tambah_obat(self, nama, jenis, satuan, stok):
        return ObatController.tambah_obat(
            nama, jenis, satuan, stok
        )

    def update_obat(self, id_obat, nama, jenis, satuan, stok):
        return ObatController.update_obat(
            id_obat, nama, jenis, satuan, stok
        )

    def hapus_obat(self, id_obat):
        return ObatController.hapus_obat(id_obat)

    def cari_obat(self, keyword):
        return ObatController.cari_obat(keyword)

    # RIWAYAT PENYERAHAN
    def get_riwayat_penyerahan(self):
        return self.resep_model.get_riwayat_penyerahan()
