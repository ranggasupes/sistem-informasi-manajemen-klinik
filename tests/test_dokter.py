from unittest.mock import patch, MagicMock
from models.dokter_model import DokterModel
from controllers.dokter_controller import DokterController

@patch("models.dokter_model.Database.get_connection")
def test_get_all_dokter(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Mock data dummy list dokter yang dikembalikan database
    mock_cursor.fetchall.return_value = [
        {
            "id_dokter": 1,
            "id_user": 141,
            "id_poli": 1,
            "nama_dokter": "Dr. Andi Pratama",
            "spesialisasi": "Dokter Spesialis Anak",
            "no_telepon": "081234567801"
        }
    ]
    
    # 3. Inisialisasi Model dan jalankan fungsi get_all_dokter
    model = DokterModel()
    data_dokter = model.get_all_dokter()
    
    # 4. Verifikasi hasil
    assert len(data_dokter) == 1
    assert data_dokter[0]["nama_dokter"] == "Dr. Andi Pratama"
    mock_cursor.execute.assert_called_once()

@patch("models.dokter_model.Database.get_connection")
def test_get_by_user_id(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Mock data dummy satu dokter berdasarkan id_user
    mock_cursor.fetchone.return_value = {
        "id_dokter": 1,
        "id_user": 141,
        "id_poli": 1,
        "nama_dokter": "Dr. Andi Pratama",
        "spesialisasi": "Dokter Spesialis Anak",
        "no_telepon": "081234567801",
        "nama_poli": "Poli Anak"
    }
    
    # 3. Inisialisasi Model dan jalankan fungsi get_by_user_id
    model = DokterModel()
    dokter = model.get_by_user_id(141)
    
    # 4. Verifikasi hasil
    assert dokter is not None
    assert dokter["id_user"] == 141
    assert dokter["nama_dokter"] == "Dr. Andi Pratama"
    mock_cursor.execute.assert_called_once()


@patch("controllers.dokter_controller.DokterModel")
def test_dokter_controller_daftar_dokter(mock_model):
    # Setup data dokter
    data_dokter = [
        {
            "id_dokter": 1,
            "id_user": 141,
            "id_poli": 1,
            "nama_dokter": "Dr. Andi Pratama",
            "spesialisasi": "Dokter Spesialis Anak",
            "no_telepon": "081234567801"
        }
    ]

    mock_model.return_value.get_all_dokter.return_value = data_dokter

    # Eksekusi controller
    controller = DokterController()
    result = controller.daftar_dokter()

    # Verifikasi
    assert result == data_dokter
    mock_model.return_value.get_all_dokter.assert_called_once()


@patch("controllers.dokter_controller.DokterModel")
def test_dokter_controller_daftar_dokter_kosong(mock_model):
    mock_model.return_value.get_all_dokter.return_value = []

    controller = DokterController()
    result = controller.daftar_dokter()

    assert result == []
    mock_model.return_value.get_all_dokter.assert_called_once()