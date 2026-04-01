"""
Sub-menu manajemen data smartphone.
CRUD: Lihat, Tambah, Edit, Hapus smartphone.
"""

from src.config.settings import SUB_KRITERIA
from src.ui.helpers import (
    clear_screen,
    input_angka,
    input_pilihan,
    input_teks,
    konfirmasi,
    pause,
    print_error,
    print_garis,
    print_header,
    print_info,
    print_menu_item,
    print_success,
    print_tabel_sederhana,
    print_warning,
    tampilkan_sub_kriteria,
)


def menu_smartphone(data_manager, smartphones, kriteria_list):
    """
    Menu utama manajemen smartphone.

    Args:
        data_manager: Objek DataManager
        smartphones: List objek Smartphone (mutable / akan dimodifikasi)
        kriteria_list: List objek Kriteria

    Returns:
        List smartphone yang sudah diperbarui
    """
    while True:
        clear_screen()
        print_header("KELOLA DATA SMARTPHONE")
        print()
        print_menu_item(1, "Lihat Semua Smartphone")
        print_menu_item(2, "Tambah Smartphone Baru")
        print_menu_item(3, "Edit Smartphone")
        print_menu_item(4, "Hapus Smartphone")
        print_menu_item(0, "Kembali ke Menu Utama")

        pilihan = input_pilihan()

        if pilihan == "1":
            _lihat_smartphones(smartphones, kriteria_list)
        elif pilihan == "2":
            smartphones = _tambah_smartphone(data_manager, smartphones, kriteria_list)
        elif pilihan == "3":
            smartphones = _edit_smartphone(data_manager, smartphones, kriteria_list)
        elif pilihan == "4":
            smartphones = _hapus_smartphone(data_manager, smartphones)
        elif pilihan == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()

    return smartphones


def _lihat_smartphones(smartphones, kriteria_list):
    """Tampilkan semua data smartphone dalam bentuk tabel."""
    clear_screen()
    print_header("DATA SMARTPHONE")

    if not smartphones:
        print_warning("Belum ada data smartphone. Silakan tambah data atau muat data default.")
        pause()
        return

    # Siapkan header tabel
    headers = ["No", "Kode", "Nama Smartphone"]
    for kr in kriteria_list:
        headers.append(f"{kr.kode}\n({kr.nama})")

    # Siapkan data tabel
    rows = []
    for i, sp in enumerate(smartphones, start=1):
        row = [i, sp.kode, sp.nama]
        for kr in kriteria_list:
            row.append(sp.get_nilai(kr.kode))
        rows.append(row)

    print()
    print_tabel_sederhana(headers, rows)
    print_info(f"Total: {len(smartphones)} smartphone")
    pause()


def _tambah_smartphone(data_manager, smartphones, kriteria_list):
    """Tambah smartphone baru."""
    clear_screen()
    print_header("TAMBAH SMARTPHONE BARU")

    if not kriteria_list:
        print_error("Data kriteria belum tersedia! Silakan muat data default terlebih dahulu.")
        pause()
        return smartphones

    # Generate kode otomatis
    kode_terakhir = 0
    for sp in smartphones:
        try:
            num = int(sp.kode.replace("A", ""))
            kode_terakhir = max(kode_terakhir, num)
        except ValueError:
            pass
    kode_baru = f"A{kode_terakhir + 1}"

    print_info(f"Kode smartphone: {kode_baru}")
    print()

    nama = input_teks("Nama Smartphone")
    if not nama:
        print_error("Nama tidak boleh kosong!")
        pause()
        return smartphones

    # Input nilai untuk setiap kriteria
    nilai = {}
    print()
    print_garis()
    print("  Masukkan nilai untuk setiap kriteria:")
    print_garis()

    for kr in kriteria_list:
        print(f"\n  {kr.kode} - {kr.nama} ({kr.jenis}):")
        tampilkan_sub_kriteria(kr.kode)

        sub = SUB_KRITERIA.get(kr.kode, {})
        if sub:
            min_val = min(sub.keys())
            max_val = max(sub.keys())
            v = input_angka(f"Nilai {kr.kode}", min_val=min_val, max_val=max_val)
        else:
            v = input_angka(f"Nilai {kr.kode}", min_val=1)

        nilai[kr.kode] = v

    # Buat objek smartphone baru
    from src.models.smartphone import Smartphone
    sp_baru = Smartphone(kode=kode_baru, nama=nama, nilai=nilai)
    smartphones.append(sp_baru)

    # Simpan
    data_manager.simpan_smartphones(smartphones)
    print_success(f"Smartphone '{nama}' ({kode_baru}) berhasil ditambahkan!")
    pause()
    return smartphones


def _edit_smartphone(data_manager, smartphones, kriteria_list):
    """Edit data smartphone yang sudah ada."""
    clear_screen()
    print_header("EDIT SMARTPHONE")

    if not smartphones:
        print_warning("Belum ada data smartphone.")
        pause()
        return smartphones

    if not kriteria_list:
        print_error("Data kriteria belum tersedia!")
        pause()
        return smartphones

    # Tampilkan daftar
    print()
    for i, sp in enumerate(smartphones, start=1):
        print(f"  {i}. {sp.kode} - {sp.nama}")

    print()
    idx = input_angka("Pilih nomor smartphone yang ingin diedit", min_val=1, max_val=len(smartphones))
    sp = smartphones[idx - 1]

    print_info(f"Mengedit: {sp.kode} - {sp.nama}")
    print()

    # Edit nama
    nama_baru = input_teks(f"Nama baru (kosongkan jika tidak diubah, saat ini: {sp.nama})")
    if nama_baru:
        sp.nama = nama_baru

    # Edit nilai kriteria
    print()
    print_garis()
    print("  Edit nilai kriteria (kosongkan/0 jika tidak diubah):")
    print_garis()

    for kr in kriteria_list:
        nilai_saat_ini = sp.get_nilai(kr.kode)
        print(f"\n  {kr.kode} - {kr.nama} (saat ini: {nilai_saat_ini}):")
        tampilkan_sub_kriteria(kr.kode)

        try:
            v_str = input(f"  Nilai baru {kr.kode} (Enter = tidak ubah): ").strip()
            if v_str:
                v = int(v_str)
                if v > 0:
                    sp.set_nilai(kr.kode, v)
        except ValueError:
            print_warning("Input tidak valid, nilai tidak diubah.")

    # Simpan
    data_manager.simpan_smartphones(smartphones)
    print_success(f"Smartphone '{sp.nama}' berhasil diperbarui!")
    pause()
    return smartphones


def _hapus_smartphone(data_manager, smartphones):
    """Hapus smartphone dari daftar."""
    clear_screen()
    print_header("HAPUS SMARTPHONE")

    if not smartphones:
        print_warning("Belum ada data smartphone.")
        pause()
        return smartphones

    # Tampilkan daftar
    print()
    for i, sp in enumerate(smartphones, start=1):
        print(f"  {i}. {sp.kode} - {sp.nama}")

    print()
    idx = input_angka("Pilih nomor smartphone yang ingin dihapus", min_val=1, max_val=len(smartphones))
    sp = smartphones[idx - 1]

    if konfirmasi(f"Hapus '{sp.nama}' ({sp.kode})?"):
        smartphones.pop(idx - 1)
        data_manager.simpan_smartphones(smartphones)
        print_success(f"Smartphone '{sp.nama}' berhasil dihapus!")
    else:
        print_info("Penghapusan dibatalkan.")

    pause()
    return smartphones
