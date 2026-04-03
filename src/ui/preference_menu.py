from src.config.settings import SUB_KRITERIA, WEIGHT_TEMPLATES
from src.ui.helpers import (
    clear_screen,
    input_choice,
    input_number,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_separator,
    print_success,
    show_sub_criteria,
)

def preference_menu(user_preference, criteria_list):
    while True:
        clear_screen()
        print_header("PREFERENSI PENGGUNA")
        print()
        print_info(f"Status Preferensi Saat Ini: {user_preference}")
        print_separator()
        print()
        
        print_menu_item(1, "Harga Maksimal")
        print_menu_item(2, "Minimal RAM")
        print_menu_item(3, "Profil Kebutuhan")
        print_menu_item(4, "Reset Preferensi")
        print_menu_item(0, "Kembali")

        choice = input_choice()

        if choice == "1":
            _set_price_constraint(user_preference)
        elif choice == "2":
            _set_ram_constraint(user_preference)
        elif choice == "3":
            _apply_profile_template(user_preference, criteria_list)
        elif choice == "4":
            user_preference.reset()
            print_success("Preferensi berhasil direset!")
            pause()
        elif choice == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()

    return user_preference

def _set_price_constraint(user_preference):
    clear_screen()
    print_header("BATAS HARGA MAKSIMAL")
    print_info("Pilih level harga maksimal yang sesuai dengan budget Anda:")
    print()
    
    show_sub_criteria("C1")
    sub_c1 = SUB_KRITERIA.get("C1", {})
    if not sub_c1:
        print_error("Data sub-kriteria harga tidak ditemukan!")
        pause()
        return

    print_info("Ketik 0 untuk membatalkan.")
    print()
    
    level = input_number("Pilih tingkat harga maksimal", min_val=0, max_val=max(sub_c1.keys()))
    
    if level == 0:
        print_info("Batal mengubah batas harga.")
    else:
        user_preference.set_price_constraint(level)
        print_success(f"Batas harga disimpan (Level {level}). Smartphone di atas harga ini tidak akan direkomendasikan.")
    
    pause()

def _set_ram_constraint(user_preference):
    clear_screen()
    print_header("MINIMAL RAM")
    print_info("Pilih kapasitas RAM minimal yang Anda inginkan:")
    print()
    
    show_sub_criteria("C2")
    sub_c2 = SUB_KRITERIA.get("C2", {})
    if not sub_c2:
        print_error("Data sub-kriteria RAM tidak ditemukan!")
        pause()
        return

    print_info("Ketik 0 untuk membatalkan.")
    print()
    
    level = input_number("Pilih tingkat RAM minimal", min_val=0, max_val=max(sub_c2.keys()))
    
    if level == 0:
        print_info("Batal mengubah batas RAM.")
    else:
        user_preference.set_ram_constraint(level)
        print_success(f"Minimal RAM disimpan (Level {level}). Smartphone di bawah RAM ini tidak akan direkomendasikan.")
    
    pause()

def _apply_profile_template(user_preference, criteria_list):
    clear_screen()
    print_header("PROFIL PENGGUNA")
    print_info("Pilih profil berikut untuk mengatur bobot kriteria secara otomatis:")
    print()
    
    profiles = list(WEIGHT_TEMPLATES.keys())
    for idx, profile in enumerate(profiles, start=1):
        print(f"  [{idx}] {profile}")
    
    print("  [0] Batal")
    print()
    
    choice = input_number("Pilih profil pengguna", min_val=0, max_val=len(profiles))
    
    if choice == 0:
        print_info("Batal memilih profil.")
        pause()
        return
        
    selected_name = profiles[choice - 1]
    weights = WEIGHT_TEMPLATES[selected_name]
    
    # Apply weights to criteria_list
    for cr in criteria_list:
        if cr.kode in weights:
            cr.bobot = weights[cr.kode]
            
    user_preference.selected_profile = selected_name
    print_success(f"Profil {selected_name} diaktifkan! Bobot kriteria telah disesuaikan.")
    
    print()
    print_info("Penyesuaian Bobot Saat Ini:")
    for cr in criteria_list:
        print(f"  - {cr.kode} ({cr.nama}): {cr.bobot}%")
        
    pause()
