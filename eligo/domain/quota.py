"""Modul Perhitungan Kuota SNBP dan Penentuan Status Eligible Domain Murni.

Modul ini bertanggung jawab atas:
    1. Menghitung persentase efektif kuota sekolah (basis akreditasi + bonus e-rapor).
    2. Menghitung jumlah kuota siswa eligible per jurusan (floor atau half_up).
    3. Menetapkan status kelayakan (HIJAU / KUNING / ABU-ABU) dan nomor peringkat.

Prinsip Rekayasa Enterprise:
    1. Pure Domain Logic (Fungsi Murni):
       Tidak ada operasi I/O, pembacaan file, atau efek samping. Seluruh state
       ditransformasi secara fungsional.
    2. Immutability (Kekekalan Objek):
       Hasil penugasan status mengembalikan list baru berisi objek `RankingResult`
       baru tanpa memutasi objek masukan.
    3. Basis Kuota Total Siswa Jurusan:
       Sesuai regulasi resmi SNBP Kemendikbudristek (Bab 9.1 design.md):
       Basis perhitungan kuota persentase adalah TOTAL SISWA PADA JURUSAN TERSEBUT,
       BUKAN hanya siswa yang mengikuti TKA.

Penjelasan Sederhana untuk Orang Awam:
    Sekolah mendapatkan "jatah" kuota siswa yang boleh mendaftar SNBP ke perguruan
    tinggi negeri berdasarkan akreditasi sekolahnya:
    - Akreditasi A: Kuota 40%
    - Akreditasi B: Kuota 25%
    - Akreditasi C: Kuota 5%
    Jika sekolah menggunakan sistem e-Rapor resmi, Kemendikbudristek memberi
    bonus tambahan kuota sebesar +5%.

    Contoh: Jurusan MIPA punya 100 siswa, sekolah akreditasi A (40%) + e-Rapor (5%) = 45%.
    Maka kuotanya = 45 siswa.
    Siswa peringkat 1 sampai 45 yang ikut TKA akan berstatus HIJAU (Eligible / Lolos Kuota).
    Siswa peringkat 46 ke bawah berstatus KUNING (Cadangan).
    Siswa yang tidak ikut TKA berstatus ABU-ABU (Tidak Berhak Ikut SNBP).
"""

from __future__ import annotations

import decimal
import math
from dataclasses import replace
from decimal import Decimal

from eligo.domain.models import EligibilityStatus, RankingResult, TkaStatus


def compute_effective_percentage(
    base_percentage: Decimal | int | float,
    e_rapor_bonus: Decimal | int | float,
    e_rapor_active: bool,
) -> Decimal:
    """Hitung persentase efektif kuota sekolah setelah memperhitungkan bonus e-Rapor.

    Rumus Bisnis:
        Persentase Efektif = Persentase Dasar + (Bonus e-Rapor jika aktif, 0 jika tidak)

    Args:
        base_percentage: Persentase dasar kuota berdasarkan akreditasi sekolah.
                         Bisa dalam format desimal rasio (0.40) atau persen bulat (40).
        e_rapor_bonus: Persentase bonus jika sekolah menggunakan e-Rapor resmi
                       (misal 0.05 atau 5).
        e_rapor_active: Boolean status apakah sekolah mengaktifkan e-Rapor.

    Returns:
        Nilai Decimal persentase efektif kuota.

    Contoh:
        >>> compute_effective_percentage(Decimal("0.40"), Decimal("0.05"), True)
        Decimal('0.45')
        >>> compute_effective_percentage(Decimal("0.40"), Decimal("0.05"), False)
        Decimal('0.40')
    """
    base = Decimal(str(base_percentage))
    bonus = Decimal(str(e_rapor_bonus)) if e_rapor_active else Decimal("0")
    return base + bonus


def compute_quota(
    total_students: int,
    effective_percentage: Decimal | int | float,
    rounding_mode: str = "floor",
) -> int:
    """Hitung jumlah kursi kuota siswa eligible untuk satu jurusan tertentu.

    Sesuai regulasi SNBP (AC-06.07):
        - Kuota dihitung dari total seluruh siswa pada jurusan tersebut.
        - Metode pembulatan default adalah 'floor' (dibulatkan ke bawah).
        - Opsi pembulatan lain adalah 'half_up' (jika diatur di config.json).
        - Edge case: Jika total siswa = 0 atau persentase = 0, kuota = 0 (tidak pernah negatif).

    Args:
        total_students: Total jumlah seluruh siswa pada jurusan tersebut (termasuk yang tidak ikut TKA).
        effective_percentage: Persentase kuota efektif (contoh: Decimal('0.45') untuk 45% atau 45).
        rounding_mode: Metode pembulatan ('floor' untuk ke bawah, 'half_up' untuk pembulatan matematis).

    Returns:
        Jumlah kursi kuota integer (>= 0).

    Contoh:
        >>> compute_quota(100, Decimal("0.40"), "floor")
        40
        >>> compute_quota(33, Decimal("0.40"), "floor")  # 13.2 -> 13
        13
        >>> compute_quota(0, Decimal("0.40"), "floor")
        0
    """
    if total_students <= 0:
        return 0

    pct = Decimal(str(effective_percentage))

    # Jika persentase diberikan dalam bentuk > 1 (misal 40 untuk 40%), ubah ke faktor desimal (0.40)
    if pct > Decimal("1"):
        pct = pct / Decimal("100")

    raw_quota = Decimal(total_students) * pct

    if rounding_mode.lower() == "half_up":
        # Pembulatan matematis 0.5 ke atas
        quota = int(raw_quota.quantize(Decimal("1"), rounding=decimal.ROUND_HALF_UP))
    else:
        # Default 'floor': pembulatan ke bawah selalu
        quota = math.floor(float(raw_quota))

    # Pastikan kuota tidak negatif dan tidak melebihi total siswa
    return max(0, min(quota, total_students))


def assign_eligibility_status(
    sorted_tka_results: list[RankingResult],
    quota: int,
) -> list[RankingResult]:
    """Tetapkan nomor peringkat (rank) dan status kelayakan (HIJAU / KUNING) bagi peserta TKA.

    Aturan Penugasan:
        - Siswa ke-1 sampai ke-min(quota, N) mendapat status HIJAU (Eligible) dengan rank 1..K.
        - Siswa ke-(quota + 1) sampai ke-N mendapat status KUNING (Cadangan) dengan rank (K+1)..N.
        - Siswa yang tidak mengikuti TKA (jika ada di dalam daftar) mendapat status ABU_ABU
          dengan rank None.

    Invarian & Penjamin Mutu:
        - Menghasilkan list baru yang berisi objek `RankingResult` baru (immutable).
        - Tidak memutasi elemen masukan (zero side-effect).
        - Setiap siswa TKA memiliki rank unik dan berurutan dari 1 sampai N.

    Args:
        sorted_tka_results: Daftar siswa yang telah diurutkan berdasarkan kunci urut multi-kriteria.
        quota: Jumlah kuota kursi eligible untuk jurusan tersebut.

    Returns:
        List baru berisi RankingResult dengan rank dan status yang telah ditetapkan.
    """
    updated_results: list[RankingResult] = []
    current_rank = 1

    for result in sorted_tka_results:
        # Jika siswa tidak ikut TKA, status otomatis ABU_ABU dan tanpa peringkat
        if result.student.tka_status != TkaStatus.IKUT:
            updated_results.append(
                replace(
                    result,
                    rank=None,
                    status=EligibilityStatus.ABU_ABU,
                )
            )
            continue

        # Siswa peserta TKA diberi nomor peringkat 1-indexed
        rank = current_rank
        current_rank += 1

        # Tentukan status berdasarkan posisi terhadap batas kuota
        if rank <= quota:
            status = EligibilityStatus.HIJAU
        else:
            status = EligibilityStatus.KUNING

        updated_results.append(
            replace(
                result,
                rank=rank,
                status=status,
            )
        )

    return updated_results