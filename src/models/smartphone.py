class Smartphone:
    # Inisialisasi objek Smartphone
    def __init__(self, kode: str, nama: str, nilai: dict):
        self.kode = kode
        self.nama = nama
        self.nilai = nilai 

    # Ambil nilai smartphone untuk kriteria tertentu    
    def get_nilai(self, kode_kriteria: str) -> int:
        return self.nilai.get(kode_kriteria, 0)

    # Set nilai smartphone untuk kriteria tertentu
    def set_nilai(self, kode_kriteria: str, value: int):
        self.nilai[kode_kriteria] = value

    # Konversi objek ke dictionary untuk serialisasi JSON
    def to_dict(self) -> dict:
        return {
            "kode": self.kode,
            "nama": self.nama,
            "nilai": self.nilai,
        }

    # Buat objek Smartphone dari dictionary
    @classmethod
    def from_dict(cls, data: dict) -> "Smartphone":
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            nilai=data["nilai"],
        )

    # Representasi string untuk debugging
    def __repr__(self) -> str:
        return f"Smartphone(kode='{self.kode}', nama='{self.nama}', nilai={self.nilai})"

    # Representasi string untuk output user-friendly
    def __str__(self) -> str:
        return f"{self.kode} - {self.nama}"
