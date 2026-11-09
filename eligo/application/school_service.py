from __future__ import annotations

from dataclasses import replace

from eligo.domain.exceptions import ErrorCode, ValidationError
from eligo.domain.models import (
    Accreditation,
    Major,
    SchoolProfile,
    SchoolType,
)
from eligo.domain.repositories import SchoolRepository


def get_school_profile(repo: SchoolRepository) -> SchoolProfile | None:
    """Mengambil profil sekolah yang saat ini tersimpan di media penyimpanan.

    Args:
        repo: Repositori penyimpanan profil sekolah.

    Returns:
        Objek SchoolProfile jika sudah pernah didaftarkan, atau None jika sistem masih baru.
    """
    return repo.load()


def save_school_profile(profile: SchoolProfile, repo: SchoolRepository) -> None:
    """Menyimpan atau memperbarui profil sekolah secara keseluruhan ke media penyimpanan.

    Fungsi ini melakukan validasi awal:
    - Nama sekolah tidak boleh berupa teks kosong.
    - Status akreditasi harus valid (A, B, atau C).

    Args:
        profile: Entitas SchoolProfile yang akan disimpan.
        repo: Repositori penyimpanan profil sekolah.

     Raises:
        ValidationError: Dengan kode SCHOOL_NAME_EMPTY jika nama sekolah kosong.
    """
    if not profile.name or not profile.name.strip():
        raise ValidationError(
            message="Nama sekolah tidak boleh kosong.",
            code=ErrorCode.SCHOOL_NAME_EMPTY,
        )

    repo.save(profile)


def update_school_settings(
    repo: SchoolRepository,
    name: str | None = None,
    school_type: SchoolType | str | None = None,
    accreditation: Accreditation | str | None = None,
    e_rapor_active: bool | None = None,
    achievement_enabled: bool | None = None,
) -> SchoolProfile:
     """Memperbarui pengaturan kelembagaan sekolah yang sudah ada.

    Fungsi ini memungkinkan pembaruan parsial terhadap parameter sekolah
    (seperti mengubah akreditasi atau menyalakan/mematikan e-Rapor).

    Args:
        repo: Repositori sekolah.
        name: Nama sekolah baru (opsional).
        school_type: Jenjang sekolah baru (SMA/SMK/MA) (opsional).
        accreditation: Akreditasi baru (A/B/C) (opsional).
        e_rapor_active: Status e-rapor aktif/nonaktif (opsional).
        achievement_enabled: Opsi poin prestasi aktif/nonaktif (opsional).

    Returns:
        Objek SchoolProfile yang telah berhasil diperbarui dan disimpan.

    Raises:
        ValidationError: Jika profil sekolah belum pernah diinisialisasi sebelumnya,
                         atau jika ada nilai masukan yang tidak sah.
    """
     current_profile = repo. load()
     if current_profile is None:
        raise ValidationError(
            message= "Profil sekolah belum didaftarkan. Harap inisialisasi profil sekolahterlebih dahulu.",
            code=ErrorCode
        )

     #Validasi nama sekolah jika diubah
     resolved_name = current_profile.name
     if name is not None:
         clean_name = name.strip()
         if not clean_name:
            raise ValidationError(
                message="Nama sekolah tidak boleh kosong.",
                code=ErrorCode.FILE_NOT_FOUND,
            )
         resolved_name = clean_name


     # Validasi jenjang sekolah jika diubah
     resolved_type = current_profile.school_type
     if school_type is not None:
        if isinstance(school_type, SchoolType):
            resolved_type = school_type
        elif isinstance(school_type, str):
            try:
                resolved_type = SchoolType(school_type.strip().upper())
            except ValueError as err:
                valid_types = ", ".join(e.value for e in SchoolType)
                raise ValidationError(
                    message=f"Jenjang sekolah '{school_type}' tidak sah. Pilihan: {valid_types}.",
                    code=ErrorCode.ENUM_INVALID,
                ) from err

            
# Validasi akreditasi jika diubah
     resolved_accreditation = current_profile.accreditation
     if accreditation is not None:
          if isinstance(accreditation, Accreditation):
            resolved_accreditation = accreditation
     elif isinstance(accreditation, str):
            try:
                resolved_accreditation = Accreditation(accreditation.strip().upper())
            except ValueError as err:
                valid_accs = ", ".join(e.value for e in Accreditation)
                raise ValidationError(
                    message=f"Pilihan akreditasi '{accreditation}' tidak valid. Pilihan: {valid_accs}.",
                    code=ErrorCode.ENUM_INVALID,
                ) from err

     resolved_erapor = current_profile.e_rapor_active if e_rapor_active is None else bool(e_rapor_active)
     resolved_ach =(
         current_profile.achievement_enabled if achievement_enabled is None else bool(achievement_enabled)

    )

     updated_profile = replace(
        current_profile,
        name=resolved_name,
        school_type=resolved_type,
        accreditation=resolved_accreditation,
        e_rapor_active=resolved_erapor,
        achievement_enabled=resolved_ach,
    )

     repo.save(updated_profile)
     return updated_profile


def add_major_to_school(repo: SchoolRepository, major: Major) -> SchoolProfile:
    """Menambahkan kurikulum jurusan baru ke dalam profil sekolah.

    Pemeriksaan integritas:
    - Memastikan kode jurusan belum pernah digunakan sebelumnya di sekolah tersebut.
    - Memastikan kurikulum memuat tepat 5 semester dengan minimal 1 mapel per semester.

    Args:
        repo: Repositori sekolah.
        major: Entitas Major baru yang akan didaftarkan.

    Returns:
        Objek SchoolProfile terbaru setelah jurusan berhasil ditambahkan.

    Raises:
        ValidationError: Jika profil sekolah belum ada, kurikulum tidak lengkap,
                         atau kode jurusan sudah terdaftar.
    """
    current_profile = repo.load()
    if current_profile is None:
        raise ValidationError(
            message="Profil sekolah belum ada. Inisialisasi profil sekolah terlebih dahulu.",
            code=ErrorCode.FILE_NOT_FOUND,
        )

    target_code = major.code.strip().upper()
    # Cek apakah kode jurusan sudah terdaftar
    for existing_major in current_profile.majors:
        if existing_major.code.upper() == target_code:
            raise ValidationError(
                message=f"Jurusan dengan kode '{major.code}' sudah terdaftar di sekolah ini.",
                code=ErrorCode.MAJOR_IN_USE,
                details={"major_code": major.code},
            )

    new_majors = current_profile.majors + (Major,)
    updated_profile = replace(current_profile, majors=new_majors)
    repo.save(updated_profile)
    return updated_profile

def get_major_by_code(repo: SchoolRepository, major_code: str) -> Major | None:
    
    profile = repo.load()
    if profile is None:
        return None

    target = major_code.strip().upper()
    for m in profile.majors:
        if m.code.upper() == target:
            return m
    return None 
