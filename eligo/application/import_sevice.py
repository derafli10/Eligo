from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from eligo.domain.exceptions import ErrorCode, ImportAbortedError, RowError, ValidationError
from eligo.domain.models import AppConfig, Major, Student
from eligo.domain.repositories import StudentRepository
from eligo.infrastructure.csv_parser import ParsedStudentRow, parse_student_csv


@dataclass(frozen=True)
class ImportPreview:
    """Objek Pratinjau Hasil Pembacaan Berkas CSV sebelum Disimpan ke Basis Data.

    Objek ini menampung informasi ringkasan hasil parsing berkas CSV di Fase 1
    sehingga operator dapat memeriksa kondisi data secara menyeluruh sebelum
    memutuskan untuk menyimpan data ke sistem.

    Atribut:
        valid_rows: Daftar baris siswa yang bersih dan lolos seluruh validasi format.
        error_rows: Daftar seluruh baris yang memiliki nilai rusak atau tidak sah.
        duplicate_rows: Daftar baris siswa valid yang nama dan kelasnya sudah ada di sistem.
        tka_count: Jumlah siswa valid yang memilih mengikuti Tes Kemampuan Akademik (TKA).
        non_tka_count: Jumlah siswa valid yang tidak mengikuti TKA.
        total_rows: Total keseluruhan baris data yang diproses dari berkas CSV.
    """

    valid_rows: list[ParsedStudentRow]
    error_rows: list[RowError]
    duplicate_rows: list[ParsedStudentRow]
    tka_count: int
    non_tka_count: int
    total_rows: int

    @property
    def row_errors(self) -> list[RowError]:
        """Alias kompatibilitas untuk error_rows."""
        return self.error_rows

    @property
    def duplicate_names(self) -> list[str]:
        """Daftar representasi teks nama dan kelas siswa yang terdeteksi kembar/duplikat."""
        return [f"{r.name} ({r.class_name})" for r in self.duplicate_rows]

    @property
    def has_errors(self) -> bool:
        """Menandakan apakah terdapat baris yang salah dalam berkas CSV."""
        return len(self.error_rows) > 0

    @property
    def has_duplicates(self) -> bool:
        """Menandakan apakah terdapat siswa yang sudah terdaftar sebelumnya."""
        return len(self.duplicate_rows) > 0


def prepare_import_preview(
    file_path: Path | str,
    major: Major,
    existing_students: list[Student],
    config: AppConfig,
) -> ImportPreview:
    """Fase 1 Impor: Membaca berkas CSV dan menyiapkan pratinjau data tanpa menulis ke disk.

    Fungsi ini membaca file CSV, memvalidasi setiap baris nilai rapor terhadap kurikulum
    jurusan yang dipilih, mendeteksi potensi duplikasi data terhadap siswa yang sudah
    ada di sekolah, dan menghitung statistik partisipasi TKA.

    Jaminan Keras (Architectural Invariant):
        Fungsi ini bersifat READ-ONLY murni. SAMA SEKALI TIDAK ADA penulisan ke disk atau
        mutasi data di dalam repositori sekolah (AC-04.05).

    Args:
        file_path: Lokasi fisik berkas CSV yang diunggah.
        major: Kurikulum jurusan yang dipilih untuk impor (misal MIPA).
        existing_students: Daftar seluruh siswa yang saat ini sudah terdaftar di sekolah.
        config: Konfigurasi aktif aplikasi (memuat tabel sinonim TKA).

    Returns:
        Objek `ImportPreview` yang memuat rincian baris valid, error, dan duplikat.
    """
    path = Path(file_path)

    # 1. Parsing berkas CSV menggunakan pengurai infrastruktur
    valid_rows, error_rows = parse_student_csv(
        file_path=path,
        major=major,
        synonyms=config.tka_synonyms,
    )

    # 2. Himpunan kunci siswa yang sudah terdaftar di database saat ini
    # Kunci pembanding: (nama_kecil, kelas_kapital)
    existing_keys: set[tuple[str, str]] = {
        (s.name.lower(), s.class_name.upper()) for s in existing_students
    }

    # 3. Identifikasi baris mana saja yang berpotensi menjadi duplikat
    duplicate_rows: list[ParsedStudentRow] = []
    tka_count = 0
    non_tka_count = 0

    for row in valid_rows:
        key = (row.name.lower(), row.class_name.upper())
        if key in existing_keys:
            duplicate_rows.append(row)

        if row.tka_status.value == "IKUT":
            tka_count += 1
        else:
            non_tka_count += 1

    total_rows = len(valid_rows) + len(error_rows)

    return ImportPreview(
        valid_rows=valid_rows,
        error_rows=error_rows,
        duplicate_rows=duplicate_rows,
        tka_count=tka_count,
        non_tka_count=non_tka_count,
        total_rows=total_rows,
    )


def commit_import(
    preview: ImportPreview,
    duplicate_resolution: str,
    existing_students: list[Student],
    student_repo: StudentRepository,
    error_report_path: Path | str | None = None,
) -> tuple[int, int]:
    """Fase 2 Impor: Menerapkan hasil pratinjau ke repositori data siswa secara permanen.

    Fungsi ini mengeksekusi komitmen data:
    1. Memeriksa pilihan resolusi duplikat pengguna:
       - "abort": Batalkan transaksi seketika, lempar `ImportAbortedError`.
       - "skip": Siswa yang sudah ada dipertahankan; baris baru dari CSV diabaikan.
       - "overwrite": Siswa yang sudah ada diperbarui nilainya dari CSV (ID tetap).
    2. Menghasilkan ID unik otomatis (`S001`, `S002`, dst.) untuk siswa baru.
    3. Menyimpan gabungan data siswa ke disk melalui `student_repo.save_all(...)`.
    4. Jika terdapat baris yang salah (`preview.error_rows`) dan `error_report_path`
       disediakan, fungsi ini otomatis menuliskan berkas CSV laporan kegagalan
       beserta rekap frekuensi kesalahan per kolom menggunakan struktur `Counter`.

    Args:
        preview: Objek `ImportPreview` dari Fase 1.
        duplicate_resolution: Keputusan penanganan data kembar ('skip', 'overwrite', atau 'abort').
        existing_students: Daftar siswa yang ada saat ini sebelum impor.
        student_repo: Implementasi antarmuka penyimpanan data siswa.
        error_report_path: Lokasi tujuan penyimpanan berkas laporan error (opsional).

    Returns:
        Tuple berupa (jumlah_siswa_berhasil_disimpan, jumlah_baris_gagal).

    Raises:
        ImportAbortedError: Jika operator memilih 'abort'.
        ValidationError: Jika opsi `duplicate_resolution` tidak valid.
        PersistenceError: Jika penyimpanan fisik ke berkas JSON mengalami kegagalan.
    """
    resolution = duplicate_resolution.strip().lower()
    if resolution not in ("skip", "overwrite", "abort"):
        raise ValidationError(
            message=(
                f"Pilihan resolusi duplikat '{duplicate_resolution}' tidak sah. "
                "Pilihan yang diizinkan: 'skip', 'overwrite', atau 'abort'."
            ),
            code=ErrorCode.ENUM_INVALID,
            details={"allowed": ["skip", "overwrite", "abort"]},
        )

    # 1. Jika operator memilih 'abort', batalkan transaksi seketika tanpa mengubah apapun
    if resolution == "abort":
        raise ImportAbortedError(
            message="Proses impor data CSV dibatalkan oleh operator.",
            code=ErrorCode.IMPORT_ABORTED,
        )

    # 2. Siapkan pemetaan siswa lama berdasarkan kunci (nama_kecil, kelas_kapital)
    existing_map: dict[tuple[str, str], Student] = {
        (s.name.lower(), s.class_name.upper()): s for s in existing_students
    }

    # 3. Hitung nomor urut ID berikutnya untuk siswa baru
    max_seq = 0
    for s in existing_students:
        if s.id.startswith("S") and s.id[1:].isdigit():
            val = int(s.id[1:])
            if val > max_seq:
                max_seq = val
    next_id_counter = max_seq + 1

    # 4. Bangun daftar siswa hasil penggabungan
    # Mulai dengan salinan siswa lama yang tidak mengalami overwrite
    final_students_map: dict[str, Student] = {s.id: s for s in existing_students}

    for row in preview.valid_rows:
        key = (row.name.lower(), row.class_name.upper())

        if key in existing_map:
            # Kasus Siswa Duplikat
            if resolution == "skip":
                # Pertahankan data lama, abaikan data dari CSV
                continue
            elif resolution == "overwrite":
                old_student = existing_map[key]
                # Perbarui nilai dan status TKA, pertahankan ID dan prestasi lama
                updated_student = Student(
                    id=old_student.id,
                    name=row.name,
                    class_name=row.class_name,
                    major_code=row.major_code,
                    tka_status=row.tka_status,
                    grades=row.grades,
                    achievements=old_student.achievements,
                )
                final_students_map[old_student.id] = updated_student
        else:
            # Kasus Siswa Baru: Buat ID unik berformat S001, S002, dst.
            assigned_id = f"S{next_id_counter:03d}"
            next_id_counter += 1
            new_student = Student(
                id=assigned_id,
                name=row.name,
                class_name=row.class_name,
                major_code=row.major_code,
                tka_status=row.tka_status,
                grades=row.grades,
                achievements=(),
            )
            final_students_map[assigned_id] = new_student

    # Urutkan seluruh siswa berdasarkan ID agar rapi dan deterministik
    final_students_list = sorted(final_students_map.values(), key=lambda s: s.id)

    # 5. Simpan ke media penyimpanan menggunakan repositori
    student_repo.save_all(final_students_list)

    # 6. Pembuatan Berkas Laporan Kesalahan CSV (jika ada baris yang bermasalah)
    if preview.error_rows and error_report_path is not None:
        rep_path = Path(error_report_path)
        # Jika diberikan direktori, buat nama file otomatis dengan penanda waktu
        if rep_path.is_dir() or (not rep_path.suffix and not rep_path.exists()):
            rep_path.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            rep_path = rep_path / f"error_report_{ts}.csv"

        # Rekap distribusi kesalahan per kolom menggunakan struktur Counter (C4)
        error_column_counts = Counter(err.column_name for err in preview.error_rows)

        try:
            with rep_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["baris_ke", "nama_kolom", "nilai_mentah", "kode_kesalahan", "pesan_penjelasan"]
                )
                for err in preview.error_rows:
                    writer.writerow(
                        [
                            err.row_number,
                            err.column_name,
                            err.raw_value,
                            err.error_code,
                            err.message,
                        ]
                    )

                # Tambahkan ringkasan rekapitulasi di akhir file
                writer.writerow([])
                writer.writerow(["# REKAPITULASI DISTRIBUSI KESALAHAN PER KOLOM"])
                for col_name, count in error_column_counts.most_common():
                    writer.writerow([f"# Kolom '{col_name}': {count} kesalahan"])
        except OSError:
            # Gagal menulis laporan log tidak boleh membatalkan commit data yang sudah sah
            pass

    saved_count = len(final_students_list)
    error_count = len(preview.error_rows)

    return saved_count, error_count