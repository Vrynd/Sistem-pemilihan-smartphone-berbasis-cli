"""
Unit test untuk modul perhitungan SAW (calculation_method.py).
Memverifikasi normalisasi, perhitungan preferensi, dan ranking
menggunakan data dari jurnal sebagai referensi.
"""

import unittest
import sys
import os

# Tambahkan root project ke path agar bisa import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.criteria import Kriteria
from src.models.smartphone import Smartphone
from src.services.calculation_method import SAWCalculator


class TestSAWCalculator(unittest.TestCase):
    """Test case untuk SAWCalculator menggunakan data dari jurnal."""

    def setUp(self):
        """Siapkan data test dari jurnal."""
        # Kriteria dari jurnal
        self.kriteria_list = [
            Kriteria("C1", "Harga",          30, "cost"),
            Kriteria("C2", "RAM",             20, "benefit"),
            Kriteria("C3", "Memory Internal", 20, "benefit"),
            Kriteria("C4", "Kamera",          15, "benefit"),
            Kriteria("C5", "Ukuran Layar",    15, "benefit"),
        ]

        # 9 Smartphone dari jurnal
        self.smartphones = [
            Smartphone("A1", "Samsung Galaxy V",          {"C1": 1, "C2": 2, "C3": 1, "C4": 3, "C5": 2}),
            Smartphone("A2", "Samsung Galaxy Grand Prime", {"C1": 2, "C2": 2, "C3": 2, "C4": 4, "C5": 3}),
            Smartphone("A3", "Samsung Galaxy J7",          {"C1": 3, "C2": 2, "C3": 3, "C4": 6, "C5": 3}),
            Smartphone("A4", "Samsung Galaxy J1 Ace",      {"C1": 1, "C2": 2, "C3": 2, "C4": 3, "C5": 2}),
            Smartphone("A5", "Samsung Galaxy J5",          {"C1": 3, "C2": 2, "C3": 2, "C4": 6, "C5": 3}),
            Smartphone("A6", "Xiaomi Redmi 3S",            {"C1": 2, "C2": 4, "C3": 3, "C4": 6, "C5": 3}),
            Smartphone("A7", "Samsung Galaxy A5",          {"C1": 4, "C2": 2, "C3": 3, "C4": 6, "C5": 3}),
            Smartphone("A8", "Oppo F1S",                   {"C1": 3, "C2": 4, "C3": 5, "C4": 6, "C5": 3}),
            Smartphone("A9", "Xiaomi Redmi Note 3",        {"C1": 2, "C2": 4, "C3": 3, "C4": 6, "C5": 3}),
        ]

        self.calculator = SAWCalculator(self.smartphones, self.kriteria_list)

    def test_buat_matriks_keputusan(self):
        """Test matriks keputusan sesuai data jurnal."""
        matriks = self.calculator.buat_matriks_keputusan()

        # Verifikasi ukuran matriks
        self.assertEqual(len(matriks), 9)       # 9 alternatif
        self.assertEqual(len(matriks[0]), 5)    # 5 kriteria

        # Verifikasi beberapa nilai (A1: [1, 2, 1, 3, 2])
        self.assertEqual(matriks[0], [1, 2, 1, 3, 2])
        # A3: [3, 2, 3, 6, 3]
        self.assertEqual(matriks[2], [3, 2, 3, 6, 3])
        # A8: [3, 4, 5, 6, 3]
        self.assertEqual(matriks[7], [3, 4, 5, 6, 3])

    def test_normalisasi_cost(self):
        """Test normalisasi kriteria cost (C1 - Harga)."""
        matriks_normal = self.calculator.normalisasi()

        # C1 (cost): min = 1
        # A1: min/X = 1/1 = 1.0
        self.assertAlmostEqual(matriks_normal[0][0], 1.0, places=4)
        # A2: min/X = 1/2 = 0.5
        self.assertAlmostEqual(matriks_normal[1][0], 0.5, places=4)
        # A3: min/X = 1/3 = 0.3333
        self.assertAlmostEqual(matriks_normal[2][0], 1/3, places=4)
        # A7: min/X = 1/4 = 0.25
        self.assertAlmostEqual(matriks_normal[6][0], 0.25, places=4)

    def test_normalisasi_benefit(self):
        """Test normalisasi kriteria benefit (C2, C3, C4, C5)."""
        matriks_normal = self.calculator.normalisasi()

        # C2 (benefit): max = 4
        # A1: X/max = 2/4 = 0.5
        self.assertAlmostEqual(matriks_normal[0][1], 0.5, places=4)
        # A6: X/max = 4/4 = 1.0
        self.assertAlmostEqual(matriks_normal[5][1], 1.0, places=4)

        # C3 (benefit): max = 5
        # A1: X/max = 1/5 = 0.2
        self.assertAlmostEqual(matriks_normal[0][2], 0.2, places=4)
        # A8: X/max = 5/5 = 1.0
        self.assertAlmostEqual(matriks_normal[7][2], 1.0, places=4)

        # C4 (benefit): max = 6
        # A1: X/max = 3/6 = 0.5
        self.assertAlmostEqual(matriks_normal[0][3], 0.5, places=4)
        # A3: X/max = 6/6 = 1.0
        self.assertAlmostEqual(matriks_normal[2][3], 1.0, places=4)

        # C5 (benefit): max = 3
        # A1: X/max = 2/3 = 0.6667
        self.assertAlmostEqual(matriks_normal[0][4], 2/3, places=4)
        # A2: X/max = 3/3 = 1.0
        self.assertAlmostEqual(matriks_normal[1][4], 1.0, places=4)

    def test_hitung_preferensi(self):
        """Test perhitungan nilai preferensi (Vi)."""
        hasil = self.calculator.hitung_preferensi()

        self.assertEqual(len(hasil), 9)

        # Verifikasi nilai Vi untuk beberapa alternatif
        # Vi dihitung: Vi = Σ(Wj/100 × rij) × 100
        a8 = next(h for h in hasil if h["kode"] == "A8")
        self.assertAlmostEqual(a8["nilai_vi"], 80.0, delta=1.0)

        a6 = next(h for h in hasil if h["kode"] == "A6")
        self.assertAlmostEqual(a6["nilai_vi"], 77.0, delta=1.0)

        a3 = next(h for h in hasil if h["kode"] == "A3")
        self.assertAlmostEqual(a3["nilai_vi"], 62.0, delta=1.0)

    def test_ranking_order(self):
        """Test ranking dari nilai tertinggi ke terendah."""
        ranking = self.calculator.ranking()

        # Verifikasi urutan: nilai harus menurun
        for i in range(len(ranking) - 1):
            self.assertGreaterEqual(
                ranking[i]["nilai_vi"],
                ranking[i + 1]["nilai_vi"],
                f"Ranking tidak terurut pada posisi {i+1} dan {i+2}"
            )

        # A8 (Oppo F1S) harus ranking pertama (Vi tertinggi = 80.0)
        self.assertEqual(ranking[0]["kode"], "A8")

        # Verifikasi ranking number
        for i, item in enumerate(ranking, start=1):
            self.assertEqual(item["ranking"], i)

    def test_ranking_top3(self):
        """Test 3 alternatif teratas berdasarkan perhitungan SAW."""
        ranking = self.calculator.ranking()

        # Top 3: A8 (80.0), A6=A9 (77.0), lalu A4 (65.5)
        self.assertEqual(ranking[0]["kode"], "A8")
        # A6 dan A9 memiliki nilai sama (77.0)
        top3_kodes = {ranking[1]["kode"], ranking[2]["kode"]}
        self.assertTrue(top3_kodes.issubset({"A6", "A9"}))

    def test_data_kosong(self):
        """Test dengan data kosong."""
        calc = SAWCalculator([], self.kriteria_list)
        self.assertEqual(calc.buat_matriks_keputusan(), [])
        self.assertEqual(calc.normalisasi(), [])
        self.assertEqual(calc.hitung_preferensi(), [])
        self.assertEqual(calc.ranking(), [])


class TestKriteria(unittest.TestCase):
    """Test case untuk model Kriteria."""

    def test_create_kriteria(self):
        """Test pembuatan objek Kriteria."""
        kr = Kriteria("C1", "Harga", 30, "cost")
        self.assertEqual(kr.kode, "C1")
        self.assertEqual(kr.nama, "Harga")
        self.assertEqual(kr.bobot, 30)
        self.assertEqual(kr.jenis, "cost")

    def test_jenis_invalid(self):
        """Test validasi jenis kriteria."""
        with self.assertRaises(ValueError):
            Kriteria("C1", "Harga", 30, "invalid")

    def test_to_dict(self):
        """Test konversi ke dictionary."""
        kr = Kriteria("C1", "Harga", 30, "cost")
        d = kr.to_dict()
        self.assertEqual(d["kode"], "C1")
        self.assertEqual(d["nama"], "Harga")
        self.assertEqual(d["bobot"], 30)
        self.assertEqual(d["jenis"], "cost")

    def test_from_dict(self):
        """Test pembuatan dari dictionary."""
        data = {"kode": "C2", "nama": "RAM", "bobot": 20, "jenis": "benefit"}
        kr = Kriteria.from_dict(data)
        self.assertEqual(kr.kode, "C2")
        self.assertEqual(kr.jenis, "benefit")


class TestSmartphone(unittest.TestCase):
    """Test case untuk model Smartphone."""

    def test_create_smartphone(self):
        """Test pembuatan objek Smartphone."""
        sp = Smartphone("A1", "Test Phone", {"C1": 1, "C2": 2})
        self.assertEqual(sp.kode, "A1")
        self.assertEqual(sp.nama, "Test Phone")

    def test_get_set_nilai(self):
        """Test get dan set nilai."""
        sp = Smartphone("A1", "Test", {"C1": 1})
        self.assertEqual(sp.get_nilai("C1"), 1)
        self.assertEqual(sp.get_nilai("C99"), 0)  # default 0

        sp.set_nilai("C1", 5)
        self.assertEqual(sp.get_nilai("C1"), 5)

    def test_to_from_dict(self):
        """Test serialisasi roundtrip."""
        sp = Smartphone("A1", "Test", {"C1": 1, "C2": 2})
        d = sp.to_dict()
        sp2 = Smartphone.from_dict(d)
        self.assertEqual(sp2.kode, sp.kode)
        self.assertEqual(sp2.nama, sp.nama)
        self.assertEqual(sp2.nilai, sp.nilai)


if __name__ == "__main__":
    unittest.main()
