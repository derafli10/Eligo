#    Modul ini mempercantik laporan di layar komputer:
#    - Mengubah tulisan angka 87.50 menjadi 87,50.
#    - Memberi warna hijau cerah untuk siswa yang LOLOS KUOTA (Eligible),
#      kuning untuk siswa CADANGAN, dan abu-abu redup untuk siswa yang tidak ikut TKA.
#    - Menyusun data ke dalam tabel rapi bergaris seperti Excel di dalam layar hitam terminal.
# 

from __future__ import annotations

import decimal
from decimal import Decimal

from rich.panel import Panel
from rich.table import Table

from eligo.domain.models import EligibilityStatus, RankingResult

__all__ = [
    "format_decimal",
    "badge_status",
    "create_student_table",
    "create_summary_panel",
]


def format_decimal(val: Decimal | int | float | None, precision: int = 2) -> str:
    # format angka desimal menjadi string dengan koma

    # nilai Desimal("87.50") akan diubah menjadi "87,50"
    # nilai Desimal asli tetap menggunakan titik untuk penghitungan

    # output: string angka dengan pemisah koma (contoh: "92,50"), atau "-" jika None.
    
    if val is None:
        return "-"

    # konversi ke desimal secara presisi
    d = Decimal(str(val))
    step = Decimal("10") ** (-precision)
    quantized = d.quantize(step, rounding=decimal.ROUND_HALF_UP)

    # ubah format string titik menjadi koma
    return f"{quantized:.{precision}f}".replace(".", ",")


def badge_status(status: EligibilityStatus | str) -> str:
    # aturan visual:
    #     - HIJAU   : [green]ELIGIBLE[/green] (lolos kuota SNBP)
    #     - KUNING  : [yellow]CADANGAN[/yellow] (memenuhi syarat TKA namun di luar kuota)
    #     - ABU_ABU : [dim]TIDAK ELIGIBLE (NON-TKA)[/dim] (didiskualifikasi dari kuota)
    raw_val = status.value if isinstance(status, EligibilityStatus) else str(status)
    val = raw_val.upper()

    if val == EligibilityStatus.HIJAU.value:
        return "[bold green]ELIGIBLE[/bold green]"
    elif val == EligibilityStatus.KUNING.value:
        return "[bold yellow]CADANGAN[/bold yellow]"
    elif val == EligibilityStatus.ABU_ABU.value:
        return "[dim]TIDAK ELIGIBLE (NON-TKA)[/dim]"
    return f"[white]{raw_val}[/white]"


def create_student_table(
    results: list[RankingResult],
    page: int = 1,
    page_size: int = 25,
) -> Table:
    # bangun objek tabel rich terpaginasi untuk menampilkan daftar hasil pemeringkatan

    # kolom yang ditampilkan:
    #     Rank, ID Siswa, Nama Siswa, Kelas, Skor S1, S2, S3, S4, S5,
    #     Rerata Rapor, Poin Prestasi, Skor Akhir, Status.
    total_items = len(results)
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    current_page = max(1, min(page, total_pages))

    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_items)
    page_items = results[start_idx:end_idx]

    table = Table(
        title=(
            f"[bold blue]TABEL PEMERINGKATAN SISWA ELIGO SNBP[/bold blue]\n"
            f"[dim]Halaman {current_page} dari {total_pages} (Menampilkan {len(page_items)} dari {total_items} siswa)[/dim]"
        ),
        header_style="bold cyan",
        border_style="bright_blue",
        show_lines=True,
    )

    table.add_column("Rank", justify="center", style="bold white")
    table.add_column("ID", justify="center")
    table.add_column("Nama Lengkap", justify="left")
    table.add_column("Kelas", justify="center")
    table.add_column("S1", justify="right")
    table.add_column("S2", justify="right")
    table.add_column("S3", justify="right")
    table.add_column("S4", justify="right")
    table.add_column("S5", justify="right")
    table.add_column("Rerata", justify="right")
    table.add_column("Poin", justify="right")
    table.add_column("Skor Akhir", justify="right", style="bold yellow")
    table.add_column("Status", justify="center")

    for item in page_items:
        rank_str = str(item.rank) if item.rank is not None else "-"
        s1 = format_decimal(item.semester_scores[0]) if len(item.semester_scores) > 0 else "-"
        s2 = format_decimal(item.semester_scores[1]) if len(item.semester_scores) > 1 else "-"
        s3 = format_decimal(item.semester_scores[2]) if len(item.semester_scores) > 2 else "-"
        s4 = format_decimal(item.semester_scores[3]) if len(item.semester_scores) > 3 else "-"
        s5 = format_decimal(item.semester_scores[4]) if len(item.semester_scores) > 4 else "-"
        rerata = format_decimal(item.report_score)
        poin = format_decimal(item.achievement_points)
        akhir = format_decimal(item.final_score)
        status_badge = badge_status(item.status)

        table.add_row(
            rank_str,
            item.student.id,
            item.student.name,
            item.student.class_name,
            s1,
            s2,
            s3,
            s4,
            s5,
            rerata,
            poin,
            akhir,
            status_badge,
        )

    return table


def create_summary_panel(
    total_students: int,
    quota: int,
    results: list[RankingResult],
    major_name: str = "",
) -> Panel:
    # bikin panel Rich ringkasan statistik kuota dan status siswa
    count_hijau = sum(1 for r in results if r.status == EligibilityStatus.HIJAU)
    count_kuning = sum(1 for r in results if r.status == EligibilityStatus.KUNING)
    count_abu = sum(1 for r in results if r.status == EligibilityStatus.ABU_ABU)

    summary_text = (
        f"[bold cyan]Jurusan:[/bold cyan] {major_name or 'Semua Jurusan'}\n"
        f"[bold]Total Siswa Jurusan:[/bold] {total_students} siswa\n"
        f"[bold]Alokasi Kuota Eligible:[/bold] {quota} kursi\n"
        f"──────────────────────────────────────────────\n"
        f"[bold green]- ELIGIBLE (HIJAU):[/bold green]   {count_hijau} siswa (Berhak mendaftar SNBP)\n"
        f"[bold yellow]- CADANGAN (KUNING):[/bold yellow]  {count_kuning} siswa (Memenuhi syarat, di luar kuota)\n"
        f"[dim]- NON-TKA (ABU-ABU):[/dim]   {count_abu} siswa (Tidak mengikuti TKA)"
    )

    return Panel(
        summary_text,
        title="[bold green]RINGKASAN KUOTA & STATUS SNBP[/bold green]",
        border_style="green",
        expand=False,
    )