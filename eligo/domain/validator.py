"""Modul Validasi Data Domain Murni (Pure Domain Validator).

Modul ini menyediakan fungsi-fungsi validasi ketat terhadap data masukan
sebelum data tersebut diterima sebagai entitas domain yang sah.

Prinsip Rekayasa Enterprise:
    1. Fail-Fast with Clear Messages:
       Setiap pelanggaran validasi langsung melempar `ValidationError` dengan
       kode error standar dari katalog `ErrorCode` dan pesan deskriptif dalam
       Bahasa Indonesia yang dapat ditampilkan langsung kepada operator.
    2. Pure Functions (Fungsi Murni):
       Seluruh fungsi hanya melakukan pemeriksaan data dan melempar exception
       jika tidak valid. Tidak ada efek samping (tanpa I/O, tanpa mutasi state).
    3. Single Responsibility:
       Tiap fungsi validasi hanya memeriksa satu aspek data
       (misal: hanya cek rentang nilai, hanya cek keberadaan jurusan).

Penjelasan Sederhana untuk Orang Awam:
    Sebelum data siswa disimpan ke dalam sistem, setiap kolom diperiksa satu per satu:
    - Apakah nilai rapor benar-benar angka bulat antara 0 sampai 100?
    - Apakah nama siswa tidak kosong?
    - Apakah jurusan yang diisi memang terdaftar di kurikulum sekolah?
    Jika ada yang salah, sistem langsung memberitahu kesalahan spesifiknya
    sehingga operator bisa memperbaiki data dengan tepat.
"""

from __future__ import annotations

from typing import Any

from eligo.domain.exceptions import ErrorCode, ValidationError
from eligo.domain.models import Major


def validate_grade(value: Any) -> int:
    """Validasi bahwa nilai rapor adalah bilangan bulat utuh dalam rentang 0 sampai 100.

    Aturan validasi bertingkat:
        1. Nilai tidak boleh kosong (None atau string kosong).
        2. Nilai harus bertipe bilangan bulat (int), bukan pecahan (float) atau teks.
        3. Nilai harus berada dalam rentang inklusif 0 sampai 100.

    Args:
        value: Nilai masukan yang akan divalidasi (bisa berupa int, float, str, atau None).

    Returns:
        Nilai integer yang telah tervalidasi (0 <= nilai <= 100).

    Raises:
        ValidationError: Dengan kode GRADE_EMPTY jika nilai kosong.
        ValidationError: Dengan kode GRADE_NOT_INT jika nilai bukan bilangan bulat.
        ValidationError: Dengan kode GRADE_OUT_OF_RANGE jika nilai di luar 0-100.

    Contoh:
        >>> validate_grade(85)
        85
        >>> validate_grade(None)
        ValidationError(code='GRADE_EMPTY')
        >>> validate_grade(85.5)
        ValidationError(code='GRADE_NOT_INT')
        >>> validate_grade(105)
        ValidationError(code='GRADE_OUT_OF_RANGE')
    """
    # Pemeriksaan 1: Apakah nilai kosong?
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValidationError(
            message="Nilai rapor kosong atau belum diisi.",
            code=ErrorCode.GRADE_EMPTY,
        )

    # Pemeriksaan 2: Apakah nilai bertipe bilangan bulat (int)?
    # Catatan: bool adalah subclass dari int di Python, jadi harus dikecualikan
    if isinstance(value, bool):
        raise ValidationError(
            message=f"Nilai rapor harus berupa bilangan bulat, ditemukan: {value!r}.",
            code=ErrorCode.GRADE_NOT_INT,
            details={"value": str(value)},
        )

    if isinstance(value, float):
        raise ValidationError(
            message=f"Nilai rapor harus bilangan bulat utuh, ditemukan: {value}.",
            code=ErrorCode.GRADE_NOT_INT,
            details={"value": str(value)},
        )

    # Jika input berupa string, coba konversi ke integer
    if isinstance(value, str):
        stripped = value.strip()
        # Tolak string yang mengandung titik desimal
        if "." in stripped or "," in stripped:
            raise ValidationError(
                message=f"Nilai rapor harus bilangan bulat, ditemukan: '{stripped}'.",
                code=ErrorCode.GRADE_NOT_INT,
                details={"value": stripped},
            )
        try:
            value = int(stripped)
        except ValueError as err:
            raise ValidationError(
                message=f"Nilai rapor harus bilangan bulat, ditemukan: '{stripped}'.",
                code=ErrorCode.GRADE_NOT_INT,
                details={"value": stripped},
            ) from err

    if not isinstance(value, int):
        raise ValidationError(
            message=f"Nilai rapor harus berupa bilangan bulat, ditemukan tipe: {type(value).__name__}.",
            code=ErrorCode.GRADE_NOT_INT,
            details={"value": str(value)},
        )

    # Pemeriksaan 3: Apakah nilai berada dalam rentang sah 0..100?
    if value < 0 or value > 100:
        raise ValidationError(
            message=f"Nilai rapor harus antara 0 dan 100, ditemukan: {value}.",
            code=ErrorCode.GRADE_OUT_OF_RANGE,
            details={"value": str(value)},
        )

    return value


def validate_name_nonempty(normalized_name: str) -> None:
    """Validasi bahwa nama siswa tidak kosong setelah proses normalisasi.

    Args:
        normalized_name: String nama yang telah melewati proses normalisasi (strip + title-case).

    Raises:
        ValidationError: Dengan kode NAME_EMPTY jika nama kosong atau hanya berisi spasi.
    """
    if not normalized_name or not normalized_name.strip():
        raise ValidationError(
            message="Nama siswa tidak boleh kosong.",
            code=ErrorCode.NAME_EMPTY,
        )


def validate_major_exists(
    major_code: str,
    majors: dict[str, Major],
) -> Major:
    """Validasi bahwa kode jurusan terdaftar dalam kurikulum sekolah.

    Args:
        major_code: Kode jurusan yang akan divalidasi (misal 'MIPA', 'IPS').
        majors: Kamus pemetaan kode jurusan ke objek Major dari profil sekolah.

    Returns:
        Objek Major yang sesuai dengan kode jurusan jika valid.

    Raises:
        ValidationError: Dengan kode MAJOR_NOT_FOUND jika jurusan tidak terdaftar.
    """
    major = majors.get(major_code.strip().upper())
    if major is None:
        available = ", ".join(sorted(majors.keys())) if majors else "(belum ada jurusan)"
        raise ValidationError(
            message=f"Jurusan '{major_code}' tidak terdaftar. Pilihan: {available}.",
            code=ErrorCode.MAJOR_NOT_FOUND,
            details={"major_code": major_code, "available": available},
        )
    return major


def validate_grades_completeness(
    grades: dict[str, int],
    expected_subjects: list[str],
) -> list[str]:
    """Periksa kelengkapan nilai rapor terhadap daftar mata pelajaran yang diharapkan.

    Args:
        grades: Kamus nilai rapor siswa untuk satu semester ({kode_mapel: nilai}).
        expected_subjects: Daftar kode mata pelajaran yang wajib ada pada semester tersebut.

    Returns:
        Daftar kode mata pelajaran yang hilang (belum memiliki nilai).
        List kosong berarti semua mata pelajaran sudah lengkap.

    Contoh:
        >>> validate_grades_completeness({"MTK": 90, "BIN": 85}, ["MTK", "BIN", "ING"])
        ['ING']
        >>> validate_grades_completeness({"MTK": 90, "BIN": 85, "ING": 88}, ["MTK", "BIN", "ING"])
        []
    """
    return [subj for subj in expected_subjects if subj not in grades]


def validate_student_payload(
    name: str,
    class_name: str,
    major_code: str,
    majors: dict[str, Major],
    semester_grades: tuple[dict[str, int], ...] | list[dict[str, int]],
) -> None:
    """Validasi muatan data siswa secara komprehensif sebelum dikonversi menjadi entitas Student.

    Pemeriksaan meliputi:
        1. Nama siswa tidak boleh kosong setelah dinormalisasi (NAME_EMPTY).
        2. Nama kelas tidak boleh kosong (NAME_EMPTY).
        3. Kode jurusan harus terdaftar di kurikulum sekolah (MAJOR_NOT_FOUND).
        4. Data nilai rapor harus memuat tepat 5 semester (GRADE_EMPTY atau CSV_PARSE_ERROR).

    Args:
        name: Nama siswa yang telah dibersihkan.
        class_name: Nama kelas siswa.
        major_code: Kode jurusan siswa.
        majors: Kamus pemetaan jurusan yang terdaftar di profil sekolah.
        semester_grades: Urutan nilai rapor untuk 5 semester.

    Raises:
        ValidationError: Jika salah satu aturan bisnis dilanggar.
    """
    validate_name_nonempty(name)
    if not class_name or not class_name.strip():
        raise ValidationError(
            message="Nama kelas siswa tidak boleh kosong.",
            code=ErrorCode.NAME_EMPTY,
        )
    validate_major_exists(major_code, majors)
    if len(semester_grades) != 5:
        raise ValidationError(
            message=f"Data nilai rapor harus memuat tepat 5 semester, ditemukan: {len(semester_grades)} semester.",
            code=ErrorCode.GRADE_EMPTY,
            details={"found_semesters": len(semester_grades)},
        )