
from unittest.mock import MagicMock, patch

from models.kunjungan_model import KunjunganModel


DB = "models.kunjungan_model.Database.get_connection"


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


def _model():
    return KunjunganModel()


# GET ALL KUNJUNGAN

@patch(DB)
def test_get_all_kunjungan_berhasil(mock_db):
    data = [{"id_kunjungan": 1, "nama_pasien": "Pasien Uji",
             "status": "Menunggu"}]
    conn, cursor = _db(mock_db, fetchall=data)

    assert _model().get_all_kunjungan() == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_all_kunjungan_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _model().get_all_kunjungan() == []


@patch(DB)
def test_get_all_kunjungan_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))
    assert _model().get_all_kunjungan() == []
    conn.close.assert_called_once()


# CREATE KUNJUNGAN

@patch(DB)
def test_create_kunjungan_berhasil(mock_db):
    conn, cursor = _db(mock_db)
    cursor.fetchone.side_effect = [None, {"nomor_baru": 3}]
    cursor.lastrowid = 15

    hasil = _model().create_kunjungan(
        id_pasien=1,
        id_poli=2,
        id_dokter=None,
        tanggal_kunjungan="2026-11-09",
        keluhan_awal="Demam"
    )

    assert hasil == {"id_kunjungan": 15, "nomor_antrian": 3}
    assert cursor.execute.call_count == 3
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_create_kunjungan_ditolak_jika_masih_aktif(mock_db):
    conn, _ = _db(mock_db, fetchone={"id_kunjungan": 10})

    hasil = _model().create_kunjungan(
        1, 2, None, "2026-11-09", "Demam"
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_create_kunjungan_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _model().create_kunjungan(
        1, 2, None, "2026-11-09", "Demam"
    ) is False


@patch(DB)
def test_create_kunjungan_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _model().create_kunjungan(
        1, 2, None, "2026-11-09", "Demam"
    ) is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


# GET ACTIVE BY USER ID

@patch(DB)
def test_get_active_by_user_id_berhasil(mock_db):
    data = {
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Menunggu"
    }
    conn, cursor = _db(mock_db, fetchone=data)

    assert _model().get_active_by_user_id(21) == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_active_by_user_id_tidak_ada_data(mock_db):
    conn, _ = _db(mock_db, fetchone=None)

    assert _model().get_active_by_user_id(21) is None
    conn.close.assert_called_once()


@patch(DB)
def test_get_active_by_user_id_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _model().get_active_by_user_id(21) is None


@patch(DB)
def test_get_active_by_user_id_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _model().get_active_by_user_id(21) is None
    conn.close.assert_called_once()


# GET ANTREAN DOKTER

@patch(DB)
def test_get_antrean_dokter_berhasil(mock_db):
    data = [{
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Menunggu"
    }]
    conn, cursor = _db(mock_db, fetchall=data)

    assert _model().get_antrean_dokter(21) == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_antrean_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _model().get_antrean_dokter(21) == []


@patch(DB)
def test_get_antrean_dokter_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _model().get_antrean_dokter(21) == []
    conn.close.assert_called_once()


# PANGGIL PASIEN

@patch(DB)
def test_panggil_pasien_berhasil(mock_db):
    conn, cursor = _db(mock_db)

    assert _model().panggil_pasien(
        id_kunjungan=10, id_user=21
    ) is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()


@patch(DB)
def test_panggil_pasien_gagal_jika_data_tidak_sesuai(mock_db):
    conn, _ = _db(mock_db, rowcount=0)

    assert _model().panggil_pasien(10, 21) is False
    conn.commit.assert_called_once()


@patch(DB)
def test_panggil_pasien_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _model().panggil_pasien(10, 21) is False


@patch(DB)
def test_panggil_pasien_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _model().panggil_pasien(10, 21) is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


# MULAI PEMERIKSAAN

@patch(DB)
def test_mulai_pemeriksaan_berhasil(mock_db):
    data = {
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Dipanggil"
    }
    conn, cursor = _db(mock_db, fetchone=data)

    hasil = _model().mulai_pemeriksaan(10, 21)

    assert hasil is not None
    assert hasil["status"] == "Diperiksa"
    conn.commit.assert_called_once()


@patch(DB)
def test_mulai_pemeriksaan_ditolak_jika_bukan_pasien_dokter(mock_db):
    conn, _ = _db(mock_db, fetchone=None)

    assert _model().mulai_pemeriksaan(10, 99) is None
    conn.rollback.assert_called_once()


@patch(DB)
def test_mulai_pemeriksaan_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _model().mulai_pemeriksaan(10, 21) is None


@patch(DB)
def test_mulai_pemeriksaan_status_sudah_diperiksa(mock_db):
    data = {
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Diperiksa"
    }
    conn, cursor = _db(mock_db, fetchone=data)

    hasil = _model().mulai_pemeriksaan(10, 21)

    assert hasil == data
    assert hasil["status"] == "Diperiksa"
    cursor.execute.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_mulai_pemeriksaan_update_gagal(mock_db):
    data = {"id_kunjungan": 10, "status": "Dipanggil"}
    conn, _ = _db(mock_db, rowcount=0, fetchone=data)

    assert _model().mulai_pemeriksaan(10, 21) is None
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_mulai_pemeriksaan_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _model().mulai_pemeriksaan(10, 21) is None
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()
