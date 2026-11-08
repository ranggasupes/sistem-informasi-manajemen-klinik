from unittest.mock import patch, MagicMock
from models.user_model import UserModel

@patch("models.user_model.Database.get_connection")
def test_login_berhasil(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Mock data user yang dikembalikan saat query pencarian username
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "admin_klinik",
        "password": "hashed_password123",
        "role": "admin"
    }
    
    # 3. Inisialisasi Model User
    model = UserModel()
    
    # 4. Simulasi fungsi autentikasi / pengecekan login (sesuaikan nama method di user_model milikmu)
    # Contoh: method mencari user berdasarkan username untuk divalidasi passwordnya
    user = model.get_user_by_username("admin_klinik")
    
    # 5. Verifikasi hasil pengujian
    assert user is not None
    assert user["username"] == "admin_klinik"
    assert user["role"] == "admin"
    
    # Memverifikasi apakah kursor database benar-benar mengeksekusi query
    mock_cursor.execute.assert_called_once()

@patch("models.user_model.Database.get_connection")
def test_login_gagal_user_tidak_ditemukan(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Mock nilai pengembalian None (artinya user tidak terdaftar di database)
    mock_cursor.fetchone.return_value = None
    
    # 3. Inisialisasi Model User
    model = UserModel()
    
    # 4. Simulasi pencarian username yang tidak ada
    user = model.get_user_by_username("user_palsu")
    
    # 5. Verifikasi bahwa user bernilai None (gagal login)
    assert user is None
    mock_cursor.execute.assert_called_once()