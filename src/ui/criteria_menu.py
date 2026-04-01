from src.ui.helpers import (
    clear_screen,
    confirm,
    input_choice,
    input_float,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_success,
    print_table,
    print_warning,
)


def criteria_menu(data_manager, criteria_list):
    while True:
        clear_screen()
        print_header("KELOLA KRITERIA & BOBOT")
        print()
        print_menu_item(1, "Lihat Kriteria & Bobot")
        print_menu_item(2, "Ubah Bobot Kriteria")
        print_menu_item(0, "Kembali ke Menu Utama")

        choice = input_choice()

        if choice == "1":
            _show_criteria(criteria_list)
        elif choice == "2":
            criteria_list = _update_weights(data_manager, criteria_list)
        elif choice == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()

    return criteria_list


def _show_criteria(criteria_list):
    clear_screen()
    print_header("DATA KRITERIA & BOBOT")

    if not criteria_list:
        print_warning("Belum ada data kriteria. Silakan muat data default.")
        pause()
        return

    headers = ["No", "Kode", "Nama Kriteria", "Bobot (%)", "Jenis"]
    rows = []

    for i, cr in enumerate(criteria_list, start=1):
        rows.append([i, cr.kode, cr.nama, cr.bobot, cr.jenis.upper()])

    print()
    print_table(headers, rows)

    total_weight = sum(cr.bobot for cr in criteria_list)
    print_info(f"Total Bobot: {total_weight}%")

    if total_weight != 100:
        print_warning(f"Total bobot harus 100%! Saat ini: {total_weight}%")

    pause()


def _update_weights(data_manager, criteria_list):
    clear_screen()
    print_header("UBAH BOBOT KRITERIA")

    if not criteria_list:
        print_warning("Belum ada data kriteria. Silakan muat data default.")
        pause()
        return criteria_list

    print()
    print("  Bobot saat ini:")
    for cr in criteria_list:
        print(f"    {cr.kode} - {cr.nama}: {cr.bobot}%")

    print()
    print_info("Masukkan bobot baru untuk setiap kriteria.")
    print_info("Total bobot harus berjumlah 100%.")
    print()

    new_weights = []
    for cr in criteria_list:
        weight = input_float(
            f"Bobot {cr.kode} ({cr.nama}), saat ini {cr.bobot}%",
            min_val=0,
            max_val=100
        )
        new_weights.append(weight)

    total = sum(new_weights)
    if total != 100:
        print_error(f"Total bobot harus 100%, tetapi total saat ini: {total}%")
        print_info("Perubahan bobot dibatalkan.")
        pause()
        return criteria_list

    print()
    print("  Bobot baru:")
    for cr, weight in zip(criteria_list, new_weights):
        print(f"    {cr.kode} - {cr.nama}: {cr.bobot}% → {weight}%")

    if confirm("Simpan perubahan bobot?"):
        for cr, weight in zip(criteria_list, new_weights):
            cr.bobot = weight
        data_manager.save_criteria(criteria_list)
        print_success("Bobot kriteria berhasil diperbarui!")
    else:
        print_info("Perubahan dibatalkan.")

    pause()
    return criteria_list
