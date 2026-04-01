import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_course import run_app


def main():
    try:
        run_app()
    except KeyboardInterrupt:
        print("\n\n  Program dihentikan oleh pengguna. Sampai jumpa! 👋\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
