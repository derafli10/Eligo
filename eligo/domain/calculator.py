"""Mesin Kalkulasi Skor Rapor dan Poin Prestasi Domain Murni (Pure Score Calculator).

Modul ini berisi seluruh fungsi perhitungan aritmetika untuk menentukan skor
semester, skor rapor rata-rata, poin prestasi, dan skor akhir siswa dalam
pipeline pemeringkatan SNBP.

Prinsip Rekayasa Enterprise:
    1. Presisi Aritmetika Decimal (Bukan Float):
       Seluruh perhitungan menggunakan `decimal.Decimal` dengan mode pembulatan
       `ROUND_HALF_UP` ke 2 angka desimal. Ini menghindari galat pembulatan biner
       yang terjadi pada tipe `float` bawaan Python.
       Contoh masalah float: `0.1 + 0.2 = 0.30000000000000004` (bukan 0.3).
       Dengan Decimal: `Decimal('0.1') + Decimal('0.2') = Decimal('0.3')` (tepat).
    2. Pure Functions (Fungsi Murni):
       Tidak ada efek samping. Tidak ada I/O, tidak ada mutasi state global.
       Setiap fungsi menerima input dan mengembalikan output secara deterministik.
    3. Auditability (Dapat Diaudit):
       Setiap langkah perhitungan dapat direproduksi secara manual oleh operator
       menggunakan kalkulator biasa, karena presisi Decimal identik dengan
       aritmetika manual manusia.

Penjelasan Sederhana untuk Orang Awam:
    Skor akhir siswa SNBP dihitung bertahap:
    1. Hitung rata-rata nilai per semester (ada 5 semester).
    2. Hitung rata-rata dari 5 rata-rata semester tersebut = "Skor Rapor".
    3. Jika sekolah mengaktifkan fitur prestasi, tambahkan poin prestasi
       (misal Juara 1 Nasional = +1.00, maksimal total +2.00).
    4. Skor Akhir = Skor Rapor + Poin Prestasi.
"""

from __future__ import annotations

import decimal
from decimal import Decimal

from eligo.domain.models import Achievement, AchievementLevel

# Konstanta mode pembulatan dan presisi yang digunakan di seluruh sistem
# ROUND_HALF_UP: angka di batas 0.5 dibulatkan ke atas (cara pembulatan standar sehari-hari)
# Contoh: 87.545 -> 87.55 (bukan 87.54 seperti pada ROUND_HALF_EVEN default Python)
ROUND_MODE = decimal.ROUND_HALF_UP

# Presisi 2 angka di belakang koma (0.01)
PRECISION = Decimal("0.01")


def compute_semester_score(grades: dict[str, int]) -> Decimal:
    """Hitung rata-rata nilai mata pelajaran untuk satu semester.

    Rumus: Skor Semester = (Jumlah Seluruh Nilai Mapel) / (Jumlah Mapel)
    Dibulatkan ke 2 angka desimal menggunakan ROUND_HALF_UP.

    Args:
        grades: Kamus pemetaan kode mata pelajaran ke nilai integer (0-100).
                Contoh: {"MTK": 92, "BIN": 88, "ING": 90}

    Returns:
        Nilai Decimal rata-rata semester dengan presisi 2 desimal.

    Raises:
        ValueError: Jika kamus grades kosong (tidak ada mata pelajaran).

    Contoh:
        >>> compute_semester_score({"MTK": 92, "BIN": 88, "ING": 90})
        Decimal('90.00')
    """
    if not grades:
        raise ValueError("Data nilai semester tidak boleh kosong (minimal 1 mata pelajaran).")

    total = Decimal(sum(grades.values()))
    count = Decimal(len(grades))
    return (total / count).quantize(PRECISION, rounding=ROUND_MODE)


def compute_report_score(semester_scores: tuple[Decimal, ...]) -> Decimal:
    """Hitung rata-rata skor rapor dari 5 semester.

    Rumus: Skor Rapor = (S1 + S2 + S3 + S4 + S5) / 5
    Dibulatkan ke 2 angka desimal menggunakan ROUND_HALF_UP.

    Args:
        semester_scores: Tuple berisi tepat 5 nilai Decimal skor per semester.

    Returns:
        Nilai Decimal rata-rata rapor 5 semester dengan presisi 2 desimal.

    Raises:
        ValueError: Jika jumlah semester bukan tepat 5.

    Contoh:
        >>> scores = (Decimal('90.00'), Decimal('91.00'), Decimal('89.50'),
        ...           Decimal('92.00'), Decimal('88.50'))
        >>> compute_report_score(scores)
        Decimal('90.20')
    """
    if len(semester_scores) != 5:
        raise ValueError(
            f"Skor rapor membutuhkan tepat 5 semester, ditemukan: {len(semester_scores)}."
        )

    total = sum(semester_scores, Decimal("0"))
    return (total / Decimal("5")).quantize(PRECISION, rounding=ROUND_MODE)


def compute_achievement_points(
    achievements: tuple[Achievement, ...],
    weights: dict[AchievementLevel, Decimal],
    max_points: Decimal,
    achievement_enabled: bool,
) -> Decimal:
    """Hitung total poin prestasi siswa berdasarkan bobot per tingkatan.

    Aturan bisnis:
        - Jika fitur prestasi dinonaktifkan oleh sekolah, poin = 0.00.
        - Setiap sertifikat prestasi memiliki bobot sesuai tingkatan:
          Kabupaten/Kota=0.25, Provinsi=0.50, Nasional=1.00, Internasional=1.50.
        - Total poin dibatasi oleh batas maksimum (default: 2.00 poin).
        - Maksimal 5 sertifikat per siswa (divalidasi saat pembuatan objek Student).

    Args:
        achievements: Tuple sertifikat prestasi siswa (maksimal 5 item).
        weights: Kamus bobot per tingkat prestasi dari konfigurasi sistem.
        max_points: Batas maksimum akumulasi poin prestasi (default: Decimal('2.00')).
        achievement_enabled: Flag apakah fitur prestasi diaktifkan oleh sekolah.

    Returns:
        Nilai Decimal total poin prestasi dengan presisi 2 desimal.
        Dijamin tidak melebihi max_points.

    Contoh:
        >>> from eligo.domain.models import Achievement, AchievementLevel
        >>> weights = {AchievementLevel.NASIONAL: Decimal('1.00'),
        ...           AchievementLevel.PROVINSI: Decimal('0.50')}
        >>> ach = (Achievement(description="OSN", level=AchievementLevel.NASIONAL),)
        >>> compute_achievement_points(ach, weights, Decimal('2.00'), True)
        Decimal('1.00')
    """
    # Jika fitur prestasi tidak diaktifkan oleh sekolah, langsung kembalikan 0.00
    if not achievement_enabled:
        return Decimal("0.00")

    # Jika siswa tidak memiliki prestasi, kembalikan 0.00
    if not achievements:
        return Decimal("0.00")

    # Hitung total bobot dari seluruh sertifikat prestasi
    total = Decimal("0")
    for ach in achievements:
        # Ambil bobot sesuai tingkat prestasi dari kamus konfigurasi
        weight = weights.get(ach.level, Decimal("0"))
        total += weight

    # Terapkan batas maksimum (cap) dan bulatkan ke 2 desimal
    capped = min(total, max_points)
    return capped.quantize(PRECISION, rounding=ROUND_MODE)


def compute_final_score(
    report_score: Decimal,
    achievement_points: Decimal,
) -> Decimal:
    """Hitung skor akhir penentu peringkat siswa.

    Rumus sederhana: Skor Akhir = Skor Rapor + Poin Prestasi
    Dibulatkan ke 2 angka desimal menggunakan ROUND_HALF_UP.

    Args:
        report_score: Skor rata-rata rapor 5 semester.
        achievement_points: Total poin prestasi (sudah dibatasi max_points).

    Returns:
        Nilai Decimal skor akhir dengan presisi 2 desimal.

    Contoh:
        >>> compute_final_score(Decimal('90.00'), Decimal('1.00'))
        Decimal('91.00')
    """
    return (report_score + achievement_points).quantize(PRECISION, rounding=ROUND_MODE)