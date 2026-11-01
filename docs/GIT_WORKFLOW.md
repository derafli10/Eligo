# Git Workflow - Tim Eligo

## Daftar Isi
- [Struktur Branch](#struktur-branch)
- [Setup Awal](#setup-awal)
- [Workflow Harian](#workflow-harian)
- [Command Cheatsheet](#command-cheatsheet)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Struktur Branch

```
main (production-ready)
  └── dev (development)
       ├── feature/nama-fitur-anggota
       ├── bugfix/nama-bug-anggota
       └── refactor/nama-refactor-anggota
```

### Aturan Branch:
- **`main`**: Hanya code yang sudah final dan tested
- **`dev`**: Branch integrasi untuk development
- **`feature/*`**: Branch untuk fitur baru
- **`bugfix/*`**: Branch untuk bug fixes
- **`refactor/*`**: Branch untuk refactoring

---

## Setup Awal

### 1. Clone Repository
```bash
# Clone repo
git clone <URL_REPO_GITHUB>
cd Eligo

# Setup remote tracking
git fetch origin
git branch --set-upstream-to=origin/main main
```

### 2. Setup Branch Lokal
```bash
# Pastikan berada di branch main
git checkout main

# Pull perubahan terbaru
git pull origin main

# Buat/checkout ke branch dev
git checkout -b dev origin/dev
# Atau jika sudah ada: git checkout dev

# Pull perubahan terbaru dev
git pull origin dev
```

### 3. Setup Virtual Environment
```bash
# Buat virtual environment (sekali saja)
python -m venv .venv

# Aktivasi virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Workflow Harian

### A. MULAI KERJA (Setiap Hari)

```bash
# 1. Aktivasi virtual environment
.venv\Scripts\activate

# 2. Pastikan di branch dev
git checkout dev

# 3. Pull perubahan terbaru dari remote
git pull origin dev

# 4. Buat branch baru untuk pekerjaan hari ini
# Format: feature/nama-fitur-namakamu atau feature/YYMMDD-namakamu-deskripsi
git checkout -b feature/241101-riko-kandidat-selection

# Contoh nama branch lain:
# - feature/kandidat-crud-budi
# - bugfix/scoring-formula-ani
# - refactor/models-layer-dodi
```

**️ PENTING:** Setiap anggota kerja di **branch sendiri**, JANGAN langsung ke `dev` atau `main`!

---

### B. SELAMA KERJA

```bash
# Check status perubahan
git status

# Tambahkan file yang diubah
git add <nama-file>
# Atau tambahkan semua:
git add .

# Commit dengan pesan yang jelas
git commit -m "feat: tambah fungsi create_kandidat di models"

# Commit lagi jika ada perubahan lain
git add .
git commit -m "test: tambah unit test untuk create_kandidat"
```

**Format Commit Message:**
- `feat:` - Fitur baru
- `fix:` - Bug fix
- `refactor:` - Refactoring code
- `test:` - Tambah/update test
- `docs:` - Update dokumentasi
- `chore:` - Update dependencies, config, dll

---

### C. PUSH KE GITHUB (Simpan Progress)

```bash
# Push branch kamu ke remote
git push origin feature/241101-riko-kandidat-selection

# Kalau pertama kali push branch baru:
git push -u origin feature/241101-riko-kandidat-selection
```

** Tips:** Push sesering mungkin (minimal 1-2x sehari) agar progress tidak hilang!

---

### D. MERGE KE DEV (Setelah Fitur Selesai)

**️ JANGAN MERGE SENDIRI! Gunakan Pull Request:**

#### Langkah-langkah:

1. **Push branch kamu dulu:**
```bash
git push origin feature/241101-riko-kandidat-selection
```

2. **Buka GitHub → Buat Pull Request:**
   - Base: `dev`
   - Compare: `feature/241101-riko-kandidat-selection`
   - Judul: Deskripsi fitur yang kamu kerjakan
   - Deskripsi: Jelaskan apa yang diubah, file apa saja, dst.

3. **Minta Review dari Tim:**
   - Tag minimal 1 anggota tim untuk review
   - Tunggu approval

4. **Setelah Approved → Merge:**
   - Klik "Merge Pull Request" di GitHub
   - Pilih "Squash and Merge" (recommended) atau "Merge Commit"
   - Delete branch setelah merge

5. **Update Lokal:**
```bash
# Kembali ke dev
git checkout dev

# Pull perubahan yang sudah merged
git pull origin dev

# Hapus branch lokal yang sudah selesai
git branch -d feature/241101-riko-kandidat-selection
```

---

### E. SEBELUM MULAI FITUR BARU

```bash
# 1. Kembali ke dev
git checkout dev

# 2. Pull perubahan terbaru
git pull origin dev

# 3. Buat branch baru
git checkout -b feature/241102-riko-fitur-selanjutnya
```

---

## Command Cheatsheet

### Everyday Commands

```bash
# === SETUP ===
git clone <url>                                    # Clone repo
git checkout dev                                    # Pindah ke branch dev
git pull origin dev                                 # Update branch dev

# === MULAI KERJA ===
git checkout -b feature/nama-fitur-kamu             # Buat branch baru
git status                                          # Cek perubahan
git diff                                            # Lihat detail perubahan

# === COMMIT ===
git add .                                           # Stage semua perubahan
git add <file>                                      # Stage file tertentu
git commit -m "feat: deskripsi perubahan"          # Commit
git log --oneline                                   # Lihat history commit

# === PUSH ===
git push origin feature/nama-fitur-kamu             # Push ke remote
git push -u origin feature/nama-fitur-kamu          # Push pertama kali

# === UPDATE ===
git fetch origin                                    # Ambil info dari remote
git pull origin dev                                 # Update dari dev
git merge dev                                       # Merge dev ke branch kamu

# === CLEANUP ===
git branch                                          # Lihat branch lokal
git branch -d feature/nama-fitur-lama              # Hapus branch lokal
git remote prune origin                             # Hapus referensi branch remote yang sudah dihapus
```

### Emergency Commands

```bash
# Batalkan perubahan yang belum di-commit
git checkout -- <file>                              # Batalkan perubahan 1 file
git reset --hard                                    # Batalkan SEMUA perubahan (HATI-HATI!)

# Batalkan commit terakhir (tapi perubahan masih ada)
git reset --soft HEAD~1

# Lihat perubahan di branch lain tanpa pindah
git diff dev..feature/branch-kamu

# Simpan perubahan sementara (stash)
git stash                                           # Simpan perubahan
git stash pop                                       # Kembalikan perubahan

# Update branch kamu dengan dev terbaru
git checkout feature/branch-kamu
git merge dev                                       # Atau: git rebase dev
```

---

## Best Practices

### 1. **Satu Branch = Satu Fitur**
   - Jangan campur-campur banyak fitur dalam 1 branch
   - Buat branch baru untuk setiap fitur/task

### 2. **Pull Sebelum Push**
   ```bash
   git pull origin dev    # Selalu pull dulu
   git push origin feature/branch-kamu
   ```

### 3. **Commit Sering, Message Jelas**
   - Commit setiap kali selesai 1 unit kerja kecil
   - Jangan commit 100 file sekaligus
   - Message: jelas, singkat, to the point

### 4. **Review Before Merge**
   - Selalu gunakan Pull Request
   - Minta review dari minimal 1 orang
   - Jangan merge sendiri tanpa review

### 5. **Komunikasi Tim**
   - Kasih tau tim kalau mau kerja di file yang sama
   - Coordinate siapa kerja di layer apa
   - Gunakan GitHub Issues/Projects untuk tracking

### 6. **Jangan Edit File yang Sama Bersamaan**
   - Koordinasi dengan tim
   - Kalau memang harus, komunikasi intensif dan merge sering

---

## Troubleshooting

### Problem 1: "Your branch is behind..."
```bash
# Solusi: Pull dulu
git pull origin dev
```

### Problem 2: Merge Conflict
```bash
# 1. Lihat file yang conflict
git status

# 2. Buka file yang conflict, cari marker:
#   <<<<<<< HEAD
#   kode kamu
#   =======
#   kode orang lain
#   >>>>>>> branch-name

# 3. Edit manual, pilih mana yang benar, hapus marker

# 4. Setelah resolve:
git add <file-yang-conflict>
git commit -m "fix: resolve merge conflict"
git push origin feature/branch-kamu
```

### Problem 3: Lupa di Branch Mana
```bash
git branch                  # Lihat branch lokal (yang aktif ada tanda *)
git branch -a               # Lihat semua branch (lokal + remote)
```

### Problem 4: Salah Commit di Branch yang Salah
```bash
# Kalau belum push:
git reset --soft HEAD~1     # Batalkan commit, perubahan masih ada
git checkout branch-yang-benar
git add .
git commit -m "pesan yang benar"

# Kalau sudah push, minta bantuan tim!
```

### Problem 5: Butuh Update dari Dev Tapi Ada Uncommitted Changes
```bash
# Simpan dulu perubahan kamu
git stash

# Update dari dev
git pull origin dev

# Kembalikan perubahan kamu
git stash pop
```

---

## Struktur File Per Layer (Hindari Conflict)

Agar tidak bentrok, bagi tugas per layer/module:

```
eligo/
├── models/          → Person A
├── views/           → Person B
├── controllers/     → Person C
├── services/        → Person D
└── utils/           → Person E
```

**Aturan:**
- 1 orang fokus di 1 layer/module
- Kalau harus edit file orang lain, koordinasi dulu
- Buat PR kecil-kecil, jangan sekaligus besar

---

## Workflow Summary

```
1. MULAI:
   git checkout dev
   git pull origin dev
   git checkout -b feature/nama-fitur-kamu

2. KERJA:
   [edit code]
   git add .
   git commit -m "feat: deskripsi"
   [ulangi]

3. PUSH:
   git push origin feature/nama-fitur-kamu

4. PULL REQUEST:
   [buat PR di GitHub]
   [minta review]
   [merge setelah approved]

5. CLEANUP:
   git checkout dev
   git pull origin dev
   git branch -d feature/nama-fitur-kamu

6. REPEAT untuk fitur berikutnya!
```

---

## Kontak

Kalau ada masalah Git yang tidak bisa diselesaikan:
1. **JANGAN** panik dan force push
2. **STOP** dulu, jangan edit apa-apa
3. **TANYA** tim/tech lead
4. Backup dulu perubahan kamu (copy folder)

---

**Dibuat untuk Tim Eligo** 
**Last Updated:** 2026-11-01
