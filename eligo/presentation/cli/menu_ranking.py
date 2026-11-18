    # Menu ini seperti "Papan Pengumuman Kelulusan Kuota SNBP" di sekolah:
    # - bisa langsung liat siapa aja siswa yang berhasil masuk kuota (warna HIJAU),
    #   siapa yang menjadi CADANGAN (warna KUNING), dan siapa yang tidak ikut (warna ABU-ABU).
    # - jika siswanya banyak (ratusan orang), tabel dibagi per halaman (misal 15 siswa per halaman).
    #   cukup menekan tombol 'N' untuk halaman berikutnya atau 'P' untuk kembali.
    # - bisa mencari nama siswa tertentu (misal: "Ahmad") dan sistem langsung menampilkan
    #   kartu rincian nilainya secara lengkap dan sekejap mata.

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from eligo.application.ranking_service import (
    run_ranking_pipeline,
    search_student_in_results,
)
from eligo.application.school_service import get_school_profile
from eligo.application.student_service import get_students_by_major
from eligo.domain.models import EligibilityStatus, RankingResult
from eligo.infrastructure.repositories.config_repo import JsonConfigRepository
from eligo.infrastructure.repositories.school_repo import JsonSchoolRepository
from eligo.infrastructure.repositories.student_repo import JsonStudentRepository
from eligo.presentation.cli.formatter import (
    badge_status,
    create_student_table,
    create_summary_panel,
    format_decimal,
)


def display_single_student_card(console: Console, result: RankingResult) -> None:
    # nampilin kartu rincian hasil pemeringkatan siswa
    rank_str = f"[bold green]Peringkat {result.rank}[/bold green]" if result.rank is not None else "[dim]Tidak Berperingkat[/dim]"
    badge_str = badge_status(result.status)

    card_text = (
        f"[bold cyan]ID Siswa:[/bold cyan]          {result.student.id}\n"
        f"[bold cyan]Nama Lengkap:[/bold cyan]      [bold white]{result.student.name}[/bold white]\n"
        f"[bold cyan]Kelas & Jurusan:[/bold cyan]   {result.student.class_name} ({result.student.major_code})\n"
        f"──────────────────────────────────────────────\n"
        f"[bold cyan]Nilai Semester 1:[/bold cyan]  {format_decimal(result.semester_scores[0]) if len(result.semester_scores) > 0 else '-'}\n"
        f"[bold cyan]Nilai Semester 2:[/bold cyan]  {format_decimal(result.semester_scores[1]) if len(result.semester_scores) > 1 else '-'}\n"
        f"[bold cyan]Nilai Semester 3:[/bold cyan]  {format_decimal(result.semester_scores[2]) if len(result.semester_scores) > 2 else '-'}\n"
        f"[bold cyan]Nilai Semester 4:[/bold cyan]  {format_decimal(result.semester_scores[3]) if len(result.semester_scores) > 3 else '-'}\n"
        f"[bold cyan]Nilai Semester 5:[/bold cyan]  {format_decimal(result.semester_scores[4]) if len(result.semester_scores) > 4 else '-'}\n"
        f"──────────────────────────────────────────────\n"
        f"[bold yellow]Rerata Nilai Rapor:[/bold yellow]   {format_decimal(result.report_score)}\n"
        f"[bold yellow]Poin Tambahan Piagam:[/bold yellow] {format_decimal(result.achievement_points)}\n"
        f"[bold green]SKOR AKHIR TOTAL:[/bold green]     [bold green]{format_decimal(result.final_score)}[/bold green]\n"
        f"──────────────────────────────────────────────\n"
        f"[bold]Peringkat Kuota:[/bold]     {rank_str}\n"
        f"[bold]Status Kelayakan:[/bold]    {badge_str}"
    )

    console.print(
        Panel(
            card_text,
            title=f"[bold green]🔍 HASIL EVALUASI: {result.student.name.upper()}[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


def display_ranking_menu(
    console: Console,
    student_repo: JsonStudentRepository,
    school_repo: JsonSchoolRepository,
    config_repo: JsonConfigRepository,
) -> None:
    """Menampilkan alur antarmuka papan peringkat pemeringkatan SNBP."""
    profile = get_school_profile(school_repo)
    if profile is None or not profile.majors:
        console.print(
            Panel(
                "[bold red]Profil sekolah atau kurikulum jurusan belum diatur![/bold red]\n"
                "[white]Harap buka Menu 1 (Profil Sekolah) untuk mengatur data sekolah.[/white]",
                title="[bold red]⚠️ DATA SEKOLAH KOSONG[/bold red]",
                border_style="red",
            )
        )
        return

    # 1. pilih Jurusan yang akan diperingkatkan
    available_majors = [m.code.upper() for m in profile.majors]
    console.print("\n[bold yellow]── PILIH JURUSAN UNTUK PEMERINGKATAN SNBP ──[/bold yellow]")
    for idx, m_code in enumerate(available_majors, start=1):
        major_obj = next(m for m in profile.majors if m.code.upper() == m_code)
        console.print(f"  [bold cyan][{idx}][/bold cyan] {major_obj.name} ({m_code})")

    choice_major_idx = Prompt.ask(
        "Pilih nomor jurusan",
        choices=[str(i) for i in range(1, len(available_majors) + 1)],
        default="1",
        console=console,
    )
    chosen_major_code = available_majors[int(choice_major_idx) - 1]
    chosen_major_obj = next(m for m in profile.majors if m.code.upper() == chosen_major_code)

    # 2. ambil data siswa jurusan tersebut
    students = get_students_by_major(chosen_major_code, student_repo)
    if not students:
        console.print(
            Panel(
                f"[bold yellow]Belum ada siswa yang terdaftar pada jurusan {chosen_major_obj.name} ({chosen_major_code}).[/bold yellow]\n"
                "[dim]Gunakan Menu 2 (Tambah Siswa Manual) atau Menu 3 (Impor CSV) untuk mengisi data.[/dim]",
                title="[bold yellow]⚠️ DATA SISWA KOSONG[/bold yellow]",
                border_style="yellow",
            )
        )
        return

    # 3. jalankan proses pemeringkatan murni (Ranking Service)
    config = config_repo.load()
    all_results, quota = run_ranking_pipeline(students, profile, config)

    # 4. tampilkan ringkasan (Summary Panel)
    summary_panel = create_summary_panel(
        total_students=len(students),
        quota=quota,
        results=all_results,
        major_name=f"{chosen_major_obj.name} ({chosen_major_code})",
    )
    console.print("\n", summary_panel, "\n")

    # 5. navigasi paginasi & filter interaktif
    current_page = 1
    page_size = 15
    active_filter = "ALL"  # ALL | HIJAU | KUNING | ABU_ABU

    while True:
        # terapkan penyaringan (filtering)
        if active_filter == "HIJAU":
            filtered_results = [r for r in all_results if r.status == EligibilityStatus.HIJAU]
            filter_label = "Hanya Siswa Eligible (Hijau)"
        elif active_filter == "KUNING":
            filtered_results = [r for r in all_results if r.status == EligibilityStatus.KUNING]
            filter_label = "Hanya Siswa Cadangan (Kuning)"
        elif active_filter == "ABU_ABU":
            filtered_results = [r for r in all_results if r.status == EligibilityStatus.ABU_ABU]
            filter_label = "Hanya Siswa Non-TKA (Abu-abu)"
        else:
            filtered_results = all_results
            filter_label = "Semua Siswa"

        total_pages = max(1, (len(filtered_results) + page_size - 1) // page_size)
        current_page = max(1, min(current_page, total_pages))

        # cetak tabel Rich
        table = create_student_table(filtered_results, page=current_page, page_size=page_size)
        console.print(table)
        console.print(f"[dim]Penyaringan Aktif: {filter_label} | Halaman {current_page} dari {total_pages}[/dim]\n")

        # menu kendali navigasi
        nav_prompt = (
            "[bold cyan]Navigasi:[/bold cyan] "
            "[bold white][N][/bold white]ext • "
            "[bold white][P][/bold white]rev • "
            "[bold white][F][/bold white]ilter Status • "
            "[bold white][C][/bold white]ari Siswa (Binary Search) • "
            "[bold red][Q][/bold red]uit (Kembali)"
        )
        console.print(nav_prompt)
        nav_choice = Prompt.ask(
            "Pilihan navigasi",
            choices=["N", "P", "F", "C", "Q", "n", "p", "f", "c", "q"],
            default="N" if current_page < total_pages else "Q",
            console=console,
        ).upper()

        if nav_choice == "Q":
            break
        elif nav_choice == "N":
            if current_page < total_pages:
                current_page += 1
            else:
                console.print("[dim]Anda sudah berada di halaman terakhir.[/dim]\n")
        elif nav_choice == "P":
            if current_page > 1:
                current_page -= 1
            else:
                console.print("[dim]Anda sudah berada di halaman pertama.[/dim]\n")
        elif nav_choice == "F":
            console.print("\n[bold yellow]Pilih Filter Status:[/bold yellow]")
            console.print("  [1] Tampilkan Semua Siswa")
            console.print("  [2] Hanya Siswa ELIGIBLE (Lampu Hijau)")
            console.print("  [3] Hanya Siswa CADANGAN (Lampu Kuning)")
            console.print("  [4] Hanya Siswa NON-TKA (Lampu Abu-Abu)")
            f_opt = Prompt.ask("Pilih filter", choices=["1", "2", "3", "4"], default="1", console=console)
            if f_opt == "1":
                active_filter = "ALL"
            elif f_opt == "2":
                active_filter = "HIJAU"
            elif f_opt == "3":
                active_filter = "KUNING"
            elif f_opt == "4":
                active_filter = "ABU_ABU"
            current_page = 1
        elif nav_choice == "C":
            # pencarian nama via binary search
            console.print("\n[bold yellow]PENCARIAN SISWA (BINARY SEARCH)[/bold yellow]")
            target_name = Prompt.ask("Masukkan nama siswa yang dicari", console=console).strip()
            if target_name:
                found_res = search_student_in_results(all_results, target_name)
                if found_res is not None:
                    display_single_student_card(console, found_res)
                else:
                    console.print(f"\n[bold red]Siswa dengan nama '{target_name}' tidak ditemukan di jurusan ini.[/bold red]\n")
                Prompt.ask("\n[dim]Tekan Enter untuk kembali ke tabel peringkat...[/dim]", default="", console=console)