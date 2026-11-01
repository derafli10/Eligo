# Struktur File Proyek Eligo

**Dokumen ini menjelaskan struktur folder dan file lengkap untuk proyek Eligo setelah setup awal.**

---

## Tree Structure Lengkap

```
Eligo/
│
├── .git/                           # Git repository (otomatis dibuat)
├── .github/                        # GitHub configuration
│   └── pull_request_template.md   # Template PR otomatis
│
├── .kiro/                          # Kiro IDE configuration
│   ├── steering/
│   │   ├── product.md             # Product requirements
│   │   ├── tech.md                # Tech stack rules
│   │   └── structure.md           # Architecture rules
│   └── hooks/                     # Kiro agent hooks (optional)
│
├── .venv/                          # Virtual environment (gitignored)
├── .mypy_cache/                    # Mypy cache (gitignored)
├── .pytest_cache/                  # Pytest cache (gitignored)
├── .ruff_cache/                    # Ruff cache (gitignored)
│
├── data/                           # Data storage
│   ├── schools.json               # Database sekolah
│   ├── schools.json.bak           # Backup sekolah
│   ├── students.json              # Database siswa
│   ├── students.json.bak          # Backup siswa
│   ├── config.json                # Konfigurasi sistem
│   ├── config.json.bak            # Backup config
│   └── import/                    # Folder untuk CSV import
│       ├── MIPA_template.csv      # Template CSV jurusan MIPA
│       ├── IPS_template.csv       # Template CSV jurusan IPS
│       └── README.md              # Panduan format CSV
│
├── docs/                           #  Dokumentasi (8 files)
│   ├── README_DOCS.md             # Index dokumentasi
│   ├── QUICK_START_GIT.md         # Quick start guide
│   ├── GIT_WORKFLOW.md            # Git workflow lengkap
│   ├── GIT_QUICK_REFERENCE.md     # Cheat sheet command
│   ├── TEAM_COORDINATION.md       # Koordinasi tim
│   ├── TASK_DIVISION.md           # Pembagian tugas strategi
│   ├── TEAM_BREAKDOWN.md          # Detail breakdown per anggota
│   ├── GITHUB_SETUP.md            # Setup repository GitHub
│   └── PROJECT_STRUCTURE.md       # Dokumen ini!
│
├── scripts/                        # Helper scripts
│   ├── git-helper.sh              # Git workflow automation
│   └── setup-git-local.sh         # Initial git setup
│
├── eligo/                          #  Main application package
│   │
│   ├── __init__.py                # Package init
│   │
│   ├── presentation/              # ️ PRESENTATION LAYER (Rafliza 40%)
│   │   ├── __init__.py
│   │   └── cli/
│   │       ├── __init__.py
│   │       ├── main.py            # Main menu orchestrator
│   │       ├── formatter.py       # Rich Console formatter
│   │       ├── menu_school.py     # Menu manajemen sekolah
│   │       ├── menu_student.py    # Menu manajemen siswa
│   │       ├── menu_import.py     # Menu impor CSV
│   │       ├── menu_ranking.py    # Menu tampilan ranking
│   │       └── menu_reset.py      # Menu reset data
│   │
│   ├── application/               #  APPLICATION LAYER
│   │   ├── __init__.py
│   │   ├── import_service.py      # (Fadli 30%) Service impor CSV
│   │   ├── school_service.py      # (Fadli 30%) Service sekolah
│   │   ├── student_service.py     # (Fadli 30%) Service siswa
│   │   ├── config_service.py      # (Fadli 30%) Service config
│   │   └── ranking_service.py     # (Ghaida 30%) Service ranking
│   │
│   ├── domain/                    #  DOMAIN LAYER (Ghaida 30%)
│   │   ├── __init__.py
│   │   ├── models.py              # Domain entities
│   │   ├── exceptions.py          # Domain exceptions
│   │   ├── repositories.py        # (Rafliza 40%) Repository interfaces
│   │   ├── calculator.py          # Kalkulasi nilai rapor
│   │   ├── quota.py               # Aturan kuota SNBP
│   │   ├── sorter.py              # Merge Sort algorithm
│   │   ├── searcher.py            # Pencarian siswa
│   │   ├── validator.py           # Validasi bisnis
│   │   └── normalizer.py          # Normalisasi data
│   │
│   └── infrastructure/            #  INFRASTRUCTURE LAYER
│       ├── __init__.py
│       ├── atomic_writer.py       # (Rafliza 40%) Atomic JSON write
│       ├── school_repo.py         # (Rafliza 40%) Repository sekolah
│       ├── student_repo.py        # (Rafliza 40%) Repository siswa
│       ├── config_repo.py         # (Rafliza 40%) Repository config
│       └── csv_parser.py          # (Fadli 30%) CSV parser
│
├── tests/                          #  Test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration & fixtures
│   │
│   ├── presentation/              # Tests untuk presentation layer
│   │   ├── __init__.py
│   │   ├── test_formatter.py
│   │   ├── test_menu_school.py
│   │   ├── test_menu_student.py
│   │   └── test_menu_ranking.py
│   │
│   ├── application/               # Tests untuk application layer
│   │   ├── __init__.py
│   │   ├── test_import_service.py
│   │   ├── test_school_service.py
│   │   ├── test_student_service.py
│   │   └── test_ranking_service.py
│   │
│   ├── domain/                    # Tests untuk domain layer
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_calculator.py
│   │   ├── test_quota.py
│   │   ├── test_sorter.py
│   │   ├── test_validator.py
│   │   └── test_normalizer.py
│   │
│   ├── infrastructure/            # Tests untuk infrastructure layer
│   │   ├── __init__.py
│   │   ├── test_atomic_writer.py
│   │   ├── test_repositories.py
│   │   └── test_csv_parser.py
│   │
│   └── integration/               # Integration tests
│       ├── __init__.py
│       ├── test_full_workflow.py
│       ├── test_import_flow.py
│       └── test_ranking_flow.py
│
├── .gitignore                      # Git ignore rules
├── main.py                         #  Application entry point (Rafliza 40%)
├── README.md                       # Project README
├── requirements.txt                # Runtime dependencies
├── requirements-dev.txt            # Development dependencies
├── pyproject.toml                  # Project configuration
└── pyrightconfig.json              # Pyright type checker config
```

---

## File Count Summary

```
Total Structure:
├── Root files:          8 files
├── Documentation:       9 files
├── Scripts:             2 files
├── Source code:        32 files (eligo/)
├── Test files:         20+ files (tests/)
└── Config/Data:        10+ files

Total: ~80+ files ketika proyek lengkap
```

---

## Breakdown per Layer

### 1 **Presentation Layer** (`eligo/presentation/cli/`)

**Owner: Rafliza (40%)**

```
presentation/cli/
├── main.py              # Menu orchestrator, keyboard handling
├── formatter.py         # Rich Console: Table, Panel, Progress, Colors
├── menu_school.py       # CRUD sekolah, setup kuota, bonus e-Rapor
├── menu_student.py      # CRUD siswa, edit nilai, manage TKA status
├── menu_import.py       # UI impor CSV, preview, konfirmasi
├── menu_ranking.py      # Display ranking, pagination, filter
└── menu_reset.py        # Reset data dengan konfirmasi ganda
```

**Karakteristik:**
-  Boleh import `rich`
-  Boleh panggil application services
-  Tidak boleh langsung akses domain
-  Tidak boleh langsung akses infrastructure

---

### 2 **Application Layer** (`eligo/application/`)

**Owner: Fadli (30%) + Ghaida (30% untuk ranking_service)**

```
application/
├── import_service.py     # (Fadli) Orchestrasi impor CSV
│                         # - Validasi preview
│                         # - Handle duplikat (Skip/Overwrite/Abort)
│                         # - Commit batch ke repository
│
├── school_service.py     # (Fadli) Business logic sekolah
│                         # - Create/Update/Delete sekolah
│                         # - Kalkulasi kuota
│                         # - Validasi data sekolah
│
├── student_service.py    # (Fadli) Business logic siswa
│                         # - CRUD siswa
│                         # - Validasi nilai rapor
│                         # - Update TKA status
│
├── config_service.py     # (Fadli) Service konfigurasi
│                         # - Load/save config
│                         # - Aturan SNBP
│                         # - Default values
│
└── ranking_service.py    # (Ghaida) Orchestrasi ranking
                          # - Pipeline pemeringkatan
                          # - Tie-breaking logic
                          # - Status eligible calculation
```

**Karakteristik:**
-  Boleh panggil domain logic
-  Boleh panggil repositories
-  Tidak boleh import `rich`
-  Tidak boleh langsung akses infrastructure detail

---

### 3 **Domain Layer** (`eligo/domain/`)

**Owner: Ghaida (30%)**

```
domain/
├── models.py             # Domain entities
│                         # - School (nama, npsn, akreditasi, e-rapor)
│                         # - Student (nama, nisn, kelas, nilai, tka)
│                         # - Grade (semester values)
│                         # - RankingResult (rank, score, status)
│
├── exceptions.py         # Domain-specific exceptions
│                         # - InvalidGradeError
│                         # - QuotaExceededError
│                         # - InvalidAccreditationError
│
├── repositories.py       # (Rafliza) Repository interfaces
│                         # - ISchoolRepository (abstract)
│                         # - IStudentRepository (abstract)
│                         # - IConfigRepository (abstract)
│
├── calculator.py         # Kalkulasi nilai rapor
│                         # - Hitung rata-rata per semester (Decimal)
│                         # - Hitung total score
│                         # - Round half up
│
├── quota.py              # Aturan kuota SNBP
│                         # - Akreditasi A: 40%
│                         # - Akreditasi B: 25%
│                         # - Akreditasi C: 5%
│                         # - Bonus e-Rapor: +5%
│
├── sorter.py             # Merge Sort algorithm (mandiri!)
│                         # - Stable sort O(n log n)
│                         # - Tanpa menggunakan sorted()
│                         # - Preserve order untuk equal items
│
├── searcher.py           # Pencarian & filtering
│                         # - Cari siswa by nama/nisn
│                         # - Filter by kelas/jurusan
│                         # - Filter by TKA status
│
├── validator.py          # Validasi bisnis domain
│                         # - Validasi nilai 0-100
│                         # - Validasi NISN format
│                         # - Validasi NPSN format
│
└── normalizer.py         # Normalisasi data
                          # - Normalize nama (Title Case)
                          # - Normalize NISN/NPSN
                          # - Trim whitespace
```

**Karakteristik (PENTING!):**
-  **TIDAK BOLEH** import `rich`
-  **TIDAK BOLEH** I/O (file read/write)
-  **TIDAK BOLEH** import `infrastructure`
-  Pure business logic
-  Type hints required
-  Docstrings required

---

### 4 **Infrastructure Layer** (`eligo/infrastructure/`)

**Owner: Rafliza (40%) + Fadli (30% untuk csv_parser)**

```
infrastructure/
├── atomic_writer.py      # (Rafliza) Atomic JSON write
│                         # - Write to .tmp
│                         # - Backup to .bak
│                         # - Rename to .json
│                         # - Auto recovery if .json corrupted
│
├── school_repo.py        # (Rafliza) Repository sekolah
│                         # - Implementasi ISchoolRepository
│                         # - CRUD with atomic write
│                         # - JSON persistence
│
├── student_repo.py       # (Rafliza) Repository siswa
│                         # - Implementasi IStudentRepository
│                         # - Batch operations
│                         # - JSON persistence
│
├── config_repo.py        # (Rafliza) Repository config
│                         # - Implementasi IConfigRepository
│                         # - Load/save config.json
│
└── csv_parser.py         # (Fadli) CSV parser
                          # - Parse CSV (koma & semicolon)
                          # - Handle UTF-8 BOM
                          # - Collect-all error strategy
                          # - Generate template per jurusan
```

**Karakteristik:**
-  Boleh I/O operations
-  Boleh akses file system
-  Implement domain interfaces
-  Tidak boleh import `rich`

---

## Data Files Structure

```
data/
├── schools.json              # Active database sekolah
├── schools.json.bak          # Backup sekolah (auto recovery)
├── students.json             # Active database siswa
├── students.json.bak         # Backup siswa
├── config.json               # System configuration
├── config.json.bak           # Backup config
│
└── import/                   # CSV import folder
    ├── MIPA_template.csv     # Template untuk jurusan MIPA
    ├── IPS_template.csv      # Template untuk jurusan IPS
    ├── BAHASA_template.csv   # Template untuk jurusan Bahasa
    └── README.md             # Panduan format CSV
```

### Format File JSON:

**schools.json:**
```json
{
  "schools": [
    {
      "id": "uuid-string",
      "nama": "SMA Negeri 1 Jakarta",
      "npsn": "12345678",
      "akreditasi": "A",
      "e_rapor": true,
      "jurusan": ["MIPA", "IPS"],
      "kuota": 40,
      "created_at": "2026-11-01T10:00:00",
      "updated_at": "2026-11-01T10:00:00"
    }
  ]
}
```

**students.json:**
```json
{
  "students": [
    {
      "id": "uuid-string",
      "school_id": "uuid-string",
      "nama": "Ahmad Fauzi",
      "nisn": "1234567890",
      "kelas": "XII MIPA 1",
      "jurusan": "MIPA",
      "tka": "IKUT",
      "nilai": {
        "mapel": ["Matematika", "B.Indonesia", "B.Inggris", "Biologi"],
        "semester": {
          "s1": ["85", "88", "86", "87"],
          "s2": ["86", "89", "87", "88"],
          "s3": ["87", "90", "88", "89"],
          "s4": ["88", "91", "89", "90"],
          "s5": ["90", "92", "90", "91"]
        }
      },
      "prestasi": "Juara 1 OSN Matematika (NASIONAL)",
      "created_at": "2026-11-01T10:00:00",
      "updated_at": "2026-11-01T10:00:00"
    }
  ]
}
```

**config.json:**
```json
{
  "version": "1.0.0",
  "aturan_kuota": {
    "A": 40,
    "B": 25,
    "C": 5,
    "bonus_erapor": 5
  },
  "jurusan_available": ["MIPA", "IPS", "BAHASA"],
  "mapel_per_jurusan": {
    "MIPA": ["Matematika", "B.Indonesia", "B.Inggris", "Biologi"],
    "IPS": ["Ekonomi", "B.Indonesia", "B.Inggris", "Geografi"],
    "BAHASA": ["B.Indonesia", "B.Inggris", "Sastra", "Antropologi"]
  },
  "semester_count": 5
}
```

---

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures
│   ├── @pytest.fixture: sample_school
│   ├── @pytest.fixture: sample_student
│   ├── @pytest.fixture: mock_repository
│   └── @pytest.fixture: temp_data_dir
│
├── presentation/
│   └── test_*.py           # Test CLI components (dengan mock)
│
├── application/
│   └── test_*.py           # Test services (dengan mock repo)
│
├── domain/
│   └── test_*.py           # Test pure logic (no mock needed)
│
├── infrastructure/
│   └── test_*.py           # Test I/O operations (dengan temp files)
│
└── integration/
    └── test_*.py           # Test full workflow end-to-end
```

---

## Configuration Files

### `pyproject.toml`
```toml
[project]
name = "eligo"
version = "1.0.0"
description = "Sistem Pemeringkatan Siswa Eligible SNBP"
requires-python = ">=3.11"
dependencies = [
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### `requirements.txt`
```
rich>=13.0.0
```

### `requirements-dev.txt`
```
pytest>=7.4.0
pytest-cov>=4.1.0
ruff>=0.1.0
mypy>=1.7.0
```

### `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environment
.venv/
venv/
ENV/
env/

# Testing & Linting
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Data files (temporary/import)
data/import/*.csv
!data/import/*_template.csv
!data/import/README.md
*.tmp
*.bak

# IDE
.vscode/
.idea/
.DS_Store
Thumbs.db

# Logs
*.log
```

---

## Entry Point: `main.py`

```python
#!/usr/bin/env python3
"""
Eligo - Sistem Pemeringkatan Siswa Eligible SNBP
Entry point aplikasi CLI.
"""

from eligo.presentation.cli.main import run_app

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print("\n\nAplikasi dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\n\nError fatal: {e}")
        raise
```

---

## Validation Checklist

Setelah setup, pastikan struktur sudah benar:

```bash
# 1. Check folder structure
ls -la

# Expected folders:
# eligo/
# tests/
# data/
# docs/
# scripts/
# .github/

# 2. Check Python packages
find eligo -name "__init__.py"

# Expected:
# eligo/__init__.py
# eligo/presentation/__init__.py
# eligo/presentation/cli/__init__.py
# eligo/application/__init__.py
# eligo/domain/__init__.py
# eligo/infrastructure/__init__.py

# 3. Check data folder
ls -la data/

# Expected:
# data/schools.json
# data/students.json
# data/config.json
# data/import/ (folder)

# 4. Check virtual environment
ls -la .venv/

# Expected:
# .venv/Scripts/ (Windows) atau .venv/bin/ (Linux/Mac)
# .venv/Lib/ (Windows) atau .venv/lib/ (Linux/Mac)

# 5. Run tests
pytest -v

# Expected:
# All tests pass
# Coverage report
```

---

## Quick Commands

```bash
# Setup awal
bash scripts/setup-git-local.sh

# Activate virtual environment
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run application
python main.py

# Run tests
pytest -v

# Run with coverage
pytest --cov=eligo --cov-report=html

# Lint code
ruff check .

# Type check
mypy eligo

# Format code
ruff format .
```

---

## References

- **Pembagian Tugas:** [TEAM_BREAKDOWN.md](TEAM_BREAKDOWN.md)
- **Git Workflow:** [GIT_WORKFLOW.md](GIT_WORKFLOW.md)
- **Quick Start:** [QUICK_START_GIT.md](QUICK_START_GIT.md)

---

**Struktur ini mengikuti Clean Architecture dengan separation of concerns yang jelas!** 

Last Updated: 2026-11-01
