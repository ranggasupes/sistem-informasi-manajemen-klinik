
from unittest.mock import MagicMock, patch

from models.resep_model import ResepModel


DB = "models.resep_model.Database.get_connection"


def _db(mock_db, fetchone="default", fetchall=None, error=None):
    conn, cursor = MagicMock(), MagicMock()
    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    if fetchone != "default":
        cursor.fetchone.return_value = fetchone
    if fetchall is not None:
        cursor.fetchall.return_value = fetchall
    if error:
        cursor.execute.side_effect = error

    return conn, cursor


def _resep():
    return ResepModel()


def _data_resep(status="Menunggu"):
    return [{
        "id_resep": 1,
        "id_obat": 5,
        "jumlah": 3,
        "status_penyerahan": status
    }]


# GET ANTREAN RESEP

@patch(DB)
def test_get_antrean_resep_berhasil(mock_db):
    data = [{"id_resep": 1, "nama_pasien": "Pasien Uji"}]
    conn, cursor = _db(mock_db, fetchall=data)

    assert _resep().get_antrean_resep() == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_antrean_resep_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _resep().get_antrean_resep() == []


@patch(DB)
def test_get_antrean_resep_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _resep().get_antrean_resep() == []
    conn.close.assert_called_once()


# GET RIWAYAT PENYERAHAN

@patch(DB)
def test_get_riwayat_penyerahan_berhasil(mock_db):
    data = [{"id_resep": 1, "nama_petugas": "admin"}]
    conn, cursor = _db(mock_db, fetchall=data)

    assert _resep().get_riwayat_penyerahan() == data
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_riwayat_penyerahan_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert _resep().get_riwayat_penyerahan() == []


@patch(DB)
def test_get_riwayat_penyerahan_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    assert _resep().get_riwayat_penyerahan() == []
    conn.close.assert_called_once()


# SERAHKAN OBAT

@patch(DB)
def test_serahkan_obat_berhasil(mock_db):
    conn, cursor = _db(mock_db)
    cursor.fetchone.side_effect = [
        {"id_kunjungan": 10},
        {"nama_obat": "Paracetamol", "stok": 20}
    ]
    cursor.fetchall.return_value = _data_resep()
    cursor.rowcount = 1

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is True
    assert "berhasil diserahkan" in hasil[1].lower()
    conn.start_transaction.assert_called_once()
    conn.commit.assert_called_once()
    conn.rollback.assert_not_called()
    conn.close.assert_called_once()


@patch(DB)
def test_serahkan_obat_koneksi_gagal(mock_db):
    mock_db.return_value = None

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "koneksi database gagal" in hasil[1].lower()


@patch(DB)
def test_serahkan_obat_ditolak_jika_kunjungan_tidak_ditemukan(mock_db):
    conn, _ = _db(mock_db, fetchone=None)

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "tidak menunggu obat" in hasil[1].lower()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_serahkan_obat_ditolak_jika_resep_kosong(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone={"id_kunjungan": 10},
        fetchall=[]
    )

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "resep tidak ditemukan" in hasil[1].lower()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_serahkan_obat_ditolak_jika_status_resep_berubah(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone={"id_kunjungan": 10},
        fetchall=_data_resep("Diserahkan")
    )

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "status resep sudah berubah" in hasil[1].lower()
    conn.rollback.assert_called_once()


@patch(DB)
def test_serahkan_obat_ditolak_jika_obat_tidak_ditemukan(mock_db):
    conn, cursor = _db(
        mock_db,
        fetchone={"id_kunjungan": 10},
        fetchall=_data_resep()
    )
    cursor.fetchone.side_effect = [
        {"id_kunjungan": 10},
        None
    ]

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "data obat tidak ditemukan" in hasil[1].lower()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_serahkan_obat_ditolak_jika_stok_tidak_cukup(mock_db):
    conn, cursor = _db(
        mock_db,
        fetchone={"id_kunjungan": 10},
        fetchall=_data_resep()
    )
    cursor.fetchone.side_effect = [
        {"id_kunjungan": 10},
        {"nama_obat": "Paracetamol", "stok": 2}
    ]

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "tidak mencukupi" in hasil[1].lower()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_serahkan_obat_error_database(mock_db):
    conn, _ = _db(mock_db, error=Exception("Database error"))

    hasil = _resep().serahkan_obat(10, 2)

    assert hasil[0] is False
    assert "penyerahan obat gagal" in hasil[1].lower()
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()
