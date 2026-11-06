from models.pasien_model import PasienModel
from views.pasien_view import PasienView

class PasienController:
    def __init__(self):
        # Menghubungkan Model dan View
        self.model = PasienModel()
        self.view = PasienView()

        # Menghubungkan tombol simpan di View dengan fungsi kontroler
        self.view.btn_simpan.configure(command=self.tambah_pasien)

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.load_data()

    def load_data(self):
        """Mengambil data dari model dan menampilkannya ke tabel view"""
        # Hapus data lama di tabel GUI agar tidak menumpuk
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Ambil data terbaru dari database melalui model
        data_pasien = self.model.get_all_pasien()
        
        # Masukkan baris demi baris data ke dalam tabel GUI
        for row in data_pasien:
            self.view.tabel.insert("", "end", values=(
                row["id_pasien"], 
                row["nama"], 
                row["nik"], 
                row["alamat"], 
                row["no_telepon"]
            ))

    def tambah_pasien(self):
        """Mengambil inputan dari form View lalu menyimpannya lewat Model"""
        nama = self.view.entry_nama.get()
        nik = self.view.entry_nik.get()
        alamat = self.view.entry_alamat.get()
        tanggal_lahir = self.view.entry_tanggal_lahir.get()
        telepon = self.view.entry_telepon.get()

        # Validasi sederhana: pastikan tidak ada yang kosong
        if not nama or not nik or not alamat or not tanggal_lahir or not telepon:
            print("Peringatan: Semua kolom form harus diisi!")
            return

        # Kirim data ke model untuk disimpan ke database
        sukses = self.model.create_pasien(nama, nik, alamat, tanggal_lahir, telepon)

        if sukses:
            print("Data pasien berhasil disimpan!")
            # Bersihkan form setelah berhasil
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_nik.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
            self.view.entry_tanggal_lahir.delete(0, 'end')
            self.view.entry_telepon.delete(0, 'end')
            
            # Segarkan kembali isi tabel
            self.load_data()
        else:
            print("Gagal menyimpan data pasien ke database.")

    def run(self):
        """Menjalankan jendela aplikasi utama"""
        self.view.mainloop()