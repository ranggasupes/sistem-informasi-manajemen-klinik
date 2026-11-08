from unittest.mock import patch, MagicMock
from models.pasien_model import PasienModel

@patch("models.pasien_model.Database.get_connection")
def test_create_pasien_berhasil(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Inisialisasi Model
    model = PasienModel()
    
    # 3. Melakukan eksekusi fungsi create_pasien
    hasil = model.create_pasien(
        id_user=121, 
        nomor_bpjs="TEST-BPJS-001", 
        nik="TEST-NIK-001", 
        nama_pasien="Pasien Uji 01", 
        jenis_kelamin="Laki-laki", 
        tanggal_lahir="2000-05-15", 
        alamat="Alamat Simulasi", 
        no_telepon="080000000001"
    )
    
    # 4. Memverifikasi hasil dan pemanggilan kursor/commit
    assert hasil is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch("models.pasien_model.Database.get_connection")
def test_get_all_pasien(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Menyiapkan data dummy tiruan yang dikembalikan
    mock_cursor.fetchall.return_value = [
        {
            "id_pasien": 1,
            "id_user": 121,
            "nomor_bpjs": "TEST-BPJS-001",
            "nik": "TEST-NIK-001",
            "nama_pasien": "Pasien Uji 01",
            "jenis_kelamin": "Laki-laki",
            "tanggal_lahir": "2000-05-15",
            "alamat": "Alamat Simulasi",
            "no_telepon": "080000000001"
        }
    ]
    
    # 3. Inisialisasi Model dan jalankan fungsi
    model = PasienModel()
    data_pasien = model.get_all_pasien()
    
    # 4. Verifikasi hasil
    assert len(data_pasien) == 1
    assert data_pasien[0]["nama_pasien"] == "Pasien Uji 01"
    mock_cursor.execute.assert_called_once()