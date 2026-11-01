# Quick Start - Rebuild dengan Copy & Understand

**Panduan cepat untuk rebuild proyek Eligo dalam 2 minggu dengan approach Copy & Understand**

---

## Kenapa Copy & Understand?

| Aspek | Build from Scratch | Copy & Understand |
|-------|-------------------|-------------------|
| Waktu | 4 minggu | **2 minggu** |
| Jam Total | 50-64 jam | **22-28 jam** |
| Risk | High | **Low** |
| Learning | Trial-error | **Best practices** |

**Penghematan: 50% lebih cepat!**

---

## Setup Awal (Day 1 - 2 jam)

### Step 1: Clone & Setup (30 menit)

```bash
# 1. Clone existing code
git clone https://github.com/USERNAME/Eligo.git
cd Eligo

# 2. Setup environment
python -m venv .venv
.venv\Scripts\activate              # Windows
# source .venv/bin/activate         # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Test bahwa code jalan
python main.py

# 5. Run tests
pytest -v
```

### Step 2: Explore Structure (30 menit)

```bash
# Lihat struktur
tree eligo -L 2

# Expected structure:
eligo/
├── presentation/cli/      # Rafliza (40%)
├── application/           # Fadli (30%) + Ghaida (30% ranking_service)
├── domain/                # Ghaida (30%)
└── infrastructure/        # Rafliza (40%) + Fadli (30% csv_parser)
```

### Step 3: Read Documentation (1 jam)

```bash
# Baca dalam urutan:
1. README.md                      # Overview proyek
2. docs/PROJECT_STRUCTURE.md      # Struktur detail
3. docs/TEAM_BREAKDOWN.md         # Pembagian tugas
4. docs/REBUILD_STRATEGY.md       # Strategi rebuild (dokumen ini!)
```

---

## Jadwal 2 Minggu

### Week 1: Understand & Learn

**Senin (Day 1) - 4-5 jam**

**Rafliza:**
- Setup & clone (30 menit)
- Read: `docs/PROJECT_STRUCTURE.md` (30 menit)
- Read: `eligo/presentation/cli/` overview (1 jam)
- Read: `eligo/infrastructure/` overview (1 jam)
- Explore: formatter.py, main.py (1 jam)

**Fadli:**
- Setup & clone (30 menit)
- Read: `docs/PROJECT_STRUCTURE.md` (30 menit)
- Read: `eligo/application/` overview (1 jam)
- Read: `eligo/infrastructure/csv_parser.py` (1.5 jam)
- Note: Questions untuk besok (30 menit)

**Ghaida:**
- Setup & clone (30 menit)
- Read: `docs/PROJECT_STRUCTURE.md` (30 menit)
- Read: `eligo/domain/` overview (2 jam)
- Read: models.py, exceptions.py (1.5 jam)
- Note: Questions untuk besok (30 menit)

---

**Rabu (Day 2) - 4-5 jam**

**Morning Standup (30 menit):**
- Share: Apa yang dipelajari Day 1
- Ask: Questions yang muncul
- Plan: Fokus Day 2

**Rafliza:**
- Deep dive: formatter.py (Rich Console) (1.5 jam)
- Deep dive: main.py orchestrator (1 jam)
- Deep dive: menu_school.py, menu_student.py (1.5 jam)
- Document: Flow diagram (30 menit)

**Fadli:**
- Deep dive: csv_parser.py (2 jam)
  - Separator detection
  - UTF-8 BOM handling
  - Error collection strategy
- Deep dive: import_service.py (1.5 jam)
- Document: Import flow diagram (30 menit)

**Ghaida:**
- Deep dive: calculator.py (2 jam)
  - Decimal usage
  - Round Half Up
- Deep dive: quota.py (1 jam)
  - Akreditasi rules
  - Bonus e-Rapor
- Deep dive: validator.py, normalizer.py (1.5 jam)
- Document: Domain logic notes (30 menit)

---

**Minggu (Day 3) - 4-5 jam**

**Rafliza:**
- Deep dive: atomic_writer.py (1.5 jam)
  - .tmp → .bak → .json flow
  - Recovery mechanism
- Deep dive: school_repo.py, student_repo.py (2 jam)
  - Repository pattern
  - CRUD operations
- Read: config_repo.py (30 menit)
- Document: Infrastructure notes (30 menit)

**Fadli:**
- Deep dive: school_service.py (1 jam)
- Deep dive: student_service.py (1.5 jam)
- Deep dive: config_service.py (1 jam)
- Run & understand: Integration tests (1 jam)

**Ghaida (CRITICAL DAY!):**
- **Deep dive: sorter.py - Merge Sort (3 jam)**
  - Algorithm walkthrough
  - Stable sort concept
  - Time complexity
  - Practice dengan contoh data
- Deep dive: searcher.py (1 jam)
- Document: Merge Sort explanation (1 jam)

**Code Reading Session (2 jam - After individual work):**
- Ghaida present: Merge Sort walkthrough
- Fadli present: CSV Parser error handling
- Rafliza present: Atomic write & recovery
- Q&A: Discuss integration points

**Progress Week 1:** 70% understanding complete

---

### Week 2: Customize & Test

**Senin (Day 4) - 4-5 jam**

**Morning Standup (30 menit):**
- Review: Week 1 understanding
- Plan: Customization needed
- Assign: Tasks untuk Week 2

**Rafliza:**
- Read: menu_import.py, menu_ranking.py, menu_reset.py (1.5 jam)
- Customize: UI text, colors, formatting (1.5 jam)
- Customize: Naming conventions (jika perlu) (1 jam)
- Document: Customization notes (30 menit)

**Fadli:**
- Customize: Validation rules (1 jam)
- Customize: Error messages (1 jam)
- Customize: CSV template format (1 jam)
- Test: CSV parser dengan data test (1 jam)

**Ghaida:**
- Deep dive: ranking_service.py (3 jam)
  - Tie-breaking implementation
  - Status eligible logic
  - Integration dengan sorter
- Customize: Ranking criteria (jika perlu) (1 jam)
- Document: Ranking flow (1 jam)

---

**Rabu (Day 5) - 4-5 jam**

**Morning Standup (30 menit):**
- Status: Customization progress
- Plan: Integration testing

**Rafliza:**
- Test: Full presentation flow (2 jam)
  - Setup sekolah
  - Manage siswa
  - Display ranking
- Fix: UI bugs (1 jam)
- Test: Error handling (1 jam)

**Fadli:**
- Test: Full import flow (2 jam)
  - CSV valid
  - CSV dengan errors
  - Duplicate handling
- Fix: Import bugs (1 jam)
- Document: Import scenarios (1 jam)

**Ghaida:**
- Test: Full ranking flow (2 jam)
  - Different scenarios
  - Tie-breaking cases
  - Status eligible calculation
- Fix: Domain bugs (1 jam)
- Optimize: Performance (jika perlu) (1 jam)

---

**Minggu (Day 6) - 4-5 jam**

**Integration Testing Bersama (4-5 jam):**

**Phase 1: Full Workflow Test (2 jam)**
- Setup: 1 sekolah SMA dengan akreditasi A
- Import: 50 siswa dari CSV
- Ranking: Generate ranking & check output
- Validate: Status eligible (Hijau/Kuning/Abu-abu)
- Export: Test report generation (jika ada)

**Phase 2: Edge Cases (1 jam)**
- Test: Sekolah dengan kuota 0
- Test: Semua siswa TIDAK ikut TKA
- Test: Tie-breaking dengan banyak siswa
- Test: CSV dengan semua error types

**Phase 3: Performance (30 menit)**
- Test: 1000 siswa ranking
- Validate: < 1 detik untuk ranking
- Check: Memory usage

**Phase 4: Bug Fixing (1 jam)**
- Fix: Issues yang ditemukan
- Re-test: Semua scenarios
- Validate: All tests passing

**Phase 5: Documentation (30 menit)**
- Update: README jika perlu
- Update: Comments di code
- Create: Release notes

**Final Check:**
-  All tests passing
-  Coverage > 80%
-  Performance acceptable
-  Documentation complete
-  **Ready for demo!**

**Progress Week 2:** 100% SELESAI!

---

## Understanding Checklist

### Rafliza - Presentation & Infrastructure

**Must Understand:**
-  Rich Console: Table, Panel, Progress bar
-  Menu orchestration & keyboard handling
-  Pagination implementation
-  Atomic write: .tmp → .bak → .json flow
-  Recovery dari .bak jika .json corrupt
-  Repository pattern & CRUD operations

**Can Explain:**
- Bagaimana Rich Table dibuat?
- Kapan atomic_writer dipanggil?
- Bagaimana recovery mechanism bekerja?
- Error handling di presentation layer?

---

### Fadli - Application & CSV

**Must Understand:**
-  CSV parser: Separator detection (`,` vs `;`)
-  UTF-8 BOM handling
-  Collect-all error strategy
-  Duplicate handling (Skip/Overwrite/Abort)
-  Service layer business logic
-  Validation flow

**Can Explain:**
- Bagaimana error collection bekerja?
- Bagaimana validasi nilai rapor?
- Bagaimana batch commit ke repository?
- Template generator logic?

---

### Ghaida - Domain & Algorithms

**Must Understand (CRITICAL!):**
-  **Merge Sort algorithm**
-  **Stable sort concept**
-  **Time complexity O(n log n)**
-  Decimal usage (no float)
-  Round Half Up implementation
-  Tie-breaking multi-level logic
-  Status eligible calculation

**Can Explain (WAJIB!):**
- **Kenapa Merge Sort, bukan Quick Sort?**
- **Bagaimana stable sort bekerja?**
- **Proof time complexity O(n log n)?**
- Bagaimana tie-breaking diterapkan?
- Logic Hijau/Kuning/Abu-abu?

---

## Daily Activities

### Morning Routine (15-30 menit)

**Daily Standup:**
1. Share: Kemarin belajar apa
2. Plan: Hari ini fokus di mana
3. Ask: Ada yang tidak jelas?

**Check:**
- Pull latest dari GitHub
- Read: Team notes/updates
- Prepare: Questions untuk hari ini

---

### During Work (3-4 jam)

**Read Code:**
- Start: High-level overview
- Then: Deep dive details
- Note: Questions & insights

**Experiment:**
- Run: Code dengan contoh data
- Test: Different scenarios
- Debug: Jika ada yang tidak jelas

**Document:**
- Write: Learning notes
- Create: Diagrams (if helpful)
- Comment: Code (if needed)

---

### End of Day (30 menit)

**Review:**
- Summary: Apa yang dipelajari
- Note: Questions untuk besok
- Update: Progress tracker

**Share:**
- Post: Update di grup
- Ask: Questions ke tim
- Help: Answer questions dari tim

---

## Code Reading Techniques

### Technique 1: Top-Down

```
1. Start: README.md (project overview)
2. Then: Project structure
3. Then: Entry point (main.py)
4. Follow: Execution flow
5. Deep dive: Each component
```

**Good for:** Understanding overall architecture

---

### Technique 2: Bottom-Up

```
1. Start: Domain models
2. Then: Domain logic (calculator, sorter)
3. Then: Application services
4. Then: Infrastructure (repos)
5. Finally: Presentation (UI)
```

**Good for:** Understanding data flow

---

### Technique 3: Feature-Based

```
1. Pick: One feature (e.g., Import CSV)
2. Trace: From UI to database
3. Understand: Full vertical slice
4. Repeat: For other features
```

**Good for:** Understanding integration

---

## Tips Produktivitas

### For Reading Code

1. **Don't read linearly**
   - Start with interfaces/contracts
   - Understand "what" before "how"

2. **Use debugger**
   - Set breakpoints
   - Step through execution
   - Inspect variables

3. **Run tests first**
   - Tests explain behavior
   - Tests show usage examples
   - Tests validate understanding

4. **Take notes**
   - Summary per file
   - Questions list
   - Aha moments

---

### For Team

1. **Daily standup** (15 menit)
   - Consistent time
   - Quick updates
   - No long discussions

2. **Code reading session** (2 jam × 3)
   - Schedule in advance
   - Prepare presentation
   - Interactive Q&A

3. **Pair understanding** (as needed)
   - Complex code → pair reading
   - Explain to each other
   - Learn together

4. **Documentation** (continuous)
   - Write as you learn
   - Share with team
   - Iterate based on feedback

---

## Success Criteria

### Individual

**Rafliza:**
-  Bisa explain presentation layer flow
-  Bisa explain atomic write mechanism
-  Bisa customize UI tanpa break
-  Bisa debug presentation issues

**Fadli:**
-  Bisa explain CSV parser logic
-  Bisa explain service layer
-  Bisa add new validation rule
-  Bisa debug import issues

**Ghaida:**
-  **Bisa explain Merge Sort algorithm**
-  Bisa explain tie-breaking logic
-  Bisa add new sorting criteria
-  Bisa debug domain logic issues

---

### Team

-  All tests passing (pytest -v)
-  Coverage > 80% (pytest --cov)
-  Linting pass (ruff check .)
-  Type check pass (mypy eligo)
-  Performance < 1s for 1000 siswa ranking
-  **Setiap orang bisa presentasi area masing-masing (15 menit)**

---

## Troubleshooting

### Problem: "Code terlalu complex, tidak paham"

**Solution:**
1. Break down: Baca function per function
2. Debug: Run dengan data kecil
3. Ask: Tanya Rafliza atau tim
4. Document: Tulis yang sudah paham

---

### Problem: "Merge Sort terlalu sulit dipahami"

**Solution (Ghaida):**
1. Read: Algorithm explanation online
2. Visualize: Gunakan visualizer (e.g., visualgo.net)
3. Practice: Implement dengan data kecil
4. Pair: Session dengan Rafliza (2 jam)

---

### Problem: "Tidak tahu harus mulai dari mana"

**Solution:**
1. Follow: Jadwal di dokumen ini
2. Start: README & PROJECT_STRUCTURE
3. Ask: Rafliza untuk guidance
4. Focus: Satu file per session

---

### Problem: "Takut salah customize code"

**Solution:**
1. Git: Buat branch untuk experiment
2. Test: Jalankan tests setelah customize
3. Revert: Jika break, git checkout
4. Ask: Review dari Rafliza sebelum commit

---

## Resources

### Documentation

- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Struktur lengkap
- **[TEAM_BREAKDOWN.md](TEAM_BREAKDOWN.md)** - Detail per anggota
- **[REBUILD_STRATEGY.md](REBUILD_STRATEGY.md)** - Strategy lengkap

### Code Reading

- Tests: `tests/` - Lihat usage examples
- Docstrings: Baca function/class docs
- Comments: Inline explanations

### External

- Merge Sort: https://visualgo.net/en/sorting
- Clean Architecture: Robert C. Martin
- Python Best Practices: Real Python

---

## Kesimpulan

### Target: Selesai dalam 2 minggu

**Week 1:** Understand & Learn (70%)
**Week 2:** Customize & Test (100%)

### Keys to Success:

1. **Read actively** - Don't just scan, understand
2. **Ask questions** - No question is stupid
3. **Document learning** - Write notes, create diagrams
4. **Test understanding** - Run code, experiment
5. **Share knowledge** - Present to team, help each other

### Remember:

**"Reading code is harder than writing code"**
- Take your time
- Be patient
- It's okay to not understand everything immediately
- Focus on understanding, not memorizing

---

**Good luck dengan rebuild! Target 2 minggu achievable dengan approach ini!**

Last Updated: 2026-11-01
