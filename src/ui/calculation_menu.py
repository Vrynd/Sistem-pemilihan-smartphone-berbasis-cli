"""
Sub-menu perhitungan dan perankingan SAW.
Tampilkan matriks keputusan, normalisasi, dan hasil ranking.
"""

from src.services.calculation_method import SAWCalculator
from src.ui.helpers import (
    clear_screen,
    input_pilihan,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_sub_header,
    print_tabel_sederhana,
    print_warning,
)


def menu_perhitungan(smartphones, kriteria_list):
    """
    Menu utama perhitungan SAW.

    Args:
        smartphones: List objek Smartphone
        kriteria_list: List objek Kriteria
    """
    while True:
        clear_screen()
        print_header("PERHITUNGAN METODE SAW")
        print()
        print_menu_item(1, "Tampilkan Matriks Keputusan")
        print_menu_item(2, "Tampilkan Matriks Normalisasi")
        print_menu_item(3, "Tampilkan Hasil Perhitungan & Ranking")
        print_menu_item(4, "Tampilkan Semua (Lengkap)")
        print_menu_item(0, "Kembali ke Menu Utama")

        pilihan = input_pilihan()

        if pilihan == "1":
            _tampilkan_matriks_keputusan(smartphones, kriteria_list)
        elif pilihan == "2":
            _tampilkan_matriks_normalisasi(smartphones, kriteria_list)
        elif pilihan == "3":
            _tampilkan_ranking(smartphones, kriteria_list)
        elif pilihan == "4":
            _tampilkan_semua(smartphones, kriteria_list)
        elif pilihan == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()


def _cek_data(smartphones, kriteria_list) -> bool:
    """Cek apakah data cukup untuk perhitungan."""
    if not smartphones:
        print_warning("Belum ada data smartphone! Silakan tambah data atau muat data default.")
        pause()
        return False
    if not kriteria_list:
        print_warning("Belum ada data kriteria! Silakan muat data default.")
        pause()
        return False
    return True


def _tampilkan_matriks_keputusan(smartphones, kriteria_list):
    """Tampilkan matriks keputusan (X)."""
    clear_screen()
    print_header("MATRIKS KEPUTUSAN (X)")

    if not _cek_data(smartphones, kriteria_list):
        return

    calc = SAWCalculator(smartphones, kriteria_list)
    matriks = calc.buat_matriks_keputusan()

    # Siapkan tabel
    headers = ["Alternatif"] + [f"{kr.kode}" for kr in kriteria_list]
    rows = []
    for i, sp in enumerate(smartphones):
        row = [f"{sp.kode} ({sp.nama})"]
        row.extend(matriks[i])
        rows.append(row)

    print()
    print_tabel_sederhana(headers, rows)

    # Tampilkan keterangan kriteria
    print_info("Keterangan Kriteria:")
    for kr in kriteria_list:
        print(f"    {kr.kode} = {kr.nama} ({kr.jenis}, bobot: {kr.bobot}%)")

    pause()


def _tampilkan_matriks_normalisasi(smartphones, kriteria_list):
    """Tampilkan matriks normalisasi (R)."""
    clear_screen()
    print_header("MATRIKS NORMALISASI (R)")

    if not _cek_data(smartphones, kriteria_list):
        return

    calc = SAWCalculator(smartphones, kriteria_list)
    matriks_normal = calc.normalisasi()

    # Siapkan tabel
    headers = ["Alternatif"] + [f"{kr.kode}" for kr in kriteria_list]
    rows = []
    for i, sp in enumerate(smartphones):
        row = [f"{sp.kode} ({sp.nama})"]
        row.extend([f"{val:.4f}" for val in matriks_normal[i]])
        rows.append(row)

    print()
    print_tabel_sederhana(headers, rows)

    print_info("Rumus normalisasi:")
    print("    Cost:    rij = min(kolom j) / Xij")
    print("    Benefit: rij = Xij / max(kolom j)")

    pause()


def _tampilkan_ranking(smartphones, kriteria_list):
    """Tampilkan hasil perhitungan dan ranking."""
    clear_screen()
    print_header("HASIL PERHITUNGAN & RANKING")

    if not _cek_data(smartphones, kriteria_list):
        return

    calc = SAWCalculator(smartphones, kriteria_list)
    ranking = calc.ranking()

    # Siapkan tabel
    headers = ["Ranking", "Kode", "Nama Smartphone", "Nilai (Vi)"]
    rows = []
    for item in ranking:
        rows.append([
            item["ranking"],
            item["kode"],
            item["nama"],
            f"{item['nilai_vi']:.3f}",
        ])

    print()
    print_tabel_sederhana(headers, rows)

    # Tampilkan rekomendasi
    if ranking:
        terbaik = ranking[0]
        print()
        print("  ╔══════════════════════════════════════════════════════╗")
        print("  ║                  REKOMENDASI TERBAIK                ║")
        print("  ╠══════════════════════════════════════════════════════╣")
        print(f"  ║  {terbaik['nama']:<40}        ║")
        print(f"  ║  Kode: {terbaik['kode']}  |  Nilai Vi: {terbaik['nilai_vi']:.3f}               ║")
        print("  ╚══════════════════════════════════════════════════════╝")

    pause()


def _tampilkan_semua(smartphones, kriteria_list):
    """Tampilkan semua langkah perhitungan SAW secara lengkap."""
    clear_screen()
    print_header("PERHITUNGAN SAW LENGKAP")

    if not _cek_data(smartphones, kriteria_list):
        return

    calc = SAWCalculator(smartphones, kriteria_list)

    # ── Langkah 1: Bobot Kriteria ──
    print_sub_header("LANGKAH 1: Bobot Kriteria (W)")
    headers_kr = ["Kode", "Nama", "Bobot (%)", "Jenis"]
    rows_kr = [[kr.kode, kr.nama, kr.bobot, kr.jenis.upper()] for kr in kriteria_list]
    print()
    print_tabel_sederhana(headers_kr, rows_kr)

    # ── Langkah 2: Matriks Keputusan (X) ──
    matriks = calc.buat_matriks_keputusan()
    print_sub_header("LANGKAH 2: Matriks Keputusan (X)")
    headers_x = ["Alternatif"] + [kr.kode for kr in kriteria_list]
    rows_x = []
    for i, sp in enumerate(smartphones):
        row = [f"{sp.kode}"]
        row.extend(matriks[i])
        rows_x.append(row)
    print()
    print_tabel_sederhana(headers_x, rows_x)

    # ── Langkah 3: Normalisasi (R) ──
    matriks_normal = calc.normalisasi()
    print_sub_header("LANGKAH 3: Matriks Normalisasi (R)")
    headers_r = ["Alternatif"] + [kr.kode for kr in kriteria_list]
    rows_r = []
    for i, sp in enumerate(smartphones):
        row = [f"{sp.kode}"]
        row.extend([f"{val:.4f}" for val in matriks_normal[i]])
        rows_r.append(row)
    print()
    print_tabel_sederhana(headers_r, rows_r)

    # ── Langkah 4: Perhitungan Preferensi ──
    print_sub_header("LANGKAH 4: Perhitungan Nilai Preferensi (Vi)")
    print()
    print("  Rumus: Vi = Σ(Wj × rij)")
    print()

    ranking = calc.ranking()
    preferensi = calc.hitung_preferensi()

    # Tampilkan detail perhitungan per alternatif
    for i, sp in enumerate(smartphones):
        detail_parts = []
        for j, kr in enumerate(kriteria_list):
            wj = kr.bobot / 100.0
            rij = matriks_normal[i][j]
            detail_parts.append(f"({wj}×{rij:.4f})")
        vi = preferensi[i]["nilai_vi"]
        formula = " + ".join(detail_parts)
        print(f"  V{sp.kode} = {formula}")
        print(f"  V{sp.kode} = {vi:.4f}")
        print()

    # ── Langkah 5: Ranking ──
    print_sub_header("LANGKAH 5: Hasil Ranking")
    headers_rank = ["Ranking", "Kode", "Nama Smartphone", "Nilai (Vi)"]
    rows_rank = []
    for item in ranking:
        rows_rank.append([
            item["ranking"],
            item["kode"],
            item["nama"],
            f"{item['nilai_vi']:.3f}",
        ])
    print()
    print_tabel_sederhana(headers_rank, rows_rank)

    # Rekomendasi
    if ranking:
        terbaik = ranking[0]
        print()
        print("  ╔══════════════════════════════════════════════════════╗")
        print("  ║                  REKOMENDASI TERBAIK                ║")
        print("  ╠══════════════════════════════════════════════════════╣")
        print(f"  ║  {terbaik['nama']:<40}        ║")
        print(f"  ║  Kode: {terbaik['kode']}  |  Nilai Vi: {terbaik['nilai_vi']:.3f}               ║")
        print("  ╚══════════════════════════════════════════════════════╝")

    pause()
