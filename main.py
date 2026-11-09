import sys

from eligo.presentation.cli.main import run_app
#panggil fungsi run_app dari eligo/presentation/cli/main.py 

if __name__ == "__main__":
# mastiin kode di bawah jalan kalo file ini dijalanin langsung, kalo import dari file lain kode nya ga jalan
    try:
        run_app()
    # coba jalanin aplikasinya
    except Exception as err:
    # kalo ada error tangkep errornya
        print(f"\n[FATAL ERROR] Terjadi kesalahan kritis di luar sistem Eligo: {err}", file=sys.stderr)
        sys.exit(1)
        # kalo dapet error, print errornya dengan sys.exit(1)