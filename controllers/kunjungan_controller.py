
from datetime import datetime

from models.kunjungan_model import KunjunganModel
from views.kunjungan_view import KunjunganView


class KunjunganController:

    def __init__(self):
        self.model = KunjunganModel()
        self.view = KunjunganView()

        self.view.btn_simpan.configure(
            command=self.tambah_kunjungan
        )

        self.load_data()

    def load_data(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_kunjungan = self.model.get_all_kunjungan()

        for row in data_kunjungan:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    row["id_kunjungan"],
                    row["tanggal_kunjungan"],
                    row["nomor_antrian"],
                    row["nama_pasien"],
                    row["nama_poli"],
                    row["nama_dokter"] or "-",
                    row["keluhan_awal"] or "-",
                    row["status"]
                )
            )

    def tambah_kunjungan(self):
        id_pasien = self.view.entry_id_pasien.get().strip()
        id_poli = self.view.entry_id_poli.get().strip()
        id_dokter = self.view.entry_id_dokter.get().strip()
        tanggal = self.view.entry_tanggal.get().strip()
        keluhan_awal = self.view.entry_keluhan.get().strip()

        if not id_pasien or not id_poli or not tanggal:
            print("ID pasien, ID poli, dan tanggal wajib diisi.")
            return

        try:
            id_pasien = int(id_pasien)
            id_poli = int(id_poli)

            if id_dokter:
                id_dokter = int(id_dokter)
            else:
                id_dokter = None

            datetime.strptime(tanggal, "%Y-%m-%d")

        except ValueError:
            print("Periksa kembali ID dan format tanggal (YYYY-MM-DD).")
            return

        sukses = self.model.create_kunjungan(
            id_pasien,
            id_poli,
            id_dokter,
            tanggal,
            keluhan_awal
        )

        if sukses:
            print("Data kunjungan berhasil disimpan.")

            self.view.entry_id_pasien.delete(0, "end")
            self.view.entry_id_poli.delete(0, "end")
            self.view.entry_id_dokter.delete(0, "end")
            self.view.entry_tanggal.delete(0, "end")
            self.view.entry_keluhan.delete(0, "end")

            self.load_data()

        else:
            print("Gagal menyimpan data kunjungan.")

    def run(self):
        self.view.mainloop()
