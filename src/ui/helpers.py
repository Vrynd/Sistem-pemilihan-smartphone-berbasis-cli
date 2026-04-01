import os
from src.config.settings import LEBAR_GARIS, SUB_KRITERIA


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str):
    print()
    print("═" * LEBAR_GARIS)
    print(f"  {title}".center(LEBAR_GARIS))
    print("═" * LEBAR_GARIS)


def print_sub_header(title: str):
    print()
    print(f"── {title} " + "─" * (LEBAR_GARIS - len(title) - 4))


def print_separator():
    print("─" * LEBAR_GARIS)


def print_success(message: str):
    print(f"\n  [✓] {message}")


def print_error(message: str):
    print(f"\n  [✗] {message}")


def print_warning(message: str):
    print(f"\n  [!] {message}")


def print_info(message: str):
    print(f"\n  [i] {message}")


def print_menu_item(number, text: str):
    print(f"  [{number}] {text}")


def input_choice(prompt: str = "Pilih menu") -> str:
    print()
    return input(f"  {prompt}: ").strip()


def input_number(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        try:
            value = int(input(f"  {prompt}: "))
            if min_val is not None and value < min_val:
                print_error(f"Nilai minimum adalah {min_val}")
                continue
            if max_val is not None and value > max_val:
                print_error(f"Nilai maksimum adalah {max_val}")
                continue
            return value
        except ValueError:
            print_error("Masukkan angka yang valid!")


def input_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        try:
            value = float(input(f"  {prompt}: "))
            if min_val is not None and value < min_val:
                print_error(f"Nilai minimum adalah {min_val}")
                continue
            if max_val is not None and value > max_val:
                print_error(f"Nilai maksimum adalah {max_val}")
                continue
            return value
        except ValueError:
            print_error("Masukkan angka yang valid!")


def input_text(prompt: str) -> str:
    return input(f"  {prompt}: ").strip()


def confirm(prompt: str = "Apakah Anda yakin?") -> bool:
    answer = input(f"  {prompt} (y/n): ").strip().lower()
    return answer in ("y", "ya", "yes")


def pause():
    input("\n  Tekan Enter untuk melanjutkan...")


def print_table(headers: list, rows: list, col_widths: list = None):
    if not col_widths:
        col_widths = []
        for i, header in enumerate(headers):
            max_len = len(str(header))
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(str(row[i])))
            col_widths.append(max_len + 2)

    # Build table borders and header
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

    # Build table rows
    for row in rows:
        row_line = "│"
        for i, width in enumerate(col_widths):
            val = str(row[i]) if i < len(row) else ""
            if isinstance(row[i], (int, float)):
                row_line += f" {val.rjust(width)} │"
            else:
                row_line += f" {val.ljust(width)} │"
        print(f"  {row_line}")

    print(f"  {separator_bot}")


def show_sub_criteria(criteria_code: str):
    sub = SUB_KRITERIA.get(criteria_code, {})
    if sub:
        for value, description in sub.items():
            print(f"      {value} = {description}")
