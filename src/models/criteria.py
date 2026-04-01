"""
Model Kriteria untuk Sistem Pemilihan Smartphone.
Merepresentasikan satu kriteria penilaian (misal: Harga, RAM, dll).
"""


class Kriteria:
    """
    Representasi satu kriteria dalam metode SAW.

    Attributes:
        kode (str): Kode kriteria, contoh: "C1", "C2"
        nama (str): Nama kriteria, contoh: "Harga", "RAM"
        bobot (float): Bobot preferensi (dalam persen, total harus 100)
        jenis (str): Jenis kriteria - "cost" atau "benefit"
    """

    JENIS_VALID = ("cost", "benefit")

    def __init__(self, kode: str, nama: str, bobot: float, jenis: str):
        self.kode = kode
        self.nama = nama
        self.bobot = bobot
        self.jenis = jenis.lower()

        if self.jenis not in self.JENIS_VALID:
            raise ValueError(
                f"Jenis kriteria harus 'cost' atau 'benefit', bukan '{jenis}'"
            )

    def to_dict(self) -> dict:
        """Konversi objek ke dictionary untuk serialisasi JSON."""
        return {
            "kode": self.kode,
            "nama": self.nama,
            "bobot": self.bobot,
            "jenis": self.jenis,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Kriteria":
        """Buat objek Kriteria dari dictionary."""
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            bobot=data["bobot"],
            jenis=data["jenis"],
        )

    def __repr__(self) -> str:
        return (
            f"Kriteria(kode='{self.kode}', nama='{self.nama}', "
            f"bobot={self.bobot}, jenis='{self.jenis}')"
        )

    def __str__(self) -> str:
        return f"{self.kode} - {self.nama} (Bobot: {self.bobot}%, Jenis: {self.jenis})"
