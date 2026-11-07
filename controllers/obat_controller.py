from models.obat_model import ObatModel


class ObatController:
    @staticmethod
    def get_all_obat():
        """Mengambil seluruh data obat"""
        return ObatModel.get_all_obat()

    @staticmethod
    def tambah_obat(*args, **kwargs):
        """Menambahkan data obat baru"""
        return ObatModel.tambah_obat(*args, **kwargs)

    @staticmethod
    def update_obat(*args, **kwargs):
        """Memperbarui data obat"""
        return ObatModel.update_obat(*args, **kwargs)

    @staticmethod
    def hapus_obat(id_obat):
        """Menghapus data obat berdasarkan ID"""
        return ObatModel.hapus_obat(id_obat)

    @staticmethod
    def cari_obat(keyword):
        """Mencari data obat berdasarkan kata kunci"""
        return ObatModel.cari_obat(keyword)

  