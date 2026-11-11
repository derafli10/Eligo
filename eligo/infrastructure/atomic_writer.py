from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from eligo.domain.exceptions import ErrorCode, PersistenceError


def atomic_write_json(
    file_path: Path | str,
    data: Any,
    indent: int = 2,
) -> None:
    # Tulis data Python ke JSON

    # Alur Teknis Penulisan:
    #     1. Pastikan folder direktori target sudah ada (buat jika belum ada)
    #     2. Tulis payload JSON ke berkas temporer file_path}.tmp
    #     3. Panggil flush() dan os.fsync() agar data tersimpan permanen ke media fisik
    #     4. Jika berkas utama {file_path} sudah ada, duplikasi ke {file_path}.bak
    #     5. Lakukan penggantian atomik: os.replace({file_path}.tmp, {file_path})
    #     6. Jika terjadi error di tahapan manapun, bersihkan berkas .tmp dan
    #        lemparkan PersistenceError(code="ATOMIC_WRITE_FAILED")

    target = Path(file_path).resolve()
    tmp_path = target.with_name(f"{target.name}.tmp")
    bak_path = target.with_name(f"{target.name}.bak")

    # 1. Pastikan direktori utama target sudah ada
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        raise PersistenceError(
            message=f"Gagal membuat direktori folder untuk: {target.parent}",
            code=ErrorCode.WRITE_FAILED,
            details={"path": str(target), "error": str(err)},
        ) from err

    try:
        # 2. Tulis data JSON ke .tmp
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
            # 3. Paksa penulisan dari buffer OS ke memori
            f.flush()
            os.fsync(f.fileno())

        # 4. Jika berkas target sudah ada dari sesi sebelumnya, buat salinan .bak
        if target.exists():
            shutil.copy2(target, bak_path)

        # 5. Ganti berkas target dengan .tmp secara atomik
        os.replace(tmp_path, target)

    except Exception as err:
        # Pembersihan kegagalan: hapus berkas .tmp agar tidak meninggalkan artefak kotor
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass

        raise PersistenceError(
            message=f"Penyimpanan atomik gagal untuk berkas: {target.name}. {err}",
            code=ErrorCode.ATOMIC_WRITE_FAILED,
            details={"path": str(target), "error": str(err)},
        ) from err