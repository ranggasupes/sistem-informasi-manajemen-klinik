
from unittest.mock import patch, MagicMock

from models.obat_model import ObatModel
from controllers.obat_controller import ObatController


DB = "models.obat_model.get_db_connection"
DATA_OBAT = {
    "id_obat": 1,
    "nama_obat": "Paracetamol",
    "jenis_obat": "Tablet",
    "satuan": "Strip",
    "stok": 50
}


def _db(mock_db, rowcount=1, fetchone="default",
        fetchall=None, error=None):
    conn, cursor = MagicMock(), MagicMock()
    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.rowcount = rowcount

    if fetchone != "default":
        cursor.fetchone.return_value = fetchone
    if fetchall is not None:
        cursor.fetchall.return_value = fetchall
    if error:
        cursor.execute.side_effect = error

    return conn, cursor


# TAMBAH OBAT

@patch(DB)
def test_tambah_obat_berhasil(mock_db):
    conn, cursor = _db(mock_db)
    assert ObatModel.tambah_obat(
        "Paracetamol", "Tablet", "Strip", 50
    ) is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()


@patch(DB)
def test_tambah_obat_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert ObatModel.tambah_obat(
        "Paracetamol", "Tablet", "Strip", 50
    ) is False


@patch(DB)
def test_tambah_obat_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))
    assert ObatModel.tambah_obat(
        "Paracetamol", "Tablet", "Strip", 50
    ) is False
    conn.rollback.assert_called_once()


# UPDATE OBAT

@patch(DB)
def test_update_obat_berhasil(mock_db):
    conn, cursor = _db(mock_db)
    assert ObatModel.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 100
    ) is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()


@patch(DB)
def test_update_obat_menggunakan_keyword(mock_db):
    _, cursor = _db(mock_db)
    assert ObatModel.update_obat(
        id_obat=1, nama_obat="Amoxicillin",
        jenis_obat="Kapsul", satuan="Strip", stok=75
    ) is True
    cursor.execute.assert_called_once()


@patch(DB)
def test_update_obat_data_tidak_ditemukan(mock_db):
    _db(mock_db, rowcount=0)
    assert ObatModel.update_obat(
        999, "Paracetamol", "Tablet", "Strip", 50
    ) is False


@patch(DB)
def test_update_obat_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert ObatModel.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 50
    ) is False


@patch(DB)
def test_update_obat_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))
    assert ObatModel.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 50
    ) is False
    conn.rollback.assert_called_once()


# HAPUS OBAT

@patch(DB)
def test_hapus_obat_berhasil(mock_db):
    conn, cursor = _db(mock_db)
    assert ObatModel.hapus_obat(1) is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()


@patch(DB)
def test_hapus_obat_data_tidak_ditemukan(mock_db):
    _db(mock_db, rowcount=0)
    assert ObatModel.hapus_obat(999) is False


@patch(DB)
def test_hapus_obat_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert ObatModel.hapus_obat(1) is False


@patch(DB)
def test_hapus_obat_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))
    assert ObatModel.hapus_obat(1) is False
    conn.rollback.assert_called_once()


# GET ALL OBAT

@patch(DB)
def test_get_all_obat_berhasil(mock_db):
    _, cursor = _db(mock_db, fetchall=[DATA_OBAT])
    assert ObatModel.get_all_obat() == [DATA_OBAT]
    cursor.fetchall.assert_called_once()


@patch(DB)
def test_get_all_obat_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert ObatModel.get_all_obat() == []


@patch(DB)
def test_get_all_obat_error_database(mock_db):
    _db(mock_db, error=Exception("Database error"))
    assert ObatModel.get_all_obat() == []


# GET OBAT BERDASARKAN ID

@patch(DB)
def test_get_by_id_berhasil(mock_db):
    _, cursor = _db(mock_db, fetchone=DATA_OBAT)
    assert ObatModel.get_by_id(1) == DATA_OBAT
    cursor.fetchone.assert_called_once()


@patch(DB)
def test_get_by_id_tidak_ditemukan(mock_db):
    _db(mock_db, fetchone=None)
    assert ObatModel.get_by_id(999) is None


@patch(DB)
def test_get_by_id_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert ObatModel.get_by_id(1) is None


@patch(DB)
def test_get_by_id_error_database(mock_db):
    _db(mock_db, error=Exception("Database error"))
    assert ObatModel.get_by_id(1) is None


# CARI OBAT

@patch(DB)
def test_cari_obat_berhasil(mock_db):
    _, cursor = _db(mock_db, fetchall=[DATA_OBAT])
    assert ObatModel.cari_obat("Para") == [DATA_OBAT]
    cursor.execute.assert_called_once()


@patch(DB)
def test_cari_obat_tidak_ditemukan(mock_db):
    _db(mock_db, fetchall=[])
    assert ObatModel.cari_obat("ObatTidakAda") == []


@patch(DB)
def test_cari_obat_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert ObatModel.cari_obat("Paracetamol") == []


@patch(DB)
def test_cari_obat_error_database(mock_db):
    _db(mock_db, error=Exception("Database error"))
    assert ObatModel.cari_obat("Paracetamol") == []


# OBAT CONTROLLER

@patch("controllers.obat_controller.ObatModel.get_all_obat")
def test_controller_get_all_obat(mock_method):
    mock_method.return_value = [{"id_obat": 1, "nama_obat": "Paracetamol"}]
    assert ObatController.get_all_obat() == mock_method.return_value
    mock_method.assert_called_once()


@patch("controllers.obat_controller.ObatModel.tambah_obat")
def test_controller_tambah_obat(mock_method):
    mock_method.return_value = True
    assert ObatController.tambah_obat(
        "Paracetamol", "Tablet", "Strip", 50
    ) is True
    mock_method.assert_called_once_with(
        "Paracetamol", "Tablet", "Strip", 50
    )


@patch("controllers.obat_controller.ObatModel.update_obat")
def test_controller_update_obat(mock_method):
    mock_method.return_value = True
    assert ObatController.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 100
    ) is True
    mock_method.assert_called_once_with(
        1, "Paracetamol", "Tablet", "Strip", 100
    )


@patch("controllers.obat_controller.ObatModel.hapus_obat")
def test_controller_hapus_obat(mock_method):
    mock_method.return_value = True
    assert ObatController.hapus_obat(1) is True
    mock_method.assert_called_once_with(1)


@patch("controllers.obat_controller.ObatModel.cari_obat")
def test_controller_cari_obat(mock_method):
    mock_method.return_value = [{"id_obat": 1, "nama_obat": "Paracetamol"}]
    assert ObatController.cari_obat("Para") == mock_method.return_value
    mock_method.assert_called_once_with("Para")
