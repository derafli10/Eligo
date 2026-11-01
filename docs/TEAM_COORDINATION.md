# Koordinasi Tim - Menghindari Merge Conflict

## Prinsip Utama

**"Communicate Early, Commit Often, Merge Frequently"**

---

## Pembagian Area Kerja

### Strategi : Hybrid
```
Sprint 1:
- Person A: models/kandidat.py
- Person B: models/pemilih.py
- Person C: views/kandidat_view.py
- Person D: controllers/kandidat_controller.py

Sprint 2 (setelah Sprint 1 di-merge):
- Person A: services/scoring.py
- Person B: views/pemilih_view.py
- ...dst
```

---


## Aturan Emas Menghindari Conflict

### 1. **Komunikasi Sebelum Edit File yang Sama**
```
 JANGAN:
   - Langsung edit file yang sedang dikerjakan orang lain
   - Merge tanpa kasih tau tim

 LAKUKAN:
   - Tanya dulu di grup: "Ada yang lagi kerja di kandidat.py?"
   - Koordinasi siapa edit bagian mana
   - Atau tunggu orang lain selesai dulu
```

### 2. **Branch Kecil dan Cepat**
```
 JANGAN:
   - Branch yang hidup berminggu-minggu
   - Kumpulan 50 file dalam 1 PR
   
 LAKUKAN:
   - Branch 1-3 hari, langsung merge
   - PR kecil: 5-10 file max
   - Frequent merge ke dev
```

### 3. **Sync Rutin dengan Dev**
```bash
# SETIAP PAGI sebelum mulai kerja:
git checkout dev
git pull origin dev
git checkout feature/branch-kamu
git merge dev

# Kalau ada conflict, resolve sekarang juga (pas tim masih pada online)
```

### 4. **Jangan Numpuk Commit**
```
 JANGAN:
   - Kerja seminggu baru commit 1x
   - 100 file berubah dalam 1 commit

 LAKUKAN:
   - Commit setiap selesai 1 fungsi kecil
   - Push minimal 1x sehari
   - Kasih commit message yang jelas
```

---

## Komunikasi Channel

### Daily Standup (15 menit)
Format:
1. **Kemarin**: Apa yang dikerjakan
2. **Hari ini**: Mau kerja di file/fitur apa
3. **Blocker**: Ada masalah? Butuh file dari siapa?

Contoh:
```
Riko:
- Kemarin: Selesai models/kandidat.py, sudah PR
- Hari ini: Mau kerja di controllers/kandidat_controller.py
- Blocker: Butuh service layer dari Budi dulu

Budi:
- Kemarin: 70% services/kandidat_service.py
- Hari ini: Selesaikan service, PR siang ini
- Blocker: Tidak ada
```

### Notification Penting
```
Format: "[FILE] nama_file.py - sedang dikerjakan oleh X"

Contoh di grup:
"[FILE] models/kandidat.py - sedang dikerjakan oleh Riko"
"[DONE] models/kandidat.py - sudah di-merge ke dev"
```

---

## Menangani Conflict

### Skenario A: Conflict Kecil (1-2 file)
```bash
# 1. Pull perubahan terbaru
git pull origin dev

# 2. Lihat file yang conflict
git status

# 3. Buka file, cari marker:
#   <<<<<<< HEAD
#   kode kamu
#   =======
#   kode orang lain
#   >>>>>>> dev

# 4. Diskusi dengan orang yang punya kode lain (call/chat)
# 5. Pilih kode yang benar atau gabungkan
# 6. Hapus marker (<<<<, ====, >>>>)
# 7. Test bahwa kode masih jalan

# 8. Commit resolution
git add .
git commit -m "fix: resolve conflict in kandidat.py"
git push
```

### Skenario B: Conflict Banyak (5+ file)
```bash
# 1. STOP! Jangan resolve sendiri
# 2. Screenshot/list file yang conflict
# 3. Call team meeting (Google Meet/Discord)
# 4. Review bareng file yang conflict
# 5. Tentukan approach:
#   Option A: Rebase branch kamu
#   Option B: Merge manual bareng-bareng
#   Option C: Buat branch baru dari dev, copy perubahan penting
# 6. Resolve bareng-bareng sambil call
```

### Skenario C: Conflict Parah (Struktur Berubah)
```bash
# 1. Backup perubahan kamu
cp -r eligo eligo-backup

# 2. Buat branch baru dari dev terbaru
git checkout dev
git pull origin dev
git checkout -b feature/new-approach

# 3. Copy manual perubahan penting dari backup
# 4. Commit bertahap
# 5. Test setiap step
```

---

## Best Practices dari Tim Lain

### Practice 1: Pairing untuk File Sensitif
```
File yang sering diubah banyak orang:
- utils/helpers.py
- models/__init__.py
- main.py

Solusi:
- Pair programming untuk edit file ini
- Atau assign 1 orang sebagai "owner" file tersebut
- Perubahan harus direview owner dulu
```

### Practice 2: Feature Flags
```python
# Untuk fitur yang belum selesai tapi harus merge
FEATURE_NEW_SCORING = False  # Set True kalau sudah siap

if FEATURE_NEW_SCORING:
    # Kode baru
else:
    # Kode lama
```

### Practice 3: Code Freeze Sebelum Demo
```
3 hari sebelum demo:
- STOP fitur baru
- Hanya bug fix di branch bugfix/*
- Test dan stabilisasi
- Merge ke main untuk demo
```

---

## Monitoring Progress

### Daily Check (di GitHub)
1. Network Graph: Lihat branch mana yang terlalu jauh dari dev
2. Pull Requests: Pastikan tidak ada PR menggantung > 2 hari
3. Issues: Update progress

### Weekly Review
1. Berapa conflict yang terjadi minggu ini?
2. File apa yang paling sering conflict?
3. Apa yang bisa diperbaiki minggu depan?

---

## Eskalasi

### Level 1: Tim bisa handle
- Conflict 1-5 file
- Resolve sendiri atau diskusi tim

### Level 2: Butuh senior
- Conflict > 10 file
- Struktur kode berubah drastis
- Tidak yakin approach yang benar

### Level 3: Emergency
- Repo corrupted
- Salah merge ke main
- Data loss

**Aturan: Jangan force push tanpa persetujuan semua tim!**

---

## Checklist Harian

Setiap anggota tim:

- [ ] Sync dari dev (`git pull origin dev`)
- [ ] Lihat PR yang perlu direview
- [ ] Standup: kasih tau mau kerja di mana
- [ ] Commit progress hari ini
- [ ] Push ke remote
- [ ] Update status di grup/project board
- [ ] Buat PR kalau ada yang bisa di-merge
- [ ] Review minimal 1 PR dari teman

---

## Goal

**Zero Conflict Weeks** 

Target:
- Minggu 1-2: Belajar (conflict wajar)
- Minggu 3-4: Kurangi conflict 50%
- Minggu 5+: Max 1-2 minor conflict per minggu

---

**Remember: Komunikasi adalah kunci!**

Lebih baik 5 menit diskusi daripada 2 jam resolve conflict.
