import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.criteria import Criteria
from src.models.smartphone import Smartphone
from src.services.calculation_method import CalculationMethod


class TestCalculationMethod(unittest.TestCase):
    def setUp(self):
        self.criteria_list = [
            Criteria("C1", "Harga",          30, "cost"),
            Criteria("C2", "RAM",             20, "benefit"),
            Criteria("C3", "Memory Internal", 20, "benefit"),
            Criteria("C4", "Kamera",          15, "benefit"),
            Criteria("C5", "Layar",           15, "benefit"),
        ]

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

        self.calculator = CalculationMethod(self.smartphones, self.criteria_list)

    def test_create_decision_matrix(self):
        matrix = self.calculator.create_decision_matrix()

        self.assertEqual(len(matrix), 9)
        self.assertEqual(len(matrix[0]), 5)

        # A1: [1, 2, 1, 3, 2]
        self.assertEqual(matrix[0], [1, 2, 1, 3, 2])
        # A3: [3, 2, 3, 6, 3]
        self.assertEqual(matrix[2], [3, 2, 3, 6, 3])
        # A8: [3, 4, 5, 6, 3]
        self.assertEqual(matrix[7], [3, 4, 5, 6, 3])

    def test_normalization_cost(self):
        normalized = self.calculator.normalization()

        # C1 (cost): min = 1
        self.assertAlmostEqual(normalized[0][0], 1.0, places=4)      # A1: 1/1
        self.assertAlmostEqual(normalized[1][0], 0.5, places=4)      # A2: 1/2
        self.assertAlmostEqual(normalized[2][0], 1/3, places=4)      # A3: 1/3
        self.assertAlmostEqual(normalized[6][0], 0.25, places=4)     # A7: 1/4

    def test_normalization_benefit(self):
        normalized = self.calculator.normalization()

        # C2 (benefit): max = 4
        self.assertAlmostEqual(normalized[0][1], 0.5, places=4)      # A1: 2/4
        self.assertAlmostEqual(normalized[5][1], 1.0, places=4)      # A6: 4/4

        # C3 (benefit): max = 5
        self.assertAlmostEqual(normalized[0][2], 0.2, places=4)      # A1: 1/5
        self.assertAlmostEqual(normalized[7][2], 1.0, places=4)      # A8: 5/5

        # C4 (benefit): max = 6
        self.assertAlmostEqual(normalized[0][3], 0.5, places=4)      # A1: 3/6
        self.assertAlmostEqual(normalized[2][3], 1.0, places=4)      # A3: 6/6

        # C5 (benefit): max = 3
        self.assertAlmostEqual(normalized[0][4], 2/3, places=4)      # A1: 2/3
        self.assertAlmostEqual(normalized[1][4], 1.0, places=4)      # A2: 3/3

    def test_calculate_preferences(self):
        results = self.calculator.calculate_preferences()

        self.assertEqual(len(results), 9)

        a8 = next(r for r in results if r["kode"] == "A8")
        self.assertAlmostEqual(a8["nilai_vi"], 80.0, delta=1.0)

        a6 = next(r for r in results if r["kode"] == "A6")
        self.assertAlmostEqual(a6["nilai_vi"], 77.0, delta=1.0)

        a3 = next(r for r in results if r["kode"] == "A3")
        self.assertAlmostEqual(a3["nilai_vi"], 62.0, delta=1.0)

    def test_ranking_order(self):
        ranking = self.calculator.ranking()

        # Values must be in descending order
        for i in range(len(ranking) - 1):
            self.assertGreaterEqual(
                ranking[i]["nilai_vi"],
                ranking[i + 1]["nilai_vi"],
                f"Ranking not sorted at position {i+1} and {i+2}"
            )

        # A8 (Oppo F1S) should be ranked first (Vi = 80.0)
        self.assertEqual(ranking[0]["kode"], "A8")

        for i, item in enumerate(ranking, start=1):
            self.assertEqual(item["ranking"], i)

    def test_ranking_top3(self):
        ranking = self.calculator.ranking()

        # Top 3: A8 (80.0), A6=A9 (77.0)
        self.assertEqual(ranking[0]["kode"], "A8")
        top3_codes = {ranking[1]["kode"], ranking[2]["kode"]}
        self.assertTrue(top3_codes.issubset({"A6", "A9"}))

    def test_empty_data(self):
        calc = CalculationMethod([], self.criteria_list)
        self.assertEqual(calc.create_decision_matrix(), [])
        self.assertEqual(calc.normalization(), [])
        self.assertEqual(calc.calculate_preferences(), [])
        self.assertEqual(calc.ranking(), [])


class TestCriteria(unittest.TestCase):
    def test_create_criteria(self):
        cr = Criteria("C1", "Harga", 30, "cost")
        self.assertEqual(cr.kode, "C1")
        self.assertEqual(cr.nama, "Harga")
        self.assertEqual(cr.bobot, 30)
        self.assertEqual(cr.jenis, "cost")

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            Criteria("C1", "Harga", 30, "invalid")

    def test_to_dict(self):
        cr = Criteria("C1", "Harga", 30, "cost")
        d = cr.to_dict()
        self.assertEqual(d["kode"], "C1")
        self.assertEqual(d["nama"], "Harga")
        self.assertEqual(d["bobot"], 30)
        self.assertEqual(d["jenis"], "cost")

    def test_from_dict(self):
        data = {"kode": "C2", "nama": "RAM", "bobot": 20, "jenis": "benefit"}
        cr = Criteria.from_dict(data)
        self.assertEqual(cr.kode, "C2")
        self.assertEqual(cr.jenis, "benefit")


class TestSmartphone(unittest.TestCase):
    def test_create_smartphone(self):
        sp = Smartphone("A1", "Test Phone", {"C1": 1, "C2": 2})
        self.assertEqual(sp.kode, "A1")
        self.assertEqual(sp.nama, "Test Phone")

    def test_get_set_value(self):
        sp = Smartphone("A1", "Test", {"C1": 1})
        self.assertEqual(sp.get_nilai("C1"), 1)
        self.assertEqual(sp.get_nilai("C99"), 0)

        sp.set_nilai("C1", 5)
        self.assertEqual(sp.get_nilai("C1"), 5)

    def test_to_from_dict(self):
        sp = Smartphone("A1", "Test", {"C1": 1, "C2": 2})
        d = sp.to_dict()
        sp2 = Smartphone.from_dict(d)
        self.assertEqual(sp2.kode, sp.kode)
        self.assertEqual(sp2.nama, sp.nama)
        self.assertEqual(sp2.nilai, sp.nilai)


if __name__ == "__main__":
    unittest.main()
