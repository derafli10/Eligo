from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ErrorCode:
    """Katalog Kode Error Standar Sistem Eligo (Bab 6.2 Technical Design Document).

    Penggunaan konstanta string ini mencegah kesalahan ketik (typo) dan menjadi
    sumber kebenaran tunggal (Single Source of Truth) untuk seluruh penandaan error.
    """

    # Kategori: Validasi Nilai & Akademik
    GRADE_OUT_OF_RANGE = "GRADE_OUT_OF_RANGE"
    GRADE_NOT_INT = "GRADE_NOT_INT"
    GRADE_EMPTY = "GRADE_EMPTY"
    NAME_EMPTY = "NAME_EMPTY"
    SCHOOL_NAME_EMPTY = "SCHOOL_NAME_EMPTY"
    ENUM_INVALID = "ENUM_INVALID"

    # Kategori: Integritas Kurikulum & Jurusan
    MAJOR_NOT_FOUND = "MAJOR_NOT_FOUND"
    SUBJECT_DUPLICATE = "SUBJECT_DUPLICATE"
    MAJOR_IN_USE = "MAJOR_IN_USE"
    SUBJECT_HAS_GRADES = "SUBJECT_HAS_GRADES"

    # Kategori: Data Siswa & Duplikasi
    DUPLICATE_STUDENT = "DUPLICATE_STUDENT"
    TKA_SYNONYM_UNKNOWN = "TKA_SYNONYM_UNKNOWN"

    # Kategori: Format & Impor CSV
    HEADER_MISMATCH = "HEADER_MISMATCH"
    CSV_PARSE_ERROR = "CSV_PARSE_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    IMPORT_ABORTED = "IMPORT_ABORTED"

    # Kategori: Prestasi Siswa
    ACHIEVEMENT_LIMIT = "ACHIEVEMENT_LIMIT"
    ACHIEVEMENT_IMPORT_DISABLED = "ACHIEVEMENT_IMPORT_DISABLED"
    ACHIEVEMENT_STUDENT_NOT_FOUND = "ACHIEVEMENT_STUDENT_NOT_FOUND"

    # Kategori: Persistensi & Pemulihan Bencana (Disaster Recovery)
    FILE_CORRUPT = "FILE_CORRUPT"
    BACKUP_CORRUPT = "BACKUP_CORRUPT"
    WRITE_FAILED = "WRITE_FAILED"
    ATOMIC_WRITE_FAILED = "ATOMIC_WRITE_FAILED"

    # Kategori: Perhitungan Kuota
    QUOTA_CALCULATION_FAILED = "QUOTA_CALCULATION_FAILED"
    QUOTA_INVALID = "QUOTA_INVALID"


# Pemetaan pesan standar ramah pengguna untuk setiap kode error
DEFAULT_ERROR_MESSAGES: dict[str, str] = {
    ErrorCode.GRADE_OUT_OF_RANGE: "Nilai rapor di luar rentang sah (harus antara 0 sampai 100).",
    ErrorCode.GRADE_NOT_INT: "Nilai rapor harus berupa bilangan bulat utuh.",
    ErrorCode.GRADE_EMPTY: "Kolom nilai rapor kosong atau belum diisi.",
    ErrorCode.NAME_EMPTY: "Nama siswa tidak boleh kosong.",
    ErrorCode.SCHOOL_NAME_EMPTY: "Nama sekolah tidak boleh kosong.",
    ErrorCode.ENUM_INVALID: "Pilihan nilai tidak valid sesuai daftar opsi yang tersedia.",
    ErrorCode.MAJOR_NOT_FOUND: "Jurusan yang dituju tidak terdaftar dalam kurikulum sekolah.",
    ErrorCode.SUBJECT_DUPLICATE: "Mata pelajaran dengan kode sama sudah ada di semester ini.",
    ErrorCode.MAJOR_IN_USE: "Jurusan tidak dapat dihapus karena masih digunakan oleh data siswa.",
    ErrorCode.SUBJECT_HAS_GRADES: "Mapel tidak dapat dihapus karena telah memuat data nilai siswa.",
    ErrorCode.DUPLICATE_STUDENT: "Siswa dengan nama dan kelas yang sama sudah terdaftar di sistem.",
    ErrorCode.TKA_SYNONYM_UNKNOWN: "Status keikutsertaan TKA tidak dikenal oleh kamus konfigurasi.",
    ErrorCode.HEADER_MISMATCH: "Struktur baris judul CSV tidak sesuai dengan kurikulum jurusan.",
    ErrorCode.CSV_PARSE_ERROR: "Terjadi kesalahan saat memproses susunan baris pada berkas CSV.",
    ErrorCode.FILE_NOT_FOUND: "Berkas yang diminta tidak ditemukan pada lokasi direktori.",
    ErrorCode.IMPORT_ABORTED: "Proses impor data CSV dibatalkan oleh pengguna.",
    ErrorCode.ACHIEVEMENT_LIMIT: "Jumlah prestasi melebihi batas maksimum 5 entri per siswa.",
    ErrorCode.ACHIEVEMENT_IMPORT_DISABLED: "Fitur prestasi belum diaktifkan pada profil sekolah.",
    ErrorCode.ACHIEVEMENT_STUDENT_NOT_FOUND: "Siswa peraih prestasi tidak ditemukan dalam daftar.",
    ErrorCode.FILE_CORRUPT: "Berkas data JSON rusak atau tidak memiliki format yang valid.",
    ErrorCode.BACKUP_CORRUPT: "Berkas cadangan pemulihan (.bak) rusak atau tidak dapat dibaca.",
    ErrorCode.WRITE_FAILED: "Gagal menyimpan berkas ke media penyimpanan fisik.",
    ErrorCode.ATOMIC_WRITE_FAILED: "Penyimpanan atomik gagal, berkas asli tetap terlindungi.",
    ErrorCode.QUOTA_CALCULATION_FAILED: "Perhitungan kuota siswa eligible mengalami kegagalan.",
    ErrorCode.QUOTA_INVALID: "Nilai kuota yang dihasilkan tidak valid.",
}


class EligoError(Exception):
    """Kelas dasar (Base Class) seluruh exception kustom dalam sistem Eligo."""

    def __init__(
        self,
        message: str,
        code: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Inisialisasi EligoError.

        Args:
            message: Pesan teks penjelasan error.
            code: Kode string unik penanda jenis error.
            details: Kamus rincian pendukung (opsional, default dict kosong).
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details if details is not None else {}

    def __str__(self) -> str:
        """Representasi string ramah pengguna."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"[{self.code}] {self.message} ({details_str})"
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        """Representasi teknis untuk keperluan logging dan debugging."""
        return (
            f"{self.__class__.__name__}(code={self.code!r}, "
            f"message={self.message!r}, details={self.details!r})"
        )


class ValidationError(EligoError):
    """Kesalahan validasi data masukan dari pengguna atau berkas.

    Exception ini di-raise saat suatu data masukan melanggar batasan format,
    tipe, atau rentang nilai yang telah ditetapkan (misal nilai rapor < 0 atau > 100).
    """

    def __init__(
        self,
        message: str,
        code: str = ErrorCode.ENUM_INVALID,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


class QuotaCalculationError(EligoError):
    """Kesalahan saat menghitung alokasi kuota siswa eligible SNBP."""

    def __init__(
        self,
        message: str,
        code: str = ErrorCode.QUOTA_CALCULATION_FAILED,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


class BusinessRuleViolationError(EligoError):
    """Pelanggaran terhadap aturan bisnis fundamental SNBP Kemendikbudristek."""

    def __init__(
        self,
        message: str,
        code: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


class IntegrityError(EligoError):
    """Pelanggaran integritas referensial antar entitas data."""

    def __init__(
        self,
        message: str,
        code: str = ErrorCode.MAJOR_IN_USE,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


class PersistenceError(EligoError):
    """Kegagalan pada lapisan infrastruktur penyimpanan (Storage / Disk I/O)."""

    def __init__(
        self,
        message: str,
        code: str = ErrorCode.WRITE_FAILED,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


class CorruptBackupError(PersistenceError):
    """Kegagalan kritis pemulihan bencana (Disaster Recovery Failure)."""

    def __init__(
        self,
        message: str,
        code: str = ErrorCode.BACKUP_CORRUPT,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


class CsvImportError(EligoError):
    """Kesalahan tingkat berkas (file-level) saat memproses dokumen CSV."""

    def __init__(
        self,
        message: str,
        code: str = ErrorCode.HEADER_MISMATCH,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


# Alias kompatibilitas untuk CsvParsingError (sesuai referensi tasks.md)
CsvParsingError = CsvImportError


class ImportAbortedError(CsvImportError):
    """Penanda pembatalan transaksi impor data oleh pengguna secara sadar."""

    def __init__(
        self,
        message: str = "Proses impor data CSV dibatalkan oleh operator.",
        code: str = ErrorCode.IMPORT_ABORTED,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)


@dataclass(frozen=True)
class RowError:
    """Objek nilai (Value Object) yang mewakili kesalahan pada baris CSV tertentu."""

    row_number: int
    column_name: str
    raw_value: str
    error_code: str
    message: str

    def __init__(
        self,
        row_number: int,
        column_name: str | None = None,
        raw_value: str | None = None,
        error_code: str = ErrorCode.GRADE_OUT_OF_RANGE,
        message: str = "",
        *,
        field_name: str | None = None,
        invalid_value: str | None = None,
    ) -> None:
        """Inisialisasi RowError dengan dukungan parameter fleksibel."""
        resolved_column = column_name if column_name is not None else (field_name or "")
        resolved_raw = raw_value if raw_value is not None else (invalid_value or "")

        object.__setattr__(self, "row_number", row_number)
        object.__setattr__(self, "column_name", resolved_column)
        object.__setattr__(self, "raw_value", resolved_raw)
        object.__setattr__(self, "error_code", error_code)
        object.__setattr__(self, "message", message)

    @property
    def field_name(self) -> str:
        """Alias untuk column_name."""
        return self.column_name

    @property
    def invalid_value(self) -> str:
        """Alias untuk raw_value."""
        return self.raw_value