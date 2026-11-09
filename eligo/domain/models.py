def __post_init__(self):
    if not self.code or not self.code.strip():
        raise ValueError("Kode mata pelajaran tidak boleh kosong.")
    if not self.name or not self.name.strip():
        raise ValueError("Nama mata pelajaran tidak boleh kosong.")

def __post_init__(self):
    if not self.description or not self.description.strip():
        raise ValueError("Deskripsi prestasi tidak boleh kosong.")

def __post_init__(self):
    if not self.code or not self.code.strip():
        raise ValueError("Kode jurusan tidak boleh kosong.")
    if not self.name or not self.name.strip():
        raise ValueError("Nama jurusan tidak boleh kosong.")
    if len(self.subjects) != 5:
        raise ValueError(
            f"Jurusan {self.code} wajib memiliki kurikulum tepat 5 semester,"
            f"ditemukan: {len(self.subjects)} semester."
        )
    
def __post_init__(self):
    if not self.name or not self.name.strip():
        raise ValueError("Nama sekolah tidak boleh kosong.")

def __post_init__(self):
    if not self.id or not self.id.strip():
        raise ValueError("ID siswa tidak boleh kosong.")
    if not self.name or not self.name.strip():
        raise ValueError("Nama siswa tidak boleh kosong.")
    if not self.class_name or not self.major_code.strip():
        raise ValueError("Kode jurusan siswa tidak boleh kosong.")
    if len(self.grades) != 5:
        raise ValueError(
            f"Data nilai siswa {self.name} ({self.id}) harus memuat tepat 5 semester,"
            f"ditemukan: {len(self.grades)} semester."
        )
    if len(self.achievements) > 5:
        raise ValueError(
            f"Siswa {self.name} ({self.id}) melebihi batas makasimum 5 prestasi."
            f"(ditemukan: {len(self.achievements)} prestasi)."
        )

    