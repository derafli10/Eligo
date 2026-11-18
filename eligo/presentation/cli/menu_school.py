#     menu ini seperti papan identitas sekolah:
#     - di sini bisa melihat nama sekolah, status akreditasi (A, B, atau C),
#       dan apakah sekolah sudah menggunakan e-Rapor resmi kementerian
#     - bisa mengubah akreditasi jika sekolah baru saja diakreditasi ulang
#     - juga bisa mendaftarkan jurusan baru (misal: MIPA, IPS, TKJ, RPL)
#       dan mengisi mata pelajaran wajib untuk tiap semester (Semester 1 sampai 5)
#       secara manual sesuai kurikulum yang berlaku di sekolah.

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from eligo.application.school_service import (
    add_major_to_school,
    get_school_profile,
    save_school_profile,
    update_school_settings,
)
from eligo.domain.exceptions import ValidationError
from eligo.domain.models import (
    Accreditation,
    Major,
    SchoolProfile,
    SchoolType,
    Subject,
)
from eligo.infrastructure.repositories.config_repo import JsonConfigRepository
from eligo.infrastructure.repositories.school_repo import JsonSchoolRepository


def display_school_profile_panel(console: Console, profile: SchoolProfile | None) -> None:
    # nampilin rincian data sekolah dan kurikulum jurusan dalam format panel dan tabel
    if profile is None:
        console.print(
            Panel(
                "[bold yellow]Profil sekolah belum pernah didaftarkan.[/bold yellow]\n"
                "[white]Silakan pilih menu 'Ubah Profile Sekolah' untuk memulai.[/white]",
                title="[bold yellow]BELUM DIKONFIGURASI[/bold yellow]",
                border_style="yellow",
            )
        )
        return

    erapor_str = (
        "[bold green]AKTIF (+5% Bonus Kuota)[/bold green]"
        if profile.e_rapor_active
        else "[dim]Non-Aktif[/dim]"
    )
    ach_str = (
        "[bold green]AKTIF (Maks. 2.00 Poin)[/bold green]"
        if profile.achievement_enabled
        else "[dim]Non-Aktif[/dim]"
    )

    profile_info = (
        f"[bold cyan]Nama Sekolah:[/bold cyan]        {profile.name}\n"
        f"[bold cyan]Jenjang Pendidikan:[/bold cyan]  {profile.school_type.value}\n"
        f"[bold cyan]Status Akreditasi:[/bold cyan]   [bold yellow]{profile.accreditation.value}[/bold yellow]\n"
        f"[bold cyan]Sistem e-Rapor:[/bold cyan]      {erapor_str}\n"
        f"[bold cyan]Opsi Poin Prestasi:[/bold cyan]  {ach_str}\n"
        f"[bold cyan]Jumlah Jurusan:[/bold cyan]      {len(profile.majors)} jurusan terdaftar"
    )

    console.print(
        Panel(
            profile_info,
            title="[bold green]PROFIL KELEMBAGAAN SEKOLAH[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )

    # nampilin tabel jurusan dan kurikulum mapelnya jika ada
    if profile.majors:
        table = Table(
            title="[bold cyan]DAFTAR JURUSAN & MATA PELAJARAN SEMESTER 1-5[/bold cyan]",
            border_style="cyan",
            header_style="bold yellow",
            show_lines=True,
        )
        table.add_column("No", justify="center", style="dim")
        table.add_column("Kode", justify="center", style="bold white")
        table.add_column("Nama Jurusan", justify="left")
        table.add_column("Daftar Mapel Wajib (S1 s.d. S5)", justify="left")

        for idx, m in enumerate(profile.majors, start=1):
            # cek apakah kurikulum mapel seluruh semester sama
            all_same = all(m.subjects[i] == m.subjects[0] for i in range(1, 5))
            if all_same:
                subjs_text = ", ".join(f"{s.name} ({s.code})" for s in m.subjects[0])
            else:
                lines: list[str] = []
                for s_idx in range(5):
                    s_str = ", ".join(s.code for s in m.subjects[s_idx])
                    lines.append(f"S{s_idx + 1}: {s_str}")
                subjs_text = " | ".join(lines)
            table.add_row(str(idx), m.code, m.name, subjs_text)

        console.print(table)


def handle_edit_school_settings(console: Console, school_repo: JsonSchoolRepository) -> None:
    # form untuk memperbarui informasi dan akreditasi sekolah
    current = get_school_profile(school_repo)

    console.print("\n[bold yellow]FORM PENGATURAN PROFIL SEKOLAH[/bold yellow]")
    console.print("[dim]Tekan Enter langsung jika tidak ingin mengubah nilai lama.[/dim]\n")

    current_name = current.name if current else "SMA Negeri 1 Contoh"
    current_type = current.school_type.value if current else "SMA"
    current_acc = current.accreditation.value if current else "A"
    current_erapor = current.e_rapor_active if current else True
    current_ach = current.achievement_enabled if current else True

    new_name = Prompt.ask("Nama Lengkap Sekolah", default=current_name, console=console)
    new_type_str = Prompt.ask(
        "Jenjang Sekolah", choices=["SMA", "SMK", "MA"], default=current_type, console=console
    )
    new_acc_str = Prompt.ask(
        "Akreditasi Sekolah", choices=["A", "B", "C"], default=current_acc, console=console
    )
    new_erapor = Confirm.ask(
        "Aktifkan Tambahan Kuota e-Rapor (+5%)?", default=current_erapor, console=console
    )
    new_ach = Confirm.ask(
        "Aktifkan Tambahan Poin Prestasi Siswa?", default=current_ach, console=console
    )

    if current is None:
        # inisialisasi awal profil sekolah TANPA jurusan apapun.
        # pengguna akan menambahkan jurusan secara manual melalui
        # menu "Tambah Jurusan Baru ke Sekolah" (opsi 3).
        new_profile = SchoolProfile(
            name=new_name,
            school_type=SchoolType(new_type_str),
            accreditation=Accreditation(new_acc_str),
            e_rapor_active=new_erapor,
            achievement_enabled=new_ach,
            majors=(),
        )
        save_school_profile(new_profile, school_repo)
    else:
        update_school_settings(
            repo=school_repo,
            name=new_name,
            school_type=new_type_str,
            accreditation=new_acc_str,
            e_rapor_active=new_erapor,
            achievement_enabled=new_ach,
        )

    console.print("\n[bold green]✅ Pengaturan profil sekolah berhasil disimpan dengan aman![/bold green]\n")


def _collect_semester_subjects(console: Console, semester_num: int) -> tuple[Subject, ...]:
    # ngumpulin daftar mata pelajaran untuk suatu semester dari kondisi kosong

    # fungsi ini minta operator memasukkan kode dan nama setiap mata pelajaran
    # secara bertahap sampai operator menekan Enter tanpa kode mapel
    console.print(f"\n[bold cyan]PENGISIAN MATA PELAJARAN SEMESTER {semester_num}[/bold cyan]")
    console.print("[dim]Kondisi awal mata pelajaran KOSONG. Masukkan satu per satu.[/dim]")
    console.print("[dim]Kosongkan 'Kode Mapel' (tekan Enter langsung) jika sudah selesai.[/dim]\n")

    subjects: list[Subject] = []
    while True:
        prompt_text = (
            f"  [No. {len(subjects) + 1}] Kode Mapel (contoh: MTK, BIN, FIS, KJD)"
            if not subjects
            else f"  [No. {len(subjects) + 1}] Kode Mapel berikutnya (Enter jika selesai)"
        )
        code_input = Prompt.ask(prompt_text, default="", console=console).strip().upper()

        if not code_input:
            if not subjects:
                console.print("  [bold red]Minimal wajib menambahkan 1 mata pelajaran per semester![/bold red]")
                continue
            break

        # cek apakah kode mapel sudah ada di semester ini
        if any(s.code == code_input for s in subjects):
            console.print(f"  [bold red]Kode mapel '{code_input}' sudah ada di semester ini![/bold red]")
            continue

        name_input = Prompt.ask(f"         Nama Lengkap Mapel untuk '{code_input}'", console=console).strip()
        if not name_input:
            console.print("  [bold red]Nama mata pelajaran tidak boleh kosong![/bold red]")
            continue

        subjects.append(Subject(code=code_input, name=name_input))
        console.print(f"  [green]✓ Mapel '{name_input} ({code_input})' ditambahkan ke Semester {semester_num}.[/green]")

    return tuple(subjects)


def handle_add_major(console: Console, school_repo: JsonSchoolRepository) -> None:
    # form untuk menambahkan jurusan baru dan mengisi mata pelajaran 5 semester secara manual
    current = get_school_profile(school_repo)
    if current is None:
        console.print("[bold red]Harap atur profil sekolah terlebih dahulu sebelum menambah jurusan.[/bold red]")
        return

    console.print("\n[bold yellow]── FORM PENAMBAHAN JURUSAN BARU ──[/bold yellow]")
    major_code = Prompt.ask("Kode Jurusan Baru (contoh: MIPA, IPS, TKJ, RPL)", console=console).strip().upper()
    major_name = Prompt.ask("Nama Lengkap Jurusan (contoh: Teknik Komputer dan Jaringan)", console=console).strip()

    if not major_code or not major_name:
        console.print("[bold red]Kode dan nama jurusan tidak boleh kosong.[/bold red]")
        return

    # validasi: pastikan kode jurusan belum pernah digunakan di sekolah ini
    for existing in current.majors:
        if existing.code.upper() == major_code:
            console.print(f"\n[bold red]❌ Jurusan dengan kode '{major_code}' sudah terdaftar di sekolah ini![/bold red]\n")
            return

    console.print(
        Panel(
            f"[bold cyan]Jurusan Baru:[/bold cyan] [bold white]{major_name} ({major_code})[/bold white]\n\n"
            f"[white]Mata pelajaran dimulai dari [bold yellow]KOSONG[/bold yellow].[/white]\n"
            f"[white]Anda akan mengisi mata pelajaran untuk [bold cyan]Semester 1 sampai Semester 5[/bold cyan] "
            f"secara manual.[/white]",
            title="[bold yellow]📖 PENGISIAN KURIKULUM MATA PELAJARAN[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
    )

    # 1. Tingkat Kelas X (Semester 1 & 2)
    console.print(
        Panel(
            "[bold white]1. Tingkat Kelas X (Semester 1 & 2)[/bold white]\n"
            "[dim]Mulai dengan mengisi mata pelajaran untuk Semester 1 (Ganjil).[/dim]",
            title="[bold cyan]TINGKAT KELAS X[/bold cyan]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    sem1_subjects = _collect_semester_subjects(console, semester_num=1)

    console.print("\n[bold cyan]Daftar Mapel Semester 1 yang telah dimasukkan:[/bold cyan]")
    for idx, s in enumerate(sem1_subjects, start=1):
        console.print(f"  {idx}. {s.name} ({s.code})")

    same_for_sem2 = Confirm.ask(
        "\n[bold yellow]Apakah daftar mata pelajaran di atas berlaku SAMA untuk Semester 2?[/bold yellow]",
        default=True,
        console=console,
    )
    if same_for_sem2:
        console.print("[dim]Menerapkan daftar mata pelajaran Semester 1 ke Semester 2...[/dim]")
        sem2_subjects = sem1_subjects
    else:
        sem2_subjects = _collect_semester_subjects(console, semester_num=2)

    # 2. Tingkat Kelas XI (Semester 3 & 4) 
    console.print(
        Panel(
            "[bold white]2. Tingkat Kelas XI (Semester 3 & 4)[/bold white]\n"
            "[dim]Mata pelajaran pada tingkat baru (Kelas XI) dapat berbeda dari Kelas X.[/dim]",
            title="[bold cyan]TINGKAT KELAS XI[/bold cyan]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    copy_sem2 = Confirm.ask(
        "[bold yellow]Apakah ingin menyalin daftar mata pelajaran dari Semester 2 untuk Semester 3?[/bold yellow]",
        default=False,
        console=console,
    )
    if copy_sem2:
        console.print("[dim]Menyalin daftar mata pelajaran Semester 2 ke Semester 3...[/dim]")
        sem3_subjects = sem2_subjects
    else:
        sem3_subjects = _collect_semester_subjects(console, semester_num=3)

    console.print("\n[bold cyan]Daftar Mapel Semester 3 yang telah dimasukkan:[/bold cyan]")
    for idx, s in enumerate(sem3_subjects, start=1):
        console.print(f"  {idx}. {s.name} ({s.code})")

    same_for_sem4 = Confirm.ask(
        "\n[bold yellow]Apakah daftar mata pelajaran di atas berlaku SAMA untuk Semester 4?[/bold yellow]",
        default=True,
        console=console,
    )
    if same_for_sem4:
        console.print("[dim]Menerapkan daftar mata pelajaran Semester 3 ke Semester 4...[/dim]")
        sem4_subjects = sem3_subjects
    else:
        sem4_subjects = _collect_semester_subjects(console, semester_num=4)

    # 3. Tingkat Kelas XII (Semester 5) 
    console.print(
        Panel(
            "[bold white]3. Tingkat Kelas XII (Semester 5)[/bold white]\n"
            "[dim]Evaluasi seleksi kuota SNBP mencakup nilai rapor hingga Semester 5.[/dim]",
            title="[bold cyan]TINGKAT KELAS XII[/bold cyan]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    copy_sem4 = Confirm.ask(
        "[bold yellow]Apakah ingin menyalin daftar mata pelajaran dari Semester 4 untuk Semester 5?[/bold yellow]",
        default=False,
        console=console,
    )
    if copy_sem4:
        console.print("[dim]Menyalin daftar mata pelajaran Semester 4 ke Semester 5...[/dim]")
        sem5_subjects = sem4_subjects
    else:
        sem5_subjects = _collect_semester_subjects(console, semester_num=5)

    all_semesters: list[tuple[Subject, ...]] = [
        sem1_subjects,
        sem2_subjects,
        sem3_subjects,
        sem4_subjects,
        sem5_subjects,
    ]

    # nampilin tabel konfirmasi kurikulum 5 semester 
    summary_table = Table(
        title=f"[bold green]KURIKULUM 5 SEMESTER: {major_name.upper()} ({major_code})[/bold green]",
        border_style="green",
        header_style="bold yellow",
        show_lines=True,
    )
    summary_table.add_column("Semester", justify="center", style="bold cyan")
    summary_table.add_column("Jumlah Mapel", justify="center")
    summary_table.add_column("Daftar Mata Pelajaran (Nama & Kode)", justify="left")

    for sem_num, subjs in enumerate(all_semesters, start=1):
        subjs_text = ", ".join(f"{s.name} ({s.code})" for s in subjs)
        summary_table.add_row(f"Semester {sem_num}", str(len(subjs)), subjs_text)

    console.print()
    console.print(summary_table)

    save_confirm = Confirm.ask(
        "\n[bold green]Simpan jurusan dan kurikulum mata pelajaran ini ke sistem?[/bold green]",
        default=True,
        console=console,
    )

    if not save_confirm:
        console.print("\n[yellow]Penambahan jurusan dibatalkan. Tidak ada data yang disimpan.[/yellow]\n")
        return

    new_major = Major(
        code=major_code,
        name=major_name,
        subjects=(
            all_semesters[0],
            all_semesters[1],
            all_semesters[2],
            all_semesters[3],
            all_semesters[4],
        ),
    )

    try:
        add_major_to_school(school_repo, new_major)
        console.print(
            f"\n[bold green]✅ Jurusan '{major_name} ({major_code})' beserta kurikulum 5 semester "
            f"berhasil ditambahkan ke sekolah![/bold green]\n"
        )
    except ValidationError as err:
        console.print(f"\n[bold red]❌ Gagal Menambahkan Jurusan:[/bold red] {err.message}\n")


def display_school_menu(
    console: Console,
    school_repo: JsonSchoolRepository,
    config_repo: JsonConfigRepository,
) -> None:
    """Menampilkan alur menu interaktif manajemen sekolah."""
    while True:
        console.print(
            Panel(
                "[bold green]1.[/bold green] Lihat Rincian Profil & Kurikulum Sekolah\n"
                "[bold green]2.[/bold green] Ubah Profile Sekolah (Nama, Akreditasi, e-Rapor)\n"
                "[bold green]3.[/bold green] Tambah Jurusan Baru ke Sekolah\n"
                "[bold red]0.[/bold red] Kembali ke Menu Utama",
                title="[bold cyan]MANAJEMEN PROFIL SEKOLAH & KURIKULUM[/bold cyan]",
                border_style="cyan",
            )
        )
        choice = Prompt.ask(
            "[bold cyan]Pilihan Anda[/bold cyan]",
            choices=["0", "1", "2", "3"],
            default="1",
            console=console,
        )

        if choice == "0":
            break
        elif choice == "1":
            profile = get_school_profile(school_repo)
            display_school_profile_panel(console, profile)
        elif choice == "2":
            handle_edit_school_settings(console, school_repo)
        elif choice == "3":
            handle_add_major(console, school_repo)