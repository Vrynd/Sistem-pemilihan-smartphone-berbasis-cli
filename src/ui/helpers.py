"""
Utilitas tampilan untuk CLI.
Berisi fungsi-fungsi helper untuk menampilkan header, tabel, pesan, dan input.
"""

import os

from src.config.settings import LEBAR_GARIS, SUB_KRITERIA


def clear_screen():
    """Bersihkan layar terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(judul: str):
    """
    Cetak header dengan border.

    Args:
        judul: Teks judul yang akan ditampilkan
    """
    print()
    print("═" * LEBAR_GARIS)
    print(f"  {judul}".center(LEBAR_GARIS))
    print("═" * LEBAR_GARIS)


def print_sub_header(judul: str):
    """Cetak sub-header dengan garis."""
    print()
    print(f"── {judul} " + "─" * (LEBAR_GARIS - len(judul) - 4))


def print_garis():
    """Cetak garis pemisah."""
    print("─" * LEBAR_GARIS)


def print_success(pesan: str):
    """Cetak pesan sukses dengan tanda [✓]."""
    print(f"\n  [✓] {pesan}")


def print_error(pesan: str):
    """Cetak pesan error dengan tanda [✗]."""
    print(f"\n  [✗] {pesan}")


def print_warning(pesan: str):
    """Cetak pesan peringatan dengan tanda [!]."""
    print(f"\n  [!] {pesan}")


def print_info(pesan: str):
    """Cetak pesan informasi dengan tanda [i]."""
    print(f"\n  [i] {pesan}")


def print_menu_item(nomor, teks: str):
    """Cetak satu item menu."""
    print(f"  [{nomor}] {teks}")


def input_pilihan(prompt: str = "Pilih menu") -> str:
    """
    Minta input pilihan menu dari pengguna.

    Returns:
        String input dari pengguna (sudah di-strip)
    """
    print()
    return input(f"  {prompt}: ").strip()


def input_angka(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Minta input angka dari pengguna dengan validasi.

    Args:
        prompt: Teks prompt
        min_val: Nilai minimum yang diperbolehkan
        max_val: Nilai maksimum yang diperbolehkan

    Returns:
        Integer yang valid
    """
    while True:
        try:
            nilai = int(input(f"  {prompt}: "))
            if min_val is not None and nilai < min_val:
                print_error(f"Nilai minimum adalah {min_val}")
                continue
            if max_val is not None and nilai > max_val:
                print_error(f"Nilai maksimum adalah {max_val}")
                continue
            return nilai
        except ValueError:
            print_error("Masukkan angka yang valid!")


def input_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """
    Minta input bilangan desimal dari pengguna dengan validasi.

    Returns:
        Float yang valid
    """
    while True:
        try:
            nilai = float(input(f"  {prompt}: "))
            if min_val is not None and nilai < min_val:
                print_error(f"Nilai minimum adalah {min_val}")
                continue
            if max_val is not None and nilai > max_val:
                print_error(f"Nilai maksimum adalah {max_val}")
                continue
            return nilai
        except ValueError:
            print_error("Masukkan angka yang valid!")


def input_teks(prompt: str) -> str:
    """
    Minta input teks dari pengguna.

    Returns:
        String input (sudah di-strip)
    """
    return input(f"  {prompt}: ").strip()


def konfirmasi(prompt: str = "Apakah Anda yakin?") -> bool:
    """
    Minta konfirmasi ya/tidak dari pengguna.

    Returns:
        True jika ya, False jika tidak
    """
    jawaban = input(f"  {prompt} (y/n): ").strip().lower()
    return jawaban in ("y", "ya", "yes")


def pause():
    """Pause dan tunggu pengguna menekan Enter."""
    input("\n  Tekan Enter untuk melanjutkan...")


def print_tabel_sederhana(headers: list, rows: list, col_widths: list = None):
    """
    Cetak tabel sederhana dengan border.

    Args:
        headers: List string header kolom
        rows: List of list, setiap list adalah satu baris data
        col_widths: Opsional, lebar tiap kolom. Jika None, dihitung otomatis.
    """
    if not col_widths:
        col_widths = []
        for i, header in enumerate(headers):
            max_len = len(str(header))
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(str(row[i])))
            col_widths.append(max_len + 2)

    # Header
    header_line = "│"
    separator_top = "┌"
    separator_mid = "├"
    separator_bot = "└"

    for i, (header, width) in enumerate(zip(headers, col_widths)):
        header_line += f" {str(header).center(width)} │"
        is_last = i == len(headers) - 1
        separator_top += "─" * (width + 2) + ("┐" if is_last else "┬")
        separator_mid += "─" * (width + 2) + ("┤" if is_last else "┼")
        separator_bot += "─" * (width + 2) + ("┘" if is_last else "┴")

    print(f"  {separator_top}")
    print(f"  {header_line}")
    print(f"  {separator_mid}")

    # Rows
    for row in rows:
        row_line = "│"
        for i, width in enumerate(col_widths):
            val = str(row[i]) if i < len(row) else ""
            # Angka rata kanan, teks rata kiri
            if isinstance(row[i], (int, float)):
                row_line += f" {val.rjust(width)} │"
            else:
                row_line += f" {val.ljust(width)} │"
        print(f"  {row_line}")

    print(f"  {separator_bot}")


def tampilkan_sub_kriteria(kode_kriteria: str):
    """
    Tampilkan sub-kriteria (opsi nilai) untuk kriteria tertentu.

    Args:
        kode_kriteria: Kode kriteria, misal "C1"
    """
    sub = SUB_KRITERIA.get(kode_kriteria, {})
    if sub:
        for nilai, deskripsi in sub.items():
            print(f"      {nilai} = {deskripsi}")
