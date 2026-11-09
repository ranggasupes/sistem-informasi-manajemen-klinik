from unittest.mock import MagicMock, patch

from controllers.admin_controller import AdminController


@patch("controllers.admin_controller.ResepModel")
@patch("controllers.admin_controller.ObatController")
def test_get_dashboard_data_berhasil(mock_obat, mock_resep):
    resep = MagicMock()
    mock_resep.return_value = resep

    resep.get_antrean_resep.return_value = [
        {"id_kunjungan": 1},
        {"id_kunjungan": 1},
        {"id_kunjungan": 2}
    ]

    resep.get_riwayat_penyerahan.return_value = [
        {"id_resep": 1},
        {"id_resep": 2}
    ]

    mock_obat.get_all_obat.return_value = [
        {"id_obat": 1},
        {"id_obat": 2},
        {"id_obat": 3}
    ]

    controller = AdminController()
    hasil = controller.get_dashboard_data()

    assert hasil == {
        "jumlah_antrean": 2,
        "jumlah_obat": 3,
        "jumlah_riwayat": 2
    }


@patch("controllers.admin_controller.ResepModel")
def test_get_antrean_resep(mock_resep):
    resep = mock_resep.return_value
    data = [{"id_resep": 1}]

    resep.get_antrean_resep.return_value = data

    controller = AdminController()
    hasil = controller.get_antrean_resep()

    assert hasil == data
    resep.get_antrean_resep.assert_called_once()


@patch("controllers.admin_controller.ResepModel")
def test_serahkan_obat(mock_resep):
    resep = mock_resep.return_value
    resep.serahkan_obat.return_value = (
        True,
        "Obat berhasil diserahkan."
    )

    controller = AdminController()
    hasil = controller.serahkan_obat(10, 2)

    assert hasil[0] is True
    resep.serahkan_obat.assert_called_once_with(10, 2)


@patch("controllers.admin_controller.ObatController.get_all_obat")
def test_get_data_obat(mock_get):
    data = [{"id_obat": 1, "nama_obat": "Paracetamol"}]
    mock_get.return_value = data

    controller = AdminController()
    hasil = controller.get_data_obat()

    assert hasil == data
    mock_get.assert_called_once()


@patch("controllers.admin_controller.ObatController.tambah_obat")
def test_tambah_obat(mock_tambah):
    mock_tambah.return_value = True

    controller = AdminController()
    hasil = controller.tambah_obat(
        "Paracetamol", "Tablet", "Strip", 20
    )

    assert hasil is True
    mock_tambah.assert_called_once_with(
        "Paracetamol", "Tablet", "Strip", 20
    )


@patch("controllers.admin_controller.ObatController.update_obat")
def test_update_obat(mock_update):
    mock_update.return_value = True

    controller = AdminController()
    hasil = controller.update_obat(
        1, "Paracetamol", "Tablet", "Strip", 30
    )

    assert hasil is True
    mock_update.assert_called_once_with(
        1, "Paracetamol", "Tablet", "Strip", 30
    )


@patch("controllers.admin_controller.ObatController.hapus_obat")
def test_hapus_obat(mock_hapus):
    mock_hapus.return_value = True

    controller = AdminController()
    hasil = controller.hapus_obat(1)

    assert hasil is True
    mock_hapus.assert_called_once_with(1)


@patch("controllers.admin_controller.ObatController.cari_obat")
def test_cari_obat(mock_cari):
    data = [{"id_obat": 1, "nama_obat": "Paracetamol"}]
    mock_cari.return_value = data

    controller = AdminController()
    hasil = controller.cari_obat("Paracetamol")

    assert hasil == data
    mock_cari.assert_called_once_with("Paracetamol")


@patch("controllers.admin_controller.ResepModel")
def test_get_riwayat_penyerahan(mock_resep):
    resep = mock_resep.return_value
    data = [{"id_resep": 1}]

    resep.get_riwayat_penyerahan.return_value = data

    controller = AdminController()
    hasil = controller.get_riwayat_penyerahan()

    assert hasil == data
    resep.get_riwayat_penyerahan.assert_called_once()