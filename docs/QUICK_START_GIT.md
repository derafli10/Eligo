# Quick Start - Git Setup untuk Tim Eligo

**Panduan super cepat untuk mulai kolaborasi dengan Git & GitHub**

**CATATAN:** Jika akan melakukan rebuild, baca dulu **[REBUILD_STRATEGY.md](REBUILD_STRATEGY.md)** untuk approach Copy & Understand yang 50% lebih cepat!

---

## Setup Repository (Sekali Saja)

### Option 1: Dengan Script

```bash
# 1. Setup git lokal
bash scripts/setup-git-local.sh

# 2. Buat repository di GitHub (via browser)
#   → https://github.com/new
#   → Nama: Eligo
#   → JANGAN centang apa-apa
#   → Create

# 3. Hubungkan dengan GitHub (ganti USERNAME dengan username GitHub kamu)
git remote add origin https://github.com/USERNAME/Eligo.git

# 4. Push ke GitHub
git push -u origin main
git push -u origin dev

# SELESAI! 
```

### Option 2: Manual

```bash
# 1. Initialize git
git init
git branch -M main

# 2. Initial commit
git add .
git commit -m "chore: initial commit - project setup"

# 3. Create dev branch
git checkout -b dev

# 4. Buat repo di GitHub (via browser)
# 5. Hubungkan
git remote add origin https://github.com/USERNAME/Eligo.git

# 6. Push
git push -u origin main
git push -u origin dev
```

---

## Join Repository (Anggota Tim)

```bash
# 1. Clone (ganti USERNAME)
git clone https://github.com/USERNAME/Eligo.git
cd Eligo

# 2. Setup environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Test
python main.py

# SIAP KERJA! 
```

---

## Daily Workflow

### Sebelum Mulai Kerja

```bash
# Cara 1: Dengan script 
bash scripts/git-helper.sh start-work

# Cara 2: Manual
git checkout dev
git pull origin dev
git checkout -b feature/YYMMDD-nama-fitur
```

### Selama Kerja

```bash
# Cara 1: Dengan script
bash scripts/git-helper.sh quick-commit

# Cara 2: Manual
git add .
git commit -m "feat: deskripsi perubahan"
git push origin feature/YYMMDD-nama-fitur
```

### Sebelum Pulang

```bash
# Pastikan progress sudah di-push
git push origin feature/YYMMDD-nama-fitur

# Buat PR di GitHub jika fitur sudah selesai
```

---

## Format Branch Name

```bash
# Format: tipe/YYMMDD-deskripsi-nama

feature/241101-kandidat-crud-riko
feature/241101-pemilih-model-ghaida
bugfix/241102-scoring-error-fadli
refactor/241102-clean-utils-riko
```

**Tipe:**
- `feature/` → Fitur baru
- `bugfix/` → Perbaikan bug
- `refactor/` → Refactoring code

---

## Format Commit Message

```bash
git commit -m "feat: tambah fungsi create_kandidat"
git commit -m "fix: perbaiki bug di scoring formula"
git commit -m "refactor: restructure models layer"
git commit -m "test: tambah unit test untuk kandidat"
git commit -m "docs: update README"
git commit -m "chore: update dependencies"
```

**Prefix:**
- `feat:` = Fitur baru
- `fix:` = Bug fix
- `refactor:` = Refactoring
- `test:` = Update test
- `docs:` = Update dokumentasi
- `chore:` = Config/dependencies

---

## Update dari Dev (Setiap Hari!)

```bash
# Cara 1: Dengan script
bash scripts/git-helper.sh daily-sync

# Cara 2: Manual
git checkout dev
git pull origin dev
git checkout feature/branch-kamu
git merge dev
```

**PENTING:** Lakukan ini sebelum mulai kerja!

---

## Buat Pull Request

```bash
# 1. Push branch
git push origin feature/branch-kamu

# 2. Buka GitHub repository di browser
# 3. Klik "Pull requests" → "New pull request"
# 4. Base: dev, Compare: feature/branch-kamu
# 5. Isi template:
#   - Deskripsi perubahan
#   - File yang diubah
#   - Cara test
# 6. Create pull request
# 7. Minta review dari minimal 1 teman
# 8. Merge setelah approved 
```

---

## Cleanup Setelah Merge

```bash
# Cara 1: Dengan script
bash scripts/git-helper.sh cleanup

# Cara 2: Manual
git checkout dev
git pull origin dev
git branch -d feature/branch-yang-sudah-merged
```

---

## Command Penting

```bash
# Lihat status
git status

# Lihat history
git log --oneline

# Lihat branch
git branch -a

# Lihat perubahan
git diff

# Batalkan perubahan (HATI-HATI!)
git checkout -- file.txt

# Simpan perubahan sementara
git stash
git stash pop
```

---

## Aturan Emas

1.  **SELALU** pull sebelum mulai kerja
2.  **COMMIT** tiap selesai bikin blok code
3.  **PUSH** minimal 1x 
4.  **KOMUNIKASI** sebelum edit file yang sama
5.  **JANGAN** force push tanpa persetujuan tim
6.  **JANGAN** commit langsung ke dev/main
7.  **JANGAN** push code yang error/belum di-test

---

## Dokumentasi Lengkap

Kalau butuh detail lebih:

- **[Git Workflow](GIT_WORKFLOW.md)** - Panduan lengkap step-by-step
- **[Team Coordination](TEAM_COORDINATION.md)** - Strategi menghindari conflict
- **[GitHub Setup](GITHUB_SETUP.md)** - Setup repository dari awal
- **[Quick Reference](GIT_QUICK_REFERENCE.md)** - Cheat sheet command

---

## Git Helper Script

```bash
# Lihat semua command
bash scripts/git-helper.sh help

# Command yang tersedia:
start-work     # Mulai fitur baru
daily-sync     # Sync dengan dev
quick-commit   # Quick commit
ready-pr       # Prepare for PR
cleanup        # Hapus merged branches
status         # Status detail
```

---

## Tips Pro

### Alias untuk Command yang Sering

Tambahkan ke `.bashrc` atau `.bash_profile`:

```bash
# Git aliases
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'
alias gco='git checkout'
alias gpull='git pull origin dev'

# Eligo aliases
alias eligo-start='bash scripts/git-helper.sh start-work'
alias eligo-sync='bash scripts/git-helper.sh daily-sync'
alias eligo-commit='bash scripts/git-helper.sh quick-commit'
```

Setelah itu:
```bash
source ~/.bashrc  # atau source ~/.bash_profile
```

Usage:
```bash
gs                    # git status
ga && gc "feat: ..."  # git add . && git commit -m "feat: ..."
eligo-sync            # daily sync
```

---

## Butuh Bantuan?

1. Cek **[Git Workflow Guide](GIT_WORKFLOW.md)** dulu
2. Tanya di grup tim
3. Jangan panik & jangan force push!

---

**Happy Coding!**

Last Updated: 2026-11-01
