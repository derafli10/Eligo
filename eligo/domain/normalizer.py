"""Modul Normalisasi Data Masukan Domain Murni (Pure Input Normalizer).

Modul ini menyediakan fungsi-fungsi pembersihan dan penyeragaman data mentah
sebelum data tersebut divalidasi dan disimpan ke dalam entitas domain.

Prinsip Rekayasa Enterprise:
    1. Pure Functions (Fungsi Murni):
       Seluruh fungsi dalam modul ini bersifat murni — hanya menerima input string
       dan mengembalikan entitas bersih tanpa efek samping (tanpa I/O, tanpa mutasi global).
    2. Idempotent (Idempoten):
       Memanggil fungsi normalisasi berulang kali pada hasil yang sudah ternormalisasi
       akan menghasilkan keluaran yang identik (f(f(x)) == f(x)).
    3. Defensive Parsing:
       Dirancang untuk menangani input kotor dari berkas CSV atau masukan keyboard operator
       dengan toleransi tinggi (spasi berlebihan, variasi huruf besar/kecil, sinonim TKA).

Penjelasan Sederhana untuk Orang Awam:
    Bayangkan data dari berkas Excel/CSV dikirim oleh banyak sekolah dengan gaya penulisan
    yang berbeda-beda. Ada yang menulis nama siswa "  AHMAD   FAUZI  ", ada yang menulis
    "ahmad Fauzi". Modul normalizer ini bertugas menyeragamkan semuanya menjadi
    "Ahmad Fauzi" agar sistem pemeringkatan tidak bingung dan menganggapnya sebagai
    siswa yang berbeda.
"""

from __future__ import annotations

import re

from eligo.domain.exceptions import ErrorCode, ValidationError
from eligo.domain.models import TkaStatus

__all__ = [
    "normalize_name",
    "normalize_class_name",
    "normalize_tka_status",
    "normalize_header",
    "normalize_csv_header",
]


def normalize_name(raw: str) -> str:
    """Bersihkan dan seragamkan penulisan nama siswa menjadi format Title Case.

    Proses normalisasi:
        1. Hapus spasi di awal dan akhir (strip).
        2. Gabungkan spasi berlebihan di tengah menjadi satu spasi (collapse).
        3. Ubah format huruf menjadi Title Case (huruf pertama tiap kata kapital).

    Args:
        raw: String nama mentah dari input pengguna atau berkas CSV.

    Returns:
        String nama yang telah ternormalisasi dalam format Title Case.
        Mengembalikan string kosong ("") jika input hanya berisi spasi atau kosong.

    Contoh:
        >>> normalize_name("  ahmad   FAUZI  ")
        'Ahmad Fauzi'
        >>> normalize_name("   ")
        ''
    """
    if not raw:
        return ""
    # Langkah 1 & 2: strip + collapse spasi berlebihan menggunakan regex \\s+
    collapsed = re.sub(r"\s+", " ", raw.strip())
    # Langkah 3: ubah ke Title Case (huruf pertama tiap kata kapital)
    return collapsed.title()


def normalize_class_name(raw: str) -> str:
    """Bersihkan dan seragamkan penulisan nama kelas menjadi format UPPERCASE.

    Args:
        raw: String nama kelas mentah (misal " xii-ipa-1 " atau "XII-MIPA-1").

    Returns:
        String nama kelas dalam format huruf kapital semua (UPPERCASE).

    Contoh:
        >>> normalize_class_name(" xii-ipa-1 ")
        'XII-IPA-1'
    """
    if not raw:
        return ""
    return raw.strip().upper()


def normalize_tka_status(
    raw: str,
    synonyms: dict[str, str],
    raise_on_unknown: bool = True,
) -> TkaStatus | None:
    """Petakan variasi penulisan status TKA ke nilai enum TkaStatus via kamus sinonim.

    Sistem SNBP menerima berbagai variasi penulisan status keikutsertaan TKA
    dari berkas CSV atau input operator. Fungsi ini menerjemahkan variasi tersebut
    ke nilai standar `TkaStatus.IKUT` atau `TkaStatus.TIDAK_IKUT` menggunakan
    kamus sinonim yang didefinisikan di berkas konfigurasi (data/config.json).

    Args:
        raw: String status TKA mentah dari input (misal "ya", "ikut", "1", "true").
        synonyms: Kamus pemetaan sinonim dari config.json.
                  Contoh: {"ikut": "IKUT", "ya": "IKUT", "tidak": "TIDAK_IKUT"}.
        raise_on_unknown: Jika True (default), melempar `ValidationError` saat sinonim
                          tidak ditemukan. Jika False, mengembalikan None.

    Returns:
        Objek `TkaStatus` (IKUT atau TIDAK_IKUT) jika ditemukan, atau None jika
        tidak dikenal dan `raise_on_unknown=False`.

    Raises:
        ValidationError: Dengan kode TKA_SYNONYM_UNKNOWN jika sinonim tidak dikenal
                         dan `raise_on_unknown=True`.

    Contoh:
        >>> synonyms = {"ikut": "IKUT", "ya": "IKUT", "tidak": "TIDAK_IKUT"}
        >>> normalize_tka_status("Ya", synonyms)
        <TkaStatus.IKUT: 'IKUT'>
        >>> normalize_tka_status("mungkin", synonyms, raise_on_unknown=False)
        None
    """
    key = raw.strip().lower()
    matched = synonyms.get(key)
    if matched is not None:
        try:
            return TkaStatus(matched)
        except ValueError:
            pass

    if raise_on_unknown:
        valid_options = ", ".join(sorted(synonyms.keys()))
        raise ValidationError(
            message=(
                f"Status TKA '{raw}' tidak dikenali. "
                f"Pilihan yang valid: {valid_options}."
            ),
            code=ErrorCode.TKA_SYNONYM_UNKNOWN,
            details={"raw_status": raw, "valid_options": valid_options},
        )
    return None


def normalize_header(raw: str) -> str:
    """Bersihkan dan seragamkan penulisan nama kolom header berkas CSV.

    Header kolom CSV dari berbagai sumber sering memiliki spasi atau tanda minus.
    Fungsi ini mengubahnya menjadi format seragam: lowercase dan mengubah spasi
    atau minus menjadi garis bawah (underscore).

    Args:
        raw: String nama kolom header mentah (misal " Sem1-MTK " atau "Nama Siswa").

    Returns:
        String header yang telah dibersihkan (misal "sem1_mtk", "nama_siswa").

    Contoh:
        >>> normalize_header(" Sem1-MTK ")
        'sem1_mtk'
        >>> normalize_header("Nama Siswa")
        'nama_siswa'
    """
    stripped = raw.strip().lower()
    return re.sub(r"[\s\-]+", "_", stripped)


def normalize_csv_header(header: str) -> str:
    """Bersihkan nama kolom header CSV (fungsi alias untuk kompatibilitas)."""
    return normalize_header(header)