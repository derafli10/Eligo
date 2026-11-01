"""Berkas Titik Masuk Utama Sistem Eligo (Root Main Entry Point).

Menjalankan Sistem Pemeringkatan Siswa Eligible SNBP (Eligo) melalui terminal interaktif.

Cara Menjalankan:
    Di terminal atau PowerShell Windows:
    $ py -3 main.py
"""

from __future__ import annotations

import sys

from eligo.presentation.cli.main import run_app

if __name__ == "__main__":
    try:
        run_app()
    except Exception as err:
        print(f"\n[FATAL ERROR] Terjadi kesalahan kritis di luar sistem Eligo: {err}", file=sys.stderr)
        sys.exit(1)
