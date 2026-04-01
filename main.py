"""
Sistem Pemilihan Smartphone
Aplikasi Sistem Pendukung Keputusan untuk membantu memilih smartphone
berdasarkan kriteria menggunakan metode Simple Additive Weighting (SAW).

Referensi:
    Harsiti & Henri Aprianti (2017). Sistem Pendukung Keputusan Pemilihan
    Smartphone dengan Menerapkan Metode Simple Additive Weighting (SAW).
    Jurnal Sistem Informasi Volume 4, Agustus 2017.
"""

import sys
import os

# Tambahkan root project ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_course import jalankan_aplikasi


def main():
    try:
        jalankan_aplikasi()
    except KeyboardInterrupt:
        print("\n\n  Program dihentikan oleh pengguna. Sampai jumpa! 👋\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
