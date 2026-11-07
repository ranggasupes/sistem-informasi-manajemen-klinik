import pytest
from unittest.mock import patch, MagicMock
from models.obat_model import ObatModel

@patch("models.obat_model.get_db_connection")
def test_tambah_obat_berhasil(mock_get_db):
    # Setup mock connection & cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Eksekusi fungsi
    result = ObatModel.tambah_obat("Paracetamol", "Tablet", "Strip", 50)

    # Verifikasi
    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()