# Git Quick Reference Card 

Cetak atau simpan ini sebagai cheat sheet!

---

## Daily Workflow

```bash
# === PAGI (Sebelum Mulai Kerja) ===
git checkout dev
git pull origin dev
git checkout feature/branch-kamu
git merge dev

# === SELAMA KERJA ===
git status                              # Cek perubahan
git add .                               # Stage perubahan
git commit -m "feat: deskripsi"        # Commit
git push origin feature/branch-kamu    # Push

# === SORE (Sebelum Pulang) ===
git add .
git commit -m "wip: progress hari ini"
git push origin feature/branch-kamu
```

---

## Mulai Fitur Baru

```bash
# Dengan script helper (RECOMMENDED):
bash scripts/git-helper.sh start-work

# Manual:
git checkout dev
git pull origin dev
git checkout -b feature/YYMMDD-nama-fitur
```

---

## Commit Format

```bash
git commit -m "feat: tambah fungsi create_kandidat"
git commit -m "fix: perbaiki bug di scoring"
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

## Update dari Dev

```bash
# Dengan script helper:
bash scripts/git-helper.sh daily-sync

# Manual:
git checkout dev
git pull origin dev
git checkout feature/branch-kamu
git merge dev
```

---

## Push & Pull Request

```bash
# 1. Push branch
git push origin feature/branch-kamu

# 2. Buka GitHub → Buat PR
#   Base: dev
#   Compare: feature/branch-kamu

# 3. Isi template PR
# 4. Minta review
# 5. Merge setelah approved

# 6. Cleanup
git checkout dev
git pull origin dev
git branch -d feature/branch-kamu
```

---

## Useful Commands

```bash
# Lihat status
git status                    # Status detail
git status -s                 # Status ringkas
git log --oneline            # History commit

# Lihat perubahan
git diff                      # Perubahan yang belum di-stage
git diff --staged            # Perubahan yang sudah di-stage
git diff dev                 # Banding dengan dev

# Branch management
git branch                    # Lihat branch lokal
git branch -a                # Lihat semua branch
git branch -d branch-name    # Hapus branch lokal

# Remote
git fetch origin             # Update info dari remote
git remote -v                # Lihat remote URL
```

---

## Emergency Commands

```bash
# Batalkan perubahan (HATI-HATI!)
git checkout -- file.txt      # Batalkan 1 file
git reset --hard             # Batalkan SEMUA (DANGEROUS!)

# Batalkan commit terakhir
git reset --soft HEAD~1      # Perubahan masih ada
git reset --hard HEAD~1      # Perubahan HILANG (DANGEROUS!)

# Simpan perubahan sementara
git stash                     # Simpan
git stash list               # Lihat stash
git stash pop                # Restore stash terakhir

# Lihat siapa yang edit file
git blame file.py            # Detail per baris
git log -p file.py           # History perubahan file
```

---

## Resolve Conflict

```bash
# 1. Lihat file yang conflict
git status

# 2. Buka file, cari marker:
#   <<<<<<< HEAD
#   kode kamu
#   =======  
#   kode orang lain
#   >>>>>>> branch-name

# 3. Edit manual, pilih/gabung kode
# 4. Hapus marker (<<<<, ====, >>>>)

# 5. Test kode

# 6. Resolve
git add file-yang-conflict.py
git commit -m "fix: resolve merge conflict"
git push origin feature/branch-kamu
```

---

## ️ Git Helper Script

```bash
# Lihat semua command
bash scripts/git-helper.sh help

# Command yang tersedia:
bash scripts/git-helper.sh start-work     # Mulai fitur baru
bash scripts/git-helper.sh daily-sync     # Sync dengan dev
bash scripts/git-helper.sh quick-commit   # Quick commit
bash scripts/git-helper.sh ready-pr       # Prepare for PR
bash scripts/git-helper.sh cleanup        # Hapus merged branches
bash scripts/git-helper.sh status         # Status detail
```

---

## Checklist Harian

**Pagi:**
- [ ] `git checkout dev`
- [ ] `git pull origin dev`
- [ ] Kasih tau tim mau kerja di mana

**Kerja:**
- [ ] Commit minimal setiap 1-2 jam
- [ ] Push minimal 1x sehari

**Sore:**
- [ ] Push progress hari ini
- [ ] Review minimal 1 PR

---

## Golden Rules

1. **Jangan pernah** force push tanpa persetujuan tim
2. **Selalu** pull sebelum push
3. **Commit sering**, message jelas
4. **Komunikasi** sebelum edit file yang sama
5. **Review** PR orang lain
6. **Test** sebelum commit
7. **Sync** dengan dev setiap hari

---

## Kalau Ada Masalah

1. **STOP** - Jangan edit apa-apa
2. **BACKUP** - Copy folder project
3. **TANYA** - Hubungi tim/tech lead
4. **SCREENSHOT** - Error message
5. **JANGAN** panic force push!

---

## Resources

- Full Guide: `docs/GIT_WORKFLOW.md`
- Team Coordination: `docs/TEAM_COORDINATION.md`
- GitHub: https://github.com/your-repo

---

**Print atau save cheat sheet ini! **

Last Updated: 2026-11-01
