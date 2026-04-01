# Sistem Pendukung Keputusan Pemilihan Smartphone (Metode SAW)

Aplikasi berbasis CLI (Command Line Interface) yang diimplementasikan menggunakan Python untuk membantu pemilihan smartphone terbaik berdasarkan kriteria tertentu menggunakan metode **Simple Additive Weighting (SAW)**. 

Proyek ini mengacu pada jurnal: *Harsiti & Henri Aprianti (2017). "Sistem Pendukung Keputusan Pemilihan Smartphone dengan Menerapkan Metode Simple Additive Weighting (SAW)". Jurnal Sistem Informasi Volume 4, Agustus 2017.*

## 🚀 Fitur Utama

- **Manajemen Data Smartphone**: Tambah, Lihat, Edit, dan Hapus data smartphone (Alternatif).
- **Manajemen Kriteria**: Lihat kriteria dan sesuaikan bobot kepentingan (Total harus 100%).
- **Perhitungan SAW**:
  - Pembentukan Matriks Keputusan (X).
  - Normalisasi Matriks (R).
  - Perhitungan Nilai Preferensi (Vi).
  - Perangkingan Otomatis.
- **Data Default**: Kemampuan untuk memuat data sampel 9 smartphone dari jurnal referensi.
- **Persistensi Data**: Data tersimpan secara otomatis dalam format JSON.

## 🛠️ Struktur Proyek

```text
Sistem Pemilihan Smartphone/
│
├── main.py                 # Entry point aplikasi
├── requirements.txt        # Dependensi (tabulate, colorama)
├── README.md               # Dokumentasi proyek
│
└── src/
    ├── config/
    │   └── settings.py      # Konfigurasi global & kriteria default
    ├── models/
    │   ├── criteria.py      # Model data Kriteria
    │   └── smartphone.py    # Model data Smartphone
    ├── services/
    │   ├── calculation_method.py  # Logika Inti Algoritma SAW
    │   └── manage_data.py         # Manajemen I/O File JSON
    ├── ui/
    │   ├── helpers.py             # Utilitas tampilan CLI
    │   ├── main_course.py         # Navigasi Menu Utama
    │   ├── menu_smartphone.py     # Menu Kelola Smartphone
    │   ├── criteria_menu.py       # Menu Kelola Kriteria
    │   └── calculation_menu.py    # Menu Proses Perhitungan
    └── data/
        └── default_data.json      # Backup data default jurnal
```

## 📦 Instalasi

1. Pastikan Anda memiliki **Python 3.x** terinstall.
2. Clone atau download repository ini.
3. Install dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Cara Penggunaan

Jalankan aplikasi dengan perintah:
```bash
python main.py
```

### Langkah Singkat:
1. Pilih menu **[4] Muat Data** untuk pertama kali jika ingin menggunakan data dari jurnal.
2. Gunakan menu **[1]** dan **[2]** untuk memodifikasi data jika diperlukan.
3. Pilih menu **[3] Proses Perhitungan** untuk melihat langkah-orang-langkah SAW dan hasil akhir rekomendasi.

## 📐 Metodologi SAW

Metode SAW (Simple Additive Weighting) sering juga dikenal istilah metode penjumlahan terbobot. Konsep dasar metode SAW adalah mencari penjumlahan terbobot dari rating kinerja pada setiap alternatif pada semua atribut.

1. **Normalisasi**:
   - Untuk kriteria **Benefit**: `rij = xij / max(xij)`
   - Untuk kriteria **Cost**: `rij = min(xij) / xij`
2. **Preferensi (Vi)**: `Vi = Σ (wj * rij)`

---
*Dibuat dengan ❤️ menggunakan Python.*
