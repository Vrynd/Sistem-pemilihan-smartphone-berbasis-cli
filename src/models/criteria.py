class Criteria:
    JENIS_VALID = ("cost", "benefit")

    # Inisialisasi objek Kriteria
    def __init__(self, kode: str, nama: str, bobot: float, jenis: str):
        self.kode = kode
        self.nama = nama
        self.bobot = bobot
        self.jenis = jenis.lower()

        # Validasi jenis kriteria
        if self.jenis not in self.JENIS_VALID:
            raise ValueError(
                f"Jenis kriteria harus 'cost' atau 'benefit', bukan '{jenis}'"
            )

    # Konversi objek ke dictionary untuk serialisasi JSON
    def to_dict(self) -> dict:
        return {
            "kode": self.kode,
            "nama": self.nama,
            "bobot": self.bobot,
            "jenis": self.jenis,
        }

    # Buat objek Kriteria dari dictionary
    @classmethod
    def from_dict(cls, data: dict) -> "Kriteria":
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            bobot=data["bobot"],
            jenis=data["jenis"],
        )

    # Representasi string untuk debugging
    def __repr__(self) -> str:
        return (
            f"Kriteria(kode='{self.kode}', nama='{self.nama}', "
            f"bobot={self.bobot}, jenis='{self.jenis}')"
        )

    # Representasi string untuk output user-friendly
    def __str__(self) -> str:
        return f"{self.kode} - {self.nama} (Bobot: {self.bobot}%, Jenis: {self.jenis})"
