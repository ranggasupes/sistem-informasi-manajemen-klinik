from models.rekam_medis_model import RekamMedisModel
from views.rekam_medis_view import RekamMedisView

class RekamMedisController:
    def __init__(self):
        self.model = RekamMedisModel()
        self.view = RekamMedisView()

        # Menghubungkan tombol simpan di View Rekam Medis
        self.view.btn_simpan.configure(command=self.tambah_rekam_medis)
        
        # Memuat data ke tabel saat pertama kali dibuka
        self.load_data()

    def load_data(self):
        """Mengambil data rekam medis dari model dan menampilkannya ke tabel view"""
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_rm = self.model.get_all_rekam_medis()
        for row in data_rm:
            self.view.tabel.insert("", "end", values=(
                row["id_rekam_medis"], 
                row["tanggal_kunjungan"], 
                row["nama_pasien"], 
                row["diagnosa"], 
                row["tindakan"], 
                row["catatan_dokter"]
            ))

    def tambah_rekam_medis(self):
        """Mengambil inputan form rekam medis lalu menyimpannya lewat model"""
        id_kunjungan = self.view.entry_id_kunjungan.get()
        diagnosa = self.view.entry_diagnosa.get()
        tindakan = self.view.entry_tindakan.get()
        catatan = self.view.entry_catatan.get()

        if not id_kunjungan or not diagnosa or not tindakan or not catatan:
            print("Peringatan: Semua kolom rekam medis harus diisi!")
            return

        sukses = self.model.create_rekam_medis(id_kunjungan, diagnosa, tindakan, catatan)
        if sukses:
            print("Data rekam medis berhasil disimpan!")
            self.view.entry_id_kunjungan.delete(0, 'end')
            self.view.entry_diagnosa.delete(0, 'end')
            self.view.entry_tindakan.delete(0, 'end')
            self.view.entry_catatan.delete(0, 'end')
            self.load_data()
        else:
            print("Gagal menyimpan data rekam medis ke database.")

    def run(self):
        self.view.mainloop()