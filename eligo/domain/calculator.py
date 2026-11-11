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
    
    return (report_score + achievement_points).quantize(PRECISION, rounding=ROUND_MODE)