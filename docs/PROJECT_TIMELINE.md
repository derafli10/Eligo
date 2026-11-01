# Timeline & Estimasi Waktu Proyek Eligo

**CATATAN:** Dokumen ini untuk referensi **Build from Scratch**. Untuk approach yang **lebih cepat dan recommended**, lihat **[REBUILD_STRATEGY.md](REBUILD_STRATEGY.md)** (Copy & Understand - 2 minggu).

---

## Build from Scratch Approach (Reference)

**Target:** Rebuild selesai dalam 1 bulan
**Jadwal Kerja:** Senin, Rabu, Minggu (3 hari per minggu)
**Total Hari Kerja:** 12 hari kerja dalam 1 bulan
**Tim:** 1 experienced (Rafliza) + 2 pemula (Fadli & Ghaida)

---

## Analisis Kompleksitas & Estimasi

### Breakdown Kompleksitas per Area

#### **Rafliza (40% beban) - Experienced**

| Component | Kompleksitas | Estimasi (jam) | Catatan |
|-----------|--------------|----------------|---------|
| **Presentation Layer** | | | |
| - formatter.py | Medium | 3 jam | Rich Console, tabel, panel, colors |
| - main.py (cli) | Medium | 4 jam | Menu orchestrator, keyboard handling |
| - menu_school.py | Low-Medium | 3 jam | CRUD sekolah, kuota display |
| - menu_student.py | Medium | 4 jam | CRUD siswa, edit nilai |
| - menu_import.py | Low | 2 jam | UI impor, preview, konfirmasi |
| - menu_ranking.py | Medium | 3 jam | Display ranking, pagination |
| - menu_reset.py | Low | 1 jam | Reset dengan konfirmasi |
| **Infrastructure Layer** | | | |
| - atomic_writer.py | Medium | 3 jam | Atomic write .tmp → .bak → .json |
| - school_repo.py | Low-Medium | 3 jam | Implement ISchoolRepository |
| - student_repo.py | Medium | 4 jam | Implement IStudentRepository + batch |
| - config_repo.py | Low | 2 jam | Implement IConfigRepository |
| **Domain Interfaces** | | | |
| - repositories.py | Low | 2 jam | Abstract interfaces |
| **Entry Point** | | | |
| - main.py (root) | Low | 1 jam | Application bootstrap |
| **Testing** | Medium | 10 jam | Unit + integration tests |
| **Integration & Polish** | Medium | 5 jam | Bug fixing, integration |
| **TOTAL** | | **50 jam** | |

**Produktivitas:** Experienced, bisa 2-3 jam efektif per hari kerja

---

#### **Fadli (30% beban) - Pemula**

| Component | Kompleksitas | Estimasi (jam) | Catatan |
|-----------|--------------|----------------|---------|
| **CSV Parser** | High | 12 jam | Parse CSV, UTF-8 BOM, error collection |
| - Basic parser | | 4 jam | Read CSV, detect separator |
| - Error handling | | 4 jam | Collect all errors strategy |
| - Template generator | | 4 jam | Generate per jurusan |
| **Application Services** | | | |
| - import_service.py | High | 8 jam | Preview, duplikat, commit batch |
| - school_service.py | Medium | 4 jam | Business logic sekolah |
| - student_service.py | Medium | 5 jam | Business logic siswa |
| - config_service.py | Low-Medium | 3 jam | Config management |
| **Testing** | Medium | 8 jam | Unit tests untuk services |
| **Learning & Debugging** | High | 10 jam | Buffer untuk pemula |
| **TOTAL** | | **50 jam** | |

**Produktivitas:** Pemula, butuh 1.5-2 jam efektif per hari kerja (dengan learning curve)

---

#### **Ghaida (30% beban) - Pemula**

| Component | Kompleksitas | Estimasi (jam) | Catatan |
|-----------|--------------|----------------|---------|
| **Domain Models** | Medium | 5 jam | School, Student, Grade entities |
| **Domain Exceptions** | Low | 2 jam | Custom exceptions |
| **Calculator** | Medium-High | 6 jam | Decimal calculation, Round Half Up |
| **Quota** | Medium | 4 jam | Akreditasi rules, bonus e-Rapor |
| **Sorter** | High | 10 jam | Merge Sort mandiri (no sorted()) |
| **Validator** | Medium | 4 jam | Business validation rules |
| **Normalizer** | Low-Medium | 3 jam | Data normalization |
| **Searcher** | Medium | 4 jam | Search & filter logic |
| **Ranking Service** | High | 8 jam | Tie-breaking, status eligible |
| **Testing** | Medium | 8 jam | Unit tests domain logic |
| **Learning & Debugging** | High | 10 jam | Buffer untuk pemula |
| **TOTAL** | | **64 jam** | |

**Produktivitas:** Pemula + domain complexity, butuh 1.5-2 jam efektif per hari kerja

---

## Estimasi Total Jam Kerja

| Anggota | Total Jam | Hari Kerja | Jam per Hari | Rekomendasi |
|---------|-----------|------------|--------------|-------------|
| **Rafliza** | 50 jam | 12 hari | 4.2 jam/hari | **4-5 jam/hari** |
| **Fadli** | 50 jam | 12 hari | 4.2 jam/hari | **4-5 jam/hari** |
| **Ghaida** | 64 jam | 12 hari | 5.3 jam/hari | **5-6 jam/hari** |

**Catatan Penting:**
- Ghaida punya beban lebih berat karena domain layer adalah core logic
- Perlu extra waktu untuk learning curve pemula
- Buffer untuk debugging & integration

---

## Rekomendasi Jadwal Kerja

### **Plan A: Balanced (RECOMMENDED)**

Fokus pada work-life balance dengan buffer yang cukup:

| Anggota | Senin | Rabu | Minggu | Total/Minggu |
|---------|-------|------|--------|--------------|
| **Rafliza** | 4 jam | 4 jam | 4 jam | 12 jam |
| **Fadli** | 4 jam | 4 jam | 4 jam | 12 jam |
| **Ghaida** | 5 jam | 5 jam | 5 jam | 15 jam |

**Total per bulan:**
- Rafliza: 12 jam × 4 minggu = 48 jam 
- Fadli: 12 jam × 4 minggu = 48 jam  (butuh 50 jam → sisa 2 jam untuk polish)
- Ghaida: 15 jam × 4 minggu = 60 jam  (butuh 64 jam → sisa 4 jam bisa dibantu Rafliza)

**Kelebihan:**
- Sustainable, tidak burnout
- Buffer cukup untuk debugging
- Work-life balance terjaga

**Kekurangan:**
- Sedikit ketat di akhir untuk Ghaida

---

### **Plan B: Moderate Push**

Jika mau sedikit lebih cepat dengan buffer lebih:

| Anggota | Senin | Rabu | Minggu | Total/Minggu |
|---------|-------|------|--------|--------------|
| **Rafliza** | 5 jam | 4 jam | 4 jam | 13 jam |
| **Fadli** | 5 jam | 4 jam | 4 jam | 13 jam |
| **Ghaida** | 6 jam | 5 jam | 5 jam | 16 jam |

**Total per bulan:**
- Rafliza: 13 jam × 4 minggu = 52 jam  (buffer 2 jam)
- Fadli: 13 jam × 4 minggu = 52 jam  (buffer 2 jam)
- Ghaida: 16 jam × 4 minggu = 64 jam  (pas!)

**Kelebihan:**
- Buffer lebih banyak
- Bisa selesai lebih cepat
- Lebih aman dari risk

**Kekurangan:**
- Agak melelahkan untuk pemula (5-6 jam coding)
- Risiko burnout di minggu 3-4

---

### **Plan C: Relaxed (With Extension)**

Jika mau lebih santai dan bisa extend 1 minggu:

| Anggota | Senin | Rabu | Minggu | Total/Minggu |
|---------|-------|------|--------|--------------|
| **Rafliza** | 3 jam | 3 jam | 3 jam | 9 jam |
| **Fadli** | 3 jam | 3 jam | 3 jam | 9 jam |
| **Ghaida** | 4 jam | 4 jam | 4 jam | 12 jam |

**Total dalam 5 minggu:**
- Rafliza: 9 jam × 5 minggu = 45 jam (butuh 50 jam → tambah 5 jam di minggu 5)
- Fadli: 9 jam × 5 minggu = 45 jam (butuh 50 jam → tambah 5 jam di minggu 5)
- Ghaida: 12 jam × 5 minggu = 60 jam (butuh 64 jam → tambah 4 jam di minggu 5)

**Kelebihan:**
- Sangat sustainable
- Kualitas code lebih baik
- Learning curve lebih comfortable untuk pemula

**Kekurangan:**
- Butuh extend 1 minggu (5 minggu total)

---

## Jadwal Detil (Plan A - Recommended)

### **Minggu 1: Setup & Foundation**

**Senin (Setup Day)**
- **Semua (2 jam):** Setup Git, environment, kickoff meeting
- **Rafliza (2 jam):** Buat skeleton structure, atomic_writer.py
- **Fadli (2 jam):** Setup & mulai csv_parser basic
- **Ghaida (3 jam):** Domain models.py & exceptions.py

**Rabu (Foundation)**
- **Rafliza (4 jam):** repositories.py interfaces, mulai school_repo.py
- **Fadli (4 jam):** csv_parser error handling
- **Ghaida (5 jam):** calculator.py & quota.py

**Minggu (Core Logic)**
- **Rafliza (4 jam):** Selesaikan school_repo.py, student_repo.py 50%
- **Fadli (4 jam):** Selesaikan csv_parser, mulai import_service
- **Ghaida (5 jam):** Mulai sorter.py (Merge Sort)

**Progress Week 1:** ~20% selesai

---

### **Minggu 2: Core Development**

**Senin**
- **Rafliza (4 jam):** Selesaikan student_repo.py, config_repo.py
- **Fadli (4 jam):** import_service.py (preview & duplikat)
- **Ghaida (5 jam):** Lanjut sorter.py + testing

**Rabu**
- **Rafliza (4 jam):** formatter.py + main.py (cli orchestrator)
- **Fadli (4 jam):** Selesaikan import_service, mulai school_service
- **Ghaida (5 jam):** Selesaikan sorter.py, mulai validator.py

**Minggu**
- **Rafliza (4 jam):** menu_school.py + menu_student.py 50%
- **Fadli (4 jam):** school_service.py + student_service.py
- **Ghaida (5 jam):** validator.py, normalizer.py, searcher.py

**Progress Week 2:** ~50% selesai

---

### **Minggu 3: Integration & Features**

**Senin**
- **Rafliza (4 jam):** Selesaikan menu_student.py, menu_import.py
- **Fadli (4 jam):** Selesaikan student_service, mulai config_service
- **Ghaida (5 jam):** Mulai ranking_service.py (core logic)

**Rabu**
- **Rafliza (4 jam):** menu_ranking.py + menu_reset.py
- **Fadli (4 jam):** Selesaikan config_service, testing services
- **Ghaida (5 jam):** Lanjut ranking_service (tie-breaking)

**Minggu (Integration Day)**
- **Rafliza (4 jam):** main.py (root), integration presentation ↔ application
- **Fadli (4 jam):** Testing import flow end-to-end
- **Ghaida (5 jam):** Selesaikan ranking_service + testing

**Progress Week 3:** ~80% selesai

---

### **Minggu 4: Testing, Polish & Deployment**

**Senin (Testing Day)**
- **Rafliza (4 jam):** Unit tests presentation layer
- **Fadli (4 jam):** Integration tests CSV import
- **Ghaida (5 jam):** Unit tests domain layer

**Rabu (Integration Testing)**
- **Semua (4-5 jam):** Integration testing full workflow
  - Test: Setup sekolah → Import siswa → Ranking → Display
  - Bug fixing bersama
  - Performance testing

**Minggu (Polish & Documentation)**
- **Rafliza (4 jam):** UI/UX polish, error messages, final testing
- **Fadli (4 jam):** Documentation, CSV template generation
- **Ghaida (5 jam):** Performance optimization, final testing

**Progress Week 4:**  100% SELESAI!

---

## Tips untuk Lead (Rafliza)

### Daily Routine

**Sebelum Hari Kerja:**
- Review PR dari hari sebelumnya (jika ada)
- Prepare task untuk hari ini
- Check blocker tim

**Selama Hari Kerja:**
- Pagi: Quick standup (15 menit) - masing-masing share rencana hari ini
- Tengah: Check-in singkat via chat
- Sore: Code review PR yang masuk hari ini

**Setelah Hari Kerja:**
- Update progress tracker
- Prepare blocker untuk besok

---

### Support untuk Pemula

**Fadli (CSV & Services):**
- Pair programming untuk CSV parser (Senin minggu 1)
- Daily code review untuk services
- Share best practices error handling

**Ghaida (Domain & Algorithms):**
- Pair programming untuk Merge Sort (Minggu minggu 1)
- Review tie-breaking logic (Senin minggu 3)
- Help dengan testing domain logic

**Time Allocation untuk Help:**
- Reserve 30-60 menit per hari kerja untuk membantu tim
- Prioritas: unblock blocker > code review > pair programming

---

## Risk Management

### Potential Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Ghaida stuck di Merge Sort | High | High | Pair programming minggu 1, reserve 2 jam Rafliza |
| Fadli stuck di CSV parser | Medium | Medium | Provide example code, pair programming |
| Integration bugs | High | Medium | Reserve minggu 4 untuk buffer |
| Scope creep | Medium | High | Strict scope freeze setelah minggu 1 |
| Burnout pemula | Medium | High | Monitor workload, adjust jika perlu |

### Contingency Plans

**Jika Ketinggalan Schedule (Week 2-3):**
1. Rafliza ambil 1-2 task dari Fadli/Ghaida
2. Extend 3-5 jam di minggu berikutnya
3. Reduce scope: Skip searcher.py atau normalizer.py (nice-to-have)

**Jika Sangat Ketinggalan (Week 3):**
1. Meeting evaluasi
2. Consider Plan C (extend 1 minggu)
3. Prioritas MVP: Ranking must work, polish bisa dikurangi

---

## Progress Tracking

### Weekly Checklist

**Week 1:**
-  Git setup selesai
-  Skeleton structure OK
-  Domain models selesai
-  CSV parser basic OK
-  Atomic writer OK

**Week 2:**
-  All repositories selesai
-  Import service selesai
-  Sorter (Merge Sort) selesai
-  School & student services selesai

**Week 3:**
-  All menus selesai
-  Ranking service selesai
-  Integration test passing
-  Basic testing selesai

**Week 4:**
-  Full test coverage > 80%
-  Documentation complete
-  Performance acceptable
-  Demo ready

---

## Kesimpulan & Rekomendasi

### Rekomendasi: **Plan A (Balanced)**

**Jadwal Kerja:**
- **Rafliza:** 4 jam/hari (Senin, Rabu, Minggu)
- **Fadli:** 4 jam/hari (Senin, Rabu, Minggu)
- **Ghaida:** 5 jam/hari (Senin, Rabu, Minggu)

**Kenapa Plan A?**
1. Sustainable untuk pemula (tidak burnout)
2. Buffer cukup untuk learning curve
3. Quality > Speed
4. Masih achievable dalam 1 bulan
5. Work-life balance terjaga

**Backup Plan:**
- Jika Week 2 sudah ketinggalan > 10%, switch ke Plan B
- Jika Week 3 masih ketinggalan, consider extend 1 minggu (Plan C)

### Key Success Factors

1. **Communication:** Daily standup wajib (15 menit)
2. **Code Review:** Review PR dalam max 24 jam
3. **Pair Programming:** Untuk task complex (Merge Sort, CSV parser)
4. **Documentation:** Write as you code
5. **Testing:** Test dari awal, jangan numpuk di akhir
6. **Flexibility:** Adjust schedule jika ada blocker

---

**Target:** 100% selesai dalam 4 minggu dengan quality code!

**Motto:** "Slow is smooth, smooth is fast" - Fokus pada quality, kecepatan akan mengikuti.

Last Updated: 2026-11-01
