from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from eligo.domain.exceptions import ErrorCode, PersistenceError
from eligo.domain.models import AchievementLevel, AppConfig
from eligo.domain.repositories import ConfigRepository


class JsonConfigRepository(ConfigRepository):
    # config repository dari json
    def __init__(self, file_path: Path | str = "data/config.json") -> None:
        # init repo lokasi berkas target
        self._path = Path(file_path).resolve()

    @property
    def file_path(self) -> Path:
        # Mengembalikan objek Path berkas target
        return self._path

    def load(self) -> AppConfig:
        # Memuat dan memvalidasi konfigurasi aplikasi dari berkas JSON
        if not self._path.exists():
            raise PersistenceError(
                message=f"Berkas konfigurasi tidak ditemukan pada: {self._path}",
                code=ErrorCode.FILE_NOT_FOUND,
                details={"path": str(self._path)},
            )

        try:
            with open(self._path, encoding="utf-8") as f:
                payload: dict[str, Any] = json.load(f)
        except json.JSONDecodeError as err:
            raise PersistenceError(
                message=f"Format berkas konfigurasi tidak valid (JSON corrupt): {err}",
                code=ErrorCode.FILE_CORRUPT,
                details={"path": str(self._path), "error": str(err)},
            ) from err
        except OSError as err:
            raise PersistenceError(
                message=f"Gagal membaca berkas konfigurasi: {err}",
                code=ErrorCode.WRITE_FAILED,
                details={"path": str(self._path), "error": str(err)},
            ) from err

        # Validasi skema versioning
        schema_version = payload.get("schema_version")
        if schema_version != 1:
            raise PersistenceError(
                message=(
                    f"Versi skema konfigurasi tidak didukung. "
                    f"Diharapkan versi 1, ditemukan: {schema_version}"
                ),
                code=ErrorCode.FILE_CORRUPT,
                details={"schema_version": schema_version},
            )

        data = payload.get("data")
        if not isinstance(data, dict):
            raise PersistenceError(
                message="Bagian 'data' pada konfigurasi harus berupa objek JSON (dict).",
                code=ErrorCode.FILE_CORRUPT,
                details={"data_type": type(data).__name__},
            )

        try:
            # Konversi persentase kuota ke Decimal
            quota_percentages = {
                str(k): Decimal(str(v))
                for k, v in data["quota_percentages"].items()
            }
            e_rapor_bonus_percentage = Decimal(str(data["e_rapor_bonus_percentage"]))
            quota_rounding_mode = str(data["quota_rounding_mode"])

            # Konversi bobot prestasi ke enum AchievementLevel dan Decimal
            achievement_weights = {
                AchievementLevel[str(k).upper()]: Decimal(str(v))
                for k, v in data["achievement_weights"].items()
            }
            achievement_max_points = Decimal(str(data["achievement_max_points"]))
            achievement_max_count = int(data["achievement_max_count"])

            tka_synonyms = {
                str(k).lower(): str(v)
                for k, v in data["tka_synonyms"].items()
            }
            page_size = int(data["page_size"])

            return AppConfig(
                quota_percentages=quota_percentages,
                e_rapor_bonus_percentage=e_rapor_bonus_percentage,
                quota_rounding_mode=quota_rounding_mode,
                achievement_weights=achievement_weights,
                achievement_max_points=achievement_max_points,
                achievement_max_count=achievement_max_count,
                tka_synonyms=tka_synonyms,
                page_size=page_size,
            )
        except (KeyError, ValueError, InvalidOperation) as err:
            raise PersistenceError(
                message=f"Data konfigurasi tidak lengkap atau bernilai tidak valid: {err}",
                code=ErrorCode.FILE_CORRUPT,
                details={"path": str(self._path), "error": str(err)},
            ) from err

    def get_config(self) -> AppConfig:
        # Alias untuk metode fungsi load() sesuai Protocol
        return self.load()