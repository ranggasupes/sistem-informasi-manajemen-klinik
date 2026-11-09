
from unittest.mock import MagicMock, patch

from models.rekam_medis_model import RekamMedisModel


# =========================================================
# GET ALL REKAM MEDIS
# =========================================================

@patch("models.rekam_medis_model.Database.get_connection")
def test_get_all_rekam_medis_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = [
        {
            "id_rekam_medis": 1,
            "id_kunjungan": 10,
            "nama_pasien": "Pasien Uji",
            "diagnosis": "Demam"
        }
    ]
    cursor.fetchall.return_value = data

    model = RekamMedisModel()
    hasil = model.get_all_rekam_medis()

    assert hasil == data
    cursor.execute.assert_called_once()
    conn.close.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_get_all_rekam_medis_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = RekamMedisModel()

    assert model.get_all_rekam_medis() == []


@patch("models.rekam_medis_model.Database.get_connection")
def test_get_all_rekam_medis_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = RekamMedisModel()
    hasil = model.get_all_rekam_medis()

    assert hasil == []
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# CREATE REKAM MEDIS
# =========================================================

@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    model = RekamMedisModel()

    hasil = model.create_rekam_medis(
        10, "120/80", 36.5, 55, "Demam", "Istirahat cukup"
    )

    assert hasil is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_data_opsional_kosong(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    model = RekamMedisModel()

    hasil = model.create_rekam_medis(
        10, "", None, 0, "Demam", ""
    )

    assert hasil is True

    values = cursor.execute.call_args[0][1]

    assert values == (
        10,
        None,
        None,
        None,
        "Demam",
        None
    )

    conn.commit.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = RekamMedisModel()

    hasil = model.create_rekam_medis(
        10, "120/80", 36.5, 55, "Demam", "Catatan"
    )

    assert hasil is False


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = RekamMedisModel()

    hasil = model.create_rekam_medis(
        10, "120/80", 36.5, 55, "Demam", "Catatan"
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# GET HISTORY BY USER ID
# =========================================================

@patch("models.rekam_medis_model.Database.get_connection")
def test_get_history_by_user_id_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    data = [
        {
            "id_rekam_medis": 25,
            "id_kunjungan": 10,
            "nomor_antrian": 3,
            "nama_poli": "Poli Umum",
            "nama_dokter": "Dokter Uji",
            "diagnosis": "Demam"
        }
    ]
    cursor.fetchall.return_value = data

    model = RekamMedisModel()
    hasil = model.get_history_by_user_id(21)

    assert hasil == data
    cursor.execute.assert_called_once()

    values = cursor.execute.call_args[0][1]
    assert values == (21,)

    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_get_history_by_user_id_data_kosong(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchall.return_value = []

    model = RekamMedisModel()
    hasil = model.get_history_by_user_id(21)

    assert hasil == []
    conn.close.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_get_history_by_user_id_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = RekamMedisModel()

    assert model.get_history_by_user_id(21) == []


@patch("models.rekam_medis_model.Database.get_connection")
def test_get_history_by_user_id_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = RekamMedisModel()
    hasil = model.get_history_by_user_id(21)

    assert hasil == []
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# CREATE REKAM MEDIS DOKTER
# =========================================================

@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_dokter_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.return_value = {
        "id_kunjungan": 10
    }
    cursor.lastrowid = 25

    model = RekamMedisModel()

    hasil = model.create_rekam_medis_dokter(
        10, 21, "120/80", 36.5, 55, "Demam", "Istirahat"
    )

    assert hasil == 25
    assert cursor.execute.call_count == 2
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_dokter_data_opsional_kosong(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.return_value = {
        "id_kunjungan": 10
    }
    cursor.lastrowid = 26

    model = RekamMedisModel()

    hasil = model.create_rekam_medis_dokter(
        10, 21, "", None, 0, "Demam", ""
    )

    assert hasil == 26

    values = cursor.execute.call_args[0][1]

    assert values == (
        10,
        None,
        None,
        None,
        "Demam",
        None
    )


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_dokter_ditolak(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    model = RekamMedisModel()

    hasil = model.create_rekam_medis_dokter(
        10, 99, "120/80", 36.5, 55, "Demam", "Catatan"
    )

    assert hasil is None
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = RekamMedisModel()

    hasil = model.create_rekam_medis_dokter(
        10, 21, "120/80", 36.5, 55, "Demam", "Catatan"
    )

    assert hasil is None


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_rekam_medis_dokter_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = RekamMedisModel()

    hasil = model.create_rekam_medis_dokter(
        10, 21, "120/80", 36.5, 55, "Demam", "Catatan"
    )

    assert hasil is None
    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# CREATE RESEP DOKTER
# =========================================================

@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {
            "id_rekam_medis": 25,
            "id_kunjungan": 10
        },
        {
            "id_obat": 1,
            "stok": 100
        }
    ]
    cursor.rowcount = 1

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 10,
            "dosis": "3 kali sehari",
            "aturan_pakai": "Sesudah makan"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is True
    assert cursor.execute.call_count == 4
    conn.commit.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_daftar_kosong(mock_db):
    conn = MagicMock()
    mock_db.return_value = conn

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(25, 21, [])

    assert hasil is False
    conn.commit.assert_not_called()
    conn.close.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = RekamMedisModel()

    assert model.create_resep_dokter(25, 21, []) is False


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_ditolak_jika_dokter_tidak_sesuai(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25,
        99,
        [
            {
                "id_obat": 1,
                "jumlah": 5,
                "dosis": "2 kali sehari",
                "aturan_pakai": "Sesudah makan"
            }
        ]
    )

    assert hasil is False
    conn.rollback.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_ditolak_jika_stok_tidak_cukup(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {
            "id_rekam_medis": 25,
            "id_kunjungan": 10
        },
        {
            "id_obat": 1,
            "stok": 5
        }
    ]

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 10,
            "dosis": "3 kali sehari",
            "aturan_pakai": "Sesudah makan"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_obat_tidak_ditemukan(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {
            "id_rekam_medis": 25,
            "id_kunjungan": 10
        },
        None
    ]

    daftar_resep = [
        {
            "id_obat": 99,
            "jumlah": 5,
            "dosis": "2 kali sehari",
            "aturan_pakai": "Sesudah makan"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_jumlah_tidak_valid(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = {
        "id_rekam_medis": 25,
        "id_kunjungan": 10
    }

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 0,
            "dosis": "2 kali sehari",
            "aturan_pakai": "Sesudah makan"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_dosis_kosong(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = {
        "id_rekam_medis": 25,
        "id_kunjungan": 10
    }

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 5,
            "dosis": "   ",
            "aturan_pakai": "Sesudah makan"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_aturan_pakai_kosong(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = {
        "id_rekam_medis": 25,
        "id_kunjungan": 10
    }

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 5,
            "dosis": "2 kali sehari",
            "aturan_pakai": "   "
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_obat_duplikat(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {
            "id_rekam_medis": 25,
            "id_kunjungan": 10
        },
        {
            "id_obat": 1,
            "stok": 100
        }
    ]

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 5,
            "dosis": "2 kali sehari",
            "aturan_pakai": "Sesudah makan"
        },
        {
            "id_obat": 1,
            "jumlah": 3,
            "dosis": "1 kali sehari",
            "aturan_pakai": "Sebelum tidur"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_update_status_gagal(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        {
            "id_rekam_medis": 25,
            "id_kunjungan": 10
        },
        {
            "id_obat": 1,
            "stok": 100
        }
    ]
    cursor.rowcount = 0

    daftar_resep = [
        {
            "id_obat": 1,
            "jumlah": 5,
            "dosis": "2 kali sehari",
            "aturan_pakai": "Sesudah makan"
        }
    ]

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25, 21, daftar_resep
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch("models.rekam_medis_model.Database.get_connection")
def test_create_resep_dokter_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = RekamMedisModel()

    hasil = model.create_resep_dokter(
        25,
        21,
        [
            {
                "id_obat": 1,
                "jumlah": 5,
                "dosis": "2 kali sehari",
                "aturan_pakai": "Sesudah makan"
            }
        ]
    )

    assert hasil is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


# =========================================================
# SELESAIKAN KUNJUNGAN TANPA RESEP
# =========================================================

@patch("models.rekam_medis_model.Database.get_connection")
def test_selesaikan_tanpa_resep_berhasil(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.rowcount = 1

    model = RekamMedisModel()

    hasil = model.selesaikan_tanpa_resep(25, 21)

    assert hasil is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_selesaikan_tanpa_resep_gagal(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.rowcount = 0

    model = RekamMedisModel()

    hasil = model.selesaikan_tanpa_resep(25, 99)

    assert hasil is False
    conn.commit.assert_called_once()


@patch("models.rekam_medis_model.Database.get_connection")
def test_selesaikan_tanpa_resep_koneksi_gagal(mock_db):
    mock_db.return_value = None

    model = RekamMedisModel()

    hasil = model.selesaikan_tanpa_resep(25, 21)

    assert hasil is False


@patch("models.rekam_medis_model.Database.get_connection")
def test_selesaikan_tanpa_resep_error_database(mock_db):
    conn = MagicMock()
    cursor = MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("Database error")

    model = RekamMedisModel()

    hasil = model.selesaikan_tanpa_resep(25, 21)

    assert hasil is False
    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()
