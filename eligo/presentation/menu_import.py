# Menu Impor Nilai Siswa CSV.

# Modul ini mengimplementasikan panduan impor berkas CSV nilai siswa dengan
# State Machine terstruktur:
#     1. Pemilihan jurusan sasaran impor.
#     2. Pembuatan berkas template CSV otomatis jika belum tersedia.
#     3. Fase 1: Pratinjau data tanpa mutasi disk.
#     4. Evaluasi duplikasi nama dan pemilihan resolusi (Skip, Overwrite, Abort).
#     5. Konfirmasi eksplisit operator sebelum komitmen data.
#     6. Fase 2: Penulisan atomik ke repositori dan pembuatan laporan error log.

# Penjelasan Sederhana:
#     Mengunggah nilai ratusan siswa tidak boleh sembarangan! panduan ini membimbing:
#     - Langkah 1: Pilih jurusan (misal MIPA). Sistem otomatis membuatkan contoh template Excel/CSV.
#     - Langkah 2: Masukkan nama berkas CSV Anda.
#     - Langkah 3: Sistem memeriksa file dan memperlihatkan pratinjau:
#       * Berapa baris yang lolos (warna hijau).
#       * Berapa baris yang nilainya salah (warna merah).
#       * Apakah ada siswa yang namanya kembar dengan yang sudah terdaftar (warna kuning).
#     - Langkah 4: Jika ada siswa kembar, Anda memilih: apakah mau dilewati (skip) atau ditimpa (overwrite).
#     - Langkah 5: Sistem bertanya sekali lagi: "Yakin mau disimpan?".
#       Jika Anda menjawab "Y", data disimpan ke buku induk sekolah. Aman banget!


from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from eligo.application.import_service import commit_import, prepare_import_preview
from eligo.application.school_service import get_school_profile
from eligo.domain.exceptions import CsvImportError, ImportAbortedError, ValidationError
from eligo.domain.models import Major
from eligo.infrastructure.csv_parser import generate_csv_template
from eligo.infrastructure.repositories.config_repo import JsonConfigRepository
from eligo.infrastructure.repositories.school_repo import JsonSchoolRepository
from eligo.infrastructure.repositories.student_repo import JsonStudentRepository

def ensure_csv_template_exists(major: Major, base_dir: Path) -> Path:
    # Masttin berkas template CSV untuk kurikulum jurusan tersedia di disk
    base_dir.mkdir(parents=True, exist_ok=True)
    template_file = base_dir / f"{major.code.lower()}_template.csv"
    
    if not template_file.exist():
        content = generate_csv_template(major)
        template_file.write_text(content, encoding="utf-8")
        
    return template_file

def display_import_menu(
    console: Console,
    student_repo: JsonStudentRepository,
    school_repo: JsonSchoolRepository,
    config_repo: JsonConfigRepository,
) -> None:
    # Nampilin panduan impor CSV
    profile = get_school_profile(school_repo)
    if profile is None or not profile.majors:
    # Cek apakah data sekolah dan jurusan sudah diatur
        console.print(
            Panel(
                "[bold red] Profil sekolah atau jurusan belum terdaftar![/bold red]\n"
                "[white]Harap atur Profil Sekolah terlebih dadhulu pada Menu 1.[/white]",
                title="[bold red]PRASYARAT BELUM TERPENUHI[/bold red]",
                border_style="red",
            )
        )
        return
    
    console.print(
        Panel(
            "[bold white] Selamat datang di panduan Unggah / Import Siswa.[/bold white]\n"
            "[dim]Sistem mendukung berkas CSV hasil ekspor Microsoft Excel (koma maupun titik koma).[/dim]",
            title="[bold green]PANDUAN IMPOR NILAI CSV[/bold green]",
            border_style="green",
        )
    )

    # 1: Pilih Jurusan Sasaran Impor
    available_majors = [m.code.upper() for m in profile.majors]
    console.print("[bold yellow]Pilih Jurusan Sasaran Impor:[/bold yellow]")
    for idx, m_code in enumerate(available_majors, start=1):
    # Nampilin daftar jurusan yang ada
        major_obj = next(m for m in profile.majors if m.code.upper() == m_code)
        console.print(f"    [{idx}] {major_obj.name} ({m_code})")

    choice_idx = Prompt.ask(
        "Pilih nomor jurusan",
        choice=[str(i) for i in range(1, len(available_majors) + 1)],
        default="1",
        console=console,
    )
    chosen_major = profile.majors[int(choice_idx) - 1]

    # 2: Sedikan Template CSV
    import_dir = Path("data/import")
    template_path = ensure_csv_template_exists(chosen_major, import_dir)
    # Ngasih tau letak template
    console.print(f"\n[dim]Berkas template tersedia di: [bold cyan]{template_path}[/bold cyan][/dim]\n")

    # 3: Masukkan Lokasi / Nama Berkas CSV
    file_path_str = Prompt.ask(
        "[bold cyan]Masukkan path berkas CSV yang akan diimpor[/bold cyan]",
        default=str(template_path),
        console=console,
    ).strip()

    csv_file = Path(file_path_str)
    if not csv_file.exist():
        console.print(f"\n[bold red]Berkas tidak ditemukan pada: {csv_file}[/bold red]\n")
        return

    # 4 & 5: Fase 1 Pratinjau (Read Only Preview)
    config = config_repo.load()
    existing_students = student_repo.load_all()

    try:
        console.print("\n[dim]Memeriksa format, mendeteksi delimiter, dan memvalidasi nilai..[/dim]")
        # Baca file CSV nya lalu cek format, valid tidaknya, siswa duplikat. Hasilnya disimpen di variabel preview
        preview = prepare_import_preview(
            file_path=csv_file,
            major=chosen_major,
            existing_students=existing_students,
            config=config,
        )
    except CsvImportError as err:
        console.print(
            Panel(
                f"[bold red]Gagal Membaca Berkas CSV:[/bold red] {err.message}\n"
                f"[dim]Detail Teknis: {err.code}[/dim]",
                title="[bold red]FORMAT BERKAS TIDAK COCOK[/bold red]",
                border_style="red",
            )
        )
        return

    # Tampilkan Ringkasan Hasil Pratinjau
    valid_color = "green" if preview.valid_rows else "yellow"
    error_color = "red" if preview.error_rows else "dim"
    dup_color = "yellow" if preview.duplicate_rows else "dim"

    preview_text = (
        f"[bold]Total baris Diproses:[/bold]    {preview.total_rows} baris\n"
        f"--------------------------------------------\n"
        f"[{valid_color}]- Baris & Valid:[/{valid_color}]   [bold {valid_color}]{len(preview.valid_rows)} siswa[/bold {valid_color}] "
        f"[green]{preview.tka_count} Ikut TKA[/green], [dim]{preview.non_tka_count} Tidak Ikut[/dim])\n"
        f"[{error_color}]- Baris Mengandung Error:[/{error_color}] [bold {error_color}]{len(preview.error_rows)} kesalahan[bold {error_color}]\n"
        f"[{dup_color}- Siswa Duplikat (kembar):[/{dup_color}] [bold {dup_color}]{len(preview.duplicate_rows)} siswa[/bold {dup_color}]"
    )
    console.print(
        Panel(
            preview_text,
            title="[bold green]PRATINJAU HASIL ANALISIS CSV[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )

    # Jika ada kesalahan baris, tampilkan beberapa contoh kesalahan
    if preview.error.rows:
        table_err = Table(
            title="[bold red]CONTOH BARIS BERMASALAH (DITOLAK[/bold red])",
            border_style="red",
            show_lines=True,
        )
        table_err.add_column("Baris", justify="center")
        table_err.add_column("Kolom", justify="center")
        table_err.add_column("Nilai Asli", justify="center")
        table_err.add_column("Pesan Kesalahan", justify="left")

        for row_err in preview.err_rows[:5]:
            table_err.add_row(str(row_err.row_number), row_err.column_name, str(row_err.raw_value), row_err.message)
        
        console.print(table_err)
        if len(preview.error_rows) > 5:
            console.print(f"[dim]... dan {len(preview.error_rows) - 5} kesalahan lainnya.[/dim]")

    if not preview.valid_rows:
        console.print("\n[bold red]Tidak ada satupun baris valid yang dapat diimpor. Proses dihentikan.[bold red]\n")
        return

    # 6: Resolusi Data Duplikat
    resolution = "skip"
    if preview.has_duplicates:
        console.print("\n[bold yellow]Terdeteksi data siswa yang sudah ada di buku inuk:[/bold yellow]")
        for d in preview.duplicate_rows[:3]:
            console.print(f"    -   {d.name} ({d.class_name})")
        if len(preview.duplicate_rows) > 3:
            console.print(f"    ... dan {len(preview.duplicate_rows) - 3} siswa lainnya.")
            
        console.print("/n[bold cyan]Pilih tindakan penanganan siswa duplikat:[/bold cyan]")
        console.print(" [1] [bold green]LEWATI (Skip)[/bold green]  : Pertahankan data lam, abaikan data dari file CSV.")
        console.print(" [2] [bold yellow]TIMPA (Overwrite)[/bold yellow]  : Perbarui nilai siswa dengan data terbaru dari file CSV.")
        console.print(" [3] [bold red]BATALKAN (Abort)[/bold red]  : Batalkan seluruh proses impor.")
        
        dup_choice = Prompt.ask("Pilihlah tindakan", choices=["1", "2", "3"], default="1", console=console)
        if dup_choice == "1":
            resolution = "skip"
        elif dup_choice == "2":
            resolution = "overwrite"
        elif dup_choice == "3":
            console.print("\n[yellow]Impor dibatalkan operator. Tidak ada perubahan data.[/yellow]\n")
            return
    
    # 7: Konfirmasi Eksplisit Sebelumm Komitmen
    console.print(
        Panel(
            f"Jumlah siswa yang akan diproses: [bold green]{len(preview.valid_rows)} siswa[/bold green]\n"
            f"Tindakan data duplikat: [bold yellow]{resolution.upper()}[/bold yellow]\n"
            f"Penyimpanan: [cyan]data/students.json[/cyan] (Atomic Write + Cadangan .bak)",
            title="[bold yellow]KONFIRMASI PENYIMPANAN DATA[/bold yellow]",
            border_style="yellow",
        )
    )
    
    yakin = Confirm.ask("Apakah Anda yakin ingin menyimpan perubahan ke database sekolah?", default=True, console=console)
    if not yakin:
        console.print("\n[yellow]Operasi penyimpanan dibatalkan. Data buku induk tetap aman (Zero Dirty Write).[/yellow]/n")
        return
    
    # 8: Fase 2 Komitmen Permanen (Commit Import)  
    try:
    # Nulis data nya ke students.json dan juga buat backup otomatis sebelum tulis
        saved_count, error_count = commit_import(
            preview=preview,
            duplicate_resolution=resolution,
            existing_students=existing_students,
            student_repo=student_repo,
            error_report_path=import_dir,
        )
        console.print(
            Panel(
                f"[bold green]Proses impor data nilai berhasil diselesaikan![/bold green]\n\n)]"
                f"- Total siswa aktif di buku induk: [bold cyan]{saved_count} siswa[/bold cyan]/n"
                f"- Baris yang ditolak: [bold red]{error_count} baris[/bold red]\n"
                + (f"- Laporan log penolakan disimpan di folder: [cyan]{import_dir}[/cyan]" if error_count > 0 else ""),
                title="[bold green]IMPOR SUKSES[/bold green]",
                border_style="green",
            )            )
    except ImportAbortedError:
        console.print("\n[yellow]Transaksi impor dibatalkan.[/yellow]\n")
    except ValidationError as err:
        console.print(f"\n[bold red]Validasi Gagal:[/bold red] {err.message}\n")