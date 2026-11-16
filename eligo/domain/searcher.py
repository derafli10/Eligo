"""Modul Pencarian Biner Berdasarkan Nama Siswa (Pure Domain Binary Searcher).

Modul ini mengimplementasikan algoritma pencarian biner (Binary Search) untuk
menemukan data siswa secara tepat (exact match) berdasarkan nama siswa
dalam kompleksitas waktu logaritmik O(log n).

Prinsip Rekayasa Enterprise:
    1. Efisiensi Skala Besar O(log n):
       Pada sekolah dengan 5.000 siswa, pencarian linear O(n) membutuhkan hingga
       5.000 komparasi. Binary Search hanya membutuhkan maksimal 13 komparasi
       (log2(5000) ~ 12.3).
    2. Zero Side-Effect (Fungsi Murni):
       Fungsi pencarian hanya membaca list input dan mengembalikan indeks integer,
       tanpa memodifikasi daftar yang diperiksa.
    3. Prekondisi Eksplisit:
       Daftar yang dimasukkan WAJIB telah diurutkan berdasarkan `student.name`
       secara ascending (abjad A-Z).

Penjelasan Sederhana untuk Orang Awam:
    Bayangkan Anda mencari nama seseorang di buku telepon tebal yang sudah tersusun rapi
    dari huruf A sampai Z. Alih-alih membaca halaman satu per satu dari awal,
    Anda membuka buku tepat di tengah-tengah:
    - Jika nama yang Anda cari ada di sebelah kiri (abjadnya lebih awal), Anda buang separuh kanan.
    - Jika ada di sebelah kanan, Anda buang separuh kiri.
    Ulangi langkah ini sampai nama yang dicari langsung ditemukan dalam hitungan detik!
"""

from __future__ import annotations

from eligo.domain.models import RankingResult
from eligo.domain.normalizer import normalize_name


def binary_search_by_name(
    sorted_by_name_list: list[RankingResult],
    target_name: str,
) -> int:
    """Cari indeks siswa di dalam daftar hasil pemeringkatan berdasarkan nama.

    PENTING (PREKONDISI):
        Daftar `sorted_by_name_list` HARUS sudah terurut secara ascending (A-Z)
        berdasarkan `student.name`. Daftar ranking utama (yang diurut berdasarkan skor)
        TIDAK BISA langsung digunakan di sini tanpa diurutkan terlebih dahulu.

    Alur Algoritma:
        1. Normalisasi nama target pencarian menggunakan `normalize_name`.
        2. Inisialisasi pointer `lo = 0` dan `hi = len(list) - 1`.
        3. Selama `lo <= hi`:
           - Hitung indeks tengah: `mid = (lo + hi) // 2`.
           - Ambil nama siswa di posisi tengah: `curr = list[mid].student.name`.
           - Jika `curr == target_norm`: DITEMUKAN! Kembalikan `mid`.
           - Jika `curr < target_norm`: Target berada di separuh kanan, geser `lo = mid + 1`.
           - Jika `curr > target_norm`: Target berada di separuh kiri, geser `hi = mid - 1`.
        4. Jika `lo > hi` dan tidak ditemukan, kembalikan `-1`.

    Args:
        sorted_by_name_list: Daftar objek RankingResult yang terurut berdasarkan nama siswa A-Z.
        target_name: String nama siswa yang dicari (bisa berisi variasi spasi / huruf).

    Returns:
        Indeks integer (0-indexed) di dalam list jika ditemukan, atau -1 jika tidak ada.

    Kompleksitas:
        - Waktu: O(log n)
        - Ruang: O(1) tambahan

    Contoh:
        >>> # Asumsi sorted_list memiliki siswa "Ahmad Fauzi", "Budi Santoso", "Citra Dewi"
        >>> binary_search_by_name(sorted_list, "budi santoso")
        1
        >>> binary_search_by_name(sorted_list, "Doni")
        -1
    """
    # Langkah 1: Bersihkan nama target dengan aturan normalisasi domain yang sama
    target_norm = normalize_name(target_name)
    if not target_norm:
        return -1

    # Langkah 2: Inisialisasi batas pencarian dua pointer
    lo = 0
    hi = len(sorted_by_name_list) - 1

    # Langkah 3: Perulangan biner membagi dua ruang pencarian pada setiap iterasi
    while lo <= hi:
        mid = (lo + hi) // 2
        curr_name = sorted_by_name_list[mid].student.name

        if curr_name == target_norm:
            # Ditemukan tepat di indeks mid
            return mid
        elif curr_name < target_norm:
            # Nama target berada di urutan abjad setelah curr_name -> geser ke kanan
            lo = mid + 1
        else:
            # Nama target berada di urutan abjad sebelum curr_name -> geser ke kiri
            hi = mid - 1

    # Langkah 4: Tidak ditemukan dalam seluruh daftar
    return -1