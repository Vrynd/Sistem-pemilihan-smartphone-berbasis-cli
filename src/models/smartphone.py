"""
Model Smartphone untuk Sistem Pemilihan Smartphone.
Merepresentasikan satu alternatif smartphone beserta nilai kriterianya.
"""


class Smartphone:
    """
    Representasi satu alternatif smartphone dalam metode SAW.

    Attributes:
        kode (str): Kode alternatif, contoh: "A1", "A2"
        nama (str): Nama smartphone, contoh: "Samsung Galaxy J7"
        nilai (dict): Nilai per kriteria, contoh: {"C1": 3, "C2": 2, "C3": 3, "C4": 6, "C5": 3}
    """

    def __init__(self, kode: str, nama: str, nilai: dict):
        self.kode = kode
        self.nama = nama
        self.nilai = nilai  # {"C1": int, "C2": int, ...}

    def get_nilai(self, kode_kriteria: str) -> int:
        """Ambil nilai smartphone untuk kriteria tertentu."""
        return self.nilai.get(kode_kriteria, 0)

    def set_nilai(self, kode_kriteria: str, value: int):
        """Set nilai smartphone untuk kriteria tertentu."""
        self.nilai[kode_kriteria] = value

    def to_dict(self) -> dict:
        """Konversi objek ke dictionary untuk serialisasi JSON."""
        return {
            "kode": self.kode,
            "nama": self.nama,
            "nilai": self.nilai,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Smartphone":
        """Buat objek Smartphone dari dictionary."""
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            nilai=data["nilai"],
        )

    def __repr__(self) -> str:
        return f"Smartphone(kode='{self.kode}', nama='{self.nama}', nilai={self.nilai})"

    def __str__(self) -> str:
        return f"{self.kode} - {self.nama}"
