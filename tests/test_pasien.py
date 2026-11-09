
from unittest.mock import patch, MagicMock
from datetime import date as real_date

from models.pasien_model import PasienModel
import controllers.pasien_controller as pasien_module
from controllers.pasien_controller import PasienController


DB = "models.pasien_model.Database.get_connection"


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


def _data_pasien():
    return {
        "id_pasien": 1,
        "id_user": 121,
        "nomor_bpjs": "TEST-BPJS-001",
        "nik": "TEST-NIK-001",
        "nama_pasien": "Pasien Uji 01",
        "jenis_kelamin": "Laki-laki",
        "tanggal_lahir": "2000-05-15",
        "alamat": "Alamat Simulasi",
        "no_telepon": "080000000001"
    }


def _buat_controller(monkeypatch):
    mocks = [MagicMock() for _ in range(4)]
    for nama, mock in zip(
        ("PasienModel", "ProfilKesehatanModel",
         "KunjunganModel", "RekamMedisModel"), mocks
    ):
        monkeypatch.setattr(pasien_module, nama, lambda m=mock: m)

    return (PasienController(), *mocks)


def _atur_tanggal(monkeypatch):
    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)


# MODEL PASIEN

@patch(DB)
def test_create_pasien_berhasil(mock_db):
    conn, cursor = _db(mock_db)
    assert PasienModel().create_pasien(
        121, "TEST-BPJS-001", "TEST-NIK-001", "Pasien Uji 01",
        "Laki-laki", "2000-05-15", "Alamat Simulasi", "080000000001"
    ) is True
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_create_pasien_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert PasienModel().create_pasien(
        121, "BPJS-001", "NIK-001", "Pasien Uji",
        "Laki-laki", "2000-05-15", "Alamat", "080000000001"
    ) is False


@patch(DB)
def test_create_pasien_error_database(mock_db):
    conn, cursor = _db(mock_db, error=Exception("Database error"))
    assert PasienModel().create_pasien(
        121, "BPJS-001", "NIK-001", "Pasien Uji",
        "Laki-laki", "2000-05-15", "Alamat", "080000000001"
    ) is False
    conn.rollback.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_all_pasien(mock_db):
    _, cursor = _db(mock_db, fetchall=[_data_pasien()])
    hasil = PasienModel().get_all_pasien()
    assert len(hasil) == 1
    assert hasil[0]["nama_pasien"] == "Pasien Uji 01"
    cursor.execute.assert_called_once()


@patch(DB)
def test_get_all_pasien_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert PasienModel().get_all_pasien() == []


@patch(DB)
def test_get_all_pasien_data_kosong(mock_db):
    conn, cursor = _db(mock_db, fetchall=[])
    assert PasienModel().get_all_pasien() == []
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_all_pasien_error_database(mock_db):
    conn, cursor = _db(mock_db, error=Exception("Database error"))
    assert PasienModel().get_all_pasien() == []
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_pasien_by_user_id_berhasil(mock_db):
    data = {"id_pasien": 1, "id_user": 121, "nama_pasien": "Pasien Uji"}
    conn, cursor = _db(mock_db, fetchone=data)
    assert PasienModel().get_pasien_by_user_id(121) == data
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == (121,)
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


@patch(DB)
def test_get_pasien_by_user_id_tidak_ditemukan(mock_db):
    _db(mock_db, fetchone=None)
    assert PasienModel().get_pasien_by_user_id(999) is None


@patch(DB)
def test_get_pasien_by_user_id_koneksi_gagal(mock_db):
    mock_db.return_value = None
    assert PasienModel().get_pasien_by_user_id(121) is None


@patch(DB)
def test_get_pasien_by_user_id_error_database(mock_db):
    conn, cursor = _db(mock_db, error=Exception("Database error"))
    assert PasienModel().get_pasien_by_user_id(121) is None
    cursor.close.assert_called_once()
    conn.close.assert_called_once()


# CONTROLLER PASIEN

def test_get_dashboard_data_berhasil(monkeypatch):
    controller, pasien, profil, *_ = _buat_controller(monkeypatch)
    data, kesehatan = _data_pasien(), {"alergi": "Tidak ada"}
    pasien.get_pasien_by_user_id.return_value = data
    profil.get_by_pasien_id.return_value = kesehatan

    hasil = controller.get_dashboard_data(121)
    assert hasil == (data, kesehatan)
    pasien.get_pasien_by_user_id.assert_called_once_with(121)
    profil.get_by_pasien_id.assert_called_once_with(1)


def test_get_dashboard_data_pasien_tidak_ditemukan(monkeypatch):
    controller, pasien, profil, *_ = _buat_controller(monkeypatch)
    pasien.get_pasien_by_user_id.return_value = None

    assert controller.get_dashboard_data(999) == (None, None)
    profil.get_by_pasien_id.assert_not_called()


def test_get_antrean_aktif(monkeypatch):
    controller, _, _, kunjungan, _ = _buat_controller(monkeypatch)
    data = [{"nomor_antrian": 3}]
    kunjungan.get_active_by_user_id.return_value = data

    assert controller.get_antrean_aktif(121) == data
    kunjungan.get_active_by_user_id.assert_called_once_with(121)


def test_get_riwayat_medis(monkeypatch):
    controller, _, _, _, rekam = _buat_controller(monkeypatch)
    data = [{"diagnosis": "Demam"}]
    rekam.get_history_by_user_id.return_value = data

    assert controller.get_riwayat_medis(121) == data
    rekam.get_history_by_user_id.assert_called_once_with(121)


# PENENTUAN POLI

def test_tentukan_poli_anak(monkeypatch):
    controller, *_ = _buat_controller(monkeypatch)
    _atur_tanggal(monkeypatch)
    assert controller.tentukan_poli(real_date(2015, 5, 10)) == (1, "Poli Anak")


def test_tentukan_poli_umum(monkeypatch):
    controller, *_ = _buat_controller(monkeypatch)
    _atur_tanggal(monkeypatch)
    assert controller.tentukan_poli(real_date(2000, 5, 10)) == (2, "Poli Umum")


def test_tentukan_poli_lansia(monkeypatch):
    controller, *_ = _buat_controller(monkeypatch)
    _atur_tanggal(monkeypatch)
    assert controller.tentukan_poli(real_date(1960, 5, 10)) == (3, "Poli Lansia")


def test_tentukan_poli_tanggal_lahir_kosong(monkeypatch):
    controller, *_ = _buat_controller(monkeypatch)
    assert controller.tentukan_poli(None) == (
        None, "Tanggal lahir pasien belum tersedia."
    )


def test_tentukan_poli_tanggal_lahir_masa_depan(monkeypatch):
    controller, *_ = _buat_controller(monkeypatch)
    _atur_tanggal(monkeypatch)
    assert controller.tentukan_poli(real_date(2030, 1, 1)) == (
        None, "Tanggal lahir tidak valid."
    )


# PENDAFTARAN KUNJUNGAN

def test_daftar_kunjungan_pasien_tidak_ditemukan(monkeypatch):
    controller, pasien, _, kunjungan, _ = _buat_controller(monkeypatch)
    pasien.get_pasien_by_user_id.return_value = None

    hasil = controller.daftar_kunjungan(999, "Demam")
    assert hasil == (False, "Data pasien tidak ditemukan.", None)
    kunjungan.create_kunjungan.assert_not_called()


def test_daftar_kunjungan_keluhan_kosong(monkeypatch):
    controller, pasien, _, kunjungan, _ = _buat_controller(monkeypatch)
    pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1, "tanggal_lahir": real_date(2000, 5, 10)
    }

    hasil = controller.daftar_kunjungan(121, "   ")
    assert hasil == (False, "Keluhan awal harus diisi.", None)
    kunjungan.create_kunjungan.assert_not_called()


def test_daftar_kunjungan_masih_memiliki_antrean(monkeypatch):
    controller, pasien, _, kunjungan, _ = _buat_controller(monkeypatch)
    pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1, "tanggal_lahir": real_date(2000, 5, 10)
    }
    antrean = {"id_kunjungan": 10, "status": "Menunggu"}
    kunjungan.get_active_by_user_id.return_value = antrean

    berhasil, pesan, data = controller.daftar_kunjungan(121, "Demam")
    assert berhasil is False
    assert "kunjungan aktif" in pesan
    assert data == antrean
    kunjungan.create_kunjungan.assert_not_called()


def test_daftar_kunjungan_berhasil(monkeypatch):
    controller, pasien, _, kunjungan, _ = _buat_controller(monkeypatch)
    _atur_tanggal(monkeypatch)
    pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1, "tanggal_lahir": real_date(2000, 5, 10)
    }
    kunjungan.get_active_by_user_id.return_value = None
    kunjungan.create_kunjungan.return_value = {
        "id_kunjungan": 15, "nomor_antrian": 4
    }

    berhasil, pesan, data = controller.daftar_kunjungan(121, "  Demam  ")
    assert berhasil is True
    assert pesan == "Pendaftaran kunjungan berhasil."
    assert data["id_kunjungan"] == 15
    assert data["nomor_antrian"] == 4
    assert data["nama_poli"] == "Poli Umum"
    assert data["tanggal_kunjungan"] == real_date(2026, 11, 9)
    assert data["status"] == "Menunggu"
    kunjungan.create_kunjungan.assert_called_once_with(
        id_pasien=1, id_poli=2, id_dokter=None,
        tanggal_kunjungan=real_date(2026, 11, 9),
        keluhan_awal="Demam"
    )


def test_daftar_kunjungan_gagal_dari_model(monkeypatch):
    controller, pasien, _, kunjungan, _ = _buat_controller(monkeypatch)
    _atur_tanggal(monkeypatch)
    pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1, "tanggal_lahir": real_date(2000, 5, 10)
    }
    kunjungan.get_active_by_user_id.return_value = None
    kunjungan.create_kunjungan.return_value = None

    berhasil, pesan, data = controller.daftar_kunjungan(121, "Demam")
    assert berhasil is False
    assert "Pendaftaran gagal" in pesan
    assert data is None
