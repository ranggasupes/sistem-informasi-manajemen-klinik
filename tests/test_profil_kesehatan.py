from unittest.mock import MagicMock, patch

from models.profil_kesehatan_model import ProfilKesehatanModel


@patch("models.profil_kesehatan_model.Database.get_connection")
def test_get_by_pasien_id_berhasil(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    data = {
        "id_profil": 1,
        "id_pasien": 10,
        "alergi": "Tidak ada",
        "penyakit_bawaan": "Tidak ada",
        "riwayat_penyakit": "Tidak ada",
        "catatan_kesehatan": "Data pengujian",
        "sumber_data": "BPJS"
    }

    cursor.fetchone.return_value = data

    hasil = ProfilKesehatanModel().get_by_pasien_id(10)

    assert hasil == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("models.profil_kesehatan_model.Database.get_connection")
def test_get_by_pasien_id_data_tidak_ditemukan(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    hasil = ProfilKesehatanModel().get_by_pasien_id(10)

    assert hasil is None
    connection.close.assert_called_once()


@patch("models.profil_kesehatan_model.Database.get_connection")
def test_get_by_pasien_id_koneksi_gagal(mock_connection):
    mock_connection.return_value = None

    hasil = ProfilKesehatanModel().get_by_pasien_id(10)

    assert hasil is None


@patch("models.profil_kesehatan_model.Database.get_connection")
def test_get_by_pasien_id_error_database(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    hasil = ProfilKesehatanModel().get_by_pasien_id(10)

    assert hasil is None
    cursor.close.assert_called_once()
    connection.close.assert_called_once()