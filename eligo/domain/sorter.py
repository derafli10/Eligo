"""Algoritma Merge Sort Mandiri dan Pembangunan Kunci Urut Multi-Kriteria.

Modul ini mengimplementasikan algoritma pengurutan Merge Sort secara mandiri
(tanpa menggunakan fungsi bawaan `sorted()` atau `.sort()`) serta fungsi
pembangunan kunci urut (sort key) deterministik untuk pipeline pemeringkatan SNBP.

Prinsip Rekayasa Enterprise:
    1. Merge Sort Mandiri (C3 — Batasan Keras UAS):
       Algoritma sorting WAJIB diimplementasikan sendiri. Penggunaan `sorted()` atau
       `.sort()` Python bawaan dilarang keras di modul ini. Hal ini merupakan
       persyaratan akademis wajib dari ketentuan UAS (C3).
    2. Stabilitas Urutan (Stable Sort):
       Merge Sort menjamin bahwa elemen-elemen dengan kunci identik akan
       mempertahankan urutan kemunculan aslinya (insertion order). Ini penting
       agar pemeringkatan bersifat deterministik dan dapat direproduksi.
    3. Kompleksitas Optimal:
       - Waktu: O(n log n) untuk semua kasus (best, average, worst).
       - Ruang: O(n) memori tambahan untuk array sementara saat proses merge.
       - Kedalaman rekursi: O(log n) — untuk 5.000 siswa hanya ~13 level,
         jauh di bawah batas rekursi Python (default 1.000).
    4. Kunci Urut Total Order (Tanpa Seri / No Ties):
       Tuple kunci urut dirancang agar DUA siswa yang berbeda SELALU menghasilkan
       kunci yang berbeda pula, dengan ID siswa sebagai tiebreaker akhir.

Penjelasan Sederhana untuk Orang Awam:
    Bayangkan Anda ingin mengurutkan 5.000 kartu siswa dari skor tertinggi ke terendah.
    Merge Sort bekerja dengan cara:
    1. Bagi tumpukan kartu menjadi dua bagian sama besar.
    2. Urutkan masing-masing bagian secara terpisah (rekursif).
    3. Gabungkan kedua bagian yang sudah terurut menjadi satu tumpukan terurut.
    Proses ini sangat efisien karena setiap langkah penggabungan hanya perlu
    membandingkan kartu teratas dari dua tumpukan.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from eligo.domain.models import RankingResult, SortKey
from eligo.domain.searcher import binary_search_by_name

# TypeVar generik agar merge_sort dapat digunakan untuk tipe data apapun
T = TypeVar("T")

__all__ = ["build_sort_key", "merge_sort", "binary_search_by_name"]


def build_sort_key(result: RankingResult) -> SortKey:
    """Bangun kunci urut multi-kriteria deterministik untuk satu siswa.

    Urutan kriteria pengurutan (sesuai regulasi SNBP):
        1. Skor Akhir Tertinggi        (-final_score)     → Descending
        2. Rata-rata Semester 5         (-S5)              → Descending
        3. Rata-rata Semester 4         (-S4)              → Descending
        4. Rata-rata Semester 3         (-S3)              → Descending
        5. Rata-rata Semester 2         (-S2)              → Descending
        6. Rata-rata Semester 1         (-S1)              → Descending
        7. Nama Siswa Abjad A-Z         (name)             → Ascending
        8. ID Siswa Terkecil            (id)               → Ascending

    Teknik: Menggunakan nilai negatif Decimal untuk membalik arah komparasi
    standar Python (yang secara default ascending) menjadi descending.
    String nama dan ID dibiarkan positif agar terurut ascending (abjad A-Z).

    Invarian Total Order:
        Dua RankingResult berbeda SELALU menghasilkan SortKey berbeda,
        karena elemen terakhir (id_asc) dijamin unik per siswa.

    Args:
        result: Objek RankingResult yang akan dibuatkan kunci urutnya.

    Returns:
        Tuple SortKey 8 elemen untuk perbandingan leksikografis.
    """
    return (
        -result.final_score,                  # Kriteria 1: Skor akhir tertinggi
        -result.semester_scores[4],           # Kriteria 2: Semester 5 tertinggi
        -result.semester_scores[3],           # Kriteria 3: Semester 4 tertinggi
        -result.semester_scores[2],           # Kriteria 4: Semester 3 tertinggi
        -result.semester_scores[1],           # Kriteria 5: Semester 2 tertinggi
        -result.semester_scores[0],           # Kriteria 6: Semester 1 tertinggi
        result.student.name,                  # Kriteria 7: Nama abjad A-Z
        result.student.id,                    # Kriteria 8: ID terkecil (tiebreaker akhir)
    )


def merge_sort(
    items: list[T],
    key_func: Callable[[T], Any] | None = None,
) -> list[T]:
    """Urutkan daftar menggunakan algoritma Merge Sort stabil secara mandiri.

    PERINGATAN ARSITEKTUR:
        Fungsi ini DILARANG KERAS memanggil `sorted()` atau `.sort()` Python bawaan.
        Pengurutan harus dilakukan sepenuhnya secara mandiri sesuai batasan C3 UAS.

    Merge Sort bekerja dengan prinsip Divide and Conquer:
        1. DIVIDE:   Bagi list menjadi dua separuh yang sama besar.
        2. CONQUER:  Urutkan tiap separuh secara rekursif.
        3. COMBINE:  Gabungkan kedua separuh terurut menjadi satu list terurut.

    Stabilitas:
        Pada proses merge, operator perbandingan menggunakan `<=` (bukan `<`)
        untuk elemen dari separuh kiri. Ini memastikan bahwa elemen dengan
        kunci identik mempertahankan urutan kemunculan aslinya.

    Args:
        items: List yang akan diurutkan. List asli TIDAK dimutasi.
        key_func: Fungsi opsional untuk mengekstrak kunci perbandingan dari setiap elemen.
                  Jika None dan elemen adalah `RankingResult`, otomatis menggunakan `build_sort_key`.

    Returns:
        List baru yang telah terurut secara ascending berdasarkan kunci.
    """
    # Otomatis gunakan build_sort_key jika items bertipe RankingResult dan key_func tidak disuplai
    effective_key = key_func
    if effective_key is None and items and isinstance(items[0], RankingResult):
        effective_key = build_sort_key  # type: ignore[assignment]

    # Basis rekursi: list dengan 0 atau 1 elemen sudah terurut secara trivial
    n = len(items)
    if n <= 1:
        return list(items)

    # DIVIDE: Bagi list menjadi dua separuh
    mid = n // 2
    left = merge_sort(items[:mid], effective_key)
    right = merge_sort(items[mid:], effective_key)

    # COMBINE: Gabungkan kedua separuh yang sudah terurut
    return _merge(left, right, effective_key)


def _merge(
    left: list[T],
    right: list[T],
    key_func: Callable[[T], Any] | None,
) -> list[T]:
    """Gabungkan dua list yang sudah terurut menjadi satu list terurut.

    Proses penggabungan menggunakan teknik dua pointer (two-pointer merge):
        - Pointer `i` melacak posisi di list kiri.
        - Pointer `j` melacak posisi di list kanan.
        - Pada setiap langkah, elemen terkecil dari kedua pointer dipindahkan
          ke list hasil, dan pointer yang bersangkutan dimajukan.

    Stabilitas dijamin dengan menggunakan operator `<=` untuk elemen kiri,
    sehingga elemen kiri yang setara akan ditempatkan sebelum elemen kanan
    (mempertahankan urutan kemunculan asli).

    Args:
        left: Separuh kiri yang sudah terurut.
        right: Separuh kanan yang sudah terurut.
        key_func: Fungsi pengekstrak kunci (opsional).

    Returns:
        List gabungan yang sudah terurut.
    """
    result: list[T] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        # Ekstrak kunci perbandingan (gunakan tipe Any untuk mendukung komparasi leksikografis tuple/SortKey)
        left_key: Any = key_func(left[i]) if key_func else left[i]
        right_key: Any = key_func(right[j]) if key_func else right[j]

        # Gunakan <= untuk stabilitas: elemen kiri yang setara ditempatkan lebih dulu
        if left_key <= right_key:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Tambahkan sisa elemen yang belum terproses
    result.extend(left[i:])
    result.extend(right[j:])

    return result