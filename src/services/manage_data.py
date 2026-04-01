"""
Modul manajemen data untuk Sistem Pemilihan Smartphone.
Mengelola baca/tulis data smartphone dan kriteria dari/ke file JSON.
"""

import json
import os

from src.config.settings import (
    DATA_DIR,
    DEFAULT_DATA_FILE,
    KRITERIA_FILE,
    SMARTPHONES_FILE,
)
from src.models.criteria import Kriteria
from src.models.smartphone import Smartphone


class DataManager:
    """
    Mengelola penyimpanan dan pembacaan data dari file JSON.
    """

    def __init__(self):
        """Pastikan direktori data ada."""
        os.makedirs(DATA_DIR, exist_ok=True)

    # ================================================================
    # Smartphone
    # ================================================================

    def simpan_smartphones(self, smartphones: list):
        """
        Simpan daftar smartphone ke file JSON.

        Args:
            smartphones: List objek Smartphone
        """
        data = [sp.to_dict() for sp in smartphones]
        self._tulis_json(SMARTPHONES_FILE, data)

    def muat_smartphones(self) -> list:
        """
        Muat daftar smartphone dari file JSON.

        Returns:
            List objek Smartphone
        """
        data = self._baca_json(SMARTPHONES_FILE)
        if data is None:
            return []
        return [Smartphone.from_dict(item) for item in data]

    # ================================================================
    # Kriteria
    # ================================================================

    def simpan_kriteria(self, kriteria_list: list):
        """
        Simpan daftar kriteria ke file JSON.

        Args:
            kriteria_list: List objek Kriteria
        """
        data = [kr.to_dict() for kr in kriteria_list]
        self._tulis_json(KRITERIA_FILE, data)

    def muat_kriteria(self) -> list:
        """
        Muat daftar kriteria dari file JSON.

        Returns:
            List objek Kriteria
        """
        data = self._baca_json(KRITERIA_FILE)
        if data is None:
            return []
        return [Kriteria.from_dict(item) for item in data]

    # ================================================================
    # Data Default (dari jurnal)
    # ================================================================

    def muat_data_default(self) -> tuple:
        """
        Muat data default dari jurnal (kriteria + smartphone).

        Returns:
            Tuple (list_kriteria, list_smartphone) atau ([], []) jika gagal
        """
        data = self._baca_json(DEFAULT_DATA_FILE)
        if data is None:
            return [], []

        kriteria_list = [Kriteria.from_dict(item) for item in data.get("kriteria", [])]
        smartphone_list = [Smartphone.from_dict(item) for item in data.get("smartphones", [])]

        return kriteria_list, smartphone_list

    def reset_ke_default(self) -> tuple:
        """
        Reset semua data ke data default dari jurnal.
        Muat data default lalu simpan ke file aktif.

        Returns:
            Tuple (list_kriteria, list_smartphone)
        """
        kriteria_list, smartphone_list = self.muat_data_default()

        if kriteria_list:
            self.simpan_kriteria(kriteria_list)
        if smartphone_list:
            self.simpan_smartphones(smartphone_list)

        return kriteria_list, smartphone_list

    # ================================================================
    # Utilitas Internal
    # ================================================================

    def _tulis_json(self, filepath: str, data):
        """Tulis data ke file JSON."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _baca_json(self, filepath: str):
        """Baca data dari file JSON. Return None jika file tidak ada."""
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def data_tersedia(self) -> bool:
        """Cek apakah file data smartphone dan kriteria sudah ada."""
        return (
            os.path.exists(SMARTPHONES_FILE)
            and os.path.exists(KRITERIA_FILE)
        )
