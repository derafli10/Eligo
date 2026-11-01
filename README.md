# Sistem Pemeringkatan Siswa Eligible SNBP (Eligo)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: Mypy](https://img.shields.io/badge/type%20checked-mypy%20strict-brightgreen.svg)](https://mypy-lang.org/)
[![Testing: Pytest](https://img.shields.io/badge/tests-189%20passed-success.svg)](https://pytest.org/)
[![License: Academic](https://img.shields.io/badge/license-Academic%20Project-lightgrey.svg)]()

> **Aplikasi Terminal Interaktif Resmi untuk Penentuan Kuota dan Pemeringkatan Siswa Eligible Seleksi Nasional Berdasarkan Prestasi (SNBP)** sesuai regulasi resmi Kemendikbudristek RI.

---

## Tim Pengembang & Pembagian Peran (40-30-30)

Proyek ini dibangun secara kolaboratif dengan pembagian tanggung jawab yang jelas:

### **Rafliza — 40% (Presentation + Infrastructure)**

| Area | Tanggung Jawab |
|---|---|
| **Presentation Layer** | Semua menu CLI (`menu_school`, `menu_student`, `menu_import`, `menu_ranking`, `menu_reset`), `formatter.py` (Rich Console), `main.py` dalam `presentation/cli/` |
| **Infrastructure** | Atomic JSON writer (`atomic_writer.py`), semua repositories (`school_repo`, `student_repo`, `config_repo`), domain repository interfaces |
| **Data** | Manajemen file `data/*.json` dan backup `.bak` |
| **Entry Point** | Orchestrasi aplikasi di `main.py` root |

**Summary:** Tampilan Rich dan JSON aman.

### **Fadli — 30% (Application Services + CSV Import)**

| Area | Tanggung Jawab |
|---|---|
| **Application Services** | Business logic services (`import_service`, `school_service`, `student_service`, `config_service`) |
| **CSV Infrastructure** | Parser CSV dengan error collection massal (`csv_parser.py`), pratinjau data, handle duplikat, template generator |

**Summary:** Impor CSV dan service sekolah/siswa/config.

### **Ghaida — 30% (Domain Core + Algorithms)**

| Area | Tanggung Jawab |
|---|---|
| **Domain Layer** | Semua domain logic (`models`, `exceptions`, `calculator`, `quota`, `sorter`, `searcher`, `validator`, `normalizer`) |
| **Ranking Logic** | Service pemeringkatan (`ranking_service`), algoritma Merge Sort, tie-breaking rules, status eligible |

**Summary:** Perhitungan SNBP, merge sort, status eligible.

---

## Fitur Utama Sistem Eligo

1. **Profil Sekolah & Penentuan Kuota Otomatis**
   - Mendukung jenjang SMA, MA, dan SMK.
   - Perhitungan kuota otomatis berdasarkan Akreditasi: **A (40%)**, **B (25%)**, **C (5%)**.
   - Bonus aktivasi e-Rapor resmi Kemendikbudristek (+5%).
   - Pembulatan matematis baku *Round Half Up* (contoh: 4,5 dibulatkan ke atas menjadi 5 kursi).

2. **Algoritma Pemeringkatan Mandiri (Merge Sort Tanpa Library)**
   - Menggunakan algoritma **Merge Sort stabil O(n log n)** yang dirakit sendiri tanpa fungsi bawaan `sorted()` di lapisan domain bisnis (memenuhi syarat wajib C3).
   - Aturan pemecah seri multi-tingkat (*Multi-Level Tie Breaking*):
     $$\text{Skor Akhir Total} \rightarrow \text{Nilai S5} \rightarrow \text{Nilai S4} \rightarrow \text{Nilai S3} \rightarrow \text{Nilai S2} \rightarrow \text{Nilai S1} \rightarrow \text{Abjad Nama} \rightarrow \text{ID Siswa}$$
   - Status kelayakan tiga warna:
     - **HIJAU (Eligible)**: Siswa masuk dalam kuota resmi sekolah.
     - **KUNING (Cadangan)**: Siswa ikut TKA namun berada di luar kuota (posisi cadangan jika ada siswa eligible yang mundur).
     - **ABU-ABU (Non-TKA)**: Siswa yang tidak mengikuti TKA (otomatis gugur dari kuota SNBP).

3. **Impor Nilai CSV Pintar (Collect-All Error Strategy)**
   - Mendukung pemisah koma (`,`) dan titik koma (`;`).
   - Mendukung berkas dengan *UTF-8 Byte Order Mark* (BOM) hasil ekspor Excel Windows.
   - Menampilkan seluruh kesalahan validasi baris sekaligus (tidak berhenti di error pertama).
   - Penanganan siswa duplikat: pilihan Lewati (*Skip*), Timpa (*Overwrite*), atau Batalkan (*Abort*).

4. **Ketahanan Data & Pemulihan Bencana Otomatis (Self-Healing Storage)**
   - Penulisan berkas JSON secara atomik (`.tmp` $\rightarrow$ `.bak` $\rightarrow$ `.json`).
   - Jika berkas database utama rusak atau terpotong (*truncated power failure*), sistem secara transparan memulihkan data dari berkas cadangan `.bak`.

5. **Reset Data Permanen Terproteksi**
   - Fitur penghapusan bersih seluruh data operasional sekolah dan siswa dengan konfirmasi ganda (*double confirmation*) untuk mencegah ketidaksengajaan.

---

## Arsitektur Sistem (Clean Architecture)

Sistem Eligo mengadopsi prinsip arsitektur bersih (*Clean Architecture*) dengan pemisahan dependensi satu arah ke dalam:

```
+-------------------------------------------------------------------+
|               LAPISAN PRESENTASI (Presentation Layer)             |
|   Rich Console CLI, Tabel Berwarna, Paginasi, Menu Interaktif     |
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                 LAPISAN APLIKASI (Application Layer)              |
|       Ranking Pipeline, Import Services, School & Student |
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                  LAPISAN DOMAIN (Pure Domain Layer)               |
|   Aturan Nilai, Kuota, Tie-Break, MergeSort Mandiri, Model Siswa  |
|             (DILARANG I/O, DILARANG IMPORT LIBRARY RICH)          |
+---------------------------------+---------------------------------+
                                  ^
                                  |
+---------------------------------+---------------------------------+
|               LAPISAN INFRASTRUKTUR (Infrastructure Layer)        |
|   Atomic Writer, Json Repositories (.bak Recovery), CSV Parser    |
+-------------------------------------------------------------------+
```

---

## Struktur Proyek

Proyek mengikuti **Clean Architecture** dengan pemisahan layer yang jelas:

```
eligo/
├── presentation/cli/      # ️ UI Layer (Rafliza 40%)
│   └── menu_*.py          # Rich Console, formatters, menus
│
├── application/           #  Service Layer (Fadli 30% + Ghaida 30%)
│   ├── *_service.py       # Business orchestration
│   └── ranking_service.py # Ranking logic (Ghaida)
│
├── domain/                #  Core Logic (Ghaida 30%)
│   ├── models.py          # Domain entities
│   ├── calculator.py      # Kalkulasi SNBP
│   ├── sorter.py          # Merge Sort mandiri
│   └── quota.py           # Aturan kuota
│
└── infrastructure/        #  I/O Layer (Rafliza 40% + Fadli 30%)
    ├── *_repo.py          # Repository pattern (Rafliza)
    ├── atomic_writer.py   # JSON atomik (Rafliza)
    └── csv_parser.py      # CSV parser (Fadli)
```

**Detail lengkap:** [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---

## Strategi Rebuild (WAJIB BACA!)

**Rekomendasi: Copy & Understand Approach (2 Minggu)**

Jika tim akan melakukan rebuild, gunakan strategi **Copy & Understand** yang 50% lebih cepat daripada build from scratch:

- **Waktu:** 2 minggu (vs 4 minggu build from scratch)
- **Effort:** 22-28 jam per orang (vs 50-64 jam)
- **Risk:** Low (code sudah proven)
- **Learning:** High (read working code)

**Detail lengkap:** [docs/REBUILD_STRATEGY.md](docs/REBUILD_STRATEGY.md)

---

## Workflow Git untuk Tim (WAJIB BACA!)

Untuk mencegah merge conflict dan memastikan kolaborasi berjalan lancar:

 **Dokumentasi Lengkap:**
- **[Git Workflow Guide](docs/GIT_WORKFLOW.md)** - Panduan lengkap dari setup hingga merge
- **[Team Coordination](docs/TEAM_COORDINATION.md)** - Strategi koordinasi tim
- **[Quick Reference](docs/GIT_QUICK_REFERENCE.md)** - Cheat sheet command Git

️ **Git Helper Script:**
```bash
# Mulai fitur baru
bash scripts/git-helper.sh start-work

# Sync dengan dev setiap pagi
bash scripts/git-helper.sh daily-sync

# Quick commit
bash scripts/git-helper.sh quick-commit

# Lihat semua command
bash scripts/git-helper.sh help
```

 **Workflow Singkat:**
```bash
# 1. PAGI - Sync dengan dev
git checkout dev && git pull origin dev

# 2. Buat branch baru untuk fitur
git checkout -b feature/YYMMDD-nama-fitur

# 3. KERJA - Commit sering
git add . && git commit -m "feat: deskripsi"

# 4. Push progress
git push origin feature/YYMMDD-nama-fitur

# 5. Buat Pull Request di GitHub
# 6. Merge setelah review
```

---

## Panduan Instalasi & Menjalankan Aplikasi

### 1. Prasyarat Sistem
- Python versi **3.11** atau yang lebih baru (mendukung Python 3.11, 3.12, 3.13, 3.14).
- Sistem Operasi: Windows 10/11, Linux, atau macOS.

### 2. Kloning / Unduh Repositori
Buka terminal (PowerShell pada Windows atau Terminal pada Linux/Mac):
```bash
cd c:/Users/ADVAN/Desktop/Eligo
```

### 3. Menyiapkan Lingkungan Virtual (Virtual Environment)
```bash
# Membuat virtual environment
py -3 -m venv .venv

# Mengaktifkan virtual environment
# Pada Windows PowerShell:
.venv\Scripts\Activate.ps1
# Pada Linux / macOS:
source .venv/bin/activate
```

### 4. Memasang Dependensi
```bash
# Dependensi utama aplikasi
pip install -r requirements.txt

# Dependensi pengujian dan audit kode (opsional)
pip install -r requirements-dev.txt
```

### 5. Menjalankan Aplikasi Eligo
```bash
py -3 main.py
```

---

## Panduan Menjalankan Pengujian Otomatis

Proyek ini dilengkapi dengan rangkaian pengujian unit, integrasi, pemulihan bencana, property-based, dan benchmark performa yang sangat lengkap:

```bash
# 1. Menjalankan seluruh pengujian otomatis (189+ test cases)
py -3 -m pytest -v

# 2. Menjalankan audit kepatuhan gaya kode dan linter
py -3 -m ruff check .

# 3. Menjalankan audit tipe data statis strict
py -3 -m mypy eligo generator
```

---

## Contoh Format Berkas CSV Impor Siswa

Sistem secara otomatis dapat membuat template berkas di folder `data/import/<JURUSAN>_template.csv`. Contoh format data untuk jurusan **MIPA** (4 mapel: Matematika, Bahasa Indonesia, Bahasa Inggris, Biologi selama 5 semester):

```csv
nama,kelas,tka,sem1_mtk,sem1_bin,sem1_ing,sem1_bio,sem2_mtk,sem2_bin,sem2_ing,sem2_bio,sem3_mtk,sem3_bin,sem3_ing,sem3_bio,sem4_mtk,sem4_bin,sem4_ing,sem4_bio,sem5_mtk,sem5_bin,sem5_ing,sem5_bio,prestasi
Ahmad Fauzi,XII MIPA 1,IKUT,85,88,86,87,86,89,87,88,87,90,88,89,88,91,89,90,90,92,90,91,Juara 1 OSN Matematika (NASIONAL)
Budi Santoso,XII MIPA 2,IKUT,80,82,81,83,82,84,83,85,83,85,84,86,85,87,86,88,86,88,87,89,
Citra Lestari,XII MIPA 1,TIDAK,92,90,91,93,93,91,92,94,94,92,93,95,95,93,94,96,96,94,95,97,
```

---

## Kepatuhan Standar Batasan Keras Rekayasa (C1–C8)

| Kode | Nama Batasan | Status Kepatuhan |
|:---:|---|:---:|
| **C1** | Isolasi Domain (Bebas I/O & Bebas Pustaka `rich`) |  **100% Patuh** (Divalidasi oleh linter aturan TID251) |
| **C2** | Versi Bahasa Python Minimal 3.11 |  **100% Patuh** (Berjalan optimal pada Python 3.11–3.14) |
| **C3** | Algoritma Pengurutan Merge Sort Mandiri |  **100% Patuh** (Diimplementasikan di `domain/sorter.py`) |
| **C4** | Struktur Data Baku Python (List, Tuple, Dict, Set) |  **100% Patuh** (Sesuai panduan standar perkuliahan) |
| **C5** | Format Penyimpanan Terstruktur JSON & CSV Atomik |  **100% Patuh** (Didukung mekanisme pemulihan `.bak`) |
| **C6** | Presisi Aritmatika Desimal Finansial (`Decimal`) |  **100% Patuh** (Bebas dari rounding error *floating-point*) |
| **C7** | Generator Dataset Realistis Terkontrol Seed |  **100% Patuh** (Keterulangan 100% deterministik seed 42) |
| **C8** | Dokumentasi Rinci & Reproduksibilitas Pengujian |  **100% Patuh** (Dokumentasi lengkap dalam Bahasa Indonesia) |
