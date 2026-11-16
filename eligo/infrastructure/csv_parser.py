from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from eligo.domain.exceptions import CsvImportError, ErrorCode, RowError
from eligo.domain.models import Major, TkaStatus
from eligo.domain.normalizer import (
    normalize_class_name,
    normalize_header,
    normalize_name,
    normalize_tka_status,
)


@dataclass(frozen=True)
class ParsedStudentRow:
    # """Objek Nilai yang menyimpan hasil penguraian satu baris siswa yang telah lolos validasi dasar

    # Objek ini merepresentasikan baris siswa yang bersih dan siap diproses lebih lanjut
    # oleh layanan aplikasi (Application Service) untuk disimpan ke database sekolah.

    row_number: int
    name: str
    class_name: str
    major_code: str
    tka_status: TkaStatus
    grades: tuple[dict[str, int], ...]
    raw_data: dict[str, str]


def detect_encoding_and_delimiter(file_path: Path | str) -> tuple[str, str]:
    # Mendeteksi encoding dan tanda pemisah kolom dari berkas CSV.

    path = Path(file_path)
    if not path.exists():
        raise CsvImportError(
            message=f"Berkas CSV tidak ditemukan di lokasi: {path}",
            code=ErrorCode.FILE_NOT_FOUND,
            details={"file_path": str(path)},
        )

    # 1. Deteksi Byte Order Mark pada byte awal
    try:
        with path.open("rb") as f:
            raw_bytes = f.read(4)
    except OSError as err:
        raise CsvImportError(
            message=f"Gagal membaca berkas CSV: {err}",
            code=ErrorCode.CSV_PARSE_ERROR,
            details={"os_error": str(err)},
        ) from err

    encoding = "utf-8-sig" if raw_bytes.startswith(b"\xef\xbb\xbf") else "utf-8"

    # 2. Deteksi Delimiter pada baris pertama teks
    delimiter = ","
    try:
        with path.open("r", encoding=encoding, errors="replace") as f:
            first_line = f.readline()
            if first_line:
                semicolon_count = first_line.count(";")
                comma_count = first_line.count(",")
                # Jika titik koma lebih dominan, gunakan titik koma
                if semicolon_count > comma_count:
                    delimiter = ";"
                else:
                    delimiter = ","
    except OSError as err:
        raise CsvImportError(
            message=f"Gagal memeriksa baris judul CSV: {err}",
            code=ErrorCode.CSV_PARSE_ERROR,
            details={"os_error": str(err)},
        ) from err

    return encoding, delimiter


def parse_student_csv(
    file_path: Path | str,
    major: Major,
    synonyms: dict[str, str],
) -> tuple[list[ParsedStudentRow], list[RowError]]:
    # Membaca dan memvalidasi berkas CSV nilai rapor siswa berdasarkan kurikulum jurusan

    # Alur:
    #     1. Deteksi encoding dan delimiter secara otomatis.
    #     2. Buka berkas dan baca header.
    #     3. Normalisasi nama-nama kolom header (huruf kecil, hapus spasi berlebih).
    #     4. Periksa apakah semua kolom wajib (nama, kelas, tka, serta mata pelajaran 5 semester)
    #        tersedia dalam berkas CSV. Jika kolom wajib hilang, proses langsung dihentikan
    #        dengan melempar CsvImportError(code='HEADER_MISMATCH')
    #     5. Memeriksa setiap baris data siswa satu per satu:
    #        - Mengabaikan baris kosong
    #        - Memeriksa nama siswa (tidak boleh kosong)
    #        - Memeriksa nama kelas siswa (tidak boleh kosong)
    #        - Memeriksa kesesuaian kode jurusan (jika kolom jurusan ada)
    #        - Memeriksa status TKA terhadap daftar sinonim yang diakui
    #        - Memeriksa setiap nilai mata pelajaran untuk Semester 1 sampai Semester 5:
    #          * Apakah selnya kosong? (GRADE_EMPTY)
    #          * Apakah bukan angka bulat? (GRADE_NOT_INT)
    #          * Apakah nilainya di luar rentang sah 0 sampai 100? (GRADE_OUT_OF_RANGE)
    #     6. Mengumpulkan baris yang valid ke valid_rows dan baris bermasalah ke error_rows

    path = Path(file_path)
    encoding, delimiter = detect_encoding_and_delimiter(path)

    # 1. Bangun daftar kolom yang diharapkan sesuai kurikulum jurusan
    # Semester 1 sampai 5 (index 0..4 pada major.subjects)
    expected_grade_columns: dict[tuple[int, str], str] = {}
    for sem_idx, semester_subjects in enumerate(major.subjects):
        sem_num = sem_idx + 1
        for subject in semester_subjects:
            key_name = f"sem{sem_num}_{subject.code.lower()}"
            expected_grade_columns[(sem_idx, subject.code)] = key_name

    try:
        with path.open("r", encoding=encoding, errors="replace") as f:
            reader = csv.reader(f, delimiter=delimiter)
            try:
                raw_headers = next(reader)
            except StopIteration:
                raise CsvImportError(
                    message="Berkas CSV kosong, tidak memuat data sama sekali.",
                    code=ErrorCode.CSV_PARSE_ERROR,
                    details={"file_path": str(path)},
                ) from None

            # Normalisasi header
            headers = [normalize_header(h) for h in raw_headers]
            header_map: dict[str, int] = {h: idx for idx, h in enumerate(headers) if h}

            # Validasi keberadaan kolom wajib
            missing_headers: list[str] = []
            if "nama" not in header_map:
                missing_headers.append("nama")
            if "kelas" not in header_map:
                missing_headers.append("kelas")

            # Periksa kolom TKA (toleransi nama kolom: 'tka' atau 'tka_status')
            tka_col_name = "tka_status" if "tka_status" in header_map else "tka"
            if tka_col_name not in header_map:
                missing_headers.append("tka_status / tka")

            # Periksa kelengkapan seluruh mata pelajaran 5 semester
            for (_sem_idx, _subj_code), expected_col in expected_grade_columns.items():
                if expected_col not in header_map:
                    missing_headers.append(expected_col)

            if missing_headers:
                missing_str = ", ".join(missing_headers)
                raise CsvImportError(
                    message=(
                        f"Format kolom CSV tidak sesuai dengan kurikulum jurusan '{major.name}'. "
                        f"Kolom yang belum ada atau salah nama: [{missing_str}]."
                    ),
                    code=ErrorCode.HEADER_MISMATCH,
                    details={
                        "major_code": major.code,
                        "missing_columns": missing_headers,
                        "detected_headers": headers,
                    },
                )

            valid_rows: list[ParsedStudentRow] = []
            error_rows: list[RowError] = []

            # 2. Proses baris data (baris ke-2 dst)
            for row_idx, row in enumerate(reader, start=2):
                # Abaikan baris yang sepenuhnya kosong
                if not row or not any(cell.strip() for cell in row):
                    continue

                row_dict: dict[str, str] = {}
                for h_name, col_idx in header_map.items():
                    if col_idx < len(row):
                        row_dict[h_name] = row[col_idx].strip()
                    else:
                        row_dict[h_name] = ""

                current_row_errors: list[RowError] = []

                # Validasi Kolom Nama
                raw_name = row_dict.get("nama", "")
                norm_name = normalize_name(raw_name)
                if not norm_name:
                    current_row_errors.append(
                        RowError(
                            row_number=row_idx,
                            column_name="nama",
                            raw_value=raw_name,
                            error_code=ErrorCode.NAME_EMPTY,
                            message="Nama siswa tidak boleh kosong.",
                        )
                    )

                # Validasi Kolom Kelas
                raw_class = row_dict.get("kelas", "")
                norm_class = normalize_class_name(raw_class)
                if not norm_class:
                    current_row_errors.append(
                        RowError(
                            row_number=row_idx,
                            column_name="kelas",
                            raw_value=raw_class,
                            error_code=ErrorCode.NAME_EMPTY,
                            message="Nama kelas siswa tidak boleh kosong.",
                        )
                    )

                # Validasi Kolom Jurusan (jika dicantumkan di CSV)
                if "jurusan" in header_map:
                    raw_major = row_dict.get("jurusan", "")
                    if raw_major and raw_major.upper() != major.code.upper():
                        current_row_errors.append(
                            RowError(
                                row_number=row_idx,
                                column_name="jurusan",
                                raw_value=raw_major,
                                error_code=ErrorCode.MAJOR_NOT_FOUND,
                                message=(
                                    f"Jurusan '{raw_major}' tidak cocok dengan "
                                    f"jurusan impor saat ini ('{major.code}')."
                                ),
                            )
                        )

                # Validasi Status TKA
                raw_tka = row_dict.get(tka_col_name, "")
                tka_enum = normalize_tka_status(raw_tka, synonyms, raise_on_unknown=False)
                if tka_enum is None:
                    valid_opts = ", ".join(sorted(synonyms.keys()))
                    current_row_errors.append(
                        RowError(
                            row_number=row_idx,
                            column_name=tka_col_name,
                            raw_value=raw_tka,
                            error_code=ErrorCode.TKA_SYNONYM_UNKNOWN,
                            message=(
                                f"Status TKA '{raw_tka}' tidak dikenal. "
                                f"Gunakan salah satu dari: {valid_opts}."
                            ),
                        )
                    )

                # Validasi Nilai Rapor Semester 1 sampai 5
                # Struktur semester_grades: 5 kamus nilai (index 0 = Sem 1)
                parsed_semesters: list[dict[str, int]] = [{} for _ in range(5)]
                for (sem_idx, subj_code), expected_col in expected_grade_columns.items():
                    raw_val = row_dict.get(expected_col, "")
                    if not raw_val:
                        current_row_errors.append(
                            RowError(
                                row_number=row_idx,
                                column_name=expected_col,
                                raw_value=raw_val,
                                error_code=ErrorCode.GRADE_EMPTY,
                                message=f"Nilai {subj_code} Semester {sem_idx + 1} kosong.",
                            )
                        )
                        continue

                    # Periksa apakah nilai adalah integer yang sah
                    if "." in raw_val or "," in raw_val:
                        current_row_errors.append(
                            RowError(
                                row_number=row_idx,
                                column_name=expected_col,
                                raw_value=raw_val,
                                error_code=ErrorCode.GRADE_NOT_INT,
                                message=(
                                    f"Nilai {subj_code} Semester {sem_idx + 1} "
                                    f"harus bilangan bulat utuh, ditemukan '{raw_val}'."
                                ),
                            )
                        )
                        continue

                    try:
                        int_val = int(raw_val)
                    except ValueError:
                        current_row_errors.append(
                            RowError(
                                row_number=row_idx,
                                column_name=expected_col,
                                raw_value=raw_val,
                                error_code=ErrorCode.GRADE_NOT_INT,
                                message=(
                                    f"Nilai {subj_code} Semester {sem_idx + 1} "
                                    f"harus angka, ditemukan '{raw_val}'."
                                ),
                            )
                        )
                        continue

                    # Periksa rentang 0 sampai 100
                    if int_val < 0 or int_val > 100:
                        current_row_errors.append(
                            RowError(
                                row_number=row_idx,
                                column_name=expected_col,
                                raw_value=raw_val,
                                error_code=ErrorCode.GRADE_OUT_OF_RANGE,
                                message=(
                                    f"Nilai {subj_code} Semester {sem_idx + 1} ({int_val}) "
                                    "di luar batas sah 0-100."
                                ),
                            )
                        )
                        continue

                    parsed_semesters[sem_idx][subj_code] = int_val

                # Evaluasi hasil baris: jika ada error, kumpulkan ke error_rows
                if current_row_errors:
                    error_rows.extend(current_row_errors)
                else:
                    # Baris bersih sempurna: buat objek ParsedStudentRow
                    assert tka_enum is not None
                    parsed_row = ParsedStudentRow(
                        row_number=row_idx,
                        name=norm_name,
                        class_name=norm_class,
                        major_code=major.code,
                        tka_status=tka_enum,
                        grades=tuple(parsed_semesters),
                        raw_data=row_dict,
                    )
                    valid_rows.append(parsed_row)

    except OSError as err:
        raise CsvImportError(
            message=f"Kesalahan sistem saat membaca berkas CSV: {err}",
            code=ErrorCode.CSV_PARSE_ERROR,
            details={"os_error": str(err)},
        ) from err

    return valid_rows, error_rows


def generate_csv_template(major: Major) -> str:
    # Membuat teks template berkas CSV standar berdasarkan kurikulum jurusan.

    headers = ["nama", "kelas", "jurusan"]
    example_row = ["Ahmad Fauzi", "XII-MIPA-1", major.code]

    for sem_idx, semester_subjects in enumerate(major.subjects):
        sem_num = sem_idx + 1
        for subject in semester_subjects:
            headers.append(f"sem{sem_num}_{subject.code.lower()}")
            example_row.append("85")

    headers.append("tka_status")
    example_row.append("ikut")

    return ",".join(headers) + "\n" + ",".join(example_row) + "\n"