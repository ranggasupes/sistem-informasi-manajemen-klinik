from unittest.mock import patch, MagicMock
from models.user_model import UserModel

@patch("models.user_model.Database.get_connection")
def test_get_user_by_username(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Mock data dummy user yang dikembalikan database
    mock_cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "admin_klinik",
        "password": "hashed_password",
        "role": "admin"
    }
    
    # 3. Inisialisasi Model User dan panggil fungsi pencarian berdasarkan username
    model = UserModel()
    user = model.get_user_by_username("admin_klinik")
    
    # 4. Verifikasi hasil
    assert user is not None
    assert user["username"] == "admin_klinik"
    assert user["role"] == "admin"
    mock_cursor.execute.assert_called_once()

@patch("models.user_model.Database.get_connection")
def test_get_all_users(mock_get_connection):
    # 1. Mock koneksi dan kursor database
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # 2. Mock data dummy list user
    mock_cursor.fetchall.return_value = [
        {"id_user": 1, "username": "admin_klinik", "role": "admin"},
        {"id_user": 2, "username": "apoteker_klinik", "role": "apoteker"}
    ]
    
    # 3. Inisialisasi Model dan jalankan fungsi ambil semua user
    model = UserModel()
    data_users = model.get_all_users()
    
    # 4. Verifikasi hasil
    assert len(data_users) == 2
    assert data_users[0]["role"] == "admin"
    mock_cursor.execute.assert_called_once()