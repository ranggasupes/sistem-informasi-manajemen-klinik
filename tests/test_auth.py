import hashlib
from unittest.mock import MagicMock, patch

from controllers.auth_controller import AuthController


def buat_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


@patch("controllers.auth_controller.UserModel")
def test_login_berhasil(mock_user):
    user_model = mock_user.return_value
    user_model.get_user_by_username.return_value = {
        "id_user": 1,
        "username": "pasien01",
        "password": buat_hash("password123"),
        "role": "pasien"
    }

    controller = AuthController()
    berhasil, hasil = controller.login("pasien01", "password123")

    assert berhasil is True
    assert hasil == {
        "id_user": 1,
        "username": "pasien01",
        "role": "pasien"
    }


@patch("controllers.auth_controller.UserModel")
def test_login_username_kosong(mock_user):
    controller = AuthController()

    berhasil, pesan = controller.login("", "password123")

    assert berhasil is False
    assert "harus diisi" in pesan.lower()
    mock_user.return_value.get_user_by_username.assert_not_called()


@patch("controllers.auth_controller.UserModel")
def test_login_password_kosong(mock_user):
    controller = AuthController()

    berhasil, pesan = controller.login("pasien01", "")

    assert berhasil is False
    assert "harus diisi" in pesan.lower()
    mock_user.return_value.get_user_by_username.assert_not_called()


@patch("controllers.auth_controller.UserModel")
def test_login_username_tidak_ditemukan(mock_user):
    user_model = mock_user.return_value
    user_model.get_user_by_username.return_value = None

    controller = AuthController()
    berhasil, pesan = controller.login("tidak_ada", "password123")

    assert berhasil is False
    assert "username tidak ditemukan" in pesan.lower()


@patch("controllers.auth_controller.UserModel")
def test_login_password_salah(mock_user):
    user_model = mock_user.return_value
    user_model.get_user_by_username.return_value = {
        "id_user": 1,
        "username": "pasien01",
        "password": buat_hash("password_benar"),
        "role": "pasien"
    }

    controller = AuthController()
    berhasil, pesan = controller.login("pasien01", "password_salah")

    assert berhasil is False
    assert "password" in pesan.lower()


@patch("controllers.auth_controller.UserModel")
def test_login_database_bermasalah(mock_user):
    user_model = mock_user.return_value
    user_model.get_user_by_username.return_value = None

    controller = AuthController()
    berhasil, pesan = controller.login("pasien01", "password123")

    assert berhasil is False
    assert "database bermasalah" in pesan.lower()