"""Protokol Antarmuka Repositori Domain (Domain Repository Protocols).

Modul ini mendefinisikan kontrak abstraksi penyimpanan data (Persistence Abstraction)
menggunakan fitur `typing.Protocol` bawaan Python (Structural Subtyping / Duck Typing Statis).

Prinsip Rekayasa Enterprise (Clean / Hexagonal Architecture):
    - Dependency Inversion Principle (DIP):
      Lapisan domain TIDAK PERNAH bergantung secara langsung pada mekanisme penyimpanan fisik
      (seperti file JSON, SQL Database, atau API eksternal). Sebaliknya, domain mendefinisikan
      "kontrak kerja" (Protocol) yang wajib dipenuhi oleh lapisan infrastruktur.
    - Testability & Mockability:
      Dengan menggunakan Protocol, pengujian unit pada lapisan domain dan aplikasi dapat
      menggunakan data tiruan di memori (in-memory mock/stub) tanpa perlu membaca atau
      menulis ke hard disk secara nyata.

Penjelasan Sederhana untuk Orang Awam:
    Bayangkan Protocol sebagai sebuah "surat perjanjian kerja". Domain mengatakan:
    "Saya tidak peduli bagaimana cara kamu menyimpan data (mau pakai file teks, file JSON,
    atau database), asalkan kamu menyediakan fungsi `load()` untuk mengambil data dan
    fungsi `save()` untuk menyimpan data, maka sistem pemeringkatan dapat bekerja."
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from eligo.domain.models import AppConfig, SchoolProfile, Student


@runtime_checkable
class SchoolRepository(Protocol):
    """Kontrak abstraksi persistensi untuk mengelola profil dan kurikulum sekolah.

    Tanggung Jawab:
        Membaca dan menyimpan data profil sekolah (nama, akreditasi, status e-rapor,
        fitur prestasi, dan struktur mata pelajaran per jurusan).
    """

    def load(self) -> SchoolProfile | None:
        """Memuat profil sekolah dari media penyimpanan.

        Returns:
            SchoolProfile jika data sekolah telah dikonfigurasi, atau None jika
            berkas belum ada / sistem baru pertama kali diinisialisasi.
        """
        ...

    def save(self, profile: SchoolProfile) -> None:
        """Menyimpan atau memperbarui profil sekolah secara permanen.

        Args:
            profile: Objek SchoolProfile yang akan disimpan.
        """
        ...

    def get_profile(self) -> SchoolProfile | None:
        """Alias fungsional untuk metode `load()`.

        Returns:
            SchoolProfile jika ada, atau None jika belum dikonfigurasi.
        """
        ...

    def save_profile(self, profile: SchoolProfile) -> None:
        """Alias fungsional untuk metode `save()`.

        Args:
            profile: Objek SchoolProfile yang akan disimpan.
        """
        ...


@runtime_checkable
class StudentRepository(Protocol):
    """Kontrak abstraksi persistensi untuk mengelola data induk siswa dan nilai rapor.

    Tanggung Jawab:
        Menangani operasi penyimpanan koleksi siswa, pembacaan seluruh siswa,
        serta penyaringan siswa berdasarkan jurusan tertentu.
    """

    def load_all(self) -> list[Student]:
        """Memuat seluruh data siswa yang tersimpan di sistem.

        Returns:
            Daftar (list) berisi seluruh objek Student. Jika belum ada siswa,
            mengembalikan list kosong ([]).
        """
        ...

    def get_all(self) -> list[Student]:
        """Alias fungsional untuk metode `load_all()`.

        Returns:
            Daftar seluruh siswa terdaftar.
        """
        ...

    def get_by_major(self, major_code: str) -> list[Student]:
        """Menyaring dan mengambil seluruh siswa yang terdaftar pada jurusan tertentu.

        Args:
            major_code: Kode jurusan sasaran (misalnya 'MIPA', 'IPS').

        Returns:
            Daftar objek Student yang memiliki atribut `major_code` sesuai parameter.
        """
        ...

    def save_all(self, students: list[Student]) -> None:
        """Menyimpan seluruh data siswa secara atomik (menimpa kondisi sebelumnya).

        Args:
            students: Daftar lengkap objek Student yang akan disimpan.
        """
        ...

    def get_next_id_seq(self) -> int:
        """Mengambil nomor urut urutan berikutnya untuk ID siswa (misal 1 untuk S001).

        Returns:
            Integer sekuens berikutnya.
        """
        ...


@runtime_checkable
class ConfigRepository(Protocol):
    """Kontrak abstraksi persistensi untuk membaca konfigurasi aplikasi.

    Tanggung Jawab:
        Menyediakan parameter bisnis dinamis seperti bobot prestasi, persentase
        kuota, dan sinonim kata kunci TKA.
    """

    def load(self) -> AppConfig:
        """Memuat objek konfigurasi aplikasi.

        Returns:
            Objek AppConfig yang telah divalidasi dan siap digunakan.
        """
        ...

    def get_config(self) -> AppConfig:
        """Alias fungsional untuk metode `load()`.

        Returns:
            Objek AppConfig.
        """
        ...