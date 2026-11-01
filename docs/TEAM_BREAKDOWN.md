# Pembagian Tugas Tim Eligo (40-30-30)

**Dokumen ini menjelaskan detail pembagian tanggung jawab setiap anggota tim untuk menghindari merge conflict.**

**CATATAN:** Estimasi waktu di dokumen ini untuk **Build from Scratch**. Jika menggunakan **Copy & Understand** approach, waktu bisa dikurangi 50%. Lihat **[REBUILD_STRATEGY.md](REBUILD_STRATEGY.md)** untuk detail.

---

## Ringkasan Pembagian

| Anggota | Bobot | Area Utama | Summary |
|---------|-------|------------|---------|
| **Rafliza** | 40% | Presentation + Infrastructure | Tampilan Rich dan JSON aman |
| **Fadli** | 30% | Application Services + CSV | Impor CSV dan service sekolah/siswa/config |
| **Ghaida** | 30% | Domain Core + Algorithms | Perhitungan SNBP, merge sort, status eligible |

---

## Detail Tanggung Jawab

### **Rafliza — 40% (Presentation + Infrastructure)**

#### File yang Dikerjakan:

```
eligo/presentation/cli/
├── main.py                  ← Orchestrasi menu utama
├── formatter.py             ← Rich Console formatter
├── menu_school.py           ← Menu manajemen sekolah
├── menu_student.py          ← Menu manajemen siswa
├── menu_import.py           ← Menu impor CSV
├── menu_ranking.py          ← Menu tampilan ranking (tanpa logic E)
└── menu_reset.py            ← Menu reset data

eligo/infrastructure/
├── atomic_writer.py         ← Atomic JSON write dengan .bak
├── school_repo.py           ← Repository sekolah
├── student_repo.py          ← Repository siswa
└── config_repo.py           ← Repository config

eligo/domain/
└── repositories.py          ← Interface repository (abstract)

Root:
├── main.py                  ← Entry point aplikasi
└── data/
    ├── *.json               ← Data files
    └── *.bak                ← Backup files
```

#### Tanggung Jawab:

1. **Presentation Layer (CLI):**
   - Semua tampilan Rich Console
   - Format tabel, panel, progress bar
   - Semua menu interaktif
   - Keyboard handling (Ctrl+C, navigation)
   - Error messages & confirmations
   - Pagination display

2. **Infrastructure (Persistence):**
   - Atomic file write (`.tmp` → `.bak` → `.json`)
   - Repository pattern implementation
   - CRUD operations untuk semua entitas
   - Data persistence & recovery

3. **Entry Point:**
   - Orchestrasi menu utama di `main.py`
   - Global exception handling
   - Application initialization

#### Boleh Edit Tanpa Koordinasi:
- Semua file di `presentation/cli/`
- Semua file di `infrastructure/*_repo.py`
- `atomic_writer.py`
- `domain/repositories.py` (interfaces)
- `main.py` (root)
- `data/*.json` & `data/*.bak`

#### Perlu Koordinasi:
- File di `application/` (jika perlu integrasi)
- Test files untuk integration testing

---

### **Fadli — 30% (Application Services + CSV Import)**

#### File yang Dikerjakan:

```
eligo/application/
├── import_service.py        ← Service impor CSV (pratinjau, commit)
├── school_service.py        ← Business logic sekolah
├── student_service.py       ← Business logic siswa
└── config_service.py        ← Service config & aturan

eligo/infrastructure/
└── csv_parser.py            ← Parse CSV, error massal, template
```

#### Tanggung Jawab:

1. **CSV Import (Heavy 30%):**
   - Parse CSV (koma & semicolon separator)
   - Handle UTF-8 BOM
   - Collect-all error strategy (tampilkan semua error sekaligus)
   - Validasi format & data
   - Handle duplicate (Skip, Overwrite, Abort)
   - Preview data sebelum commit
   - Generate template CSV per jurusan

2. **Application Services:**
   - Business logic untuk manajemen sekolah
   - Business logic untuk manajemen siswa
   - Business logic untuk config & aturan
   - Orchestration layer antara presentation & domain
   - Validation & error handling di app level

#### Boleh Edit Tanpa Koordinasi:
- Semua file di `application/` (4 services)
- `infrastructure/csv_parser.py`
- Test files untuk services & parser

#### Perlu Koordinasi:
- Jika perlu ubah interface yang dipakai Rafliza (presentation)
- Jika perlu ubah contract domain yang dipakai Ghaida
- Integration test dengan layers lain

---

### **Ghaida — 30% (Domain Core + Algorithms)**

#### File yang Dikerjakan:

```
eligo/domain/
├── models.py                ← Domain entities (School, Student, dll)
├── exceptions.py            ← Domain-specific exceptions
├── calculator.py            ← Kalkulasi nilai rapor (Decimal)
├── quota.py                 ← Aturan kuota akreditasi & bonus e-Rapor
├── sorter.py                ← Merge Sort algorithm (mandiri, O(n log n))
├── searcher.py              ← Pencarian siswa
├── validator.py             ← Validasi bisnis domain
└── normalizer.py            ← Normalisasi data domain

eligo/application/
└── ranking_service.py       ← Pipeline pemeringkatan & tie-breaking
```

#### Tanggung Jawab:

1. **Domain Models:**
   - Entity classes (School, Student, Grade, dll)
   - Value objects
   - Domain exceptions
   - Business invariants

2. **Business Logic (Core SNBP):**
   - Kalkulasi nilai rapor dengan `Decimal` (no float!)
   - Aturan kuota: Akreditasi A (40%), B (25%), C (5%)
   - Bonus e-Rapor (+5%)
   - Pembulatan Round Half Up

3. **Algorithms:**
   - Merge Sort mandiri (tanpa `sorted()`)
   - Stable sort O(n log n)
   - Tie-breaking multi-level:
     - Total score → S5 → S4 → S3 → S2 → S1 → Nama → ID
   - Pencarian & filtering

4. **Ranking Logic:**
   - Status eligible (Hijau/Kuning/Abu-abu)
   - Eligible: dalam kuota
   - Cadangan: luar kuota tapi ikut TKA
   - Non-TKA: tidak ikut TKA
   - Ranking service orchestration

#### Boleh Edit Tanpa Koordinasi:
- Semua file di `domain/` (8 files)
- `application/ranking_service.py`
- Test files untuk domain & ranking

#### Perlu Koordinasi:
- Jika perlu ubah interface repository (dipakai Rafliza)
- Jika perlu ubah contract service (dipakai Fadli)
- Integration test dengan layers lain

---

## Aturan Koordinasi

### File Shared (Perlu Diskusi Dulu):

1. **Test Fixtures** (`tests/conftest.py`):
   - Kasih tau di grup sebelum ubah
   - Buat PR kecil khusus untuk fixtures

2. **Configuration** (`pyproject.toml`, `requirements*.txt`):
   - Koordinasi sebelum tambah dependency
   - Test bahwa tidak break existing code

3. **Documentation** (`README.md`, `docs/*.md`):
   - Boleh parallel edit (jarang conflict)
   - Review section masing-masing

4. **Integration Points:**
   - Interface repository: Ghaida (define) ↔ Rafliza (implement)
   - Service contracts: Fadli (define) ↔ Rafliza (consume)
   - Domain models: Ghaida (define) ↔ Fadli (use)

### Strategi Menghindari Conflict:

```
(Standup):
  "Hari ini saya kerja di: eligo/presentation/cli/menu_school.py"
  "Butuh: school_service dari Fadli (sudah ready)"
  "Blocker: Tidak ada"

(Check-in):
  "Progress 50%, sudah bisa list schools"
  "Nanti PR untuk review"

(Commit):
  git commit -m "feat(presentation): add school list menu"
  git push origin feature/241101-school-menu-rafliza
  [Buat PR]

(Review):
  Review PR dari Fadli & Ghaida
```

---

## Branch Naming Convention

Format: `tipe/YYMMDD-deskripsi-nama`

### Rafliza:
```bash
feature/241101-menu-school-rafliza
feature/241102-formatter-rich-rafliza
feature/241103-atomic-writer-rafliza
bugfix/241104-menu-navigation-rafliza
refactor/241105-repository-pattern-rafliza
```

### Fadli:
```bash
feature/241101-csv-parser-fadli
feature/241102-import-service-fadli
feature/241103-school-service-fadli
bugfix/241104-csv-validation-fadli
refactor/241105-service-layer-fadli
```

### Ghaida:
```bash
feature/241101-domain-models-ghaida
feature/241102-calculator-ghaida
feature/241103-merge-sort-ghaida
feature/241104-ranking-logic-ghaida
bugfix/241105-tie-breaking-ghaida
refactor/241106-domain-refactor-ghaida
```

---

## Integration Map

```
┌─────────────────────────────────────────────────────┐
│                                                      │
│                    main.py (Root)                    │
│                   [Rafliza: Entry]                   │
│                                                      │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          Presentation Layer (CLI Menus)             │
│                  [Rafliza: 40%]                     │
│   menu_school → menu_student → menu_import → ...    │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│         Application Layer (Services)                │
│                  [Fadli: 30%]                       │
│   school_service ← import_service → student_service │
└─────────────────┬────────────────────┬──────────────┘
                  │                    │
                  ▼                    ▼
┌─────────────────────────┐  ┌───────────────────────┐
│    Domain Layer         │  │  Ranking Service      │
│   [Ghaida: 30%]         │  │  [Ghaida: 30%]        │
│  models → calculator    │  │  sorter → quota       │
│  validator → normalizer │  │  tie-breaking logic   │
└─────────┬───────────────┘  └───────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│     Infrastructure Layer (Persistence)              │
│              [Rafliza: 40%]                         │
│  school_repo ← atomic_writer → student_repo         │
└─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│                 Data Files                          │
│              [Rafliza: 40%]                         │
│          data/*.json & data/*.bak                   │
└─────────────────────────────────────────────────────┘
```

---

## Daily Checklist per Anggota

### Rafliza (Presentation + Infrastructure):
```
□ Pull dari dev
□ Cek apakah ada update di domain/repositories.py (dari Ghaida)
□ Cek apakah ada update di application services (dari Fadli)
□ Mulai kerja di presentation/cli atau infrastructure
□ Test integrasi dengan services
□ Commit progress
□ Push branch
□ Buat PR jika fitur selesai
□ Review PR dari Fadli & Ghaida
```

### Fadli (Application Services + CSV):
```
□ Pull dari dev
□ Cek apakah ada update di domain models (dari Ghaida)
□ Cek apakah ada update di repositories (dari Rafliza)
□ Mulai kerja di application atau csv_parser
□ Test business logic
□ Commit progress
□ Push branch
□ Buat PR jika service selesai
□ Review PR dari Rafliza & Ghaida
```

### Ghaida (Domain Core + Algorithms):
```
□ Pull dari dev
□ Kerja di domain layer (pure logic, no I/O)
□ Implement algorithms & business rules
□ Unit test semua domain logic
□ Commit progress
□ Push branch
□ Buat PR jika domain feature selesai
□ Review PR dari Rafliza & Fadli
```

---

## Success Metrics

```
 Zero merge conflicts
 Semua anggota sukses push & PR minimal 1x
 Integration test passing
 Code review < 1 hari
```

```
 Max 1-2 minor conflicts per week
 PR review time < 1 hari
 All tests passing
 Coverage > 80% per layer
```

---

## Komunikasi

### Format Daily Standup (15 menit):

**Rafliza:**
- Kemarin: Selesai menu_school.py
- Hari ini: Kerja atomic_writer.py & school_repo.py
- Blocker: Butuh interface Repository dari Ghaida (sudah ada)

**Fadli:**
- Kemarin: 80% csv_parser.py
- Hari ini: Selesaikan csv_parser & mulai import_service
- Blocker: Butuh domain models dari Ghaida (work in progress)

**Ghaida:**
- Kemarin: Selesai models.py & calculator.py
- Hari ini: Implement sorter.py (merge sort)
- Blocker: Tidak ada

---

## Tips Kolaborasi

1. **Communicate Early:**
   - Kasih tau sebelum ubah file shared
   - Diskusi interface sebelum implement

2. **Small PRs:**
   - 1 PR = 1 feature kecil
   - Max 5-10 files per PR
   - Merge frequent

3. **Test Integration:**
   - Test dengan mock dulu
   - Integration test setelah merge

4. **Review Promptly:**
   - Review PR dalam max 1 hari
   - Constructive feedback
   - Approve jika no blocker

5. **Sync Daily:**
   - Pull dari dev
   - Merge dev ke branch sebelum PR

---

**Dengan pembagian ini, tim bisa kerja parallel dengan minimal conflict!**

Last Updated: 2026-11-01
