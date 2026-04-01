from src.config.settings import SUB_KRITERIA
from src.ui.helpers import (
    clear_screen,
    confirm,
    input_choice,
    input_number,
    input_text,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_separator,
    print_success,
    print_table,
    print_warning,
    show_sub_criteria,
)


def smartphone_menu(data_manager, smartphones, criteria_list):
    while True:
        clear_screen()
        print_header("KELOLA DATA SMARTPHONE")
        print()
        print_menu_item(1, "Lihat Semua Smartphone")
        print_menu_item(2, "Tambah Smartphone Baru")
        print_menu_item(3, "Edit Smartphone")
        print_menu_item(4, "Hapus Smartphone")
        print_menu_item(0, "Kembali ke Menu Utama")

        choice = input_choice()

        if choice == "1":
            _show_smartphones(smartphones, criteria_list)
        elif choice == "2":
            smartphones = _add_smartphone(data_manager, smartphones, criteria_list)
        elif choice == "3":
            smartphones = _edit_smartphone(data_manager, smartphones, criteria_list)
        elif choice == "4":
            smartphones = _delete_smartphone(data_manager, smartphones)
        elif choice == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()

    return smartphones


def _show_smartphones(smartphones, criteria_list):
    clear_screen()
    print_header("DATA SMARTPHONE")

    if not smartphones:
        print_warning("Belum ada data smartphone. Silakan tambah data atau muat data default.")
        pause()
        return

    headers = ["No", "Kode", "Nama Smartphone"]
    for cr in criteria_list:
        headers.append(f"{cr.kode}\n({cr.nama})")

    rows = []
    for i, sp in enumerate(smartphones, start=1):
        row = [i, sp.kode, sp.nama]
        for cr in criteria_list:
            row.append(sp.get_nilai(cr.kode))
        rows.append(row)

    print()
    print_table(headers, rows)
    print_info(f"Total: {len(smartphones)} smartphone")
    pause()


def _add_smartphone(data_manager, smartphones, criteria_list):
    clear_screen()
    print_header("TAMBAH SMARTPHONE BARU")

    if not criteria_list:
        print_error("Data kriteria belum tersedia! Silakan muat data default terlebih dahulu.")
        pause()
        return smartphones

    # Auto-generate code
    last_code = 0
    for sp in smartphones:
        try:
            num = int(sp.kode.replace("A", ""))
            last_code = max(last_code, num)
        except ValueError:
            pass
    new_code = f"A{last_code + 1}"

    print_info(f"Kode smartphone: {new_code}")
    print()

    name = input_text("Nama Smartphone")
    if not name:
        print_error("Nama tidak boleh kosong!")
        pause()
        return smartphones

    values = {}
    print()
    print_separator()
    print("  Masukkan nilai untuk setiap kriteria:")
    print_separator()

    for cr in criteria_list:
        print(f"\n  {cr.kode} - {cr.nama} ({cr.jenis}):")
        show_sub_criteria(cr.kode)

        sub = SUB_KRITERIA.get(cr.kode, {})
        if sub:
            min_val = min(sub.keys())
            max_val = max(sub.keys())
            v = input_number(f"Nilai {cr.kode}", min_val=min_val, max_val=max_val)
        else:
            v = input_number(f"Nilai {cr.kode}", min_val=1)

        values[cr.kode] = v

    from src.models.smartphone import Smartphone
    new_sp = Smartphone(kode=new_code, nama=name, nilai=values)
    smartphones.append(new_sp)

    data_manager.save_smartphones(smartphones)
    print_success(f"Smartphone '{name}' ({new_code}) berhasil ditambahkan!")
    pause()
    return smartphones


def _edit_smartphone(data_manager, smartphones, criteria_list):
    clear_screen()
    print_header("EDIT SMARTPHONE")

    if not smartphones:
        print_warning("Belum ada data smartphone.")
        pause()
        return smartphones

    if not criteria_list:
        print_error("Data kriteria belum tersedia!")
        pause()
        return smartphones

    print()
    for i, sp in enumerate(smartphones, start=1):
        print(f"  {i}. {sp.kode} - {sp.nama}")

    print()
    idx = input_number("Pilih nomor smartphone yang ingin diedit", min_val=1, max_val=len(smartphones))
    sp = smartphones[idx - 1]

    print_info(f"Mengedit: {sp.kode} - {sp.nama}")
    print()

    new_name = input_text(f"Nama baru (kosongkan jika tidak diubah, saat ini: {sp.nama})")
    if new_name:
        sp.nama = new_name

    print()
    print_separator()
    print("  Edit nilai kriteria (kosongkan/0 jika tidak diubah):")
    print_separator()

    for cr in criteria_list:
        current_value = sp.get_nilai(cr.kode)
        print(f"\n  {cr.kode} - {cr.nama} (saat ini: {current_value}):")
        show_sub_criteria(cr.kode)

        try:
            v_str = input(f"  Nilai baru {cr.kode} (Enter = tidak ubah): ").strip()
            if v_str:
                v = int(v_str)
                if v > 0:
                    sp.set_nilai(cr.kode, v)
        except ValueError:
            print_warning("Input tidak valid, nilai tidak diubah.")

    data_manager.save_smartphones(smartphones)
    print_success(f"Smartphone '{sp.nama}' berhasil diperbarui!")
    pause()
    return smartphones


def _delete_smartphone(data_manager, smartphones):
    clear_screen()
    print_header("HAPUS SMARTPHONE")

    if not smartphones:
        print_warning("Belum ada data smartphone.")
        pause()
        return smartphones

    print()
    for i, sp in enumerate(smartphones, start=1):
        print(f"  {i}. {sp.kode} - {sp.nama}")

    print()
    idx = input_number("Pilih nomor smartphone yang ingin dihapus", min_val=1, max_val=len(smartphones))
    sp = smartphones[idx - 1]

    if confirm(f"Hapus '{sp.nama}' ({sp.kode})?"):
        smartphones.pop(idx - 1)
        data_manager.save_smartphones(smartphones)
        print_success(f"Smartphone '{sp.nama}' berhasil dihapus!")
    else:
        print_info("Penghapusan dibatalkan.")

    pause()
    return smartphones
