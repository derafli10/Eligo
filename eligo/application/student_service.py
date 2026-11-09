
from __future__ import annotations

from eligo.domain.exceptions import ErrorCode, ValidationError
from eligo.domain.models import Achievement, SchoolProfile, Student, TkaStatus
from eligo.domain.normalizer import (
    normalize_class_name,
    normalize_name,
    normalize_tka_status,
)
from eligo.domain.repositories import StudentRepository
from eligo.domain.validator import (
    validate_grade,
    validate_major_exists,
    validate_name_nonempty,
)


def get_all_students(repo: StudentRepository) -> list[Student]:
    """Mengambil seluruh daftar siswa yang terdaftar di basis data sekolah.

    Args:
        repo: Repositori siswa.

    Returns:
        List seluruh entitas Student.
    """
    return repo.load_all()


def get_students_by_major(major_code: str, repo: StudentRepository) -> list[Student]:
    """Mengambil daftar siswa yang terdaftar pada jurusan tertentu.

    Args:
        major_code: Kode jurusan (misal 'MIPA' atau 'IPS').
        repo: Repositori siswa.

    Returns:
        List siswa yang terdaftar pada jurusan tersebut.
    """
    return repo.get_by_major(major_code)


def get_student_by_id(student_id: str, repo: StudentRepository) -> Student | None:
    """Mencari data siswa berdasarkan nomor pengenal unik (ID).

    Args:
        student_id: ID siswa (misal 'S001').
        repo: Repositori siswa.

    Returns:
        Objek Student jika ditemukan, atau None jika tidak ada.
    """
    target = student_id.strip().upper()
    for s in repo.load_all():
        if s.id.upper() == target:
            return s
    return None


def add_student(
    name: str,
    class_name: str,
    major_code: str,
    tka_status: TkaStatus | str,
    grades: tuple[dict[str, int], ...] | list[dict[str, int]],
    achievements: tuple[Achievement, ...] | list[Achievement],
    school_profile: SchoolProfile,
    repo: StudentRepository,
    tka_synonyms: dict[str, str] | None = None,
) -> Student:
    """Mendaftarkan siswa baru secara manual ke dalam buku induk sekolah.

    Validasi Berlapis:
        1. Nama siswa dinormalisasi (Title Case) dan dipastikan tidak kosong.
        2. Nama kelas dinormalisasi (UPPERCASE) dan dipastikan tidak kosong.
        3. Kode jurusan dipastikan terdaftar di dalam kurikulum profil sekolah.
        4. Status TKA dipetakan ke enum TkaStatus.
        5. Data nilai rapor harus memuat tepat 5 semester, dan setiap nilai harus
           berupa bilangan bulat antara 0 sampai 100.
        6. Sertifikat prestasi tidak boleh melebihi batas 5 item.
        7. Mencegah pendaftaran ganda jika kombinasi (nama, kelas) sudah ada di sistem.

    Args:
        name: Nama lengkap calon siswa.
        class_name: Nama kelas rombongan belajar.
        major_code: Kode jurusan yang dipilih.
        tka_status: Pilihan keikutsertaan TKA.
        grades: Kumpulan nilai rapor untuk 5 semester.
        achievements: Daftar sertifikat prestasi siswa.
        school_profile: Profil sekolah aktif untuk validasi kurikulum.
        repo: Repositori data siswa.
        tka_synonyms: Kamus sinonim TKA (opsional).

    Returns:
        Objek Student baru yang telah tersimpan lengkap dengan ID unik.

    Raises:
        ValidationError: Jika salah satu aturan validasi atau batasan bisnis dilanggar.
    """
    # 1. Normalisasi teks
    norm_name = normalize_name(name)   # untuk merapikan nama supaya huruf kapital
    validate_name_nonempty(norm_name)

    norm_class = normalize_class_name(class_name)   #untuk merapikan nama kelas 
    if not norm_class:
        raise ValidationError(
            message="Nama kelas siswa tidak boleh kosong.",
            code=ErrorCode.NAME_EMPTY,
        )

    # 2. Validasi kesesuaian kurikulum jurusan
    majors_dict = {m.code.upper(): m for m in school_profile.majors}
    validate_major_exists(major_code, majors_dict)
    clean_major_code = major_code.strip().upper()

    # 3. Validasi status TKA
    if isinstance(tka_status, TkaStatus):
        resolved_tka = tka_status
    else:
        synonyms = tka_synonyms or {"ikut": "IKUT", "ya": "IKUT", "tidak": "TIDAK_IKUT"}
        maybe_tka = normalize_tka_status(str(tka_status), synonyms, raise_on_unknown=True)
        assert maybe_tka is not None
        resolved_tka = maybe_tka

    # 4. Validasi nilai rapor 5 semester
    if len(grades) != 5:   #untuk memper jelas bahwa jumlah nilai harus tepat 5/persemester
        raise ValidationError(
            message=f"Nilai rapor harus memuat tepat 5 semester, ditemukan: {len(grades)} semester.",
            code=ErrorCode.GRADE_EMPTY,
            details={"found_semesters": len(grades)},
        )

    validated_semesters: list[dict[str, int]] = []
    for _sem_idx, sem_dict in enumerate(grades):
        clean_sem_grades: dict[str, int] = {}
        for subj_code, raw_val in sem_dict.items():
            valid_val = validate_grade(raw_val)
            clean_sem_grades[subj_code.strip().upper()] = valid_val
        validated_semesters.append(clean_sem_grades)

    # 5. Validasi batas maksimal 5 prestasi
    if len(achievements) > 5: #satu siswa hanya boleh mencantumkan 5 prestasi nya
        raise ValidationError(
            message=f"Maksimal 5 prestasi per siswa, ditemukan: {len(achievements)}.",
            code=ErrorCode.ACHIEVEMENT_LIMIT,
            details={"count": len(achievements)},
        )

    # 6. Cek duplikasi terhadap siswa yang sudah terdaftar
    current_students = repo.load_all()
    for s in current_students:
        if s.name.lower() == norm_name.lower() and s.class_name.upper() == norm_class.upper():
            raise ValidationError(
                message=f"Siswa '{norm_name}' kelas '{norm_class}' sudah terdaftar (ID: {s.id}).",
                code=ErrorCode.DUPLICATE_STUDENT,
                details={"existing_id": s.id},
            )

    # 7. Penomoran ID unik otomatis (S001, S002, dst)
    next_seq = repo.get_next_id_seq()
    assigned_id = f"S{next_seq:03d}"

    new_student = Student(
        id=assigned_id,
        name=norm_name,
        class_name=norm_class,
        major_code=clean_major_code,
        tka_status=resolved_tka,
        grades=tuple(validated_semesters),
        achievements=tuple(achievements),
    )

    all_updated = current_students + [new_student]
    repo.save_all(all_updated)
    return new_student


def update_student(
    student: Student,
    school_profile: SchoolProfile, #untuk memerikasa jurusan nya
    repo: StudentRepository, # akses untuk penyimpanan data nya
) -> Student:
    """Memperbarui informasi atau nilai rapor siswa yang sudah terdaftar.

    Args:
        student: Entitas Student yang telah dimodifikasi.
        school_profile: Profil sekolah untuk validasi kurikulum jurusan.
        repo: Repositori siswa.

    Returns:
        Objek Student yang telah berhasil diperbarui dan disimpan.

    Raises:
        ValidationError: Jika siswa tidak ditemukan atau data nilai tidak valid.
    """
    current_students = repo.load_all()
    found_idx = -1
    for idx, s in enumerate(current_students):
        if s.id == student.id:
            found_idx = idx
            break

    if found_idx == -1:
        raise ValidationError(
            message=f"Siswa dengan ID '{student.id}' tidak ditemukan di buku induk.",
            code=ErrorCode.FILE_NOT_FOUND,
        )

    # Validasi jurusan yang kode nya belum terdaftar
    majors_dict = {m.code.upper(): m for m in school_profile.majors}
    validate_major_exists(student.major_code, majors_dict)

    # Validasi nilai rapor  setiap nilai di recap
    #untuk memmastikan engg ada nilai yang salah
    for sem_dict in student.grades:
        for val in sem_dict.values():
            validate_grade(val)

    updated_list = list(current_students)
    updated_list[found_idx] = student
    repo.save_all(updated_list)
    return student

#ini untuk menghapus siswa
def delete_student(student_id: str, repo: StudentRepository) -> bool:
    """Menghapus siswa dari basis data sekolah berdasarkan ID-nya.

    Args:
        student_id: ID siswa yang akan dihapus.
        repo: Repositori siswa.

    Returns:
        True jika siswa berhasil ditemukan dan dihapus, False jika ID tidak ditemukan.
    """
    current_students = repo.load_all()
    target = student_id.strip().upper()
    filtered = [s for s in current_students if s.id.upper() != target]

    if len(filtered) == len(current_students):
        return False  # Tidak ada siswa yang cocok
# jadi kalo ada yang terhapus simpan datr baru tanpa data siswa yang di hapus
    repo.save_all(filtered)
    return True