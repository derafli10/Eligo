"""Model Data Domain Murni (Pure Domain Models) Sistem Eligo.

Modul ini mendefinisikan seluruh struktur data inti, objek nilai (Value Objects),
entitas domain, dan enumerasi yang digunakan dalam sistem pemeringkatan siswa eligible SNBP.

Prinsip Rekayasa Enterprise:
    1. Immutability (Kekekalan Data):
       Seluruh model domain didefinisikan menggunakan `@dataclass(frozen=True)`.
       Setelah objek dibuat, nilainya tidak dapat diubah (read-only). Ini mencegah
       terjadinya efek samping (side-effects) yang tidak terduga saat data diproses
       atau disimulasikan.
    2. Zero Dependency & Pure Domain:
       Modul ini murni hanya bergantung pada pustaka standar Python (standard library).
       Dilarang keras mengimpor pustaka pihak ketiga (misalnya `rich`) atau melakukan
       operasi I/O (membaca/menulis file).
    3. Presisi Finansial / Aritmetika Skor:
       Semua perhitungan nilai dan skor akhir WAJIB menggunakan `decimal.Decimal`
       (bukan `float`) untuk menghindari galat pembulatan biner,
       sehingga hasil pemeringkatan 100% deterministik dan dapat diaudit secara manual.

Penjelasan Konsep Bisnis (Untuk Pemahaman Orang Awam):
    - SNBP (Seleksi Nasional Berdasarkan Prestasi) adalah jalur seleksi masuk perguruan
      tinggi negeri tanpa tes tulis, melainkan berbasis nilai rapor semester 1-5 dan prestasi.
    - Siswa Eligible adalah siswa sekolah yang berhak mendaftar SNBP sesuai kuota sekolah
      berdasarkan akreditasi (misal Akreditasi A berhak atas 40% siswa terbaik).
    - TKA (Tes Kemampuan Akademik): Merupakan syarat wajib keikutsertaan. Siswa yang tidak ikut
      TKA otomatis berstatus ABU_ABU (tidak eligible) dan tidak mendapat peringkat kuota.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class SchoolType(StrEnum):
    """Jenis institusi pendidikan jenjang menengah atas yang diakui dalam SNBP.

    Nilai Enumerasi:
        SMA: Sekolah Menengah Atas (jurusan MIPA, IPS, Bahasa, atau Kurikulum Merdeka).
        SMK: Sekolah Menengah Kejuruan (fokus vokasi dan kompetensi keahlian).
        MA:  Madrasah Aliyah (pendidikan menengah berciri khas keagamaan Islam).
    """

    SMA = "SMA"
    SMK = "SMK"
    MA = "MA"


class Accreditation(StrEnum):
    """Peringkat status akreditasi resmi sekolah dari BAN-S/M atau Kemendikbudristek.

    Status akreditasi menjadi faktor utama penentu persentase kuota siswa eligible SNBP:
        - Akreditasi A: Berhak atas kuota 40% siswa terbaik per jurusan.
        - Akreditasi B: Berhak atas kuota 25% siswa terbaik per jurusan.
        - Akreditasi C: Berhak atas kuota 5% (atau 10% sesuai konfigurasi) siswa terbaik.
    """

    A = "A"
    B = "B"
    C = "C"


class TkaStatus(StrEnum):
    """Status keikutsertaan siswa dalam Tes Kemampuan Akademik (TKA).

    Berdasarkan regulasi resmi:
        - IKUT: Siswa mengikuti TKA secara sah. Memenuhi prasyarat untuk dihitung
          skor akhirnya dan berhak memperebutkan kuota eligible (status HIJAU atau KUNING).
        - TIDAK_IKUT: Siswa tidak mengikuti TKA. Sesuai aturan pemeringkatan, siswa ini
          otomatis berstatus ABU_ABU (didiskualifikasi dari kuota) dan tidak mendapatkan
          nomor peringkat kuota, terlepas dari seberapa tinggi nilai rapornya.
    """

    IKUT = "IKUT"
    TIDAK_IKUT = "TIDAK_IKUT"


class AchievementLevel(StrEnum):
    """Tingkatan jenjang prestasi akademik atau non-akademik siswa.

    Tingkat prestasi menentukan bobot poin tambahan yang ditambahkan ke skor rapor siswa:
        - KABUPATEN_KOTA: Prestasi tingkat Kabupaten / Kota (bobot default: +0.25 poin).
        - PROVINSI:       Prestasi tingkat Provinsi (bobot default: +0.50 poin).
        - NASIONAL:       Prestasi tingkat Nasional (bobot default: +1.00 poin).
        - INTERNASIONAL:  Prestasi tingkat Internasional (bobot default: +1.50 poin).
    """

    KABUPATEN_KOTA = "KABUPATEN_KOTA"
    PROVINSI = "PROVINSI"
    NASIONAL = "NASIONAL"
    INTERNASIONAL = "INTERNASIONAL"


class EligibilityStatus(StrEnum):
    """Kategori status kelayakan (eligibilitas) siswa dalam seleksi kuota SNBP.

    Makna Status Visual (Dua Warna Utama + Status Netral):
        - HIJAU:   Siswa lolos kuota sekolah (peringkat 1 sampai batas kuota).
                   Siswa ini berhak didaftarkan ke portal SNBP oleh pihak sekolah.
        - KUNING:  Siswa cadangan / tidak lolos kuota utama (peringkat di atas kuota),
                   namun tetap memenuhi syarat karena telah mengikuti TKA.
        - ABU_ABU: Siswa tidak eligible / didiskualifikasi karena TIDAK mengikuti TKA.
                   Nilai rapor tidak diperhitungkan dalam kuota dan peringkatnya None.
    """

    HIJAU = "HIJAU"
    KUNING = "KUNING"
    ABU_ABU = "ABU_ABU"


@dataclass(frozen=True)
class Subject:
    """Mata pelajaran yang diajarkan dalam kurikulum satu semester.

    Atribut:
        code: Kode alfanumerik kapital unik per mapel (misalnya 'MTK', 'BIN', 'ING').
        name: Nama lengkap mata pelajaran dalam format title-case (misalnya 'Matematika').

    Contoh Penggunaan:
        subject = Subject(code="MTK", name="Matematika")
    """

    code: str
    name: str

    def __post_init__(self) -> None:
        """Validasi integritas data mata pelajaran saat inisialisasi."""
        if not self.code or not self.code.strip():
            raise ValueError("Kode mata pelajaran tidak boleh kosong.")
        if not self.name or not self.name.strip():
            raise ValueError("Nama mata pelajaran tidak boleh kosong.")


@dataclass(frozen=True)
class Achievement:
    """Sertifikat atau bukti prestasi penghargaan yang diraih oleh siswa.

    Atribut:
        description: Uraian kompetisi atau juara (misal 'Juara 1 OSN Astronomi').
        level: Tingkatan wilayah penyelenggaraan kompetisi (AchievementLevel).

    Contoh Penggunaan:
        prestasi = Achievement(
            description="Juara 1 OSN Matematika",
            level=AchievementLevel.NASIONAL
        )
    """

    description: str
    level: AchievementLevel

    def __post_init__(self) -> None:
        """Validasi integritas deskripsi prestasi."""
        if not self.description or not self.description.strip():
            raise ValueError("Deskripsi prestasi tidak boleh kosong.")


@dataclass(frozen=True)
class Major:
    """Komponen jurusan atau peminatan akademik di sekolah (misal MIPA, IPS).

    Setiap jurusan memiliki struktur kurikulum yang terdiri dari 5 semester (Semester 1 s.d. 5).
    Pada masing-masing semester, terdapat daftar mata pelajaran yang wajib dinilai.

    Atribut:
        code: Kode pengenal unik jurusan (misalnya: 'MIPA', 'IPS', 'RPL').
        name: Nama resmi jurusan (misalnya: 'Matematika dan Ilmu Pengetahuan Alam').
        subjects: Tuple 2-dimensi dengan panjang tepat 5 elemen (indeks 0 = Semester 1,
                  indeks 4 = Semester 5). Tiap elemen adalah tuple Subject semester bersangkutan.
    """

    code: str
    name: str
    subjects: tuple[tuple[Subject, ...], ...]

    def __post_init__(self) -> None:
        """Validasi struktur kurikulum 5 semester."""
        if not self.code or not self.code.strip():
            raise ValueError("Kode jurusan tidak boleh kosong.")
        if not self.name or not self.name.strip():
            raise ValueError("Nama jurusan tidak boleh kosong.")
        if len(self.subjects) != 5:
            raise ValueError(
                f"Jurusan {self.code} wajib memiliki kurikulum tepat 5 semester, "
                f"ditemukan: {len(self.subjects)} semester."
            )


@dataclass(frozen=True)
class SchoolProfile:
    """Profil kelembagaan sekolah beserta konfigurasi kurikulum jurusannya.

    Atribut:
        name: Nama lengkap sekolah (misalnya: 'SMA Negeri 1 Jakarta').
        school_type: Kategori jenjang sekolah (SMA / SMK / MA).
        accreditation: Status akreditasi (A / B / C) penentu persentase kuota.
        e_rapor_active: Flag apakah sekolah menggunakan sistem e-Rapor resmi.
                        Jika True, sekolah berhak atas tambahan bonus kuota (misal +5%).
        achievement_enabled: Flag apakah sekolah mengaktifkan poin prestasi tambahan
                             dalam perhitungan pemeringkatan SNBP.
        majors: Tuple berisi seluruh jurusan yang terdaftar di sekolah tersebut.
    """

    name: str
    school_type: SchoolType
    accreditation: Accreditation
    e_rapor_active: bool
    achievement_enabled: bool
    majors: tuple[Major, ...]

    def __post_init__(self) -> None:
        """Validasi nama sekolah dan kelengkapan jurusan."""
        if not self.name or not self.name.strip():
            raise ValueError("Nama sekolah tidak boleh kosong.")


@dataclass(frozen=True)
class Student:
    """Entitas data siswa yang memuat identitas diri, nilai rapor, dan prestasi.

    Atribut:
        id: Nomor pengenal unik siswa secara terurut (misalnya: 'S001', 'S002').
        name: Nama lengkap siswa yang telah dibersihkan spasi gandanya (Title Case).
        class_name: Nama rombongan belajar / kelas siswa (misalnya: 'XII-MIPA-1').
        major_code: Kode jurusan siswa di sekolah (Foreign Key ke Major.code).
        tka_status: Status Tes Kemampuan Akademik (TkaStatus.IKUT / TIDAK_IKUT).
        grades: Tuple 5 elemen (indeks 0 = Semester 1, indeks 4 = Semester 5).
                Tiap elemen adalah dict kode mapel ke nilai bulat (0-100).
                Contoh: ({"MTK": 90, "BIN": 88}, ...)
        achievements: Tuple prestasi siswa (maksimal 5 prestasi sesuai aturan bisnis).
    """

    id: str
    name: str
    class_name: str
    major_code: str
    tka_status: TkaStatus
    grades: tuple[dict[str, int], ...]
    achievements: tuple[Achievement, ...]

    def __post_init__(self) -> None:
        """Validasi struktur nilai dan batasan prestasi siswa."""
        if not self.id or not self.id.strip():
            raise ValueError("ID siswa tidak boleh kosong.")
        if not self.name or not self.name.strip():
            raise ValueError("Nama siswa tidak boleh kosong.")
        if not self.class_name or not self.class_name.strip():
            raise ValueError("Nama kelas siswa tidak boleh kosong.")
        if not self.major_code or not self.major_code.strip():
            raise ValueError("Kode jurusan siswa tidak boleh kosong.")
        if len(self.grades) != 5:
            raise ValueError(
                f"Data nilai siswa {self.name} ({self.id}) harus memuat tepat 5 semester, "
                f"ditemukan: {len(self.grades)} semester."
            )
        if len(self.achievements) > 5:
            raise ValueError(
                f"Siswa {self.name} ({self.id}) melebihi batas maksimum 5 prestasi "
                f"(ditemukan: {len(self.achievements)} prestasi)."
            )


@dataclass(frozen=True)
class RankingResult:
    """Nilai Keluaran (Value Object) dari proses pipeline pemeringkatan siswa.

    Objek ini merepresentasikan baris hasil evaluasi seorang siswa setelah
    melewati seluruh tahapan perhitungan nilai, tie-breaking, dan alokasi kuota.

    Atribut:
        student: Objek data siswa sumber.
        semester_scores: Tuple 5 nilai Decimal rata-rata tiap semester (1 s.d. 5) 2 desimal.
        report_score: Nilai rata-rata dari 5 semester rapor (presisi 2 desimal).
        achievement_points: Total poin prestasi dari sertifikat (maksimal 2.00 poin).
                            Bernilai Decimal('0.00') jika non-aktif atau siswa non-TKA.
        final_score: Skor akhir penentu peringkat (report_score + achievement_points).
        rank: Peringkat kuota (1, 2, ...). Bernilai None bagi siswa yang tidak ikut TKA.
        status: Status kelayakan (HIJAU = Lolos Kuota, KUNING = Cadangan, ABU_ABU = Non-TKA).
    """

    student: Student
    semester_scores: tuple[Decimal, ...]
    report_score: Decimal
    achievement_points: Decimal
    final_score: Decimal
    rank: int | None
    status: EligibilityStatus


# Definisi Tipe Kunci Pengurutan Multi-Kriteria (SortKey)
# ==============================================================================
# Sesuai aturan tie-breaking resmi SNBP Kemendikbudristek (Bab 5.1 & BR-05 design.md):
# Pengurutan dilakukan secara deterministik tanpa seri dengan urutan kriteria:
#   1. Skor Akhir Tertinggi (-final_score)
#   2. Rata-rata Semester 5 Tertinggi (-S5)
#   3. Rata-rata Semester 4 Tertinggi (-S4)
#   4. Rata-rata Semester 3 Tertinggi (-S3)
#   5. Rata-rata Semester 2 Tertinggi (-S2)
#   6. Rata-rata Semester 1 Tertinggi (-S1)
#   7. Nama Siswa Abjad A-Z (name_asc)
#   8. ID Siswa Terkecil (id_asc) -> Jaminan mutlak tidak ada hasil seri.
# Nilai negatif membalik komparasi standar (ascending) menjadi descending.
SortKey = tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, str, str]


@dataclass(frozen=True)
class AppConfig:
    """Objek konfigurasi parameter bisnis yang dimuat dari berkas data/config.json.

    Menghindari adanya hardcoded magic numbers di dalam kode program sehingga
    seluruh aturan bobot dan persentase dapat disesuaikan secara dinamis oleh sekolah.

    Atribut:
        quota_percentages: Pemetaan akreditasi ke persentase kuota desimal
                           (contoh: {'A': Decimal('0.40'), 'B': Decimal('0.25')}).
        e_rapor_bonus_percentage: Persentase tambahan kuota e-rapor (misal Decimal('0.05')).
        quota_rounding_mode: Metode pembulatan kuota ('floor' atau 'half_up').
        achievement_weights: Poin tambahan per tingkat prestasi (Kabupaten, Provinsi, dst).
        achievement_max_points: Batas maksimum akumulasi poin prestasi (misal Decimal('2.00')).
        achievement_max_count: Batas jumlah sertifikat prestasi (misal 5).
        tka_synonyms: Kamus pemetaan variasi penulisan string status TKA ke enum TkaStatus.
        page_size: Jumlah baris data per halaman pada antarmuka tabel CLI.
    """

    quota_percentages: dict[str, Decimal]
    e_rapor_bonus_percentage: Decimal
    quota_rounding_mode: str
    achievement_weights: dict[AchievementLevel, Decimal]
    achievement_max_points: Decimal
    achievement_max_count: int
    tka_synonyms: dict[str, str]
    page_size: int