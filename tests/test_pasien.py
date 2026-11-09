
from unittest.mock import patch, MagicMock
from datetime import date as real_date

from models.pasien_model import PasienModel
import controllers.pasien_controller as pasien_module
from controllers.pasien_controller import PasienController


# ==========================================
# TEST PASIEN MODEL
# ==========================================

@patch("models.pasien_model.Database.get_connection")
def test_create_pasien_berhasil(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    model = PasienModel()

    hasil = model.create_pasien(
        id_user=121,
        nomor_bpjs="TEST-BPJS-001",
        nik="TEST-NIK-001",
        nama_pasien="Pasien Uji 01",
        jenis_kelamin="Laki-laki",
        tanggal_lahir="2000-05-15",
        alamat="Alamat Simulasi",
        no_telepon="080000000001"
    )

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("models.pasien_model.Database.get_connection")
def test_create_pasien_koneksi_gagal(mock_get_connection):
    mock_get_connection.return_value = None

    model = PasienModel()

    hasil = model.create_pasien(
        121, "BPJS-001", "NIK-001", "Pasien Uji",
        "Laki-laki", "2000-05-15", "Alamat", "080000000001"
    )

    assert hasil is False


@patch("models.pasien_model.Database.get_connection")
def test_create_pasien_error_database(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    model = PasienModel()

    hasil = model.create_pasien(
        121, "BPJS-001", "NIK-001", "Pasien Uji",
        "Laki-laki", "2000-05-15", "Alamat", "080000000001"
    )

    assert hasil is False
    mock_conn.rollback.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("models.pasien_model.Database.get_connection")
def test_get_all_pasien(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        {
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
    ]

    model = PasienModel()
    data_pasien = model.get_all_pasien()

    assert len(data_pasien) == 1
    assert data_pasien[0]["nama_pasien"] == "Pasien Uji 01"
    mock_cursor.execute.assert_called_once()


@patch("models.pasien_model.Database.get_connection")
def test_get_all_pasien_koneksi_gagal(mock_get_connection):
    mock_get_connection.return_value = None

    model = PasienModel()

    assert model.get_all_pasien() == []


@patch("models.pasien_model.Database.get_connection")
def test_get_all_pasien_data_kosong(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    model = PasienModel()

    hasil = model.get_all_pasien()

    assert hasil == []
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("models.pasien_model.Database.get_connection")
def test_get_all_pasien_error_database(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    model = PasienModel()

    hasil = model.get_all_pasien()

    assert hasil == []
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("models.pasien_model.Database.get_connection")
def test_get_pasien_by_user_id_berhasil(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    data_pasien = {
        "id_pasien": 1,
        "id_user": 121,
        "nama_pasien": "Pasien Uji"
    }

    mock_cursor.fetchone.return_value = data_pasien

    model = PasienModel()

    hasil = model.get_pasien_by_user_id(121)

    assert hasil == data_pasien
    mock_cursor.execute.assert_called_once()
    assert mock_cursor.execute.call_args[0][1] == (121,)
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("models.pasien_model.Database.get_connection")
def test_get_pasien_by_user_id_tidak_ditemukan(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    model = PasienModel()

    hasil = model.get_pasien_by_user_id(999)

    assert hasil is None


@patch("models.pasien_model.Database.get_connection")
def test_get_pasien_by_user_id_koneksi_gagal(mock_get_connection):
    mock_get_connection.return_value = None

    model = PasienModel()

    assert model.get_pasien_by_user_id(121) is None


@patch("models.pasien_model.Database.get_connection")
def test_get_pasien_by_user_id_error_database(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    model = PasienModel()

    hasil = model.get_pasien_by_user_id(121)

    assert hasil is None
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ==========================================
# HELPER TEST CONTROLLER
# ==========================================

def buat_controller(monkeypatch):
    mock_pasien = MagicMock()
    mock_profil = MagicMock()
    mock_kunjungan = MagicMock()
    mock_rekam_medis = MagicMock()

    monkeypatch.setattr(
        pasien_module, "PasienModel", lambda: mock_pasien
    )
    monkeypatch.setattr(
        pasien_module, "ProfilKesehatanModel", lambda: mock_profil
    )
    monkeypatch.setattr(
        pasien_module, "KunjunganModel", lambda: mock_kunjungan
    )
    monkeypatch.setattr(
        pasien_module, "RekamMedisModel", lambda: mock_rekam_medis
    )

    controller = PasienController()

    return (
        controller,
        mock_pasien,
        mock_profil,
        mock_kunjungan,
        mock_rekam_medis
    )


# ==========================================
# TEST DASHBOARD PASIEN
# ==========================================

def test_get_dashboard_data_berhasil(monkeypatch):
    controller, mock_pasien, mock_profil, _, _ = (
        buat_controller(monkeypatch)
    )

    data_pasien = {
        "id_pasien": 1,
        "nama_pasien": "Pasien Uji"
    }
    data_profil = {"alergi": "Tidak ada"}

    mock_pasien.get_pasien_by_user_id.return_value = data_pasien
    mock_profil.get_by_pasien_id.return_value = data_profil

    pasien, profil = controller.get_dashboard_data(121)

    assert pasien == data_pasien
    assert profil == data_profil
    mock_pasien.get_pasien_by_user_id.assert_called_once_with(121)
    mock_profil.get_by_pasien_id.assert_called_once_with(1)


def test_get_dashboard_data_pasien_tidak_ditemukan(monkeypatch):
    controller, mock_pasien, mock_profil, _, _ = (
        buat_controller(monkeypatch)
    )

    mock_pasien.get_pasien_by_user_id.return_value = None

    pasien, profil = controller.get_dashboard_data(999)

    assert pasien is None
    assert profil is None
    mock_profil.get_by_pasien_id.assert_not_called()


# ==========================================
# TEST ANTREAN DAN RIWAYAT MEDIS
# ==========================================

def test_get_antrean_aktif(monkeypatch):
    controller, _, _, mock_kunjungan, _ = (
        buat_controller(monkeypatch)
    )

    data_antrean = [{"nomor_antrian": 3}]
    mock_kunjungan.get_active_by_user_id.return_value = data_antrean

    hasil = controller.get_antrean_aktif(121)

    assert hasil == data_antrean
    mock_kunjungan.get_active_by_user_id.assert_called_once_with(121)


def test_get_riwayat_medis(monkeypatch):
    controller, _, _, _, mock_rekam = (
        buat_controller(monkeypatch)
    )

    data_riwayat = [{"diagnosis": "Demam"}]
    mock_rekam.get_history_by_user_id.return_value = data_riwayat

    hasil = controller.get_riwayat_medis(121)

    assert hasil == data_riwayat
    mock_rekam.get_history_by_user_id.assert_called_once_with(121)


# ==========================================
# TEST PENENTUAN POLI
# ==========================================

def test_tentukan_poli_anak(monkeypatch):
    controller, *_ = buat_controller(monkeypatch)

    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)

    hasil = controller.tentukan_poli(real_date(2015, 5, 10))

    assert hasil == (1, "Poli Anak")


def test_tentukan_poli_umum(monkeypatch):
    controller, *_ = buat_controller(monkeypatch)

    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)

    hasil = controller.tentukan_poli(real_date(2000, 5, 10))

    assert hasil == (2, "Poli Umum")


def test_tentukan_poli_lansia(monkeypatch):
    controller, *_ = buat_controller(monkeypatch)

    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)

    hasil = controller.tentukan_poli(real_date(1960, 5, 10))

    assert hasil == (3, "Poli Lansia")


def test_tentukan_poli_tanggal_lahir_kosong(monkeypatch):
    controller, *_ = buat_controller(monkeypatch)

    hasil = controller.tentukan_poli(None)

    assert hasil == (
        None,
        "Tanggal lahir pasien belum tersedia."
    )


def test_tentukan_poli_tanggal_lahir_masa_depan(monkeypatch):
    controller, *_ = buat_controller(monkeypatch)

    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)

    hasil = controller.tentukan_poli(real_date(2030, 1, 1))

    assert hasil == (None, "Tanggal lahir tidak valid.")


# ==========================================
# TEST PENDAFTARAN KUNJUNGAN
# ==========================================

def test_daftar_kunjungan_pasien_tidak_ditemukan(monkeypatch):
    controller, mock_pasien, _, mock_kunjungan, _ = (
        buat_controller(monkeypatch)
    )

    mock_pasien.get_pasien_by_user_id.return_value = None

    berhasil, pesan, data = controller.daftar_kunjungan(
        999, "Demam"
    )

    assert berhasil is False
    assert pesan == "Data pasien tidak ditemukan."
    assert data is None
    mock_kunjungan.create_kunjungan.assert_not_called()


def test_daftar_kunjungan_keluhan_kosong(monkeypatch):
    controller, mock_pasien, _, mock_kunjungan, _ = (
        buat_controller(monkeypatch)
    )

    mock_pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1,
        "tanggal_lahir": real_date(2000, 5, 10)
    }

    berhasil, pesan, data = controller.daftar_kunjungan(
        121, "   "
    )

    assert berhasil is False
    assert pesan == "Keluhan awal harus diisi."
    assert data is None
    mock_kunjungan.create_kunjungan.assert_not_called()


def test_daftar_kunjungan_masih_memiliki_antrean(monkeypatch):
    controller, mock_pasien, _, mock_kunjungan, _ = (
        buat_controller(monkeypatch)
    )

    mock_pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1,
        "tanggal_lahir": real_date(2000, 5, 10)
    }

    antrean = {
        "id_kunjungan": 10,
        "status": "Menunggu"
    }
    mock_kunjungan.get_active_by_user_id.return_value = antrean

    berhasil, pesan, data = controller.daftar_kunjungan(
        121, "Demam"
    )

    assert berhasil is False
    assert "kunjungan aktif" in pesan
    assert data == antrean
    mock_kunjungan.create_kunjungan.assert_not_called()


def test_daftar_kunjungan_berhasil(monkeypatch):
    controller, mock_pasien, _, mock_kunjungan, _ = (
        buat_controller(monkeypatch)
    )

    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)

    mock_pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1,
        "tanggal_lahir": real_date(2000, 5, 10)
    }

    mock_kunjungan.get_active_by_user_id.return_value = None
    mock_kunjungan.create_kunjungan.return_value = {
        "id_kunjungan": 15,
        "nomor_antrian": 4
    }

    berhasil, pesan, data = controller.daftar_kunjungan(
        121, "  Demam  "
    )

    assert berhasil is True
    assert pesan == "Pendaftaran kunjungan berhasil."
    assert data["id_kunjungan"] == 15
    assert data["nomor_antrian"] == 4
    assert data["nama_poli"] == "Poli Umum"
    assert data["tanggal_kunjungan"] == real_date(2026, 11, 9)
    assert data["status"] == "Menunggu"

    mock_kunjungan.create_kunjungan.assert_called_once_with(
        id_pasien=1,
        id_poli=2,
        id_dokter=None,
        tanggal_kunjungan=real_date(2026, 11, 9),
        keluhan_awal="Demam"
    )


def test_daftar_kunjungan_gagal_dari_model(monkeypatch):
    controller, mock_pasien, _, mock_kunjungan, _ = (
        buat_controller(monkeypatch)
    )

    mock_date = MagicMock()
    mock_date.today.return_value = real_date(2026, 11, 9)
    monkeypatch.setattr(pasien_module, "date", mock_date)

    mock_pasien.get_pasien_by_user_id.return_value = {
        "id_pasien": 1,
        "tanggal_lahir": real_date(2000, 5, 10)
    }

    mock_kunjungan.get_active_by_user_id.return_value = None
    mock_kunjungan.create_kunjungan.return_value = None

    berhasil, pesan, data = controller.daftar_kunjungan(
        121, "Demam"
    )

    assert berhasil is False
    assert "Pendaftaran gagal" in pesan
    assert data is None
