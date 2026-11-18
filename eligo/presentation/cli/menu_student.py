#     Menu ini bekerja seperti "Buku Absensi & Rapor Siswa":
#     - bisa melihat siapa aja siswa yang sudah terdaftar di sekolah
#     - bisa mendaftarkan siswa baru secara manual satu per satu:
#       masukkan nama siswa, kelasnya (misal XII-MIPA-1), lalu masukkan nilai
#       rapornya dari semester 1 sampai 5
#     - jika salah ketik nilai (misalnya mengetik 105 atau huruf), sistem langsung
#       mengingatkan dengan ramah agar memasukkan angka yang benar
#     - siswa otomatis mendapatkan nomor induk berurutan seperti S001, S002, dst.

from __future__ import annotations

from dataclasses import replace

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from eligo.application.school_service import get_school_profile
from eligo.application.student_service import (
    add_student,
    delete_student,
    get_all_students,
    get_student_by_id,
    get_students_by_major,
    update_student,
)
from eligo.domain.exceptions import ValidationError
from eligo.domain.models import (
    Achievement,
    AchievementLevel,
    SchoolProfile,
    Student,
)
from eligo.infrastructure.repositories.config_repo import JsonConfigRepository
from eligo.infrastructure.repositories.school_repo import JsonSchoolRepository
from eligo.infrastructure.repositories.student_repo import JsonStudentRepository


def render_student_list_table(console: Console, students: list[Student], title: str = "DAFTAR SISWA") -> None:
    # cetak tabel ringkasan data siswa ke konsol
    if not students:
        console.print(
            Panel(
                "[bold yellow]Belum ada data siswa yang terdaftar.[/bold yellow]\n"
                "[dim]Gunakan menu 'Tambah Siswa Manual' atau menu 'Impor CSV' untuk memasukkan data.[/dim]",
                title=f"[bold yellow]ℹ️ {title}[/bold yellow]",
                border_style="yellow",
            )
        )
        return

    table = Table(
        title=f"[bold cyan]{title} ({len(students)} Siswa)[/bold cyan]",
        border_style="cyan",
        header_style="bold yellow",
        show_lines=True,
    )
    table.add_column("No", justify="center", style="dim")
    table.add_column("ID", justify="center", style="bold white")
    table.add_column("Nama Lengkap", justify="left")
    table.add_column("Kelas", justify="center")
    table.add_column("Jurusan", justify="center")
    table.add_column("Status TKA", justify="center")
    table.add_column("Prestasi", justify="center")

    for idx, s in enumerate(students, start=1):
        tka_str = "[bold green]IKUT[/bold green]" if s.tka_status.value == "IKUT" else "[dim]TIDAK[/dim]"
        ach_count = f"{len(s.achievements)} sertifikat" if s.achievements else "-"
        table.add_row(str(idx), s.id, s.name, s.class_name, s.major_code, tka_str, ach_count)

    console.print(table)


def handle_add_student_manual(
    console: Console,
    student_repo: JsonStudentRepository,
    school_profile: SchoolProfile,
    config_repo: JsonConfigRepository,
) -> None:
    # form penambahan siswa baru secara manual
    console.print("\n[bold yellow]── FORM PENDAFTARAN SISWA BARU ──[/bold yellow]")

    # 1. identitas siswa
    name = Prompt.ask("Nama Lengkap Siswa", console=console).strip()
    if not name:
        console.print("[bold red]Nama siswa tidak boleh kosong.[/bold red]")
        return

    class_name = Prompt.ask("Nama Kelas (contoh: XII-MIPA-1)", console=console).strip()
    if not class_name:
        console.print("[bold red]Nama kelas tidak boleh kosong.[/bold red]")
        return

    # 2. pilihan jurusan
    available_majors = [m.code.upper() for m in school_profile.majors]
    console.print(f"[cyan]Jurusan yang tersedia di sekolah:[/cyan] {', '.join(available_majors)}")
    major_code = Prompt.ask("Pilih Kode Jurusan", choices=available_majors, console=console).upper()

    chosen_major = next(m for m in school_profile.majors if m.code.upper() == major_code)

    # 3. status TKA
    ikut_tka = Confirm.ask("Apakah siswa mengikuti Tes Kemampuan Akademik (TKA)?", default=True, console=console)
    tka_val = "IKUT" if ikut_tka else "TIDAK_IKUT"

    # 4. input nilai rapor semester 1 sampai 5
    console.print("\n[bold cyan]Input Nilai Rapor Semester 1 s.d. 5 (Rentang 0 - 100):[/bold cyan]")
    grades_list: list[dict[str, int]] = []

    for sem_idx in range(5):
        sem_num = sem_idx + 1
        console.print(f"[bold yellow]► Nilai Semester {sem_num}:[/bold yellow]")
        sem_dict: dict[str, int] = {}
        semester_subjects = chosen_major.subjects[sem_idx]

        for subj in semester_subjects:
            while True:
                val = IntPrompt.ask(f"  Nilai {subj.name} ({subj.code})", default=80, console=console)
                if 0 <= val <= 100:
                    sem_dict[subj.code] = val
                    break
                console.print("  [bold red]Nilai harus berada dalam rentang 0 sampai 100![/bold red]")
        grades_list.append(sem_dict)

    # 5. input sertifikat prestasi (opsional)
    achievements: list[Achievement] = []
    if school_profile.achievement_enabled:
        has_ach = Confirm.ask("\nApakah siswa memiliki sertifikat prestasi juara?", default=False, console=console)
        if has_ach:
            console.print("[dim]Anda dapat memasukkan hingga maksimal 5 prestasi.[/dim]")
            while len(achievements) < 5:
                desc = Prompt.ask(f"Nama/Deskripsi Prestasi ke-{len(achievements) + 1} (Kosongkan jika selesai)", default="", console=console).strip()
                if not desc:
                    break
                level_str = Prompt.ask(
                    "Tingkat Kejuaraan",
                    choices=["KABUPATEN_KOTA", "PROVINSI", "NASIONAL", "INTERNASIONAL"],
                    default="KABUPATEN_KOTA",
                    console=console,
                )
                achievements.append(Achievement(description=desc, level=AchievementLevel(level_str)))

    # 6. simpan siswa via student service
    cfg = config_repo.load()
    try:
        new_stu = add_student(
            name=name,
            class_name=class_name,
            major_code=major_code,
            tka_status=tka_val,
            grades=grades_list,
            achievements=achievements,
            school_profile=school_profile,
            repo=student_repo,
            tka_synonyms=cfg.tka_synonyms,
        )
        console.print(
            Panel(
                f"[bold green]Siswa berhasil didaftarkan![/bold green]\n"
                f"[bold cyan]ID Baru Siswa:[/bold cyan] {new_stu.id}\n"
                f"[bold cyan]Nama Lengkap:[/bold cyan]  {new_stu.name}\n"
                f"[bold cyan]Kelas & Jurusan:[/bold cyan] {new_stu.class_name} ({new_stu.major_code})",
                title="[bold green]✅ PENDAFTARAN BERHASIL[/bold green]",
                border_style="green",
            )
        )
    except ValidationError as err:
        console.print(f"\n[bold red]❌ Gagal Menyimpan Data Siswa:[/bold red] {err.message}\n")


def _render_grades_table(matched: Student) -> Table:
    # helper untuk membuat perenderan tabel rincian nilai 5 semester siswa
    table = Table(
        title=f"[bold yellow]RINCIAN NILAI RAPOR (SEMESTER 1 s.d. 5) - {matched.name.upper()} ({matched.id})[/bold yellow]",
        border_style="yellow",
        show_lines=True,
    )
    table.add_column("Mata Pelajaran", justify="left", style="bold white")
    for sem in range(1, 6):
        table.add_column(f"Sem {sem}", justify="center")

    all_subj_codes: set[str] = set()
    for sem_dict in matched.grades:
        all_subj_codes.update(sem_dict.keys())

    for subj_code in sorted(all_subj_codes):
        row_vals = [subj_code]
        for sem_idx in range(5):
            val = matched.grades[sem_idx].get(subj_code, "-")
            row_vals.append(str(val))
        table.add_row(*row_vals)

    return table


def _handle_edit_student_grade(
    console: Console,
    student: Student,
    student_repo: JsonStudentRepository,
    school_profile: SchoolProfile | None,
) -> Student:
    # pengeditan nilai rapor siswa pada semester dan mata pelajaran tertentu

    # Alur:
    #     1. minta semester berapa yang ingin diedit (1 s.d. 5)
    #     2. minta kode mata pelajaran yang ingin diubah nilainya
    #     3. minta nilai baru (rentang 0 s.d. 100)
    #     4. minta konfirmasi apakah yakin ingin mengganti nilai tersebut (y/n)
    #     5. jika Ya (y): simpan perubahan ke repositori dan tampilkan tabel nilai terbaru
    #     6. jika Tidak (n): batalkan perubahan dan pertahankan nilai lama
    current_student = student

    while True:
        console.print("\n[bold yellow]── FORM EDIT NILAI RAPOR ──[/bold yellow]")

        # 1. minta edit data semester berapa
        sem_str = Prompt.ask(
            "Edit data semester berapa?",
            choices=["1", "2", "3", "4", "5"],
            console=console,
        )
        sem_idx = int(sem_str) - 1
        current_sem_grades = current_student.grades[sem_idx]

        if not current_sem_grades:
            console.print(f"[bold red]Tidak ada mata pelajaran yang terdaftar pada Semester {sem_str}.[/bold red]")
            if not Confirm.ask("Coba pilih semester lain?", default=True, console=console):
                break
            continue

        # 2. mata pelajaran apa (input kode mata pelajarannya)
        available_codes = sorted(current_sem_grades.keys())
        console.print(f"[cyan]Mata pelajaran tersedia di Semester {sem_str}:[/cyan] {', '.join(available_codes)}")
        subj_code = Prompt.ask(
            "Mata pelajaran apa yang ingin diedit? (masukkan kode mapel)",
            console=console,
        ).strip().upper()

        if subj_code not in current_sem_grades:
            console.print(
                f"[bold red]Kode mapel '{subj_code}' tidak ditemukan pada Semester {sem_str}. "
                f"Pilihan yang tersedia: {', '.join(available_codes)}[/bold red]"
            )
            if not Confirm.ask("Coba lagi?", default=True, console=console):
                break
            continue

        old_val = current_sem_grades[subj_code]
        console.print(f"[dim]Nilai saat ini untuk {subj_code} Semester {sem_str}: {old_val}[/dim]")

        # 3. minta nilai baru untuk mengganti nilai lama yang dipilih
        while True:
            new_val = IntPrompt.ask(
                f"Masukkan nilai baru untuk {subj_code} Semester {sem_str} (0 - 100)",
                default=old_val,
                console=console,
            )
            if 0 <= new_val <= 100:
                break
            console.print("[bold red]Nilai harus berupa bilangan bulat antara 0 sampai 100![/bold red]")

        if new_val == old_val:
            console.print(f"[yellow]Nilai baru sama dengan nilai lama ({old_val}). Tidak ada perubahan yang disimpan.[/yellow]")
            if not Confirm.ask("Apakah ingin mengedit nilai mata pelajaran lainnya?", default=False, console=console):
                break
            continue

        # 4. konfirmasi apakah yakin ingin mengganti nilai tersebut?
        confirm_save = Confirm.ask(
            f"Apakah Anda yakin ingin mengganti nilai {subj_code} Semester {sem_str} "
            f"dari [bold red]{old_val}[/bold red] menjadi [bold green]{new_val}[/bold green]?",
            default=True,
            console=console,
        )

        # 5. jika y, simpan. jika n, batalkan
        if confirm_save:
            updated_grades_list = list(current_student.grades)
            new_sem_dict = dict(updated_grades_list[sem_idx])
            new_sem_dict[subj_code] = new_val
            updated_grades_list[sem_idx] = new_sem_dict

            updated_student = replace(current_student, grades=tuple(updated_grades_list))

            if school_profile is not None:
                try:
                    update_student(updated_student, school_profile, student_repo)
                except ValidationError as err:
                    console.print(f"[bold red]Gagal memperbarui nilai: {err.message}[/bold red]")
                    break
            else:
                all_students = student_repo.load_all()
                all_updated = [updated_student if s.id == current_student.id else s for s in all_students]
                student_repo.save_all(all_updated)

            current_student = updated_student
            console.print(
                f"\n[bold green]✅ Berhasil! Nilai {subj_code} Semester {sem_str} "
                f"milik {current_student.name} telah diubah menjadi {new_val}.[/bold green]\n"
            )

            # tampilin tabel rincian nilai terbaru
            console.print(_render_grades_table(current_student))
        else:
            console.print("\n[yellow]Pengeditan nilai dibatalkan. Nilai lama tetap dipertahankan.[/yellow]\n")

        # tanyakan apakah ingin mengedit nilai lainnya
        another = Confirm.ask(
            "Apakah Anda ingin mengedit nilai mata pelajaran lainnya untuk siswa ini?",
            default=False,
            console=console,
        )
        if not another:
            break

    return current_student


def handle_view_student_details(
    console: Console,
    student_repo: JsonStudentRepository,
    school_profile: SchoolProfile | None = None,
) -> None:
    # cari dan nampilin rincian nilai rapor lengkap seorang siswa serta menyediakan opsi edit nilai
    keyword = Prompt.ask("Masukkan ID Siswa (contoh: S001) atau Nama Siswa", console=console).strip()
    if not keyword:
        return

    students = student_repo.load_all()
    matched: Student | None = None

    # cari berdasarkan ID dulu
    target_id = keyword.upper()
    for s in students:
        if s.id.upper() == target_id or keyword.lower() in s.name.lower():
            matched = s
            break

    if matched is None:
        console.print(f"\n[bold red]Tidak ditemukan siswa dengan kata kunci '{keyword}'.[/bold red]\n")
        return

    # tampilin kartu identitas siswa
    tka_badge = "[bold green]IKUT TKA[/bold green]" if matched.tka_status.value == "IKUT" else "[dim]TIDAK IKUT[/dim]"
    info_text = (
        f"[bold cyan]ID Siswa:[/bold cyan]      {matched.id}\n"
        f"[bold cyan]Nama Lengkap:[/bold cyan]  {matched.name}\n"
        f"[bold cyan]Kelas:[/bold cyan]         {matched.class_name}\n"
        f"[bold cyan]Jurusan:[/bold cyan]       {matched.major_code}\n"
        f"[bold cyan]Status TKA:[/bold cyan]    {tka_badge}\n"
        f"[bold cyan]Jml Prestasi:[/bold cyan]  {len(matched.achievements)} sertifikat"
    )
    console.print(
        Panel(
            info_text,
            title="[bold green]KARTU RINCIAN DATA SISWA[/bold green]",
            border_style="green",
        )
    )

    # tampilin tabel nilai rapor tiap semester
    console.print(_render_grades_table(matched))

    # beri opsi untuk edit data nilai jika ada kesalahan input
    want_edit = Confirm.ask(
        "\n[bold yellow]Apakah Anda ingin mengedit nilai rapor siswa ini?[/bold yellow]",
        default=False,
        console=console,
    )
    if want_edit:
        _handle_edit_student_grade(console, matched, student_repo, school_profile)


def handle_delete_student(console: Console, student_repo: JsonStudentRepository) -> None:
    # hapus data siswa dengan konfirmasi keamanan
    student_id = Prompt.ask("Masukkan ID Siswa yang akan dihapus (contoh: S001)", console=console).strip().upper()
    student = get_student_by_id(student_id, student_repo)

    if student is None:
        console.print(f"[bold red]Siswa dengan ID '{student_id}' tidak ditemukan.[/bold red]")
        return

    console.print(
        Panel(
            f"ID: [bold white]{student.id}[/bold white]\n"
            f"Nama: [bold yellow]{student.name}[/bold yellow]\n"
            f"Kelas: {student.class_name} ({student.major_code})",
            title="[bold red]KONFIRMASI PENGHAPUSAN SISWA[/bold red]",
            border_style="red",
        )
    )

    yakin = Confirm.ask(f"Apakah Anda benar-benar yakin ingin menghapus {student.name} dari database?", default=False, console=console)
    if yakin:
        delete_student(student.id, student_repo)
        console.print(f"\n[bold green]✅ Data siswa {student.name} ({student.id}) berhasil dihapus dari sistem.[/bold green]\n")
    else:
        console.print("\n[yellow]Penghapusan dibatalkan. Data siswa tetap aman.[/yellow]\n")


def display_student_menu(
    console: Console,
    student_repo: JsonStudentRepository,
    school_repo: JsonSchoolRepository,
    config_repo: JsonConfigRepository,
) -> None:
    # nampilin alur menu manajemen siswa
    profile = get_school_profile(school_repo)
    if profile is None or not profile.majors:
        console.print(
            Panel(
                "[bold red]Profil sekolah atau kurikulum jurusan belum diatur![/bold red]\n"
                "[white]Harap buka Menu 1 (Profil Sekolah) terlebih dahulu sebelum mengelola siswa.[/white]",
                title="[bold red]⚠️ PRASYARAT KURIKULUM BELUM TERPENUHI[/bold red]",
                border_style="red",
            )
        )
        return

    while True:
        console.print(
            Panel(
                "[bold green]1.[/bold green] Daftar Seluruh Siswa Terdaftar (Buku Induk)\n"
                "[bold green]2.[/bold green] Saring Daftar Siswa Berdasarkan Jurusan\n"
                "[bold green]3.[/bold green] Tambah Siswa Baru Secara Manual (Entri Nilai)\n"
                "[bold green]4.[/bold green] Cari Siswa, Lihat, dan Edit Rincian Nilai 5 Semester\n"
                "[bold green]5.[/bold green] Hapus Data Siswa dari Buku Induk\n"
                "[bold red]0.[/bold red] Kembali ke Menu Utama",
                title="[bold cyan]MANAJEMEN DATA SISWA (BUKU INDUK)[/bold cyan]",
                border_style="cyan",
            )
        )
        choice = Prompt.ask(
            "[bold cyan]Pilihan Anda[/bold cyan]",
            choices=["0", "1", "2", "3", "4", "5"],
            default="1",
            console=console,
        )

        if choice == "0":
            break
        elif choice == "1":
            students = get_all_students(student_repo)
            render_student_list_table(console, students, "BUKU INDUK SELURUH SISWA")
        elif choice == "2":
            available_majors = [m.code.upper() for m in profile.majors]
            chosen_major = Prompt.ask("Pilih Jurusan", choices=available_majors, console=console).upper()
            filtered = get_students_by_major(chosen_major, student_repo)
            render_student_list_table(console, filtered, f"DAFTAR SISWA JURUSAN {chosen_major}")
        elif choice == "3":
            handle_add_student_manual(console, student_repo, profile, config_repo)
        elif choice == "4":
            handle_view_student_details(console, student_repo, profile)
        elif choice == "5":
            handle_delete_student(console, student_repo)