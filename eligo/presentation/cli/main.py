#   modul ini seperti "Lobi Resepsionis" di gedung sekolah:
#     1. menu pilihan terpadu:
#        Saat program dibuka, layar menampilkan menu rapi dengan nomor pilihan (1 sampai 5):
#        - Menu 1: Profil Sekolah & Pengaturan Kuota
#        - Menu 2: Buku Induk & Manajemen Data Siswa
#        - Menu 3: Unggah Nilai dari Berkas Excel/CSV
#        - Menu 4: Papan Peringkat & Hasil Seleksi SNBP
#        - Menu 5: Reset Seluruh Data (Hapus Permanen)
#        - Menu 0: Keluar dari Aplikasi
#     2. tombol darurat yang aman (Ctrl+C):
#        jika operator sedang mengetik lalu berubah pikiran dan menekan tombol Ctrl+C,
#        program TIDAK AKAN RUSAK atau memunculkan tulisan error bahasa Inggris yang menakutkan
#        (Traceback Error). sistem menangkap tombol tersebut dengan tenang, menampilkan pesan ramah:
#        "Operasi dibatalkan oleh pengguna. Kembali ke menu utama...", dan data sekolah tetap aman.

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from eligo.domain.exceptions import EligoError
from eligo.infrastructure.repositories.config_repo import JsonConfigRepository
from eligo.infrastructure.repositories.school_repo import JsonSchoolRepository
from eligo.infrastructure.repositories.student_repo import JsonStudentRepository
from eligo.presentation.cli.menu_import import display_import_menu
from eligo.presentation.cli.menu_ranking import display_ranking_menu
from eligo.presentation.cli.menu_reset import display_reset_menu
from eligo.presentation.cli.menu_school import display_school_menu
from eligo.presentation.cli.menu_student import display_student_menu


def print_welcome_banner(console: Console) -> None:
    # cetak spanduk selamat datang dan identitas sistem pemeringkatan Eligo
    banner_text = (
        "[bold cyan]SISTEM PEMERINGKATAN SISWA ELIGIBLE SNBP (ELIGO)[/bold cyan]\n"
        "[white]Aplikasi Resmi Penentuan Kuota & Peringkat Seleksi Nasional Berdasarkan Prestasi[/white]\n"
        "[dim]Sesuai Regulasi Kemendikbudristek • Algoritma Mandiri • Penyimpanan Aman[/dim]"
    )
    console.print(
        Panel(
            banner_text,
            border_style="bright_blue",
            padding=(1, 2),
        )
    )


def print_main_menu_options(console: Console) -> None:
    # nampilin pilihan menu utama
    menu_text = (
        "[bold green]1.[/bold green] Profil Sekolah, Akreditasi & Kurikulum Jurusan\n"
        "[bold green]2.[/bold green] Buku Induk Siswa (Lihat, Tambah, Ubah, Hapus)\n"
        "[bold green]3.[/bold green] Unggah / Impor Nilai Rapor Siswa dari Berkas CSV\n"
        "[bold green]4.[/bold green] Papan Peringkat SNBP, Filter Status & Pencarian Siswa\n"
        "[bold yellow]5.[/bold yellow] Reset Seluruh Data (Hapus Permanen)\n"
        "[bold red]0.[/bold red] Keluar dari Aplikasi"
    )
    console.print(
        Panel(
            menu_text,
            title="[bold yellow]MENU UTAMA[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
    )


def main_loop(
    console: Console,
    school_repo: JsonSchoolRepository | None = None,
    student_repo: JsonStudentRepository | None = None,
    config_repo: JsonConfigRepository | None = None,
) -> None:
    # perulangan utama pengguna (Main Application Loop).

    # fungsi menyajikan menu hingga operator secara sadar memilih opsi 0 untuk keluar.

    s_repo = school_repo or JsonSchoolRepository("data/school.json")
    st_repo = student_repo or JsonStudentRepository("data/students.json")
    c_repo = config_repo or JsonConfigRepository("data/config.json")

    while True:
        try:
            print_main_menu_options(console)
            choice = Prompt.ask(
                "[bold cyan]Pilih nomor menu yang Anda inginkan[/bold cyan]",
                choices=["0", "1", "2", "3", "4", "5"],
                default="4",
                console=console,
            )

            if choice == "0":
                console.print("\n[bold green]Terima kasih telah menggunakan Sistem Eligo. Sampai jumpa![/bold green]\n")
                break
            elif choice == "1":
                display_school_menu(console, s_repo, c_repo)
            elif choice == "2":
                display_student_menu(console, st_repo, s_repo, c_repo)
            elif choice == "3":
                display_import_menu(console, st_repo, s_repo, c_repo)
            elif choice == "4":
                display_ranking_menu(console, st_repo, s_repo, c_repo)
            elif choice == "5":
                display_reset_menu(console)

        except KeyboardInterrupt:
            # titik penangkap pembatalan: operator menekan Ctrl+C saat berada di sub-menu
            console.print("\n[yellow]⚠️ Operasi dibatalkan oleh pengguna. Kembali ke menu utama...[/yellow]\n")
            continue
        except EligoError as err:
            console.print(
                Panel(
                    f"[bold red]Terjadi Kesalahan Sistem:[/bold red] {err.message}\n"
                    f"[dim]Kode Kesalahan: {err.code}[/dim]",
                    title="[bold red]❌ PEMBERITAHUAN KESALAHAN[/bold red]",
                    border_style="red",
                )
            )


def run_app() -> None:
    # titik masuk eksekusi utama aplikasi terminal (CLI Application Runner).

    # fungsi ini membungkus seluruh aplikasi dengan penanganan KeyboardInterrupt di tingkat paling luar
    console = Console()
    print_welcome_banner(console)

    try:
        main_loop(console)
    except KeyboardInterrupt:
        # penanganan Ctrl+C jika ditekan langsung di prompt menu paling luar
        console.print("\n[dim]Aplikasi dihentikan oleh pengguna via pintasan keyboard. Sampai jumpa![/dim]\n")
        sys.exit(0)