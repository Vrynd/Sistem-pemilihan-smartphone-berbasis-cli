from src.services.calculation_method import CalculationMethod
from src.ui.helpers import (
    clear_screen,
    input_choice,
    pause,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_sub_header,
    print_table,
    print_warning,
)


def calculation_menu(smartphones, criteria_list, user_preference=None):
    while True:
        clear_screen()
        print_header("PERHITUNGAN METODE SAW")
        print()
        if user_preference and user_preference.is_active:
            print_info(f"Preferensi Aktif: {user_preference}")
            print()

        print_menu_item(1, "Matriks Keputusan")
        print_menu_item(2, "Matriks Normalisasi")
        print_menu_item(3, "Hasil Perhitungan & Ranking")
        print_menu_item(4, "Lihat Semua")
        print_menu_item(0, "Kembali")

        choice = input_choice()

        if choice == "1":
            _show_decision_matrix(smartphones, criteria_list, user_preference)
        elif choice == "2":
            _show_normalized_matrix(smartphones, criteria_list, user_preference)
        elif choice == "3":
            _show_ranking(smartphones, criteria_list, user_preference)
        elif choice == "4":
            _show_full_calculation(smartphones, criteria_list, user_preference)
        elif choice == "0":
            break
        else:
            print_error("Pilihan tidak valid!")
            pause()


def _check_data(smartphones, criteria_list) -> bool:
    if not smartphones:
        print_warning("Belum ada data smartphone! Silakan tambah data atau muat data default.")
        pause()
        return False
    if not criteria_list:
        print_warning("Belum ada data kriteria! Silakan muat data default.")
        pause()
        return False
    return True


def _show_decision_matrix(smartphones, criteria_list, user_preference=None):
    clear_screen()
    print_header("MATRIKS KEPUTUSAN (X)")

    if not _check_data(smartphones, criteria_list):
        return

    calc = CalculationMethod(smartphones, criteria_list, user_preference)
    
    if not calc.smartphones:
        print_warning("Tidak ada smartphone yang memenuhi kriteria preferensi Anda.")
        pause()
        return
        
    matrix = calc.create_decision_matrix()

    headers = ["Alternatif"] + [f"{cr.kode}" for cr in criteria_list]
    rows = []
    for i, sp in enumerate(calc.smartphones):
        row = [f"{sp.kode} ({sp.nama})"]
        row.extend(matrix[i])
        rows.append(row)

    print()
    print_table(headers, rows)

    print_info("Keterangan Kriteria:")
    for cr in criteria_list:
        print(f"    {cr.kode} = {cr.nama} ({cr.jenis}, bobot: {cr.bobot}%)")

    pause()


def _show_normalized_matrix(smartphones, criteria_list, user_preference=None):
    clear_screen()
    print_header("MATRIKS NORMALISASI (R)")

    if not _check_data(smartphones, criteria_list):
        return

    calc = CalculationMethod(smartphones, criteria_list, user_preference)
    
    if not calc.smartphones:
        print_warning("Tidak ada smartphone yang memenuhi kriteria preferensi Anda.")
        pause()
        return
        
    normalized = calc.normalization()

    headers = ["Alternatif"] + [f"{cr.kode}" for cr in criteria_list]
    rows = []
    for i, sp in enumerate(calc.smartphones):
        row = [f"{sp.kode} ({sp.nama})"]
        row.extend([f"{val:.4f}" for val in normalized[i]])
        rows.append(row)

    print()
    print_table(headers, rows)

    print_info("Rumus normalisasi:")
    print("    Cost:    rij = min(kolom j) / Xij")
    print("    Benefit: rij = Xij / max(kolom j)")

    pause()


def _show_ranking(smartphones, criteria_list, user_preference=None):
    clear_screen()
    print_header("HASIL PERHITUNGAN & RANKING")

    if not _check_data(smartphones, criteria_list):
        return

    calc = CalculationMethod(smartphones, criteria_list, user_preference)
    
    if not calc.smartphones:
        print_warning("Tidak ada smartphone yang memenuhi kriteria preferensi Anda.")
        pause()
        return
        
    ranking = calc.ranking()

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
    print_table(headers, rows)

    if ranking:
        best = ranking[0]
        # Build box width dynamically based on content (min 58)
        content_lines = [
            "REKOMENDASI TERBAIK",
            f"{best['nama']}",
            f"Kode: {best['kode']} | Nilai Vi: {best['nilai_vi']:.3f}%"
        ]
        
        box_padding = 4
        max_content_len = max(len(line) for line in content_lines)
        box_width = max(max_content_len + box_padding, 58)
        
        print()
        print(f"  ╔{'═' * box_width}╗")
        print(f"  ║{content_lines[0].center(box_width)}║")
        print(f"  ╠{'═' * box_width}╣")
        print(f"  ║  {content_lines[1].ljust(box_width - box_padding + 2)}║")
        print(f"  ║  {content_lines[2].ljust(box_width - box_padding + 2)}║")
        print(f"  ╚{'═' * box_width}╝")

    pause()


def _show_full_calculation(smartphones, criteria_list, user_preference=None):
    clear_screen()
    print_header("PERHITUNGAN SAW LENGKAP")

    if not _check_data(smartphones, criteria_list):
        return

    calc = CalculationMethod(smartphones, criteria_list, user_preference)
    
    if not calc.smartphones:
        print_warning("Tidak ada smartphone yang memenuhi kriteria preferensi Anda.")
        pause()
        return

    # Step 1: Criteria weights
    print_sub_header("LANGKAH 1: Bobot Kriteria (W)")
    headers_cr = ["Kode", "Nama", "Bobot (%)", "Jenis"]
    rows_cr = [[cr.kode, cr.nama, cr.bobot, cr.jenis.upper()] for cr in criteria_list]
    print()
    print_table(headers_cr, rows_cr)

    # Step 2: Decision matrix
    matrix = calc.create_decision_matrix()
    print_sub_header("LANGKAH 2: Matriks Keputusan (X)")
    headers_x = ["Alternatif"] + [cr.kode for cr in criteria_list]
    rows_x = []
    for i, sp in enumerate(calc.smartphones):
        row = [f"{sp.kode}"]
        row.extend(matrix[i])
        rows_x.append(row)
    print()
    print_table(headers_x, rows_x)

    # Step 3: Normalization
    normalized = calc.normalization()
    print_sub_header("LANGKAH 3: Matriks Normalisasi (R)")
    headers_r = ["Alternatif"] + [cr.kode for cr in criteria_list]
    rows_r = []
    for i, sp in enumerate(calc.smartphones):
        row = [f"{sp.kode}"]
        row.extend([f"{val:.4f}" for val in normalized[i]])
        rows_r.append(row)
    print()
    print_table(headers_r, rows_r)

    # Step 4: Preference calculation
    print_sub_header("LANGKAH 4: Perhitungan Nilai Preferensi (Vi)")
    print()
    print("  Rumus: Vi = Σ(Wj × rij)")
    print()

    ranking = calc.ranking()
    preferences = calc.calculate_preferences()

    for i, sp in enumerate(smartphones):
        detail_parts = []
        for j, cr in enumerate(criteria_list):
            wj = cr.bobot / 100.0
            rij = normalized[i][j]
            detail_parts.append(f"({wj}×{rij:.4f})")
        vi = preferences[i]["nilai_vi"]
        formula = " + ".join(detail_parts)
        print(f"  V{sp.kode} = {formula}")
        print(f"  V{sp.kode} = {vi:.4f}")
        print()

    # Step 5: Ranking
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
    print_table(headers_rank, rows_rank)

    if ranking:
        best = ranking[0]
        # Build box width dynamically based on content (min 58)
        content_lines = [
            "REKOMENDASI TERBAIK",
            f"{best['nama']}",
            f"Kode: {best['kode']} | Nilai Vi: {best['nilai_vi']:.3f}%"
        ]
        
        box_padding = 4
        max_content_len = max(len(line) for line in content_lines)
        box_width = max(max_content_len + box_padding, 58)
        
        print()
        print(f"  ╔{'═' * box_width}╗")
        print(f"  ║{content_lines[0].center(box_width)}║")
        print(f"  ╠{'═' * box_width}╣")
        print(f"  ║  {content_lines[1].ljust(box_width - box_padding + 2)}║")
        print(f"  ║  {content_lines[2].ljust(box_width - box_padding + 2)}║")
        print(f"  ╚{'═' * box_width}╝")

    pause()
