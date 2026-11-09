from unittest.mock import MagicMock, patch

from models.resep_model import ResepModel


@patch("models.resep_model.Database.get_connection")
def test_get_antrean_resep_berhasil(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    data = [{"id_resep": 1, "nama_pasien": "Pasien Uji"}]
    cursor.fetchall.return_value = data

    hasil = ResepModel().get_antrean_resep()

    assert hasil == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("models.resep_model.Database.get_connection")
def test_get_antrean_resep_koneksi_gagal(mock_connection):
    mock_connection.return_value = None

    hasil = ResepModel().get_antrean_resep()

    assert hasil == []


@patch("models.resep_model.Database.get_connection")
def test_get_antrean_resep_error_database(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    hasil = ResepModel().get_antrean_resep()

    assert hasil == []
    connection.close.assert_called_once()


@patch("models.resep_model.Database.get_connection")
def test_get_riwayat_penyerahan_berhasil(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    data = [{"id_resep": 1, "nama_petugas": "admin"}]
    cursor.fetchall.return_value = data

    hasil = ResepModel().get_riwayat_penyerahan()

    assert hasil == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("models.resep_model.Database.get_connection")
def test_get_riwayat_penyerahan_koneksi_gagal(mock_connection):
    mock_connection.return_value = None

    hasil = ResepModel().get_riwayat_penyerahan()

    assert hasil == []


@patch("models.resep_model.Database.get_connection")
def test_get_riwayat_penyerahan_error_database(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    hasil = ResepModel().get_riwayat_penyerahan()

    assert hasil == []
    connection.close.assert_called_once()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_berhasil(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {"id_kunjungan": 10},
        {"nama_obat": "Paracetamol", "stok": 20}
    ]

    cursor.fetchall.return_value = [
        {
            "id_resep": 1,
            "id_obat": 5,
            "jumlah": 3,
            "status_penyerahan": "Menunggu"
        }
    ]

    cursor.rowcount = 1

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is True
    assert "berhasil diserahkan" in hasil[1].lower()

    connection.start_transaction.assert_called_once()
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_koneksi_gagal(mock_connection):
    mock_connection.return_value = None

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "koneksi database gagal" in hasil[1].lower()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_ditolak_jika_kunjungan_tidak_ditemukan(
    mock_connection
):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "tidak menunggu obat" in hasil[1].lower()

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_ditolak_jika_resep_kosong(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    cursor.fetchone.return_value = {"id_kunjungan": 10}
    cursor.fetchall.return_value = []

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "resep tidak ditemukan" in hasil[1].lower()

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_ditolak_jika_status_resep_berubah(
    mock_connection
):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    cursor.fetchone.return_value = {"id_kunjungan": 10}
    cursor.fetchall.return_value = [
        {
            "id_resep": 1,
            "id_obat": 5,
            "jumlah": 3,
            "status_penyerahan": "Diserahkan"
        }
    ]

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "status resep sudah berubah" in hasil[1].lower()

    connection.rollback.assert_called_once()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_ditolak_jika_obat_tidak_ditemukan(
    mock_connection
):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {"id_kunjungan": 10},
        None
    ]

    cursor.fetchall.return_value = [
        {
            "id_resep": 1,
            "id_obat": 5,
            "jumlah": 3,
            "status_penyerahan": "Menunggu"
        }
    ]

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "data obat tidak ditemukan" in hasil[1].lower()

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_ditolak_jika_stok_tidak_cukup(
    mock_connection
):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {"id_kunjungan": 10},
        {"nama_obat": "Paracetamol", "stok": 2}
    ]

    cursor.fetchall.return_value = [
        {
            "id_resep": 1,
            "id_obat": 5,
            "jumlah": 5,
            "status_penyerahan": "Menunggu"
        }
    ]

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "tidak mencukupi" in hasil[1].lower()

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


@patch("models.resep_model.Database.get_connection")
def test_serahkan_obat_error_database(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()

    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    hasil = ResepModel().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "penyerahan obat gagal" in hasil[1].lower()

    connection.rollback.assert_called_once()
    connection.close.assert_called_once()