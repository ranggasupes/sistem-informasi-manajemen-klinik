from models.kunjungan_model import KunjunganModel
from views.kunjungan_view import KunjunganView

class KunjunganController:
    def __init__(self):
        self.model = KunjunganModel()
        self.view = KunjunganView()

        self.view.btn_simpan.configure(command=self.tambah_kunjungan)
        self.load_data()

    def load_data(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_kunjungan = self.model.get_all_kunjungan()
        for row in data_kunjungan:
            self.view.tabel.insert("", "end", values=(
                row["id_kunjungan"], 
                row["tanggal_kunjungan"], 
                row["nomor_antrian"],
                row["nama_pasien"],
                row["nama_poli"],  # Menambahkan kolom nama poli di sini
                row["nama_dokter"] if row["nama_dokter"] else "-",
                row["keluhan_awal"]
            ))

    def tambah_kunjungan(self):
        id_pasien = self.view.entry_id_pasien.get()
        id_poli = "1" # Bisa disesuaikan nanti jika form input poli sudah dibuat di view
        id_dokter = self.view.entry_id_dokter.get()
        nomor_antrian = "1" # Bisa disesuaikan dengan inputan antrian
        tanggal = self.view.entry_tanggal.get()
        keluhan_awal = self.view.entry_keluhan.get() # Sesuaikan jadi keluhan_awal

        if not id_pasien or not id_dokter or not tanggal or not keluhan_awal:
            print("Peringatan: Semua kolom kunjungan harus diisi!")
            return

        sukses = self.model.create_kunjungan(id_pasien, id_poli, id_dokter, nomor_antrian, tanggal, keluhan_awal)
        if sukses:
            print("Data kunjungan berhasil disimpan!")
            self.load_data()
        else:
            print("Gagal menyimpan data kunjungan ke database.")
            
    def run(self):
        self.view.mainloop()