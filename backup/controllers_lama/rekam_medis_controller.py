
from models.rekam_medis_model import RekamMedisModel
from views.rekam_medis_view import RekamMedisView


class RekamMedisController:

    def __init__(self):
        self.model = RekamMedisModel()
        self.view = RekamMedisView()

        self.view.btn_simpan.configure(
            command=self.tambah_rekam_medis
        )

        self.load_data()

    def load_data(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_rm = self.model.get_all_rekam_medis()

        for row in data_rm:
            tanggal = row["tanggal_pemeriksaan"]

            if tanggal:
                tanggal = tanggal.strftime("%d-%m-%Y %H:%M")
            else:
                tanggal = "-"

            self.view.tabel.insert(
                "",
                "end",
                values=(
                    row["id_rekam_medis"],
                    row["id_kunjungan"],
                    tanggal,
                    row["nama_pasien"],
                    row["tekanan_darah"] or "-",
                    row["diagnosis"] or "-",
                    row["catatan"] or "-"
                )
            )

    def tambah_rekam_medis(self):
        id_kunjungan = self.view.entry_id_kunjungan.get().strip()
        tekanan_darah = self.view.entry_tekanan_darah.get().strip()
        suhu_tubuh = self.view.entry_suhu_tubuh.get().strip()
        berat_badan = self.view.entry_berat_badan.get().strip()
        diagnosis = self.view.entry_diagnosis.get().strip()
        catatan = self.view.entry_catatan.get("1.0", "end").strip()

        if not id_kunjungan or not diagnosis:
            print("ID kunjungan dan diagnosis wajib diisi.")
            return

        try:
            id_kunjungan = int(id_kunjungan)

            if suhu_tubuh:
                suhu_tubuh = float(suhu_tubuh)

            if berat_badan:
                berat_badan = float(berat_badan)

        except ValueError:
            print("ID kunjungan, suhu tubuh, atau berat badan tidak valid.")
            return

        sukses = self.model.create_rekam_medis(
            id_kunjungan,
            tekanan_darah,
            suhu_tubuh,
            berat_badan,
            diagnosis,
            catatan
        )

        if sukses:
            print("Data rekam medis berhasil disimpan!")

            self.view.entry_id_kunjungan.delete(0, "end")
            self.view.entry_tekanan_darah.delete(0, "end")
            self.view.entry_suhu_tubuh.delete(0, "end")
            self.view.entry_berat_badan.delete(0, "end")
            self.view.entry_diagnosis.delete(0, "end")
            self.view.entry_catatan.delete("1.0", "end")

            self.load_data()

        else:
            print(
                "Gagal menyimpan rekam medis. "
                "Periksa ID kunjungan atau kemungkinan data sudah tercatat."
            )

    def run(self):
        self.view.mainloop()
