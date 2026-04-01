"""
Sub-menu manajemen kriteria dan bobot.
Lihat kriteria & bobot, ubah bobot dengan validasi total 100%.
"""

from src.ui.helpers import (
    clear_screen,
    input_float,
    input_pilihan,
    konfirmasi,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_success,
    print_tabel_sederhana,
    print_warning,
)


def menu_kriteria(data_manager, kriteria_list):
    """
    Menu utama manajemen kriteria.

    Args:
        data_manager: Objek DataManager
        kriteria_list: List objek Kriteria (mutable)

    Returns:
        List kriteria yang sudah diperbarui
    """
    while True:
        clear_screen()
        print_header("KELOLA KRITERIA & BOBOT")
        print()
        print_menu_item(1, "Lihat Kriteria & Bobot")
        print_menu_item(2, "Ubah Bobot Kriteria")
        print_menu_item(0, "Kembali ke Menu Utama")

        pilihan = input_pilihan()

        if pilihan == "1":
            _lihat_kriteria(kriteria_list)
        elif pilihan == "2":
            kriteria_list = _ubah_bobot(data_manager, kriteria_list)
        elif pilihan == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()

    return kriteria_list


def _lihat_kriteria(kriteria_list):
    """Tampilkan semua kriteria beserta bobotnya."""
    clear_screen()
    print_header("DATA KRITERIA & BOBOT")

    if not kriteria_list:
        print_warning("Belum ada data kriteria. Silakan muat data default.")
        pause()
        return

    headers = ["No", "Kode", "Nama Kriteria", "Bobot (%)", "Jenis"]
    rows = []

    for i, kr in enumerate(kriteria_list, start=1):
        rows.append([i, kr.kode, kr.nama, kr.bobot, kr.jenis.upper()])

    print()
    print_tabel_sederhana(headers, rows)

    total_bobot = sum(kr.bobot for kr in kriteria_list)
    print_info(f"Total Bobot: {total_bobot}%")

    if total_bobot != 100:
        print_warning(f"Total bobot harus 100%! Saat ini: {total_bobot}%")

    pause()


def _ubah_bobot(data_manager, kriteria_list):
    """Ubah bobot setiap kriteria dengan validasi total 100%."""
    clear_screen()
    print_header("UBAH BOBOT KRITERIA")

    if not kriteria_list:
        print_warning("Belum ada data kriteria. Silakan muat data default.")
        pause()
        return kriteria_list

    # Tampilkan bobot saat ini
    print()
    print("  Bobot saat ini:")
    for kr in kriteria_list:
        print(f"    {kr.kode} - {kr.nama}: {kr.bobot}%")

    print()
    print_info("Masukkan bobot baru untuk setiap kriteria.")
    print_info("Total bobot harus berjumlah 100%.")
    print()

    bobot_baru = []
    for kr in kriteria_list:
        bobot = input_float(
            f"Bobot {kr.kode} ({kr.nama}), saat ini {kr.bobot}%",
            min_val=0,
            max_val=100
        )
        bobot_baru.append(bobot)

    # Validasi total
    total = sum(bobot_baru)
    if total != 100:
        print_error(f"Total bobot harus 100%, tetapi total saat ini: {total}%")
        print_info("Perubahan bobot dibatalkan.")
        pause()
        return kriteria_list

    # Konfirmasi perubahan
    print()
    print("  Bobot baru:")
    for kr, bobot in zip(kriteria_list, bobot_baru):
        print(f"    {kr.kode} - {kr.nama}: {kr.bobot}% → {bobot}%")

    if konfirmasi("Simpan perubahan bobot?"):
        for kr, bobot in zip(kriteria_list, bobot_baru):
            kr.bobot = bobot
        data_manager.simpan_kriteria(kriteria_list)
        print_success("Bobot kriteria berhasil diperbarui!")
    else:
        print_info("Perubahan dibatalkan.")

    pause()
    return kriteria_list
