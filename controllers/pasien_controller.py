
from models.pasien_model import PasienModel
from views.pasien_view import PasienView


class PasienController:

    def __init__(self):
        self.model = PasienModel()
        self.view = PasienView()

        self.view.btn_simpan.configure(
            command=self.tambah_pasien
        )

        self.load_data()

    def daftar_pasien(self):
        return self.model.get_all_pasien()

    def simpan_pasien(self, id_user, nomor_bpjs, nik,
                      nama_pasien, jenis_kelamin, tanggal_lahir,
                      alamat, no_telepon):

        if not id_user or not nik or not nama_pasien:
            return False, "ID User, NIK, dan nama pasien wajib diisi."

        try:
            id_user = int(id_user)
        except ValueError:
            return False, "ID User harus berupa angka."

        success = self.model.create_pasien(
            id_user,
            nomor_bpjs,
            nik,
            nama_pasien,
            jenis_kelamin,
            tanggal_lahir,
            alamat,
            no_telepon
        )

        if success:
            return True, "Data pasien berhasil disimpan."

        return False, "Gagal menyimpan data pasien."

    def load_data(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_pasien = self.daftar_pasien()

        for row in data_pasien:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    row["id_pasien"],
                    row["nama_pasien"],
                    row["nik"],
                    row["alamat"],
                    row["no_telepon"]
                )
            )

    def tambah_pasien(self):
        id_user = self.view.entry_id_user.get()
        nomor_bpjs = self.view.entry_nomor_bpjs.get()
        nik = self.view.entry_nik.get()
        nama_pasien = self.view.entry_nama.get()
        jenis_kelamin = self.view.entry_jenis_kelamin.get()
        tanggal_lahir = self.view.entry_tanggal_lahir.get()
        alamat = self.view.entry_alamat.get()
        no_telepon = self.view.entry_telepon.get()

        if not all([
            id_user,
            nik,
            nama_pasien,
            tanggal_lahir
        ]):
            print("ID User, NIK, nama, dan tanggal lahir wajib diisi.")
            return

        sukses, pesan = self.simpan_pasien(
            id_user,
            nomor_bpjs,
            nik,
            nama_pasien,
            jenis_kelamin,
            tanggal_lahir,
            alamat,
            no_telepon
        )

        print(pesan)

        if sukses:
            self.view.entry_id_user.delete(0, "end")
            self.view.entry_nomor_bpjs.delete(0, "end")
            self.view.entry_nik.delete(0, "end")
            self.view.entry_nama.delete(0, "end")
            self.view.entry_jenis_kelamin.set("")
            self.view.entry_tanggal_lahir.delete(0, "end")
            self.view.entry_alamat.delete(0, "end")
            self.view.entry_telepon.delete(0, "end")

            self.load_data()

    def run(self):
        self.view.mainloop()
