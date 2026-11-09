
from unittest.mock import MagicMock, patch

from models.kunjungan_model import KunjunganModel


# =========================================================
# GET ALL KUNJUNGAN
# =========================================================

@patch("models.kunjungan_model.Database.get_connection")
def test_get_all_kunjungan_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = [
        {
            "id_kunjungan": 1,
            "nama_pasien": "Pasien Uji",
            "status": "Menunggu"
        }
    ]
    cursor.fetchall.return_value = data

    model = KunjunganModel()
    hasil = model.get_all_kunjungan()

    assert hasil == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_get_all_kunjungan_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = KunjunganModel()

    assert model.get_all_kunjungan() == []


@patch("models.kunjungan_model.Database.get_connection")
def test_get_all_kunjungan_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = KunjunganModel()
    hasil = model.get_all_kunjungan()

    assert hasil == []
    conn.close.assert_called_once()


# =========================================================
# CREATE KUNJUNGAN
# =========================================================

@patch("models.kunjungan_model.Database.get_connection")
def test_create_kunjungan_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        None,
        {"nomor_baru": 3}
    ]
    cursor.lastrowid = 15

    model = KunjunganModel()

    hasil = model.create_kunjungan(
        id_pasien=1,
        id_poli=2,
        id_dokter=None,
        tanggal_kunjungan="2026-11-09",
        keluhan_awal="Demam"
    )

    assert hasil == {
        "id_kunjungan": 15,
        "nomor_antrian": 3
    }

    assert cursor.execute.call_count == 3
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_create_kunjungan_ditolak_jika_masih_aktif(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.return_value = {
        "id_kunjungan": 10
    }

    model = KunjunganModel()

    hasil = model.create_kunjungan(
        1, 2, None, "2026-11-09", "Demam"
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch("models.kunjungan_model.Database.get_connection")
def test_create_kunjungan_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = KunjunganModel()

    hasil = model.create_kunjungan(
        1, 2, None, "2026-11-09", "Demam"
    )

    assert hasil is False


@patch("models.kunjungan_model.Database.get_connection")
def test_create_kunjungan_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = KunjunganModel()

    hasil = model.create_kunjungan(
        1, 2, None, "2026-11-09", "Demam"
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# GET ACTIVE BY USER ID
# =========================================================

@patch("models.kunjungan_model.Database.get_connection")
def test_get_active_by_user_id_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = {
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Menunggu"
    }
    cursor.fetchone.return_value = data

    model = KunjunganModel()
    hasil = model.get_active_by_user_id(21)

    assert hasil == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_get_active_by_user_id_tidak_ada_data(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    model = KunjunganModel()
    hasil = model.get_active_by_user_id(21)

    assert hasil is None
    conn.close.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_get_active_by_user_id_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = KunjunganModel()

    assert model.get_active_by_user_id(21) is None


@patch("models.kunjungan_model.Database.get_connection")
def test_get_active_by_user_id_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = KunjunganModel()
    hasil = model.get_active_by_user_id(21)

    assert hasil is None
    conn.close.assert_called_once()


# =========================================================
# GET ANTREAN DOKTER
# =========================================================

@patch("models.kunjungan_model.Database.get_connection")
def test_get_antrean_dokter_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = [
        {
            "id_kunjungan": 10,
            "nama_pasien": "Pasien Uji",
            "status": "Menunggu"
        }
    ]
    cursor.fetchall.return_value = data

    model = KunjunganModel()
    hasil = model.get_antrean_dokter(21)

    assert hasil == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_get_antrean_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = KunjunganModel()

    assert model.get_antrean_dokter(21) == []


@patch("models.kunjungan_model.Database.get_connection")
def test_get_antrean_dokter_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = KunjunganModel()
    hasil = model.get_antrean_dokter(21)

    assert hasil == []
    conn.close.assert_called_once()


# =========================================================
# PANGGIL PASIEN
# =========================================================

@patch("models.kunjungan_model.Database.get_connection")
def test_panggil_pasien_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.rowcount = 1

    model = KunjunganModel()

    hasil = model.panggil_pasien(
        id_kunjungan=10,
        id_user=21
    )

    assert hasil is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_panggil_pasien_gagal_jika_data_tidak_sesuai(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.rowcount = 0

    model = KunjunganModel()

    hasil = model.panggil_pasien(10, 21)

    assert hasil is False
    conn.commit.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_panggil_pasien_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = KunjunganModel()

    assert model.panggil_pasien(10, 21) is False


@patch("models.kunjungan_model.Database.get_connection")
def test_panggil_pasien_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = KunjunganModel()

    hasil = model.panggil_pasien(10, 21)

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# MULAI PEMERIKSAAN
# =========================================================

@patch("models.kunjungan_model.Database.get_connection")
def test_mulai_pemeriksaan_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = {
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Dipanggil"
    }

    cursor.fetchone.return_value = data
    cursor.rowcount = 1

    model = KunjunganModel()

    hasil = model.mulai_pemeriksaan(10, 21)

    assert hasil is not None
    assert hasil["status"] == "Diperiksa"
    conn.commit.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_mulai_pemeriksaan_ditolak_jika_bukan_pasien_dokter(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    model = KunjunganModel()

    hasil = model.mulai_pemeriksaan(10, 99)

    assert hasil is None
    conn.rollback.assert_called_once()


@patch("models.kunjungan_model.Database.get_connection")
def test_mulai_pemeriksaan_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = KunjunganModel()

    assert model.mulai_pemeriksaan(10, 21) is None


@patch("models.kunjungan_model.Database.get_connection")
def test_mulai_pemeriksaan_status_sudah_diperiksa(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = {
        "id_kunjungan": 10,
        "nama_pasien": "Pasien Uji",
        "status": "Diperiksa"
    }
    cursor.fetchone.return_value = data

    model = KunjunganModel()
    hasil = model.mulai_pemeriksaan(10, 21)

    assert hasil == data
    assert hasil["status"] == "Diperiksa"
    cursor.execute.assert_called_once()
    conn.commit.assert_not_called()


@patch("models.kunjungan_model.Database.get_connection")
def test_mulai_pemeriksaan_update_gagal(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.return_value = {
        "id_kunjungan": 10,
        "status": "Dipanggil"
    }
    cursor.rowcount = 0

    model = KunjunganModel()
    hasil = model.mulai_pemeriksaan(10, 21)

    assert hasil is None
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch("models.kunjungan_model.Database.get_connection")
def test_mulai_pemeriksaan_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = KunjunganModel()
    hasil = model.mulai_pemeriksaan(10, 21)

    assert hasil is None
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()
