import pytest
from unittest.mock import patch, MagicMock
from models.obat_model import ObatModel
from controllers.obat_controller import ObatController


# =========================
# TAMBAH OBAT
# =========================

@patch("models.obat_model.get_db_connection")
def test_tambah_obat_berhasil(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    result = ObatModel.tambah_obat("Paracetamol", "Tablet", "Strip", 50)

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_tambah_obat_koneksi_gagal(mock_get_db):
    mock_get_db.return_value = None

    result = ObatModel.tambah_obat("Paracetamol", "Tablet", "Strip", 50)

    assert result is False


@patch("models.obat_model.get_db_connection")
def test_tambah_obat_error_database(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    result = ObatModel.tambah_obat("Paracetamol", "Tablet", "Strip", 50)

    assert result is False
    mock_conn.rollback.assert_called_once()


# =========================
# UPDATE OBAT
# =========================

@patch("models.obat_model.get_db_connection")
def test_update_obat_berhasil(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    result = ObatModel.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 100
    )

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_update_obat_menggunakan_keyword(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    result = ObatModel.update_obat(
        id_obat=1,
        nama_obat="Amoxicillin",
        jenis_obat="Kapsul",
        satuan="Strip",
        stok=75
    )

    assert result is True
    mock_cursor.execute.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_update_obat_data_tidak_ditemukan(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    result = ObatModel.update_obat(
        999, "Paracetamol", "Tablet", "Strip", 50
    )

    assert result is False


@patch("models.obat_model.get_db_connection")
def test_update_obat_koneksi_gagal(mock_get_db):
    mock_get_db.return_value = None

    result = ObatModel.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 50
    )

    assert result is False


@patch("models.obat_model.get_db_connection")
def test_update_obat_error_database(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    result = ObatModel.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 50
    )

    assert result is False
    mock_conn.rollback.assert_called_once()


# =========================
# HAPUS OBAT
# =========================

@patch("models.obat_model.get_db_connection")
def test_hapus_obat_berhasil(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    result = ObatModel.hapus_obat(1)

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_hapus_obat_data_tidak_ditemukan(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    result = ObatModel.hapus_obat(999)

    assert result is False


@patch("models.obat_model.get_db_connection")
def test_hapus_obat_koneksi_gagal(mock_get_db):
    mock_get_db.return_value = None

    result = ObatModel.hapus_obat(1)

    assert result is False


@patch("models.obat_model.get_db_connection")
def test_hapus_obat_error_database(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    result = ObatModel.hapus_obat(1)

    assert result is False
    mock_conn.rollback.assert_called_once()


# =========================
# GET ALL OBAT
# =========================

@patch("models.obat_model.get_db_connection")
def test_get_all_obat_berhasil(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    data_obat = [
        {
            "id_obat": 1,
            "nama_obat": "Paracetamol",
            "jenis_obat": "Tablet",
            "satuan": "Strip",
            "stok": 50
        }
    ]
    mock_cursor.fetchall.return_value = data_obat

    result = ObatModel.get_all_obat()

    assert result == data_obat
    mock_cursor.fetchall.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_get_all_obat_koneksi_gagal(mock_get_db):
    mock_get_db.return_value = None

    result = ObatModel.get_all_obat()

    assert result == []


@patch("models.obat_model.get_db_connection")
def test_get_all_obat_error_database(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    result = ObatModel.get_all_obat()

    assert result == []


# =========================
# GET OBAT BERDASARKAN ID
# =========================

@patch("models.obat_model.get_db_connection")
def test_get_by_id_berhasil(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    data_obat = {
        "id_obat": 1,
        "nama_obat": "Paracetamol",
        "jenis_obat": "Tablet",
        "satuan": "Strip",
        "stok": 50
    }
    mock_cursor.fetchone.return_value = data_obat

    result = ObatModel.get_by_id(1)

    assert result == data_obat
    mock_cursor.fetchone.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_get_by_id_tidak_ditemukan(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    result = ObatModel.get_by_id(999)

    assert result is None


@patch("models.obat_model.get_db_connection")
def test_get_by_id_koneksi_gagal(mock_get_db):
    mock_get_db.return_value = None

    result = ObatModel.get_by_id(1)

    assert result is None


@patch("models.obat_model.get_db_connection")
def test_get_by_id_error_database(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    result = ObatModel.get_by_id(1)

    assert result is None


# =========================
# CARI OBAT
# =========================

@patch("models.obat_model.get_db_connection")
def test_cari_obat_berhasil(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    data_obat = [
        {
            "id_obat": 1,
            "nama_obat": "Paracetamol",
            "jenis_obat": "Tablet",
            "satuan": "Strip",
            "stok": 50
        }
    ]
    mock_cursor.fetchall.return_value = data_obat

    result = ObatModel.cari_obat("Para")

    assert result == data_obat
    mock_cursor.execute.assert_called_once()


@patch("models.obat_model.get_db_connection")
def test_cari_obat_tidak_ditemukan(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    result = ObatModel.cari_obat("ObatTidakAda")

    assert result == []


@patch("models.obat_model.get_db_connection")
def test_cari_obat_koneksi_gagal(mock_get_db):
    mock_get_db.return_value = None

    result = ObatModel.cari_obat("Paracetamol")

    assert result == []


@patch("models.obat_model.get_db_connection")
def test_cari_obat_error_database(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    result = ObatModel.cari_obat("Paracetamol")

    assert result == []

    # =========================
# TEST OBAT CONTROLLER
# =========================

@patch("controllers.obat_controller.ObatModel.get_all_obat")
def test_controller_get_all_obat(mock_method):
    mock_method.return_value = [{"id_obat": 1, "nama_obat": "Paracetamol"}]

    result = ObatController.get_all_obat()

    assert result == mock_method.return_value
    mock_method.assert_called_once()


@patch("controllers.obat_controller.ObatModel.tambah_obat")
def test_controller_tambah_obat(mock_method):
    mock_method.return_value = True

    result = ObatController.tambah_obat(
        "Paracetamol", "Tablet", "Strip", 50
    )

    assert result is True
    mock_method.assert_called_once_with(
        "Paracetamol", "Tablet", "Strip", 50
    )


@patch("controllers.obat_controller.ObatModel.update_obat")
def test_controller_update_obat(mock_method):
    mock_method.return_value = True

    result = ObatController.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 100
    )

    assert result is True
    mock_method.assert_called_once_with(
        1, "Paracetamol", "Tablet", "Strip", 100
    )


@patch("controllers.obat_controller.ObatModel.hapus_obat")
def test_controller_hapus_obat(mock_method):
    mock_method.return_value = True

    result = ObatController.hapus_obat(1)

    assert result is True
    mock_method.assert_called_once_with(1)


@patch("controllers.obat_controller.ObatModel.cari_obat")
def test_controller_cari_obat(mock_method):
    mock_method.return_value = [
        {"id_obat": 1, "nama_obat": "Paracetamol"}
    ]

    result = ObatController.cari_obat("Para")

    assert result == mock_method.return_value
    mock_method.assert_called_once_with("Para")