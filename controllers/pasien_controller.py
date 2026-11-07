from models.pasien_model import PasienModel

class PasienController:
    def __init__(self):
        self.model = PasienModel()

    def daftar_pasien(self):
        return self.model.get_all_pasien()

    def simpan_pasien(self, nama, nik, alamat, no_telp):
        if not nama or not nik:
            return False, "Nama dan NIK wajib diisi!"
        
        success = self.model.tambah_pasien(nama, nik, alamat, no_telp)
        if success:
            return True, "Data pasien berhasil disimpan."
        return False, "Gagal menyimpan data ke database."