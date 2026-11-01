# Setup GitHub Repository - Panduan Lengkap

## Tujuan
Menyiapkan repository GitHub untuk tim Eligo agar siap untuk kolaborasi tanpa merge conflict.

---

## Persiapan

### Yang Dibutuhkan:
1. Akun GitHub (buat di https://github.com jika belum punya)
2. Git terinstall di komputer
3. Proyek Eligo sudah ada di lokal

---

## Langkah 1: Buat Repository di GitHub

### A. Via Website GitHub

1. **Login ke GitHub**
   - Buka https://github.com
   - Login dengan akun kamu

2. **Buat Repository Baru**
   - Klik tombol **"+"** di pojok kanan atas
   - Pilih **"New repository"**

3. **Isi Detail Repository**
   ```
   Repository name: Eligo
   Description: Sistem Pemeringkatan Siswa Eligible SNBP
   Visibility: 
     - Public (jika mau terbuka)
     - Private (jika mau tertutup untuk tim saja)
   
   JANGAN centang:
    Add a README file
    Add .gitignore
    Choose a license
   
   (Karena kita sudah punya file ini di lokal)
   ```

4. **Klik "Create repository"**

5. **Copy URL Repository**
   - Setelah dibuat, akan muncul URL seperti:
   - HTTPS: `https://github.com/username/Eligo.git`
   - SSH: `git@github.com:username/Eligo.git`
   - Copy URL ini (pilih HTTPS jika belum setup SSH)

---

## Langkah 2: Hubungkan Lokal dengan GitHub

Buka terminal di folder proyek Eligo:

```bash
cd c:/Users/ADVAN/Desktop/Eligo
```

### A. Cek Status Git Lokal

```bash
# Cek apakah sudah ada git init
git status

# Jika belum ada, init dulu:
git init
```

### B. Setup Remote Repository

```bash
# Tambahkan remote (ganti URL dengan URL repo kamu)
git remote add origin https://github.com/username/Eligo.git

# Cek apakah sudah terhubung
git remote -v
```

Output yang benar:
```
origin  https://github.com/username/Eligo.git (fetch)
origin  https://github.com/username/Eligo.git (push)
```

### C. Setup Branch Utama

```bash
# Pastikan branch utama bernama 'main'
git branch -M main
```

---

## Langkah 3: Push Kode Pertama Kali

### A. Review File yang Akan Di-commit

```bash
# Lihat file apa saja
git status

# Pastikan .gitignore sudah benar
cat .gitignore
```

### B. Commit Initial Code

```bash
# Stage semua file
git add .

# Cek apa yang akan di-commit
git status

# Commit
git commit -m "chore: initial commit - project setup"
```

### C. Push ke GitHub

```bash
# Push ke branch main
git push -u origin main
```

**Catatan:** Jika muncul error authentication:
- Windows: Akan muncul dialog login GitHub
- Linux/Mac: Mungkin perlu setup SSH key atau Personal Access Token

---

## Langkah 4: Buat Branch Development

```bash
# Buat branch dev dari main
git checkout -b dev

# Push branch dev ke GitHub
git push -u origin dev
```

---

## Langkah 5: Setup Repository Settings di GitHub

### A. Set Default Branch ke 'dev'

1. Buka repository di GitHub
2. Klik **Settings** (tab di atas)
3. Klik **Branches** (menu kiri)
4. Di "Default branch", klik tombol switch/panah
5. Pilih **dev**
6. Klik **Update**
7. Konfirmasi "I understand, update the default branch"

**Kenapa?** Agar semua PR otomatis target ke `dev`, bukan `main`

### B. Setup Branch Protection (RECOMMENDED)

**Untuk Branch `main`:**

1. Masih di **Settings → Branches**
2. Klik **"Add branch protection rule"**
3. Branch name pattern: `main`
4. Centang:
   -  **Require a pull request before merging**
     -  Require approvals: 1
   -  **Require status checks to pass before merging** (jika ada CI/CD)
   -  **Do not allow bypassing the above settings**
5. Klik **Create**

**Untuk Branch `dev`:**

1. Klik **"Add branch protection rule"** lagi
2. Branch name pattern: `dev`
3. Centang:
   -  **Require a pull request before merging**
     -  Require approvals: 1
   - ⬜ Yang lain optional
4. Klik **Create**

**Manfaat:**
- Tidak ada yang bisa langsung push ke `main` atau `dev`
- Semua perubahan harus via Pull Request
- Minimal 1 orang harus review sebelum merge

### C. Setup PR Template (Sudah Ada)

PR template sudah dibuat di `.github/pull_request_template.md`. GitHub akan otomatis menggunakannya.

---

## Langkah 6: Invite Anggota Tim

### A. Invite Collaborators

1. Di repository, klik **Settings**
2. Klik **Collaborators** (atau "Collaborators and teams")
3. Klik **Add people**
4. Masukkan username GitHub anggota tim:
   - Rafliza (username GitHub: ...)
   - Ghaida (username GitHub: ...)
   - Fadli (username GitHub: ...)
5. Pilih role: **Write** (bisa push, buat branch, buat PR)
6. Klik **Add**

### B. Anggota Tim Menerima Invitation

Setiap anggota akan dapat email. Harus:
1. Buka email dari GitHub
2. Klik **Accept invitation**
3. Atau buka langsung: `https://github.com/username/Eligo/invitations`

---

## Langkah 7: Anggota Tim Clone Repository

Setiap anggota tim jalankan:

```bash
# Clone repository
git clone https://github.com/username/Eligo.git

# Masuk ke folder
cd Eligo

# Setup branch tracking
git fetch origin
git checkout main
git checkout dev

# Setup virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# atau: source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Test aplikasi
python main.py
```

---

## Langkah 8: Verifikasi Setup

### Checklist untuk Setiap Anggota:

```bash
# 1. Cek remote
git remote -v
# Output harus ada origin ke GitHub

# 2. Cek branch
git branch -a
# Output harus ada:
#  * dev
#  main
#  remotes/origin/dev
#  remotes/origin/main

# 3. Cek status
git status
# Output: On branch dev, working tree clean

# 4. Test pull
git pull origin dev
# Output: Already up to date

# 5. Test buat branch
git checkout -b feature/test-setup
# Output: Switched to a new branch 'feature/test-setup'

# 6. Cleanup test
git checkout dev
git branch -d feature/test-setup
```

Jika semua command di atas berhasil, setup sudah benar! 

---

## Workflow Setelah Setup

Setelah semua setup selesai, setiap anggota tim:

### Daily Workflow:

```bash
# 1. PAGI - Update dari remote
git checkout dev
git pull origin dev

# 2. Buat branch untuk pekerjaan hari ini
git checkout -b feature/241101-nama-fitur

# 3. KERJA - Commit sering
[edit code]
git add .
git commit -m "feat: deskripsi"
[repeat]

# 4. Push ke remote
git push origin feature/241101-nama-fitur

# 5. Buat Pull Request di GitHub
# 6. Minta review dari tim
# 7. Merge setelah approved

# 8. CLEANUP
git checkout dev
git pull origin dev
git branch -d feature/241101-nama-fitur
```

---

## Troubleshooting Setup

### Problem 1: "remote origin already exists"

```bash
# Lihat remote yang ada
git remote -v

# Jika salah, remove dan add lagi
git remote remove origin
git remote add origin https://github.com/username/Eligo.git
```

### Problem 2: "fatal: refusing to merge unrelated histories"

```bash
# Jika GitHub punya initial commit yang berbeda
git pull origin main --allow-unrelated-histories
```

### Problem 3: Authentication Failed

**Windows:**
```bash
# Use GitHub CLI (recommended)
# Install dari: https://cli.github.com
gh auth login

# Atau use credential manager
git config --global credential.helper manager
```

**Linux/Mac:**
```bash
# Setup SSH key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"
# Follow instructions
# Add SSH key to GitHub: Settings → SSH Keys

# Atau use Personal Access Token
# GitHub → Settings → Developer settings → Personal access tokens
# Copy token dan paste saat diminta password
```

### Problem 4: "src refspec main does not match any"

```bash
# Pastikan sudah ada commit
git status

# Jika belum ada commit
git add .
git commit -m "chore: initial commit"
git push -u origin main
```

### Problem 5: Can't Push to Protected Branch

```bash
# Jangan push langsung ke main/dev!
# Selalu buat branch dulu
git checkout -b feature/your-feature
git push origin feature/your-feature
# Lalu buat PR di GitHub
```

---

## Optional: Setup GitHub Projects

Untuk tracking task lebih mudah:

1. Di repository, klik tab **Projects**
2. Klik **New project**
3. Pilih template: **Board**
4. Buat kolom:
   - **To Do**
   - **In Progress**
   - **In Review**
   - **Done**
5. Tambahkan task sebagai "issues"
6. Drag-drop issue antar kolom sesuai progress

---

## Best Practices Setelah Setup

1. **Main branch = Production**
   - Hanya code yang sudah final
   - Merge dari dev setelah sprint selesai

2. **Dev branch = Integration**
   - Tempat merge semua feature branch
   - Harus selalu dalam kondisi runnable

3. **Feature branches = Individual work**
   - 1 branch = 1 fitur/task
   - Hidup singkat (1-3 hari)
   - Merge via PR setelah selesai

4. **Komunikasi**
   - Kasih tau di grup sebelum merge ke dev
   - Review PR orang lain
   - Standup harian

---

## Kontak & Bantuan

Jika ada masalah saat setup:

1. Screenshot error message
2. Tanya di grup tim
3. Jangan force push / delete branch utama!

---

## Setup Checklist

Pastikan semua ini sudah dilakukan:

**Owner/Lead:**
- [ ] Repository dibuat di GitHub
- [ ] Branch protection rules di-setup
- [ ] Semua anggota di-invite
- [ ] Default branch di-set ke `dev`

**Setiap Anggota:**
- [ ] Invitation accepted
- [ ] Repository di-clone
- [ ] Virtual environment di-setup
- [ ] Dependencies terinstall
- [ ] Aplikasi bisa dijalankan
- [ ] Test buat branch berhasil
- [ ] Sudah baca Git Workflow Guide

---

**Setup selesai! Siap kolaborasi! **

Last Updated: 2026-11-01
