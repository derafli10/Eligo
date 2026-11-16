from __future__ import annotations

from decimal import Decimal

from eligo.domain.models import AppConfig
from eligo.domain.repositories import ConfigRepository


def get_app_config(repo: ConfigRepository) -> AppConfig:
    """Mengambil objek konfigurasi aktif aplikasi dari repositori.

    Args:
        repo: Repositori konfigurasi sistem.

    Returns:
        Objek AppConfig yang memuat seluruh parameter bisnis sistem.
    """
    return repo.load()


def get_tka_synonyms(repo: ConfigRepository) -> dict[str, str]:
    """Mengambil kamus sinonim variasi kata untuk status keikutsertaan TKA.

    Args:
        repo: Repositori konfigurasi.

    Returns:
        Kamus pemetaan kata mentah ke nilai standar (misal {"ya": "IKUT", "ikut": "IKUT"}).
    """
    # Muat seluruh konfigurasi dan simpan di variabel lokal "config"
 # Ambil atribut tka_synonyms saja. Gunanya: CSV bisa berisi "ya", "ikut", "Ya", dll.,
 # dan kamus ini menyeragamkan semuanya menjadi satu nilai baku, mis. "IKUT".
    config = repo.load()
    return config.tka_synonyms


def get_quota_percentages(repo: ConfigRepository) -> dict[str, Decimal]:
    """Mengambil tabel persentase kuota dasar untuk masing-masing akreditasi sekolah.

    Args:
        repo: Repositori konfigurasi.

    Returns:
        Kamus persentase kuota, contoh: {"A": Decimal("0.40"), "B": Decimal("0.25")}.
    """
    config = repo.load()
    return config.quota_percentages