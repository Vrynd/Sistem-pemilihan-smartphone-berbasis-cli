import os

# Informasi Aplikasi
APP_NAME = "Sistem Pemilihan Smartphone"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistem Pendukung Keputusan Pemilihan Smartphone dengan Metode SAW"

# Path File Data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SMARTPHONES_FILE = os.path.join(DATA_DIR, "smartphones.json")
KRITERIA_FILE = os.path.join(DATA_DIR, "kriteria.json")
DEFAULT_DATA_FILE = os.path.join(DATA_DIR, "default_data.json")

# Kriteria Default (dari jurnal)
DEFAULT_KRITERIA = [
    {"kode": "C1", "nama": "Harga",             "bobot": 30, "jenis": "cost"},
    {"kode": "C2", "nama": "RAM",               "bobot": 20, "jenis": "benefit"},
    {"kode": "C3", "nama": "Memory Internal",   "bobot": 20, "jenis": "benefit"},
    {"kode": "C4", "nama": "Kamera",            "bobot": 15, "jenis": "benefit"},
    {"kode": "C5", "nama": "Layar",      "bobot": 15, "jenis": "benefit"},
]

# Sub-Kriteria (konversi nilai dari jurnal)
SUB_KRITERIA = {
    "C1": {  # Harga (cost)
        1: "< Rp 1.000.000",
        2: "Rp 1.000.000 - Rp 2.000.000",
        3: "Rp 2.000.000 - Rp 3.000.000",
        4: "Rp 3.000.000 - Rp 4.000.000",
        5: "Rp 4.000.000 - Rp 5.000.000",
        6: "> Rp 5.000.000",
    },
    "C2": {  # RAM (benefit)
        1: "512 MB",
        2: "1 GB",
        3: "2 GB",
        4: "3 GB atau lebih",
    },
    "C3": {  # Memory Internal (benefit)
        1: "4 GB",
        2: "8 GB",
        3: "16 GB",
        4: "32 GB",
        5: "64 GB",
    },
    "C4": {  # Kamera (benefit)
        1: "2 MP",
        2: "5 MP",
        3: "8 MP",
        4: "12 MP",
        5: "13 MP",
        6: "16 MP atau lebih",
    },
    "C5": {  # Layar (benefit)
        1: "< 4 inci",
        2: "4 - 5 inci",
        3: "> 5 inci",
    },
}

# Command Line Interface
LEBAR_GARIS = 80
