# Pembagian Tugas Tim - Menghindari Merge Conflict

**REKOMENDASI:** Jika akan melakukan rebuild, gunakan **[Copy & Understand approach](REBUILD_STRATEGY.md)** yang 50% lebih cepat (2 minggu vs 4 minggu)!

---

## Strategi Pembagian

Untuk menghindari merge conflict, setiap anggota tim bekerja di **area yang berbeda**.

---

## Strategi Pembagian Tim (40-30-30)

Pembagian berdasarkan kompleksitas dan bobot kerja yang seimbang.

### **Rafliza — 40% (Presentation + Infrastructure)**

```
┌──────────────────────────────────────────────────────┐
│  ️ PRESENTATION LAYER (CLI)                        │
│   eligo/presentation/cli/                         │
│      ├── main.py                  (orkestrasi)      │
│      ├── formatter.py             (Rich display)    │
│      ├── menu_school.py           (menu sekolah)    │
│      ├── menu_student.py          (menu siswa)      │
│      ├── menu_import.py           (menu impor)      │
│      ├── menu_ranking.py          (menu ranking)    │
│      └── menu_reset.py            (menu reset)      │
│                                                      │
│   INFRASTRUCTURE LAYER                            │
│   eligo/infrastructure/                           │
│      ├── atomic_writer.py         (write JSON safe) │
│      ├── school_repo.py           (repo sekolah)    │
│      ├── student_repo.py          (repo siswa)      │
│      └── config_repo.py           (repo config)     │
│                                                      │
│   DOMAIN CONTRACTS                                │
│      └── domain/repositories.py   (interfaces)      │
│                                                      │
│   DATA FILES                                      │
│      └── data/*.json & data/*.bak                   │
│                                                      │
│   ENTRY POINT                                     │
│      └── main.py                                    │
└─────────────────────────────────────────────────────┘

Tanggung Jawab: Semua tampilan Rich Console, JSON atomik,
repository pattern, dan orchestrasi menu utama.
```

### **Fadli — 30% (Application Services + CSV Import)**

```
┌─────────────────────────────────────────────────────┐
│   APPLICATION LAYER (Services)                    │
│   eligo/application/                              │
│      ├── import_service.py        (impor CSV logic) │
│      ├── school_service.py        (service sekolah) │
│      ├── student_service.py       (service siswa)   │
│      └── config_service.py        (service config)  │
│                                                      │
│   INFRASTRUCTURE (CSV Parser)                     │
│   eligo/infrastructure/                           │
│      └── csv_parser.py            (parse CSV, err)  │
└─────────────────────────────────────────────────────┘

Tanggung Jawab: Parsing CSV dengan validasi error massal,
pratinjau data, handle duplikat, business services untuk
sekolah/siswa/config.
```

### **Ghaida — 30% (Domain Core + Algorithms)**

```
┌─────────────────────────────────────────────────────┐
│   DOMAIN LAYER (Business Logic)                   │
│   eligo/domain/                                   │
│      ├── models.py                (entities)        │
│      ├── exceptions.py            (domain errors)   │
│      ├── calculator.py            (kalkulasi nilai) │
│      ├── quota.py                 (aturan kuota)    │
│      ├── sorter.py                (merge sort)      │
│      ├── searcher.py              (pencarian)       │
│      ├── validator.py             (validasi bisnis) │
│      └── normalizer.py            (normalisasi)     │
│                                                      │
│   APPLICATION (Ranking Logic)                     │
│   eligo/application/                              │
│      └── ranking_service.py       (pemeringkatan)   │
└─────────────────────────────────────────────────────┘

Tanggung Jawab: Perhitungan SNBP, algoritma Merge Sort,
status eligible, tie-breaking rules, domain models,
dan business validation.
```

### Summary Satu Kalimat

- **Rafliza 40%:** Tampilan Rich dan JSON aman.
- **Fadli 30%:** Impor CSV dan service sekolah/siswa/config.
- **Ghaida 30%:** Perhitungan SNBP, merge sort, status eligible.

### Aturan:
 **Boleh edit** di area kamu tanpa kasih tau
 **Boleh edit test** untuk area kamu
 **Jangan edit** area orang lain tanpa koordinasi
 **Jangan edit** file shared tanpa diskusi dulu

---

### Core Features

**Rafliza: CLI & Repository Infrastructure**
```bash
Files:
├── eligo/presentation/cli/main.py
├── eligo/presentation/cli/formatter.py
├── eligo/presentation/cli/menu_*.py (semua menu)
├── eligo/infrastructure/atomic_writer.py
├── eligo/infrastructure/*_repo.py (semua repo)
├── domain/repositories.py (interface)
└── tests/presentation/ & tests/infrastructure/

Features:
- Rich Console display & formatting
- Semua menu interaktif
- Atomic JSON write
- Repository pattern implementation
```

**Fadli: Application Services & CSV Import**
```bash
Files:
├── eligo/infrastructure/csv_parser.py
├── eligo/application/import_service.py
├── eligo/application/school_service.py
├── eligo/application/student_service.py
├── eligo/application/config_service.py
└── tests/application/ & tests/csv_parser/

Features:
- Parse CSV dengan error massal
- Pratinjau & handle duplikat
- Business logic services
- Template generator
```

**Ghaida: Domain Logic & Ranking**
```bash
Files:
├── eligo/domain/models.py
├── eligo/domain/exceptions.py
├── eligo/domain/calculator.py
├── eligo/domain/quota.py
├── eligo/domain/sorter.py
├── eligo/domain/searcher.py
├── eligo/domain/validator.py
├── eligo/domain/normalizer.py
├── eligo/application/ranking_service.py
└── tests/domain/

Features:
- Domain models & exceptions
- Kalkulasi nilai & kuota
- Merge Sort algorithm
- Tie-breaking rules
- Status eligible logic
```

---


## Koordinasi File Shared

### File yang Sering Di-edit Banyak Orang:

**1. `main.py`**
```
Owner: Fadli
Aturan:
- Fadli koordinator untuk perubahan di file ini
- Orang lain mau edit? Tanya Fadli dulu
- Atau buat PR kecil ke Fadli's branch
```

**2. `requirements.txt` / `requirements-dev.txt`**
```
Aturan:
- Kasih tau di grup sebelum tambah dependency
- Buat PR terpisah khusus untuk dependency
- Test bahwa tidak break existing code
```

**3. `README.md` & docs/**
```
Owner: Bisa siapa saja
Aturan:
- Documentation update bisa parallel
- Jarang conflict karena beda section
- Jika conflict, easy to resolve
```

**4. `tests/conftest.py` atau shared fixtures**
```
Aturan:
- Koordinasi di grup dulu
- Buat PR kecil khusus untuk test fixtures
- Test bahwa tidak break existing tests
```

---

## Branch Naming Convention

```bash
# Format: tipe/YYMMDD-fitur-nama

# Rafliza:
feature/241101-school-crud-rafliza
feature/241103-csv-import-rafliza
bugfix/241105-repository-error-rafliza

# Ghaida:
feature/241101-student-model-ghaida
feature/241102-calculator-logic-ghaida
refactor/241104-sorter-optimization-ghaida

# Fadli:
feature/241101-menu-structure-fadli
feature/241103-rich-formatter-fadli
bugfix/241106-keyboard-interrupt-fadli
```

**Manfaat:**
- Jelas siapa yang punya branch
- Jelas kapan branch dibuat
- Jelas apa isi branch
- Mudah tracking di GitHub

---

## GitHub Project Board Setup

### Kolom:

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│     To Do    │  In Progress │    Review    │     Done     │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ - Setup repo │ - School CRUD│ - CSV parser │ - Git setup  │
│ - Design     │   (Rafliza)  │   (Ghaida)   │ - README     │
│ - Plan arch  │ - Calculator │              │              │
│              │   (Ghaida)   │              │              │
│              │ - Menu UI    │              │              │
│              │   (Fadli)    │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## Communication Channels

### Daily:
- **WhatsApp/Telegram Group**: Quick questions, status update
- **Standup (15 min)**: Sync

### Weekly:
- **Review (1 hour)**: Demo, retrospective, planning
- **GitHub Discussions**: Technical decisions, architecture

### Ad-hoc:
- **Discord/Meet**: Pair programming, conflict resolution
- **GitHub PR Comments**: Code review, suggestions

---

## Golden Rules Reminder

1. **Communicate Early**: Kasih tau sebelum edit file orang lain
2. **Commit Often**: Minimal 3x sehari
3. **Push Daily**: Jangan simpan progress di lokal saja
4. **Review Quickly**: Review PR dalam max 1 hari
5. **Sync Morning**: Pull dari dev setiap pagi
6. **Test Before PR**: Pastikan code jalan sebelum PR
7. **Small PRs**: 5-10 files per PR lebih baik dari 50 files

---

**Remember: Coordination > Code!** 

Better to spend 5 minutes coordinating than 2 hours resolving conflicts.

Last Updated: 2026-11-01
