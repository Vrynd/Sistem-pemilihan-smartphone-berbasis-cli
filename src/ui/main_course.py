"""
Menu utama aplikasi Sistem Pemilihan Smartphone.
Navigasi ke seluruh fitur: kelola smartphone, kriteria, perhitungan SAW.
"""

from src.config.settings import APP_DESCRIPTION, APP_NAME, APP_VERSION
from src.services.manage_data import DataManager
from src.ui.calculation_menu import menu_perhitungan
from src.ui.criteria_menu import menu_kriteria
from src.ui.helpers import (
    clear_screen,
    input_pilihan,
    konfirmasi,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_success,
    print_warning,
)
from src.ui.menu_smartphone import menu_smartphone


def jalankan_aplikasi():
    """Entry point utama aplikasi. Menampilkan menu dan memproses pilihan."""

    data_manager = DataManager()

    # Muat data yang tersimpan (jika ada)
    kriteria_list = data_manager.muat_kriteria()
    smartphones = data_manager.muat_smartphones()

    # Jika belum ada data, tawarkan muat data default
    if not data_manager.data_tersedia():
        clear_screen()
        print_header(APP_NAME)
        print_info("Belum ada data tersimpan.")
        if konfirmasi("Muat data default dari jurnal?"):
            kriteria_list, smartphones = data_manager.reset_ke_default()
            print_success(f"Data default berhasil dimuat! ({len(smartphones)} smartphone, {len(kriteria_list)} kriteria)")
            pause()

    # Loop menu utama
    while True:
        clear_screen()
        print_header(APP_NAME)
        print(f"  {APP_DESCRIPTION}")
        print(f"  Versi: {APP_VERSION}")
        print()

        # Status data
        _tampilkan_status(smartphones, kriteria_list)
        print()

        print_menu_item(1, "Kelola Data Smartphone")
        print_menu_item(2, "Kelola Kriteria & Bobot")
        print_menu_item(3, "Proses Perhitungan SAW")
        print_menu_item(4, "Muat Data Default (Jurnal)")
        print_menu_item(5, "Reset Semua Data")
        print_menu_item(0, "Keluar")

        pilihan = input_pilihan()

        if pilihan == "1":
            smartphones = menu_smartphone(data_manager, smartphones, kriteria_list)

        elif pilihan == "2":
            kriteria_list = menu_kriteria(data_manager, kriteria_list)

        elif pilihan == "3":
            menu_perhitungan(smartphones, kriteria_list)

        elif pilihan == "4":
            _muat_default(data_manager, smartphones, kriteria_list)
            # Reload data setelah muat default
            kriteria_list = data_manager.muat_kriteria()
            smartphones = data_manager.muat_smartphones()

        elif pilihan == "5":
            hasil = _reset_data(data_manager)
            if hasil:
                kriteria_list, smartphones = hasil

        elif pilihan == "0":
            clear_screen()
            print_header("TERIMA KASIH")
            print_info("Terima kasih telah menggunakan Sistem Pemilihan Smartphone!")
            print_info("Sampai jumpa! 👋")
            print()
            break

        else:
            print_error("Pilihan tidak valid!")
            pause()


def _tampilkan_status(smartphones, kriteria_list):
    """Tampilkan status data saat ini."""
    sp_count = len(smartphones)
    kr_count = len(kriteria_list)

    if sp_count > 0 and kr_count > 0:
        print(f"  📱 Data Smartphone : {sp_count} smartphone")
        print(f"  📋 Data Kriteria   : {kr_count} kriteria")
    else:
        print_warning("Data belum tersedia. Silakan muat data default (menu 4).")


def _muat_default(data_manager, smartphones, kriteria_list):
    """Muat data default dari jurnal."""
    clear_screen()
    print_header("MUAT DATA DEFAULT")

    if smartphones or kriteria_list:
        print_warning("Sudah ada data tersimpan!")
        print_info("Memuat data default akan MENIMPA data yang ada.")
        if not konfirmasi("Lanjutkan?"):
            print_info("Dibatalkan.")
            pause()
            return

    kriteria_list, smartphones = data_manager.reset_ke_default()
    print_success(f"Data default berhasil dimuat!")
    print_info(f"  → {len(smartphones)} smartphone")
    print_info(f"  → {len(kriteria_list)} kriteria")
    pause()


def _reset_data(data_manager):
    """Reset semua data ke data default."""
    clear_screen()
    print_header("RESET SEMUA DATA")
    print_warning("Semua data smartphone dan kriteria akan direset ke data default jurnal.")

    if konfirmasi("Apakah Anda yakin ingin mereset semua data?"):
        kriteria_list, smartphones = data_manager.reset_ke_default()
        print_success("Semua data berhasil direset ke default!")
        print_info(f"  → {len(smartphones)} smartphone")
        print_info(f"  → {len(kriteria_list)} kriteria")
        pause()
        return kriteria_list, smartphones
    else:
        print_info("Reset dibatalkan.")
        pause()
        return None
