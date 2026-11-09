from unittest.mock import MagicMock, patch
from models.dokter_model import DokterModel
from controllers.dokter_controller import DokterController


DB = "models.dokter_model.Database.get_connection"

DATA_DOKTER = {
    "id_dokter": 1,
    "id_user": 141,
    "id_poli": 1,
    "nama_dokter": "Dr. Andi Pratama",
    "spesialisasi": "Dokter Spesialis Anak",
    "no_telepon": "081234567801",
    "nama_poli": "Poli Anak"
}


def _db(mock_db, fetchone=None, fetchall=None, error=None):
    conn, cursor = MagicMock(), MagicMock()
    mock_db.return_value = conn
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = fetchone
    cursor.fetchall.return_value = fetchall or []

    if error:
        cursor.execute.side_effect = error

    return conn, cursor


# ==================== PENGUJIAN DOKTER MODEL ====================

@patch(DB)
def test_get_all_dokter(mock_db):
    _, cursor = _db(mock_db, fetchall=[DATA_DOKTER])

    result = DokterModel().get_all_dokter()

    assert len(result) == 1
    assert result[0]["nama_dokter"] == DATA_DOKTER["nama_dokter"]
    cursor.execute.assert_called_once()


@patch(DB)
def test_get_all_dokter_kosong(mock_db):
    _db(mock_db)

    assert DokterModel().get_all_dokter() == []


@patch(DB)
def test_get_all_dokter_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert DokterModel().get_all_dokter() == []


@patch(DB)
def test_get_by_user_id(mock_db):
    _, cursor = _db(mock_db, fetchone=DATA_DOKTER)

    result = DokterModel().get_by_user_id(141)

    assert result["id_user"] == 141
    assert result["nama_dokter"] == DATA_DOKTER["nama_dokter"]
    cursor.execute.assert_called_once()


@patch(DB)
def test_get_by_user_id_tidak_ditemukan(mock_db):
    _db(mock_db)

    assert DokterModel().get_by_user_id(999) is None


@patch(DB)
def test_get_by_user_id_koneksi_gagal(mock_db):
    mock_db.return_value = None

    assert DokterModel().get_by_user_id(141) is None


# ==================== PENGUJIAN DOKTER CONTROLLER ====================

@patch("controllers.dokter_controller.DokterModel")
def test_dokter_controller_daftar_dokter(mock_model):
    mock_model.return_value.get_all_dokter.return_value = [DATA_DOKTER]

    result = DokterController().daftar_dokter()

    assert result == [DATA_DOKTER]
    mock_model.return_value.get_all_dokter.assert_called_once()


@patch("controllers.dokter_controller.DokterModel")
def test_dokter_controller_daftar_dokter_kosong(mock_model):
    mock_model.return_value.get_all_dokter.return_value = []

    result = DokterController().daftar_dokter()

    assert result == []
    mock_model.return_value.get_all_dokter.assert_called_once()


@patch("controllers.dokter_controller.KunjunganModel")
def test_dokter_controller_get_antrean(mock_kunjungan):
    mock_kunjungan.return_value.get_antrean_dokter.return_value = [{"id_kunjungan": 10}]
    
    controller = DokterController()
    controller.kunjungan = mock_kunjungan.return_value
    
    result = controller.get_antrean(141)
    assert len(result) == 1
    controller.kunjungan.get_antrean_dokter.assert_called_once_with(141)


@patch("controllers.dokter_controller.KunjunganModel")
def test_dokter_controller_panggil_pasien(mock_kunjungan):
    controller = DokterController()
    controller.kunjungan = mock_kunjungan.return_value
    
    controller.panggil_pasien(10, 141)
    controller.kunjungan.panggil_pasien.assert_called_once_with(10, 141)


@patch("controllers.dokter_controller.KunjunganModel")
def test_dokter_controller_mulai_pemeriksaan(mock_kunjungan):
    controller = DokterController()
    controller.kunjungan = mock_kunjungan.return_value
    
    controller.mulai_pemeriksaan(10, 141)
    controller.kunjungan.mulai_pemeriksaan.assert_called_once_with(10, 141)


@patch("controllers.dokter_controller.ObatController")
def test_dokter_controller_get_daftar_obat(mock_obat_ctrl):
    mock_obat_ctrl.get_all_obat.return_value = [{"id_obat": 1, "nama_obat": "Paracetamol"}]
    
    result = DokterController().get_daftar_obat()
    assert len(result) == 1
    assert result[0]["nama_obat"] == "Paracetamol"


@patch("controllers.dokter_controller.RekamMedisModel")
def test_dokter_controller_simpan_pemeriksaan(mock_rm):
    controller = DokterController()
    controller.rekam_medis = mock_rm.return_value
    
    data_dummy = {
        "id_kunjungan": 10,
        "tekanan_darah": "120/80",
        "suhu_tubuh": "36.5",
        "berat_badan": "65",
        "diagnosis": "Flu",
        "catatan": "Istirahat cukup"
    }
    
    controller.simpan_pemeriksaan(data_dummy, 141)
    controller.rekam_medis.create_rekam_medis_dokter.assert_called_once()


@patch("controllers.dokter_controller.RekamMedisModel")
def test_dokter_controller_simpan_resep(mock_rm):
    controller = DokterController()
    controller.rekam_medis = mock_rm.return_value
    
    controller.simpan_resep(1, 141, ["Paracetamol"])
    controller.rekam_medis.create_resep_dokter.assert_called_once()


@patch("controllers.dokter_controller.RekamMedisModel")
def test_dokter_controller_selesaikan_tanpa_resep(mock_rm):
    controller = DokterController()
    controller.rekam_medis = mock_rm.return_value
    
    controller.selesaikan_tanpa_resep(1, 141)
    controller.rekam_medis.selesaikan_tanpa_resep.assert_called_once()


@patch("controllers.dokter_controller.RekamMedisModel")
def test_dokter_controller_get_riwayat(mock_rm):
    controller = DokterController()
    controller.rekam_medis = mock_rm.return_value
    
    controller.get_riwayat(141)
    controller.rekam_medis.get_history_by_doctor_id.assert_called_once_with(141)