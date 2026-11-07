from models.obat_model import ObatModel


class ObatController:
    @staticmethod
    def get_all_obat():
        return ObatModel.get_all_obat()

    @staticmethod
    def tambah_obat(nama_obat, jenis_obat, satuan, stok):
        return ObatModel.tambah_obat(nama_obat, jenis_obat, satuan, stok)

    @staticmethod
    def update_obat(id_obat, nama_obat, jenis_obat, satuan, stok):
        return ObatModel.update_obat(id_obat, nama_obat, jenis_obat, satuan, stok)

    @staticmethod
    def hapus_obat(id_obat):
        return ObatModel.hapus_obat(id_obat)

    @staticmethod
    def cari_obat(keyword):
        return ObatModel.cari_obat(keyword)

