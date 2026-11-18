from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eligo.domain.exceptions import CorruptBackupError, ErrorCode
from eligo.domain.models import Achievement, AchievementLevel, Student, TkaStatus
from eligo.domain.repositories import StudentRepository
from eligo.infrastructure.atomic_writer import atomic_write_json

logger = logging.getLogger(__name__)


class JsonStudentRepository(StudentRepository):
    # Implementasi StudentRepository berbasis JSON dengan pemulihan otomatis

    def __init__(self, file_path: Path | str = "data/students.json") -> None:
        # Inisialisasi repositori siswa dengan path berkas target
        self._path = Path(file_path).resolve()
        self._bak_path = self._path.with_name(f"{self._path.name}.bak")

    @property
    def file_path(self) -> Path:
        # Mengembalikan objek Path berkas utama
        return self._path

    def load_all(self) -> list[Student]:
        # Memuat seluruh data siswa dengan deteksi korupsi dan pemulihan otomatis dari .bak.

        # Alur Pemulihan:
        #     1. Coba baca berkas utama students.json
        #     2. Jika berkas utama tidak ditemukan dan tidak ada .bak, kembalikan list kosong ([])
        #     3. Jika berkas utama rusak / JSON terpotong, tangkap exception dan coba baca students.json.bak
        #     4. Jika .bak valid, simpan ulang ke students.json untuk memperbaiki file utama
        #     5. Jika berkas utama korup dan .bak juga korup, lempar CorruptBackupError

        main_corrupted = False

        # 1. Baca berkas utama
        if self._path.exists():
            try:
                students, _ = self._read_and_deserialize(self._path)
                return students
            except Exception as err:
                logger.warning(
                    f"Berkas data siswa utama '{self._path}' rusak: {err}. Memulai alur pemulihan dari .bak..."
                )
                main_corrupted = True

        # 2. Pemulihan dari berkas cadangan
        if self._bak_path.exists():
            try:
                restored_students, _ = self._read_and_deserialize(self._bak_path)
                logger.warning(
                    f"Pemulihan berhasil! Memulihkan {len(restored_students)} siswa dari {self._bak_path.name} ke berkas utama."
                )

                # Tulis balik data yang berhasil dipulihkan ke berkas utama secara atomik
                self.save_all(restored_students)
                return restored_students
            except Exception as bak_err:
                logger.error(f"Berkas cadangan '{self._bak_path}' juga korup: {bak_err}")
                if main_corrupted:
                    raise CorruptBackupError(
                        message=(
                            f"Berkas data siswa '{self._path.name}' dan berkas cadangan "
                            f"'{self._bak_path.name}' keduanya korup atau tidak dapat dibaca."
                        ),
                        code=ErrorCode.BACKUP_CORRUPT,
                        details={
                            "main_path": str(self._path),
                            "bak_path": str(self._bak_path),
                            "bak_error": str(bak_err),
                        },
                    ) from bak_err

        # Jika berkas utama korup dan tidak ada cadangan sama sekali
        if main_corrupted:
            raise CorruptBackupError(
                message=(
                    f"Berkas data siswa '{self._path.name}' rusak dan tidak ditemukan berkas "
                    f"cadangan ({self._bak_path.name}) untuk pemulihan."
                ),
                code=ErrorCode.BACKUP_CORRUPT,
                details={"main_path": str(self._path)},
            )

        # Berkas belum ada dan belum ada data (awal penggunaan sistem)
        return []

    def get_all(self) -> list[Student]:
        # Alias untuk load_all()
        return self.load_all()

    def get_by_major(self, major_code: str) -> list[Student]:
        # Saring dan ambil siswa yang terdaftar pada jurusan tertentu
        
        all_students = self.load_all()
        target = major_code.strip().upper()
        return [s for s in all_students if s.major_code.upper() == target]

    def save_all(self, students: list[Student]) -> None:
        # Simpan seluruh data siswa ke JSON secara atomik
        
        payload = self._serialize_students(students)
        atomic_write_json(self._path, payload, indent=2)

    def get_next_id_seq(self) -> int:
        # Hitung nomor urut berikutnya untuk penomoran ID siswa baru
        
        students = self.load_all()
        if not students:
            return 1

        max_seq = 0
        for s in students:
            if s.id.startswith("S") and s.id[1:].isdigit():
                val = int(s.id[1:])
                if val > max_seq:
                    max_seq = val

        return max_seq + 1

    def _read_and_deserialize(self, path: Path) -> tuple[list[Student], int]:
        # Baca JSON dari path dan konversi ke list Student dan next_id_seq
        with open(path, encoding="utf-8") as f:
            payload: dict[str, Any] = json.load(f)

        schema_version = payload.get("schema_version")
        if schema_version != 1:
            raise ValueError(
                f"Versi skema tidak didukung: {schema_version} (wajib versi 1)."
            )

        data = payload.get("data")
        if not isinstance(data, dict):
            raise ValueError("Payload 'data' harus berupa dictionary.")

        next_id_seq = int(data.get("next_id_seq", 1))
        students_raw = data.get("students", [])

        students: list[Student] = []
        for item in students_raw:
            # Penguraian nilai (5 semester)
            grades_list = [dict(g) for g in item.get("grades", [])]

            # Penguraian prestasi
            achievements_list = [
                Achievement(
                    description=str(a["description"]),
                    level=AchievementLevel(str(a["level"]).upper()),
                )
                for a in item.get("achievements", [])
            ]

            student = Student(
                id=str(item["id"]),
                name=str(item["name"]),
                class_name=str(item["class_name"]),
                major_code=str(item["major_code"]),
                tka_status=TkaStatus(str(item["tka_status"]).upper()),
                grades=tuple(grades_list),
                achievements=tuple(achievements_list),
            )
            students.append(student)

        return students, next_id_seq

    def _serialize_students(self, students: list[Student]) -> dict[str, Any]:
        # Konversi daftar objek Student ke JSON
        max_seq = 0
        students_data = []

        for s in students:
            if s.id.startswith("S") and s.id[1:].isdigit():
                val = int(s.id[1:])
                if val > max_seq:
                    max_seq = val

            achievements_data = [
                {"description": a.description, "level": a.level.value}
                for a in s.achievements
            ]

            students_data.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "class_name": s.class_name,
                    "major_code": s.major_code,
                    "tka_status": s.tka_status.value,
                    "grades": list(s.grades),
                    "achievements": achievements_data,
                }
            )

        return {
            "schema_version": 1,
            "last_updated": datetime.now(UTC).isoformat(),
            "data": {
                "next_id_seq": max_seq + 1,
                "students": students_data,
            },
        }