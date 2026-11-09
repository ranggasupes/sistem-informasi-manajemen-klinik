
from unittest.mock import MagicMock, patch

from models.rekam_medis_model import RekamMedisModel


def _db(
    mock_db,
    fetchone="default",
    fetchall=None,
    error=None,
    rowcount=1,
    fetchone_side_effect=None
):
    conn, cursor = MagicMock(), MagicMock()

    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.rowcount = rowcount

    if fetchone_side_effect is not None:
        cursor.fetchone.side_effect = fetchone_side_effect
    elif fetchone != "default":
        cursor.fetchone.return_value = fetchone

    if fetchall is not None:
        cursor.fetchall.return_value = fetchall

    if error:
        cursor.execute.side_effect = error

    return conn, cursor


def _resep(
    jumlah=5,
    dosis="2 kali sehari",
    aturan="Sesudah makan",
    id_obat=1
):
    return {
        "id_obat": id_obat,
        "jumlah": jumlah,
        "dosis": dosis,
        "aturan_pakai": aturan
    }


def _rekam_medis():
    return {"id_kunjungan": 10}


def _obat(stok=100):
    return {"id_obat": 1, "stok": stok}


def _model():
    return RekamMedisModel()


DB = "models.rekam_medis_model.Database.get_connection"


# GET ALL REKAM MEDIS
@patch(DB)
def test_get_all_rekam_medis_berhasil(mock_db):
    conn, cursor = _db(
        mock_db,
        fetchall=[{"id_rekam_medis": 1}]
    )

    hasil = _model().get_all_rekam_medis()

    assert hasil == [{"id_rekam_medis": 1}]
    cursor.execute.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_all_rekam_medis_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert _model().get_all_rekam_medis() == []


@patch(DB)
def test_get_all_rekam_medis_error_database(mock_db):
    conn, cursor = _db(
        mock_db,
        error=Exception("Database error")
    )

    assert _model().get_all_rekam_medis() == []
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# RIWAYAT REKAM MEDIS PASIEN
@patch(DB)
def test_get_history_by_user_id_berhasil(mock_db):
    data = [
        {
            "id_rekam_medis": 25,
            "diagnosis": "Demam"
        }
    ]

    conn, cursor = _db(mock_db, fetchall=data)

    assert _model().get_history_by_user_id(21) == data
    assert cursor.execute.call_args[0][1] == (21,)
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_history_by_user_id_data_kosong(mock_db):
    conn, _ = _db(mock_db, fetchall=[])

    assert _model().get_history_by_user_id(21) == []
    conn.close.assert_called_once()


@patch(DB)
def test_get_history_by_user_id_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert _model().get_history_by_user_id(21) == []


@patch(DB)
def test_get_history_by_user_id_error_database(mock_db):
    conn, cursor = _db(
        mock_db,
        error=Exception("Database error")
    )

    assert _model().get_history_by_user_id(21) == []
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# CREATE REKAM MEDIS DOKTER
@patch(DB)
def test_create_rekam_medis_dokter_berhasil(mock_db):
    conn, cursor = _db(
        mock_db,
        fetchone_side_effect=[
            {"id_kunjungan": 10},
            None
        ]
    )

    cursor.lastrowid = 25

    hasil = _model().create_rekam_medis_dokter(
        10,
        21,
        "120/80",
        36.5,
        55,
        "Demam",
        "Istirahat"
    )

    assert hasil == 25
    assert cursor.execute.call_count == 3
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_create_rekam_medis_dokter_data_opsional_kosong(mock_db):
    _, cursor = _db(
        mock_db,
        fetchone_side_effect=[
            {"id_kunjungan": 10},
            None
        ]
    )

    cursor.lastrowid = 26

    hasil = _model().create_rekam_medis_dokter(
        10,
        21,
        "",
        None,
        0,
        "Demam",
        ""
    )

    assert hasil == 26
    assert cursor.execute.call_args[0][1] == (
        10, None, None, None, "Demam", None
    )


@patch(DB)
def test_create_rekam_medis_dokter_ditolak(mock_db):
    conn, _ = _db(mock_db, fetchone=None)

    hasil = _model().create_rekam_medis_dokter(
        10,
        99,
        "120/80",
        36.5,
        55,
        "Demam",
        "Catatan"
    )

    assert hasil is None
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_create_rekam_medis_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert _model().create_rekam_medis_dokter(
        10,
        21,
        "120/80",
        36.5,
        55,
        "Demam",
        "Catatan"
    ) is None


@patch(DB)
def test_create_rekam_medis_dokter_error_database(mock_db):
    conn, cursor = _db(
        mock_db,
        error=Exception("Database error")
    )

    hasil = _model().create_rekam_medis_dokter(
        10,
        21,
        "120/80",
        36.5,
        55,
        "Demam",
        "Catatan"
    )

    assert hasil is None
    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# CREATE RESEP DOKTER
@patch(DB)
def test_create_resep_dokter_berhasil(mock_db):
    conn, cursor = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat()
        ]
    )

    hasil = _model().create_resep_dokter(
        25,
        21,
        [_resep()]
    )

    assert hasil is True
    assert cursor.execute.call_count == 4
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_create_resep_dokter_daftar_kosong(mock_db):
    conn, _ = _db(mock_db)

    assert _model().create_resep_dokter(
        25,
        21,
        []
    ) is False

    conn.close.assert_called_once()
    conn.commit.assert_not_called()


@patch(DB)
def test_create_resep_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep()]
    ) is False


@patch(DB)
def test_create_resep_dokter_ditolak_jika_dokter_tidak_sesuai(
    mock_db
):
    conn, _ = _db(mock_db, fetchone=None)

    assert _model().create_resep_dokter(
        25,
        99,
        [_resep()]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_ditolak_jika_stok_tidak_cukup(
    mock_db
):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat(stok=2)
        ]
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep(jumlah=5)]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_obat_tidak_ditemukan(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            None
        ]
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep()]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_jumlah_tidak_valid(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat()
        ]
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep(jumlah=0)]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_dosis_kosong(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat()
        ]
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep(dosis="")]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_aturan_pakai_kosong(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat()
        ]
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep(aturan="")]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_obat_duplikat(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat()
        ]
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [
            _resep(id_obat=1),
            _resep(id_obat=1)
        ]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_update_status_gagal(mock_db):
    conn, _ = _db(
        mock_db,
        fetchone_side_effect=[
            {
                "id_rekam_medis": 25,
                "id_kunjungan": 10
            },
            _obat()
        ],
        rowcount=0
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep()]
    ) is False

    conn.rollback.assert_called_once()


@patch(DB)
def test_create_resep_dokter_error_database(mock_db):
    conn, cursor = _db(
        mock_db,
        error=Exception("Database error")
    )

    assert _model().create_resep_dokter(
        25,
        21,
        [_resep()]
    ) is False

    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# SELESAIKAN TANPA RESEP
@patch(DB)
def test_selesaikan_tanpa_resep_berhasil(mock_db):
    conn, cursor = _db(mock_db, rowcount=1)

    hasil = _model().selesaikan_tanpa_resep(25, 21)

    assert hasil is True
    conn.commit.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_selesaikan_tanpa_resep_gagal(mock_db):
    conn, _ = _db(mock_db, rowcount=0)

    hasil = _model().selesaikan_tanpa_resep(25, 21)

    assert hasil is False
    conn.commit.assert_called_once()


@patch(DB)
def test_selesaikan_tanpa_resep_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert _model().selesaikan_tanpa_resep(
        25,
        21
    ) is False


@patch(DB)
def test_selesaikan_tanpa_resep_error_database(mock_db):
    conn, cursor = _db(
        mock_db,
        error=Exception("Database error")
    )

    hasil = _model().selesaikan_tanpa_resep(25, 21)

    assert hasil is False
    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# RIWAYAT REKAM MEDIS DOKTER
@patch(DB)
def test_get_history_by_doctor_id_berhasil(mock_db):
    data = [
        {
            "id_rekam_medis": 25,
            "diagnosis": "Demam"
        }
    ]

    conn, cursor = _db(mock_db, fetchall=data)

    assert _model().get_history_by_doctor_id(21) == data
    assert cursor.execute.call_args[0][1] == (21,)
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_history_by_doctor_id_data_kosong(mock_db):
    conn, _ = _db(mock_db, fetchall=[])

    assert _model().get_history_by_doctor_id(21) == []
    conn.close.assert_called_once()


@patch(DB)
def test_get_history_by_doctor_id_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert _model().get_history_by_doctor_id(21) == []


@patch(DB)
def test_get_history_by_doctor_id_error_database(mock_db):
    conn, cursor = _db(
        mock_db,
        error=Exception("Database error")
    )

    assert _model().get_history_by_doctor_id(21) == []
    cursor.close.assert_called_once()
    conn.close.assert_called_once()
