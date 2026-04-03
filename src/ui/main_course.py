import datetime
from src.config.settings import APP_DESCRIPTION, APP_NAME, APP_VERSION
from src.services.manage_data import DataManager
from src.services.calculation_method import CalculationMethod
from src.ui.calculation_menu import calculation_menu
from src.ui.criteria_menu import criteria_menu
from src.ui.helpers import (
    clear_screen,
    confirm,
    input_choice,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_success,
    print_warning,
)
from src.ui.menu_smartphone import smartphone_menu
from src.models.user_preference import UserPreference
from src.ui.preference_menu import preference_menu


def run_app():
    data_manager = DataManager()
    user_preference = UserPreference()
    last_calculated_time = None

    criteria_list = data_manager.load_criteria()
    smartphones = data_manager.load_smartphones()

    # Offer to load default data if no data exists
    if not data_manager.is_data_available():
        clear_screen()
        print_header(APP_NAME)
        print_info("Belum ada data tersimpan.")
        if confirm("Muat data default dari jurnal?"):
            criteria_list, smartphones = data_manager.reset_to_default()
            print_success(f"Data default berhasil dimuat! ({len(smartphones)} smartphone, {len(criteria_list)} kriteria)")
            pause()

    # Main menu loop
    while True:
        clear_screen()
        print_header(APP_NAME)
        print(f"  {APP_DESCRIPTION}")
        print(f"  Versi: {APP_VERSION}")
        print()

        _show_status(smartphones, criteria_list, user_preference, last_calculated_time)
        print()

        print_menu_item(1, "Proses Perhitungan")
        print_menu_item(2, "Preferensi")
        print_menu_item(3, "Pengaturan")
        print_menu_item(4, "Keluar")

        choice = input_choice()

        if choice == "1":
            calculation_menu(smartphones, criteria_list, user_preference)
            last_calculated_time = datetime.datetime.now()

        elif choice == "2":
            user_preference = preference_menu(user_preference, criteria_list)
            # Opsional: Jika user ganti preferensi, asumsi kalkulasi hangus / harus diulang
            last_calculated_time = None

        elif choice == "3":
            smartphones, criteria_list = _data_management_menu(data_manager, smartphones, criteria_list)
            last_calculated_time = None

        elif choice == "4" or choice == "0":
            clear_screen()
            print_header("TERIMA KASIH")
            print_info("Terima kasih telah menggunakan Sistem Pemilihan Smartphone!")
            print_info("Sampai jumpa!")
            print()
            break

        else:
            print_error("Pilihan tidak valid!")
            pause()

def _data_management_menu(data_manager, smartphones, criteria_list):
    while True:
        clear_screen()
        print_header("PENGATURAN")
        print()
        print_menu_item(1, "Data Smartphone")
        print_menu_item(2, "Kriteria & Bobot")
        print_menu_item(3, "Muat Data")
        print_menu_item(4, "Reset Data")
        print_menu_item(0, "Kembali")

        choice = input_choice()

        if choice == "1":
            smartphones = smartphone_menu(data_manager, smartphones, criteria_list)
        elif choice == "2":
            criteria_list = criteria_menu(data_manager, criteria_list)
        elif choice == "3":
            _load_default(data_manager, smartphones, criteria_list)
            criteria_list = data_manager.load_criteria()
            smartphones = data_manager.load_smartphones()
        elif choice == "4":
            result = _reset_data(data_manager)
            if result:
                criteria_list, smartphones = result
        elif choice == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()

    return smartphones, criteria_list


def _show_status(smartphones, criteria_list, user_preference, last_calculated_time):
    sp_count = len(smartphones)
    cr_count = len(criteria_list)

    if sp_count > 0 and cr_count > 0:
        print(f"  📱 Data Smartphone : {sp_count} smartphone")
        print(f"  📋 Data Kriteria   : {cr_count} kriteria")
        if user_preference.is_active:
            print(f"  🧑 Preferensi User : {user_preference}")
            
        # Calculate Highlights Dashboard
        calc = CalculationMethod(smartphones, criteria_list, user_preference)
        ranking = calc.ranking() if calc.smartphones else []
        
        top_name = ranking[0]['nama'] if ranking else "Tidak Tersedia"
        
        if calc.smartphones:
            # C1 is Cost (1 is cheapest class)
            termurah = min(calc.smartphones, key=lambda x: x.get_nilai("C1")).nama
            # C2 & C3 are Benefit (RAM & Memory)
            terkuat = max(calc.smartphones, key=lambda x: x.get_nilai("C2") + x.get_nilai("C3")).nama
        else:
            termurah = "Tidak Tersedia"
            terkuat = "Tidak Tersedia"
            
        print()
        print("  📊 HIGHLIGHTS DASHBOARD")
        
        # Tampilkan Informasi Waktu Kalkulasi
        if last_calculated_time:
            time_str = last_calculated_time.strftime("%d-%m-%Y %H:%M:%S")
            print(f"  🕒 Terakhir Dihitung : {time_str}")
            print(f"  🏆 Rekomendasi Top   : \033[93m{top_name}\033[0m")
        else:
            print("  🕒 Terakhir Dihitung : (Belum Pernah / Perlu Hitung Ulang)")
            print(f"  🏆 Rekomendasi Top   : (Tunggu Kalkulasi...)")
            
        print(f"  💰 Harga Termurah    : {termurah}")
        print(f"  ⚡ Performa Tertinggi: {terkuat}")
        
    else:
        print_warning("Data belum tersedia. Silakan muat data default (menu 5).")


def _load_default(data_manager, smartphones, criteria_list):
    clear_screen()
    print_header("MUAT DATA DEFAULT")

    if smartphones or criteria_list:
        print_warning("Sudah ada data tersimpan!")
        print_info("Memuat data default akan MENIMPA data yang ada.")
        if not confirm("Lanjutkan?"):
            print_info("Dibatalkan.")
            pause()
            return

    criteria_list, smartphones = data_manager.reset_to_default()
    print_success("Data default berhasil dimuat!")
    print_info(f"  → {len(smartphones)} smartphone")
    print_info(f"  → {len(criteria_list)} kriteria")
    pause()


def _reset_data(data_manager):
    clear_screen()
    print_header("RESET SEMUA DATA")
    print_warning("Semua data smartphone dan kriteria akan DIHAPUS.")

    if confirm("Apakah Anda yakin ingin menghapus semua data?"):
        data_manager.clear_all_data()
        print_success("Semua data berhasil dihapus!")
        pause()
        return [], []
    else:
        print_info("Reset dibatalkan.")
        pause()
        return None

