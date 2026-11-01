# Rencana Tugas Implementasi (Implementation Tasks)
**Sistem Pemeringkatan Siswa Eligible SNBP (Eligo)**  
**Versi:** 1.0  
**Tanggal:** 25 Oktober 2026  
**Peran:** Principal Software Architect & QA Lead  
**Status:** Siap Diimplementasikan (Ready for Implementation)  
**Referensi:** `.kiro/specs/snbp-ranking/requirements.md` v1.0, `.kiro/specs/snbp-ranking/design.md` v1.0, `#docs/PRD.md` v1.0  

---

## Daftar Isi

1. [Strategi Pelaksanaan & Jalur Kerja Paralel](#1-strategi-pelaksanaan--jalur-kerja-paralel)
2. [Milestone Roadmap & Dependency Graph](#2-milestone-roadmap--dependency-graph)
3. [Fase 0: Pondasi Bersama, Environment & Kontrak Tipe Data](#3-fase-0-pondasi-bersama-environment--kontrak-tipe-data)
4. [Fase 1: Komponen Domain Murni & Infrastruktur Persistensi Dasar](#4-fase-1-komponen-domain-murni--infrastruktur-persistensi-dasar)
5. [Fase 2: Application Services, Ranking Pipeline & CSV Parser](#5-fase-2-application-services-ranking-pipeline--csv-parser)
6. [Fase 3: Presentation Layer (CLI Rich) & Alur Interaksi Operator](#6-fase-3-presentation-layer-cli-rich--alur-interaksi-operator)
7. [Fase 4: Ekspor, Simulasi What-If, Benchmark & Data Fiktif Generator](#7-fase-4-ekspor-simulasi-what-if-benchmark--data-fiktif-generator)
8. [Fase 5: QA Hardening, Golden Tests, Pemulihan Bencana & Verifikasi NFR](#8-fase-5-qa-hardening-golden-tests-pemulihan-bencana--verifikasi-nfr)
9. [Matriks Ketertelusuran Lengkap (Requirements → Design → Task → Test)](#9-matriks-ketertelusuran-lengkap-requirements--design--task--test)
10. [Checklist Kepatuhan Batasan Keras Rekayasa (C1–C8)](#10-checklist-kepatuhan-batasan-keras-rekayasa-c1c8)

---

## 1. Strategi Pelaksanaan & Jalur Kerja Paralel

Untuk memastikan proyek selesai tepat waktu dengan kualitas standar enterprise tanpa konflik integrasi (*merge conflicts* atau *blocking dependencies*), pekerjaan dibagi secara ketat ke dalam **3 Jalur Kepemilikan (Tracks)** yang merujuk pada Bab 3.4 `design.md`:

```
                 [FASE 0: KONTRAK DATA & SETUP BERSAMA]
                 (models.py, exceptions.py, conftest.py)
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   [TREK ANGGOTA 1]        [TREK ANGGOTA 2]        [TREK ANGGOTA 3]
    Data & Impor            Inti Perhitungan        Tampilan & Kualitas
    (Rafliza)                (Ghaida)               (Fadli)
  - atomic_writer.py      - calculator.py         - formatter.py
  - repositories/         - sorter.py (MergeSort) - menu_school.py
  - csv_parser.py         - quota.py              - menu_student.py
  - import_service.py     - normalizer.py         - school/student_service
  - data_generator.py     - ranking_service.py    - main.py (CLI loop)
  - test_infrastructure   - simulation_service.py - test_formatter.py
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                   [FASE 3 & 4: INTEGRASI SISTEM]
      - menu_ranking.py (menghubungkan ranking_service & formatter)
      - menu_import.py (menghubungkan import_service & Rich UI)
      - menu_simulation.py (menghubungkan simulation_service)
      - menu_benchmark.py (menghubungkan sorter & timeit)
                                  │
                                  ▼
                   [FASE 5: QA & VERIFIKASI AKHIR]
      - Golden Tests (Bagian 8 PRD)
      - Property Tests (Merge Sort vs sorted() oracle)
      - Uji Pemulihan JSON Rusak (.bak recovery)
      - Uji Performa N=150 & N=5.000
```

### Prinsip Kerja Paralel
1. **Contract-First**: Seluruh model domain (`models.py`), kode error (`exceptions.py`), dan antarmuka abstraksi (`repositories.py`) dikunci pada Fase 0. Tidak ada anggota yang boleh mengubah tanda tangan fungsi publik tanpa persetujuan 2 anggota lainnya.
2. **Mocking & Stubbing**: Selama Fase 1 dan 2, Anggota 3 dapat mengembangkan menu CLI menggunakan data dummy in-memory sebelum repositori Anggota 1 dan engine Anggota 2 selesai.
3. **No Domain Pollution**: Anggota 2 dilarang keras mengimpor pustaka `rich`, `csv`, atau melakukan operasi I/O di dalam direktori `domain/`.
4. **Deterministic Testing**: Setiap task wajib menyertakan unit test otomatis yang dapat dieksekusi secara independen via `pytest`.

---

## 2. Milestone Roadmap & Dependency Graph

| Milestone | Target Luaran | Verifikasi Keberhasilan |
|---|---|---|
| **M0: Foundation** | Setup environment, linter, type checker, model domain, hierarki exception | `pytest`, `mypy --strict`, dan `ruff check` lolos 100% |
| **M1: Core Logic & Storage** | Merge sort mandiri, kalkulator skor `Decimal`, repositori atomik `.bak`, parser CSV | Unit tests domain dan infrastructure lolos dengan branch coverage ≥ 90% |
| **M2: Service Orchestration** | Pipeline ranking terintegrasi, state machine impor CSV, simulasi what-if | Ranking service lolos golden test Bagian 8; impor mengumpulkan semua error |
| **M3: Terminal Interface** | Seluruh menu CLI interaktif aktif dengan format Rich dan penanganan Ctrl+C global | Operator dapat menavigasi seluruh alur tanpa crash atau unhandled exception |
| **M4: Deliverables & Benchmark** | Data fiktif 150 & 5.000 siswa, ekspor CSV/TXT, runner benchmark | Waktu proses 150 siswa < 200 ms; 5.000 siswa < 5.000 ms; C1–C8 terpenuhi |
| **M5: QA Sign-off** | Seluruh skenario batas, pemulihan bencana, audit determinisme lolos | Cakupan tes total ≥ 90%, zero defect pada golden test fixtures |

---

## 3. Fase 0: Pondasi Bersama, Environment & Kontrak Tipe Data [SELESAI]

### TASK-0.1: Inisialisasi Proyek, Konfigurasi Lingkungan & Tooling Dev [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: Tidak ada
- **Referensi**: C1, C2, C8, NFR Kode
- **Langkah Pengerjaan**:
  1. Buat berkas `requirements.txt` hanya berisi `rich>=13.0.0` dan `pytest>=8.0.0`.
  2. Buat berkas `requirements-dev.txt` berisi `ruff>=0.3.0` dan `mypy>=1.9.0`.
  3. Konfigurasikan `pyproject.toml` untuk:
     - `ruff`: line-length = 100, target-version = "py311", aturan linting: E, F, I (isort), UP, B (bugbear).
     - `mypy`: strict = true, disallow_untyped_defs = true, warn_return_any = true.
     - Tambahkan aturan linter/mypy khusus yang melarang `import rich` dan operasi I/O di folder `eligo/domain/`.
  4. Siapkan struktur folder lengkap sesuai Bab 3.3 `design.md`:
     `eligo/{domain,application,infrastructure/repositories,presentation/cli}`, `data/{import,exports}`, `tests/{domain,application,infrastructure,benchmark}`, `generator/`.
  5. Buat `.gitignore` yang mengecualikan `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `data/import/`, `data/exports/`, `*.tmp`, `*.bak`.
- **Deliverables**: `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, `.gitignore`, struktur folder berserta `__init__.py`.
- **DoD**: Perintah `py -3 -m pytest`, `py -3 -m mypy eligo`, dan `py -3 -m ruff check .` dapat dijalankan tanpa error di terminal Windows. (Terpenuhi: 33 tests passed, 0 ruff errors, 0 mypy issues).

### TASK-0.2: Implementasi Model Domain, Enum, Value Objects & Protocol [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 3 (Fadli) didampingi Anggota 2 (Rafliza)
- **Prasyarat**: TASK-0.1
- **Referensi**: REQ-01, REQ-02, REQ-03, REQ-06, ADR-01, Bab 4.1 & 5.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/models.py`:
     - Enum: `SchoolType` (SMA, SMK, MA), `Accreditation` (A, B, C), `TkaStatus` (IKUT, TIDAK_IKUT), `AchievementLevel` (KABUPATEN_KOTA, PROVINSI, NASIONAL, INTERNASIONAL), `EligibilityStatus` (HIJAU, KUNING, ABU_ABU).
     - Dataclass frozen: `Subject`, `Achievement`, `Major`, `SchoolProfile`, `Student`, `RankingResult`, `AppConfig`.
     - Tipe alias `SortKey`: `tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, str, str]`.
     - Pastikan seluruh skor menggunakan `Decimal` dan collection menggunakan immutable `tuple` (kecuali list inner grades dict).
  2. Buat `eligo/domain/repositories.py`:
     - Definisikan `typing.Protocol` untuk:
       - `SchoolRepository`: `get_profile() -> SchoolProfile`, `save_profile(profile: SchoolProfile) -> None`.
       - `StudentRepository`: `get_all() -> list[Student]`, `get_by_major(major_code: str) -> list[Student]`, `save_all(students: list[Student]) -> None`.
       - `ConfigRepository`: `get_config() -> AppConfig`.
- **Deliverables**: `eligo/domain/models.py`, `eligo/domain/repositories.py`.
- **DoD**: Tipe data tervalidasi via `mypy --strict`, immutabilitas `frozen=True` terbukti gagal saat di-assign ulang di unit test. (Terpenuhi).

### TASK-0.3: Implementasi Hierarki Exception & Katalog Kode Error [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-0.1
- **Referensi**: REQ-04, REQ-05, REQ-13, Bab 6 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/exceptions.py`:
     - Base class: `EligoError(Exception)` menyimpan `code: str`, `message: str`, `details: dict[str, Any]`.
     - Subclass domain: `ValidationError`, `QuotaCalculationError`, `BusinessRuleViolationError`.
     - Subclass infrastructure: `PersistenceError`, `CorruptBackupError`, `CsvParsingError`.
     - Value object untuk baris CSV: `RowError(row_number: int, field_name: str, invalid_value: str, error_code: str, message: str)`.
  2. Daftarkan 20 katalog kode error standar sesuai Bab 6.2 `design.md` (misal `GRADE_OUT_OF_RANGE`, `TKA_SYNONYM_UNKNOWN`, `CORRUPT_JSON`, dll.).
- **Deliverables**: `eligo/domain/exceptions.py`, `tests/domain/test_exceptions.py`.
- **DoD**: Semua subclass dapat di-instantiate, memuat kode error, dan dapat di-catch sesuai hierarki inheritance. (Terpenuhi).

### TASK-0.4: Konfigurasi Default & Fixture Uji Dasar (conftest.py) [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-0.2, TASK-0.3
- **Referensi**: C6, REQ-01, REQ-02, Bab 7 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `data/config.json` dengan `schema_version: 1` memuat:
     - Persentase kuota akreditasi: A=40, B=25, C=5.
     - Bonus e-rapor: 5.
     - Mode pembulatan kuota: `floor`.
     - Bobot prestasi: KABUPATEN_KOTA=0.25, PROVINSI=0.50, NASIONAL=1.00, INTERNASIONAL=1.50.
     - Batas maksimum poin prestasi: 2.00.
     - Batas jumlah prestasi per siswa: 5.
     - Sinonim status TKA: {"ya": "IKUT", "ikut": "IKUT", "1": "IKUT", "true": "IKUT", "tidak": "TIDAK_IKUT", "tidak ikut": "TIDAK_IKUT", "0": "TIDAK_IKUT", "false": "TIDAK_IKUT"}.
  2. Buat `tests/conftest.py`:
     - Fixture `sample_config() -> AppConfig` membaca konfigurasi default.
     - Fixture `sample_school_profile() -> SchoolProfile` (SMA fiktif, Akreditasi A, e-Rapor aktif, Jurusan MIPA & IPS).
- **Deliverables**: `data/config.json`, `tests/conftest.py`.
- **DoD**: Fixture dapat di-inject ke pengujian pytest tanpa membaca file disk secara hardcode. (Terpenuhi).

---

## 4. Fase 1: Komponen Domain Murni & Infrastruktur Persistensi Dasar

### [TREK ANGGOTA 1] TASK-1.1: Penulisan Berkas Atomik & Rotasi Backup (.bak)
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-0.3
- **Referensi**: C5, REQ-13 (AC-13.01, AC-13.02), ADR-04, Bab 9.5 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/infrastructure/atomic_writer.py` dengan fungsi:
     `atomic_write_json(file_path: Path, data: dict[str, Any], indent: int = 2) -> None`.
  2. Alur teknis:
     - Tulis payload JSON ke `target.tmp`.
     - Panggil `f.flush()` dan `os.fsync(f.fileno())` untuk memastikan data terbilas ke storage fisik.
     - Jika file `target` sudah ada, buat cadangan aman: `shutil.copy2(target, target.bak)`.
     - Lakukan penggantian atomik: `os.replace(target.tmp, target)`.
  3. Tangani exception: jika terjadi kegagalan sebelum `os.replace`, hapus file `.tmp` dan lempar `PersistenceError(code="ATOMIC_WRITE_FAILED")`.
- **Deliverables**: `eligo/infrastructure/atomic_writer.py`, `tests/infrastructure/test_atomic_writer.py`.
- **DoD**: Tes memverifikasi: (1) berkas utama terbuat sempurna, (2) berkas `.bak` terbentuk saat penulisan kedua, (3) interupsi sebelum commit tidak merusak berkas asli. (Terpenuhi).

### [TREK ANGGOTA 1] TASK-1.2: Repositori Sekolah & Konfigurasi Berbasis JSON
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-0.2, TASK-1.1
- **Referensi**: REQ-01, REQ-02, REQ-13, Bab 5.2 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/infrastructure/repositories/config_repo.py`:
     - Implementasi pembacaan `data/config.json` menjadi `AppConfig`.
     - Validasi `schema_version == 1`.
  2. Buat `eligo/infrastructure/repositories/school_repo.py`:
     - Implementasi `SchoolRepository` (baca/tulis `data/school.json`).
     - Terapkan pemulihan otomatis: jika `school.json` rusak atau tidak valid, coba baca `school.json.bak` dan pulihkan.
     - Jika keduanya tidak ada/rusak, kembalikan `None` atau lempar `CorruptBackupError`.
- **Deliverables**: `eligo/infrastructure/repositories/config_repo.py`, `eligo/infrastructure/repositories/school_repo.py`, `tests/infrastructure/test_school_repo.py`.
- **DoD**: Pengujian memverifikasi serialisasi/deserialisasi objek `SchoolProfile`, penanganan missing file, dan pemulihan dari file `.bak`. (Terpenuhi).

### [TREK ANGGOTA 1] TASK-1.3: Repositori Siswa Berbasis JSON dengan Pemulihan Otomatis
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-0.2, TASK-1.1
- **Referensi**: REQ-03, REQ-13 (AC-13.03, AC-13.04, AC-13.05), Bab 5.2 & 9.5 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/infrastructure/repositories/student_repo.py`:
     - Implementasi `StudentRepository` (baca/tulis `data/students.json`).
     - Konversi list `Student` ke dict terstruktur dengan `schema_version: 1`, `metadata`, dan list siswa.
     - Menggunakan `atomic_write_json`.
  2. Mekanisme Pemulihan Bencana:
     - Logika `load_with_recovery`: Jika parsing JSON gagal atau struktur korup, log peringatan, muat `students.json.bak`, lalu timpa balik berkas utama dengan data cadangan.
     - Jika cadangan juga korup, lempar `CorruptBackupError(code="BACKUP_CORRUPT")`.
- **Deliverables**: `eligo/infrastructure/repositories/student_repo.py`, `tests/infrastructure/test_student_repo.py`, `tests/infrastructure/test_recovery.py`.
- **DoD**: Unit test menguji skenario file korup terpotong (truncated JSON) berhasil dipulihkan secara transparan dari `.bak`. (Terpenuhi).

---

### [TREK ANGGOTA 2] TASK-1.4: Modul Normalisasi & Validasi Domain Murni
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-0.2, TASK-0.3
- **Referensi**: REQ-03, REQ-04, REQ-05, Bab 4.1 & 7.4 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/normalizer.py`:
     - `normalize_name(raw: str) -> str`: strip whitespace, collapse multi-spaces via regex `\s+`, ubah ke Title Case (misal `"  ahmad   FAUZI "` → `"Ahmad Fauzi"`).
     - `normalize_class_name(raw: str) -> str`: strip dan uppercase.
     - `normalize_tka_status(raw: str, synonyms: dict[str, str]) -> TkaStatus`: case-insensitive lookup terhadap kamus sinonim config. Lempar `ValidationError(code="TKA_SYNONYM_UNKNOWN")` jika tidak dikenal.
     - `normalize_header(raw: str) -> str`: strip, lowercase, ubah spasi/tanda minus menjadi underscore.
  2. Buat `eligo/domain/validator.py`:
     - `validate_grade(val: Any) -> int`: pastikan integer antara 0 dan 100. Nilai bertipe float atau string bukan digit melempar `ValidationError(code="GRADE_NOT_INT")`. Nilai di luar 0..100 melempar `ValidationError(code="GRADE_OUT_OF_RANGE")`.
     - `validate_student_payload(...)`: validasi kelengkapan nama tidak kosong, jurusan terdaftar di profil sekolah, semester 1..5 lengkap.
- **Deliverables**: `eligo/domain/normalizer.py`, `eligo/domain/validator.py`, `tests/domain/test_normalizer.py`, `tests/domain/test_validator.py`.
- **DoD**: Seluruh kasus uji boundary table (Tabel 7.4 `design.md`) lolos verifikasi. (Terpenuhi).

### [TREK ANGGOTA 2] TASK-1.5: Mesin Kalkulasi Skor Decimal & Batas Prestasi
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-0.2, TASK-0.4
- **Referensi**: REQ-06 (AC-06.01, AC-06.02, AC-06.03, AC-06.04), ADR-01, Bab 4.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/calculator.py`:
     - Gunakan konstanta `ROUND_MODE = decimal.ROUND_HALF_UP` dan pembulatan `Decimal("0.01")`.
     - `compute_semester_score(grades: dict[str, int]) -> Decimal`: jumlah nilai dibagi jumlah mapel, dibulatkan ke 2 desimal.
     - `compute_report_score(semester_scores: tuple[Decimal, ...]) -> Decimal`: rata-rata 5 semester, dibulatkan ke 2 desimal.
     - `compute_achievement_points(achievements: tuple[Achievement, ...], weights: dict[str, Decimal], max_points: Decimal, enabled: bool) -> Decimal`:
       - Jika `enabled=False` atau siswa tidak ikut TKA, poin = `Decimal("0.00")`.
       - Ambil maksimal 5 prestasi teratas (jika > 5, tolak saat validasi).
       - Poin = `min(total_poin_terkumpul, max_points)`.
     - `compute_final_score(report_score: Decimal, achievement_points: Decimal) -> Decimal`: `report_score + achievement_points`.
- **Deliverables**: `eligo/domain/calculator.py`, `tests/domain/test_calculator.py`.
- **DoD**: Unit test membuktikan presisi floating point tidak terjadi (misal `0.1 + 0.2 != 0.3` di float dicegah dengan `Decimal`), dan batas poin 2.00 berfungsi mutlak. (Terpenuhi).

### [TREK ANGGOTA 2] TASK-1.6: Algoritma Merge Sort Mandiri & Kunci Urut Multi-Kriteria
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-0.2, TASK-1.5
- **Referensi**: C3, REQ-06 (AC-06.05, AC-06.06), ADR-03, Bab 9.2 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/sorter.py`:
     - Fungsi pembuat kunci urut: `build_sort_key(item: RankingResult) -> SortKey`.
       Urutan elemen tuple:
       `(-item.final_score, -item.semester_scores[4], -item.semester_scores[3], -item.semester_scores[2], -item.semester_scores[1], -item.semester_scores[0], item.student.name, item.student.id)`.
     - Tanda minus pada `Decimal` membalik urutan komparasi standar menjadi *descending* (nilai terbesar di depan).
     - String `name` dan `id` bernilai positif menghasilkan urutan abjad *ascending*.
     - Implementasikan fungsi rekursif `merge_sort[T](items: list[T], key_func: Callable[[T], Any]) -> list[T]` secara mandiri.
     - Operator pada proses merge wajib `<=` untuk mempertahankan **stabilitas** urutan (*stable sort*).
     - **Dilarang keras** menggunakan fungsi bawaan `sorted()` atau `.sort()` di dalam modul ini.
- **Deliverables**: `eligo/domain/sorter.py`, `tests/domain/test_sorter.py`.
- **DoD**:
  - Property test: Hasil `merge_sort` identik dengan `sorted(items, key=...)` sebagai oracle.
  - Test stabilitas: Elemen dengan kunci identik mempertahankan urutan kemunculan aslinya.
  - Tidak ada panggilan `sorted` pada kode produksi `eligo/domain/sorter.py`. (Terpenuhi).

### [TREK ANGGOTA 2] TASK-1.7: Perhitungan Kuota & Penentuan Status Eligible
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-0.2, TASK-0.4
- **Referensi**: REQ-06 (AC-06.07, AC-06.08, AC-06.09, AC-06.10, AC-06.11), Bab 4.1 & 9.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/quota.py`:
     - `compute_effective_percentage(base_pct: int, e_rapor_bonus: int, e_rapor_active: bool) -> int`: `base_pct + (e_rapor_bonus if e_rapor_active else 0)`.
     - `compute_quota(total_students: int, effective_percentage: int, rounding_mode: str = "floor") -> int`:
       - `math.floor((total_students * effective_percentage) / 100)`.
       - Catatan penting: Basis perhitungan adalah **total siswa pada jurusan tersebut**, BUKAN hanya yang mengikuti TKA.
     - `assign_eligibility_status(sorted_tka_results: list[RankingResult], quota: int) -> list[RankingResult]`:
       - Siswa ke-1 s.d. `min(quota, len(sorted_tka_results))` berstatus `HIJAU` dengan rank `1..K`.
       - Siswa sisanya berstatus `KUNING` dengan rank `(K+1)..N`.
       - Siswa non-TKA (diproses di pipeline) berstatus `ABU_ABU` dengan rank `None`.
- **Deliverables**: `eligo/domain/quota.py`, `tests/domain/test_quota.py`.
- **DoD**: Pengujian edge case kuota 0 (misal 5% dari 10 siswa = floor(0.5) = 0 siswa hijau), dan kasus kuota melebihi jumlah peserta TKA. (Terpenuhi).

### [TREK ANGGOTA 2] TASK-1.8: Modul Pencarian Binary Search Berdasarkan Nama
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-0.2, TASK-1.4
- **Referensi**: C4, REQ-07 (AC-07.03), Bab 9.3 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/domain/searcher.py`:
     - `binary_search_by_name(sorted_by_name_list: list[RankingResult], target_name: str) -> int`:
       - Normalisasi nama target via `normalize_name`.
       - Invarian: `sorted_by_name_list` harus telah terurut berdasarkan `student.name` secara *ascending*.
       - Algoritma binary search klasik dua pointer (`lo`, `hi`), kembalikan indeks jika cocok, atau `-1` jika tidak ditemukan.
- **Deliverables**: `eligo/domain/searcher.py`, `tests/domain/test_searcher.py`.
- **DoD**: Unit test memverifikasi pencarian nama di awal, tengah, akhir daftar, dan kasus nama tidak ditemukan dengan kompleksitas O(log n). (Terpenuhi).

---

### [TREK ANGGOTA 3] TASK-1.9: Formatter Terminal & Utilitas UI Rich
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: TASK-0.2
- **Referensi**: C1, REQ-14 (AC-14.02, AC-14.03, AC-14.05), Bab 3.3 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/formatter.py`:
     - `format_decimal(val: Decimal, precision: int = 2) -> str`: Ubah format titik menjadi koma sesuai standar Indonesia (misal `Decimal("87.50")` → `"87,50"`). Nilai Decimal asli tidak boleh bermutasi.
     - `badge_status(status: EligibilityStatus) -> str`: Return text beranotasi warna Rich: `[green]ELIGIBLE[/green]` (HIJAU), `[yellow]CADANGAN[/yellow]` (KUNING), `[dim]TIDAK ELIGIBLE (NON-TKA)[/dim]` (ABU_ABU).
     - `create_student_table(results: list[RankingResult], page: int, page_size: int) -> rich.table.Table`: Buat tabel kaya dengan kolom: Rank, ID, Nama, Kelas, Skor S1–S5, Rerata Rapor, Poin Prestasi, Skor Akhir, Status.
     - `create_summary_panel(...) -> rich.panel.Panel`: Panel statistik ringkasan kuota dan jumlah per status.
- **Deliverables**: `eligo/presentation/cli/formatter.py`, `tests/presentation/test_formatter.py`.
- **DoD**: Format desimal koma tervalidasi via unit test; tabel Rich dapat dirender tanpa error ANSI di terminal Windows. (Terpenuhi).

---

## 5. Fase 2: Application Services, Ranking Pipeline & CSV Parser

### [TREK ANGGOTA 1] TASK-2.1: Robust CSV Parser dengan Deteksi BOM & Delimiter
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-0.3, TASK-1.4
- **Referensi**: REQ-04 (AC-04.01, AC-04.02), REQ-05 (AC-05.04), ADR-05, Bab 4.2 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/infrastructure/csv_parser.py`:
     - `detect_encoding_and_delimiter(file_path: Path) -> tuple[str, str]`:
       - Baca 4 byte pertama untuk mendeteksi UTF-8 BOM (`\xef\xbb\xbf`). Jika ada gunakan `utf-8-sig`, jika tidak `utf-8`.
       - Baca baris header untuk mendeteksi pembatas: prioritas titik koma `;` jika count(;) > count(,), selain itu koma `,`.
     - `parse_csv_rows(file_path: Path, expected_subjects: list[str]) -> tuple[list[dict[str, str]], list[RowError]]`:
       - Baca seluruh baris menggunakan `csv.reader`.
       - Normalisasi header.
       - Validasi struktur kolom wajib (nama, kelas, tka, mapel per semester).
       - Strategi **Collect-All Errors**: Kumpulkan seluruh baris rusak ke dalam `list[RowError]`, jangan berhenti di error pertama!
- **Deliverables**: `eligo/infrastructure/csv_parser.py`, `tests/infrastructure/test_csv_parser.py`.
- **DoD**: Lolos pengujian matriks CSV: CSV bersih, CSV dengan BOM Windows, CSV pemisah titik koma, CSV dengan header acak, dan CSV dengan sel kosong. (Terpenuhi).

### [TREK ANGGOTA 1] TASK-2.2: Import Service & State Machine Alur Impor
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-1.3, TASK-1.4, TASK-2.1
- **Referensi**: REQ-04 (AC-04.04, AC-04.05, AC-04.06, AC-04.07), REQ-05, Bab 9.4 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/application/import_service.py`:
     - Dataclass `ImportPreview`: `valid_students: list[Student]`, `row_errors: list[RowError]`, `duplicate_names: list[str]`, `total_rows: int`.
     - `prepare_import_preview(file_path: Path, major: Major, existing_students: list[Student], config: AppConfig) -> ImportPreview`:
       - Panggil `csv_parser`.
       - Lakukan validasi domain untuk setiap baris yang berhasil di-parse.
       - Identifikasi siswa duplikat berdasarkan komposit `(nama_ternormalisasi, kelas)`.
       - **Kritis**: Tidak ada penulisan data ke disk pada tahap ini!
     - `commit_import(preview: ImportPreview, duplicate_action: str, existing_students: list[Student], repo: StudentRepository, error_report_dir: Path) -> tuple[int, int]`:
       - Tangani resolusi duplikat: `"skip"` (pertahankan data lama), `"overwrite"` (timpa dengan data baru), atau batalkan jika `"abort"`.
       - Berikan ID auto-increment baru (`S001`, `S002`, dst.) untuk siswa baru.
       - Simpan hasil akhir via `repo.save_all(...)`.
       - Jika ada baris error, tulis log kegagalan ke `error_report_<timestamp>.csv` di folder `data/import/`.
- **Deliverables**: `eligo/application/import_service.py`, `tests/application/test_import_service.py`.
- **DoD**: Terbukti tidak ada penulisan ke `students.json` saat operator membatalkan sebelum konfirmasi (*zero dirty write*). (Terpenuhi).

---

### [TREK ANGGOTA 2] TASK-2.3: Ranking Service (Pipeline Utama Pemeringkatan)
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-1.5, TASK-1.6, TASK-1.7, TASK-1.8
- **Referensi**: REQ-06, REQ-07, Bab 4.1 & 9.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/application/ranking_service.py`:
     - `run_ranking_pipeline(students: list[Student], profile: SchoolProfile, config: AppConfig) -> tuple[list[RankingResult], int]`:
       - Tahap 1: Pisahkan siswa TKA dan non-TKA via `s.tka_status == TkaStatus.IKUT`.
       - Tahap 2: Untuk setiap siswa TKA, hitung `semester_scores` (S1..S5), `report_score`, `achievement_points` (dengan limit), dan `final_score`.
       - Tahap 3: Urutkan siswa TKA menggunakan `merge_sort` mandiri dan `build_sort_key`.
       - Tahap 4: Hitung kuota efektif berdasarkan akreditasi sekolah dan status e-Rapor.
       - Tahap 5: Tetapkan rank (1..N) dan status (`HIJAU` atau `KUNING`) pada siswa TKA via `assign_eligibility_status`.
       - Tahap 6: Konversi siswa non-TKA menjadi `RankingResult` berstatus `ABU_ABU`, rank `None`, skor `None`.
       - Tahap 7: Gabungkan hasil `ranked_tka + abu_abu_results` dan kembalikan bersama nilai kuota.
     - `search_student_in_results(results: list[RankingResult], target_name: str) -> Optional[RankingResult]`:
       - Siapkan list yang diurutkan berdasarkan `student.name` via `sorted(results, key=lambda r: r.student.name)` (diizinkan di Application/Presentation).
       - Panggil `binary_search_by_name`.
- **Deliverables**: `eligo/application/ranking_service.py`, `tests/application/test_ranking_service.py`.
- **DoD**: Pipeline terbukti deterministik (1.000 kali pengujian menghasilkan urutan yang identik tanpa variasi). (Terpenuhi).

### [TREK ANGGOTA 2] TASK-2.4: Simulation Service (Isolasi What-If & Set Difference)
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-2.3
- **Referensi**: REQ-09, ADR-02, Bab 4.1 & 9.6 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/application/simulation_service.py`:
     - Dataclass `SimulationDiff`: `baseline_quota: int`, `simulated_quota: int`, `newly_eligible_ids: set[str]`, `no_longer_eligible_ids: set[str]`, `rank_changes: dict[str, tuple[int, int]]`.
     - `run_simulation(students: list[Student], profile: SchoolProfile, config: AppConfig, overrides: dict[str, Any]) -> tuple[list[RankingResult], list[RankingResult], SimulationDiff]`:
       - Buat salinan deepcopy: `sim_students = copy.deepcopy(students)` dan `sim_profile = copy.deepcopy(profile)`.
       - Terapkan perubahan simulasi (misal ubah akreditasi sekolah A → B, atau ubah status TKA siswa tertentu dari TIDAK_IKUT → IKUT).
       - Jalankan `run_ranking_pipeline` untuk baseline dan simulasi secara murni tanpa I/O.
       - Lakukan analisis selisih menggunakan operasi `set`:
         - `base_set = {r.student.id for r in baseline if r.status == HIJAU}`
         - `sim_set = {r.student.id for r in simulated if r.status == HIJAU}`
         - `newly_eligible = sim_set - base_set`
         - `no_longer_eligible = base_set - sim_set`
- **Deliverables**: `eligo/application/simulation_service.py`, `tests/application/test_simulation_service.py`.
- **DoD**: Pengujian memverifikasi data asli (`students` & `profile`) sama sekali tidak bermutasi setelah simulasi dijalankan. (Terpenuhi).

---

### [TREK ANGGOTA 3] TASK-2.5: Application Services untuk Sekolah, Siswa & Konfigurasi
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: TASK-1.2, TASK-1.3
- **Referensi**: REQ-01, REQ-02, REQ-03, REQ-10, Bab 4.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/application/school_service.py`:
     - Use cases: inisialisasi profil sekolah, pembaruan akreditasi, toggle e-Rapor, penambahan jurusan baru dan mata pelajaran.
  2. Buat `eligo/application/student_service.py`:
     - Use cases: tambah siswa manual, edit data siswa, hapus siswa, validasi data via `validator.py`, generasi ID unik `S001` format konsisten.
  3. Buat `eligo/application/config_service.py`:
     - Use case: penyedia konfigurasi aktif aplikasi.
- **Deliverables**: `eligo/application/school_service.py`, `eligo/application/student_service.py`, `eligo/application/config_service.py`.
- **DoD**: Unit test menguji CRUD siswa dan sekolah terhubung dengan repositori dan melempar `ValidationError` jika data salah. (Terpenuhi).

---

## 6. Fase 3: Presentation Layer (CLI Rich) & Alur Interaksi Operator

### [TREK ANGGOTA 3] TASK-3.1: Kerangka Menu Utama & Handler KeyboardInterrupt Global
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: TASK-1.9, TASK-2.5
- **Referensi**: C1, REQ-14 (AC-14.01, AC-14.04), Bab 4.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/main.py`:
     - Loop menu utama menggunakan Rich console.
     - Pilihan menu: (1) Profil Sekolah & Jurusan, (2) Manajemen Siswa, (3) Impor Nilai CSV, (4) Hasil Pemeringkatan SNBP, (5) Simulasi What-If, (6) Benchmark Algoritma, (0) Keluar.
     - **Titik Tunggal Global Interrupt**: Tangkap `KeyboardInterrupt` pada loop utama di `main.py`. Tampilkan pesan ramah `"[yellow]Operasi dibatalkan oleh pengguna. Kembali ke menu utama...[/yellow]"` tanpa merusak aplikasi (tidak ada stack trace mentah).
  2. Buat entry point root `main.py` yang memanggil `eligo.presentation.cli.main.run_app()`.
- **Deliverables**: `main.py`, `eligo/presentation/cli/main.py`.
- **DoD**: Menekan Ctrl+C pada sembarang prompt input kembali ke menu utama secara mulus dan state data tetap utuh. (Terpenuhi).

### [TREK ANGGOTA 3] TASK-3.2: Menu Profil Sekolah & Manajemen Siswa Manual
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: TASK-2.5, TASK-3.1
- **Referensi**: REQ-01, REQ-02, REQ-03, REQ-14
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/menu_school.py`:
     - Tampilan informasi sekolah dalam bentuk Panel Rich.
     - Form interaktif untuk mengubah akreditasi (pilihan A/B/C) dan toggle e-rapor aktif.
  2. Buat `eligo/presentation/cli/menu_student.py`:
     - Tabel daftar siswa dengan paginasi.
     - Form interaktif penambahan siswa manual: input nama, pilih kelas, pilih jurusan, input nilai semester 1–5 untuk tiap mata pelajaran wajib, input status TKA, dan prestasi.
- **Deliverables**: `eligo/presentation/cli/menu_school.py`, `eligo/presentation/cli/menu_student.py`.
- **DoD**: Operator dapat mendaftarkan profil sekolah dan memasukkan data siswa secara manual dengan umpan balik visual error saat input salah. (Terpenuhi).

### [TREK ANGGOTA 3] TASK-3.3: Menu Hasil Pemeringkatan, Paginasi & Detail Siswa
- **Owner**: Anggota 3 (Fadli) didampingi Anggota 2 (Ghaida)
- **Prasyarat**: TASK-1.9, TASK-2.3, TASK-3.1
- **Referensi**: REQ-06, REQ-07, REQ-14, Bab 4.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/menu_ranking.py`:
     - Tampilkan tabel hasil pemeringkatan lengkap menggunakan `create_student_table` dari `formatter.py`.
     - Fitur paginasi (default 15 siswa per halaman) dengan navigasi `[N]ext`, `[P]rev`, `[Q]uit`.
     - Fitur filter status: Tampilkan Semua / Hanya Eligible (Hijau) / Cadangan (Kuning) / Non-TKA (Abu-abu).
     - Fitur cari siswa berdasarkan nama: Menggunakan `search_student_in_results` (Binary Search) dan menampilkan kartu profil lengkap siswa yang ditemukan beserta rincian nilai tiap semesternya.
- **Deliverables**: `eligo/presentation/cli/menu_ranking.py`.
- **DoD**: Tampilan tabel berwarna rapi, desimal ditampilkan dengan koma, navigasi paginasi bekerja responsif, dan pencarian nama berfungsi tepat. (Terpenuhi).

### [TREK ANGGOTA 1 & 3] TASK-3.4: Menu Interaktif Impor CSV dengan State Machine
- **Owner**: Anggota 1 (Rafliza) & Anggota 3 (Fadli)
- **Prasyarat**: TASK-2.2, TASK-3.1
- **Referensi**: REQ-04, REQ-05, REQ-14, Bab 9.4 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/menu_import.py`:
     - Alur interaktif sesuai diagram sequence Bab 9.4:
       1. Operator memilih jurusan target impor.
       2. Sistem menyediakan template CSV di `data/import/<jurusan>_template.csv` jika belum ada.
       3. Operator memasukkan path berkas CSV yang akan diimpor.
       4. Panggil `import_service.prepare_import_preview`.
       5. Tampilkan ringkasan pratinjau: Jumlah Baris Valid (Hijau), Baris Error (Merah), Duplikat (Kuning).
       6. Jika ada duplikat, tampilkan pilihan: `[1] Lewati (Skip)`, `[2] Timpa (Overwrite)`, `[3] Batalkan (Abort)`.
       7. Tampilkan konfirmasi eksplisit: `"Simpan perubahan ke database? (Y/N)"`.
       8. Hanya jika operator menekan `Y`, panggil `import_service.commit_import`.
- **Deliverables**: `eligo/presentation/cli/menu_import.py`.
- **DoD**: Data tidak pernah tersimpan jika operator memilih `N` atau menekan Ctrl+C di tahap konfirmasi. (Terpenuhi).

---

## 7. Fase 4: Ekspor, Simulasi What-If, Benchmark & Data Fiktif Generator [SELESAI]

### [TREK ANGGOTA 3] TASK-4.1: Ekspor Hasil Pemeringkatan ke CSV & TXT [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: TASK-2.3, TASK-1.1
- **Referensi**: REQ-08 (AC-08.01, AC-08.02, AC-08.03, AC-08.04), Bab 5.3 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/infrastructure/export_writer.py`:
     - `export_to_csv(file_path: Path, results: list[RankingResult]) -> None`:
       - Tulis header standar: `rank,id,nama,kelas,skor_akhir,status`.
       - Tulis nilai desimal dengan titik atau format standar ekspor, status berupa teks.
     - `export_to_txt(file_path: Path, results: list[RankingResult], school: SchoolProfile, quota: int) -> None`:
       - Tulis laporan formal rapi: kop profil sekolah, kuota, tabel pemeringkatan berjarak tetap (fixed-width columns), dan tanggal ekspor.
  2. Buat `eligo/application/export_service.py` untuk mengorkestrasi penulisan ke folder `data/exports/` dengan penamaan otomatis: `ranking_<jurusan>_<YYYYMMDD_HHMMSS>.[csv|txt]`.
- **Deliverables**: `eligo/infrastructure/export_writer.py`, `eligo/application/export_service.py`, `tests/infrastructure/test_export_writer.py`.
- **DoD**: File CSV dan TXT terbuat di direktori `data/exports/` dengan isi data yang sinkron dengan tabel pemeringkatan di layar. (Terpenuhi).

### [TREK ANGGOTA 2 & 3] TASK-4.2: Menu Simulasi Interaktif What-If & Visualisasi Perubahan Status [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 2 (Ghaida) & Anggota 3 (Fadli)
- **Prasyarat**: TASK-2.4, TASK-3.1
- **Referensi**: REQ-09 (AC-09.01, AC-09.02, AC-09.03), Bab 4.1 & 9.6 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/menu_simulation.py`:
     - Pilihan skenario simulasi:
       - Skenario A: Perubahan Akreditasi Sekolah (misal A ke B atau sebaliknya).
       - Skenario B: Siswa Non-TKA beralih status menjadi Ikut TKA.
     - Panggil `simulation_service.run_simulation`.
     - Tampilkan tabel komparasi sebelum dan sesudah:
       - Perubahan kuota: Kuota Asli vs Kuota Simulasi.
       - Siswa yang Baru Masuk Kuota Eligible (`newly_eligible`): Ditandai teks tebal hijau `+ MASUK`.
       - Siswa yang Terlempar dari Kuota (`no_longer_eligible`): Ditandai teks tebal merah `- KELUAR`.
     - Tegaskan kepada operator bahwa simulasi ini murni kalkulasi memori dan tidak mengubah file `students.json` sama sekali.
- **Deliverables**: `eligo/presentation/cli/menu_simulation.py`.
- **DoD**: Hasil simulasi menampilkan diferensiasi siswa yang berubah status dengan akurat dan data disk terbukti tidak berubah (verifikasi via hash/mtime berkas). (Terpenuhi).

### [TREK ANGGOTA 1] TASK-4.3: Generator Data Fiktif Realistis Terkontrol Seed [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-0.2, TASK-1.4
- **Referensi**: C7, REQ-11, NFR Performa, Bab 3.3 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `generator/data_generator.py`:
     - Gunakan `random.Random(seed=42)` untuk **keterulangan 100% deterministik**.
     - Kamus nama fiktif kombinatorial Indonesia (100 nama depan fiktif + 100 nama belakang fiktif) untuk mencegah duplikasi identitas riil.
     - Distribusi nilai rapor normal/realistis (rerata 75–90, rentang 60–100).
     - Proporsi TKA realistis: ~85% IKUT, ~15% TIDAK_IKUT.
     - Proporsi prestasi: ~20% memiliki 1–3 sertifikat.
     - Fungsi CLI mandiri: `py -3 -m generator.data_generator --size [150|5000] --major MIPA --output data/students.json`.
- **Deliverables**: `generator/data_generator.py`, `tests/generator/test_data_generator.py`.
- **DoD**: Eksekusi generator dengan seed yang sama menghasilkan dataset yang bit-for-bit identik. (Terpenuhi).

### [TREK ANGGOTA 3] TASK-4.4: Runner Benchmark & Menu Perbandingan Algoritma [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 3 (Fadli) didampingi Anggota 2 (Ghaida)
- **Prasyarat**: TASK-1.6, TASK-4.3
- **Referensi**: C3, REQ-12 (AC-12.01, AC-12.02, AC-12.03), Bab 4.1 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `eligo/presentation/cli/menu_benchmark.py`:
     - Muat dataset siswa fiktif (pilihan ukuran: dataset aktif, 150 siswa, atau 5.000 siswa).
     - Jalankan pengukuran waktu komputasi pengurutan menggunakan `time.perf_counter_ns()` sebanyak `K=5` iterasi.
     - Ukur waktu eksekusi:
       - `Merge Sort` mandiri (`domain/sorter.py`).
       - `Timsort` bawaan Python (`sorted()`).
     - Tampilkan tabel komparasi di layar: Waktu Rata-rata Merge Sort vs Timsort, Rasio Performa, dan Verifikasi Kesamaan Hasil Pengurutan (keduanya harus menghasilkan urutan yang identik).
- **Deliverables**: `eligo/presentation/cli/menu_benchmark.py`, `tests/benchmark/test_benchmark.py`.
- **DoD**: Benchmark berjalan tanpa crash pada N=5.000 dan menampilkan laporan perbandingan waktu yang jelas. (Terpenuhi).

---

## 8. Fase 5: QA Hardening, Golden Tests, Pemulihan Bencana & Verifikasi NFR [SELESAI]

### [QA LEAD / TREK ANGGOTA 2] TASK-5.1: Verifikasi Golden Test Suite Berdasarkan PRD Bagian 8 [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 2 (Ghaida) & QA Lead
- **Prasyarat**: TASK-2.3, TASK-0.4
- **Referensi**: REQ-06, Bagian 8 PRD, Bab 7.2 `design.md`
- **Langkah Pengerjaan**:
  1. Buat skrip kalibrasi di `tests/calibrate_golden.py` untuk mencari nilai integer rapor per semester yang menghasilkan nilai rata-rata dan skor akhir yang persis sama dengan Tabel Contoh 1 & Contoh 2 Bagian 8 PRD.
  2. Implementasikan `tests/application/test_ranking_service.py`:
     - **Golden Test Kasus 1**: Pemeringkatan standar SMA Akreditasi A (kuota 40% dari 10 siswa = 4 siswa eligible). Verifikasi urutan juara, pemecah seri via nilai semester terbaru (S5 > S4 > dst.), dan status `HIJAU`/`KUNING`.
     - **Golden Test Kasus 2**: Pemecah seri kompleks (Siswa B dan Siswa C memiliki skor akhir dan seluruh nilai semester identik). Verifikasi penentu akhir berdasarkan abjad nama (`name_asc`).
     - **Golden Test Kasus 3**: Kasus siswa berprestasi tinggi tetapi tidak mengikuti TKA otomatis berstatus `ABU_ABU` dan berada di luar kuota.
     - **Golden Test Kasus 4**: Akumulasi bobot prestasi (golden_dataset_example2: Eko, Fani, Gani, Dara).
- **Deliverables**: `tests/application/test_ranking_service.py`.
- **DoD**: 100% assertions pada golden test suite lolos (*zero variance* terhadap spesifikasi PRD). (Terpenuhi).

### [QA LEAD / TREK ANGGOTA 2] TASK-5.2: Property-Based & Stress Test Merge Sort [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 2 (Ghaida)
- **Prasyarat**: TASK-1.6
- **Referensi**: C3, REQ-06, Bab 7.3 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `tests/domain/test_sorter_property.py`:
     - Uji invarian: Ukuran list sebelum dan sesudah merge sort harus sama persis (tidak ada elemen hilang/ganda).
     - Uji kesetaraan oracle: `merge_sort(data, key=build_sort_key) == sorted(data, key=build_sort_key)` untuk 50 iterasi random list (panjang 0 s.d. 1.000).
     - Uji stabilitas: Elemen dengan skor dan nama identik tetap mempertahankan urutan aslinya.
     - Uji batas rekursi: Pastikan pengurutan 5.000 siswa tidak melebihi `sys.getrecursionlimit()`.
- **Deliverables**: `tests/domain/test_sorter_property.py`.
- **DoD**: Seluruh uji invarian dan ekuivalensi oracle lolos tanpa kegagalan. (Terpenuhi).

### [QA LEAD / TREK ANGGOTA 1] TASK-5.3: Pengujian Pemulihan Bencana & Integritas Storage [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 1 (Rafliza)
- **Prasyarat**: TASK-1.1, TASK-1.3
- **Referensi**: C5, REQ-13, Bab 7.5 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `tests/infrastructure/test_recovery.py`:
     - Skenario A: `students.json` korup (karakter terpotong di tengah JSON) tetapi `students.json.bak` valid. Verifikasi sistem otomatis memulihkan file utama dan membaca data dengan sukses.
     - Skenario B: Baik file utama maupun `.bak` keduanya korup. Verifikasi sistem melempar `CorruptBackupError` dengan pesan audit yang jelas dan tidak menghapus file yang ada.
     - Skenario C: File `.tmp` tertinggal akibat proses terputus paksa. Verifikasi operasi tulis berikutnya membersihkan file sementara tanpa error.
- **Deliverables**: `tests/infrastructure/test_recovery.py`.
- **DoD**: Sistem terbukti tahan terhadap kerusakan file lokal dan mampu memulihkan diri secara mandiri (*self-healing*). (Terpenuhi).

### [QA LEAD / TREK ANGGOTA 3] TASK-5.4: Verifikasi Kinerja & NFR Benchmark (150 & 5.000 Siswa) [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Anggota 3 (Fadli)
- **Prasyarat**: TASK-2.3, TASK-4.3
- **Referensi**: REQ-11, NFR Performa, Bab 10 `design.md`
- **Langkah Pengerjaan**:
  1. Buat `tests/benchmark/test_performance.py`:
     - Generate dataset 150 siswa fiktif via `data_generator`. Ukur waktu eksekusi end-to-end `run_ranking_pipeline`. Assert waktu < 200 ms.
     - Generate dataset 5.000 siswa fiktif. Ukur waktu eksekusi. Assert waktu < 5.000 ms (5 detik).
     - Ukur alokasi memori menggunakan modul `tracemalloc`. Assert penambahan memori saat memproses 5.000 siswa < 50 MB.
- **Deliverables**: `tests/benchmark/test_performance.py`.
- **DoD**: Seluruh ambang batas performa NFR terlampaui di lingkungan pengujian standar. (Terpenuhi).

### [QA LEAD / SELURUH TIM] TASK-5.5: Dokumentasi Proyek, Panduan Pengguna & Final Review [SELESAI]
- **Status**: SELESAI (100% Lolos Verifikasi)
- **Owner**: Seluruh Tim (Dipimpin QA Lead)
- **Prasyarat**: Seluruh task sebelumnya
- **Referensi**: C8, REQ-14
- **Langkah Pengerjaan**:
  1. Lengkapi `README.md`:
     - Deskripsi sistem Eligo, identitas 3 anggota tim dan peran masing-masing.
     - Panduan instalasi dan menjalankan aplikasi: `py -3 -m venv venv`, `pip install -r requirements.txt`, `py -3 main.py`.
     - Panduan menjalankan suite pengujian: `py -3 -m pytest tests/ -v`.
     - Dokumentasi format CSV dan contoh struktur template impor.
  2. Lakukan audit kepatuhan kode via `py -3 -m ruff check .` dan `py -3 -m mypy eligo generator`.
  3. Pastikan tidak ada berkas temporer atau data riil siswa yang tertinggal di git repository.
- **Deliverables**: `README.md`, laporan lolos linting dan pengetikan statis.
- **DoD**: Dokumen `README.md` jelas, instruktif, dan dapat dijalankan oleh pihak eksternal/dosen penguji dari *clean install*. (Terpenuhi).

---

## 9. Matriks Ketertelusuran Lengkap (Requirements → Design → Task → Test)

| Requirement | Komponen Desain | Task ID | Test Suite |
|---|---|---|---|
| **REQ-01** (Profil Sekolah) | `models.SchoolProfile`, `school_repo.py`, `school_service.py` | TASK-0.2, TASK-1.2, TASK-2.5 | `tests/infrastructure/test_school_repo.py` |
| **REQ-02** (Konfigurasi Fleksibel) | `models.AppConfig`, `config_repo.py`, `config_service.py` | TASK-0.2, TASK-0.4, TASK-1.2 | `tests/domain/test_quota.py`, `tests/conftest.py` |
| **REQ-03** (Manajemen Siswa) | `models.Student`, `student_repo.py`, `validator.py` | TASK-0.2, TASK-1.3, TASK-1.4, TASK-2.5 | `tests/domain/test_validator.py`, `test_student_repo.py` |
| **REQ-04** (Impor CSV) | `csv_parser.py`, `import_service.py`, `menu_import.py` | TASK-2.1, TASK-2.2, TASK-3.4 | `tests/infrastructure/test_csv_parser.py`, `test_import_service.py` |
| **REQ-05** (Validasi Input) | `validator.py`, `normalizer.py`, `exceptions.py` | TASK-0.3, TASK-1.4, TASK-2.1 | `tests/domain/test_validator.py`, `test_normalizer.py` |
| **REQ-06** (Algoritma Pemeringkatan) | `calculator.py`, `sorter.py`, `quota.py`, `ranking_service.py` | TASK-1.5, TASK-1.6, TASK-1.7, TASK-2.3 | `tests/domain/test_calculator.py`, `test_sorter.py`, `test_quota.py`, `test_ranking_service.py` |
| **REQ-07** (Tampilan Hasil & Cari) | `formatter.py`, `searcher.py`, `menu_ranking.py` | TASK-1.8, TASK-1.9, TASK-3.3 | `tests/domain/test_searcher.py`, `tests/presentation/test_formatter.py` |
| **REQ-08** (Ekspor Laporan) | `export_writer.py`, `export_service.py` | TASK-4.1 | `tests/infrastructure/test_export_writer.py` |
| **REQ-09** (Simulasi What-If) | `simulation_service.py`, `menu_simulation.py` | TASK-2.4, TASK-4.2 | `tests/application/test_simulation_service.py` |
| **REQ-10** (Keberlanjutan Data) | `atomic_writer.py`, `student_repo.py` | TASK-1.1, TASK-1.3 | `tests/infrastructure/test_atomic_writer.py` |
| **REQ-11** (Skalabilitas & Data Fiktif) | `data_generator.py` | TASK-4.3, TASK-5.4 | `tests/generator/test_data_generator.py`, `test_performance.py` |
| **REQ-12** (Benchmark Efisiensi) | `sorter.py`, `menu_benchmark.py` | TASK-1.6, TASK-4.4 | `tests/domain/test_sorter_property.py` |
| **REQ-13** (Penanganan Error & Pemulihan) | `atomic_writer.py`, `exceptions.py`, `student_repo.py` | TASK-0.3, TASK-1.1, TASK-1.3, TASK-5.3 | `tests/infrastructure/test_recovery.py`, `test_atomic_writer.py` |
| **REQ-14** (Pengalaman Pengguna CLI) | `main.py`, `formatter.py`, modul-modul `menu_*.py` | TASK-1.9, TASK-3.1, TASK-3.2, TASK-3.3 | `tests/presentation/test_formatter.py`, verifikasi interaktif |

---

## 10. Checklist Kepatuhan Batasan Keras Rekayasa (C1–C8)

Setiap pengembang wajib melakukan verifikasi mandiri terhadap daftar periksa berikut sebelum mengajukan *pull request* / penggabungan kode:

- [ ] **C1 (Teknologi Minimalis)**: Aplikasi berjalan murni di terminal menggunakan Python 3.11+. Satu-satunya dependensi pihak ketiga di lingkungan produksi adalah `rich` dan `pytest`. Tidak ada framework atau GUI.
- [ ] **C2 (Zero External State)**: Tidak ada dependensi ke DBMS (MySQL, SQLite, PostgreSQL), tidak ada HTTP/socket network call, dan tidak ada akses internet. Seluruh state disimpan dalam berkas lokal JSON dan CSV.
- [ ] **C3 (Merge Sort Mandiri)**: Seluruh pemeringkatan di jalur produksi dieksekusi menggunakan fungsi `merge_sort()` buatan sendiri di `domain/sorter.py`. Fungsi `sorted()` hanya digunakan untuk oracle pengujian dan benchmark.
- [ ] **C4 (Struktur Data Wajib UAS)**:
  - `list`: Menampung koleksi siswa dan baris data.
  - `nested dict`: Menyimpan relasi nilai rapor `grades[semester][subject_code]`.
  - `set`: Menghitung selisih siswa eligible pada simulasi (`new_eligible = sim - base`).
  - `tuple`: Kunci urut leksikografis deterministik `SortKey` dan koleksi immutable pada model domain.
  - `Counter`: Menghitung agregat distribusi kelas dan akreditasi pada ringkasan statistik.
  - `binary search`: Pencarian cepat nama siswa pada list hasil ranking terurut.
  - `string manipulation`: Normalisasi spasi berlebih, format Title Case, dan parsing header CSV.
- [ ] **C5 (Penyimpanan Atomik & Backup)**: Penulisan file JSON selalu melalui skema `.tmp` → `fsync` → `.bak` → `os.replace`.
- [ ] **C6 (Konfigurasi Dinamis)**: Seluruh angka bisnis (persentase kuota 40/25/5%, bonus 5%, bobot prestasi, cap 2.00, batas 5 sertifikat) dibaca dari `config.json` dan tidak di-hardcode.
- [ ] **C7 (Data Fiktif)**: Seluruh data siswa yang disertakan dalam repositori adalah data fiktif hasil generasi algoritmik.
- [ ] **C8 (Keterbacaan & Pemahaman Tim)**: Kode terstruktur bersih dalam 4 lapisan terpisah, dilengkapi type hints lengkap dan docstring jelas sehingga setiap anggota tim mampu mempresentasikan seluruh alur kerja sistem.

---
*Dokumen Rencana Tugas Implementasi ini siap digunakan oleh Tim Pengembang Eligo.*
