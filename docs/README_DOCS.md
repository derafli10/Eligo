# Dokumentasi Tim Eligo - Index

Selamat datang di pusat dokumentasi proyek Eligo! Semua panduan yang kamu butuhkan ada di sini.

---

## Quick Start (Mulai dari Sini!)

### Untuk Tech Lead / Project Manager:
1. **[Rebuild Strategy](REBUILD_STRATEGY.md)** - Copy & Understand approach (2 minggu!)
2. **[GitHub Setup](GITHUB_SETUP.md)** - Setup repository GitHub dari awal
3. **[Task Division](TASK_DIVISION.md)** - Pembagian tugas antar anggota tim

### Untuk Semua Anggota Tim:
1. **[Rebuild Strategy](REBUILD_STRATEGY.md)** - **BACA INI DULU!** (Copy & Understand)
2. **[Quick Start Rebuild](QUICK_START_REBUILD.md)** - Panduan 2 minggu step-by-step
3. **[Quick Start Git](QUICK_START_GIT.md)** - Git workflow cepat
4. **[Git Quick Reference](GIT_QUICK_REFERENCE.md)** - Cheat sheet command (cetak/bookmark!)

---

## Dokumentasi Lengkap

### Git & GitHub Workflow

| Dokumen | Deskripsi | Untuk Siapa | Prioritas |
|---------|-----------|-------------|-----------|
| **[Quick Start Rebuild](QUICK_START_REBUILD.md)** | Panduan rebuild 2 minggu step-by-step | Semua | **VERY HIGH** |
| **[Quick Start Git](QUICK_START_GIT.md)** | Panduan super cepat mulai kerja | Semua |  |
| **[Git Workflow](GIT_WORKFLOW.md)** | Panduan lengkap workflow Git dari A-Z | Semua |  |
| **[Git Quick Reference](GIT_QUICK_REFERENCE.md)** | Cheat sheet command Git | Semua |  |
| **[GitHub Setup](GITHUB_SETUP.md)** | Setup repository GitHub pertama kali | Tech Lead |  |
| **[Project Structure](PROJECT_STRUCTURE.md)** | Struktur file & folder lengkap | Semua |  |
| **[Project Timeline](PROJECT_TIMELINE.md)** | Timeline & estimasi waktu 1 bulan | Tech Lead | High |
| **[Rebuild Strategy](REBUILD_STRATEGY.md)** | Copy & Understand vs Build (2 minggu!) | Tech Lead | **VERY HIGH** |
| **[Team Coordination](TEAM_COORDINATION.md)** | Strategi koordinasi & hindari conflict | Semua |  |
| **[Task Division](TASK_DIVISION.md)** | Pembagian tugas & area kerja (40-30-30) | Tech Lead |  |
| **[Team Breakdown](TEAM_BREAKDOWN.md)** | Detail breakdown per anggota tim | Semua |  |

---

## Panduan per Role

### ‍ Tech Lead / Project Manager

**Setup Awal:**
1. Baca [GitHub Setup](GITHUB_SETUP.md)
2. Setup repository di GitHub
3. Baca [Task Division](TASK_DIVISION.md) & [Team Breakdown](TEAM_BREAKDOWN.md)
4. Assign tugas ke anggota tim
5. Setup GitHub Projects board

**Daily:**
- Monitor PR dan merge conflicts
- Facilitate standup meeting
- Review & merge PR

**Checklist:**
```
□ Repository created di GitHub
□ All team members invited
□ Branch protection rules active
□ Default branch set to 'dev'
□ GitHub Projects board setup
□ Tasks assigned
```

---

### ‍ Developer (Rafliza - Presentation + Infrastructure)

**Area Kerja (40%):**
```
eligo/presentation/cli/      (semua menu + formatter)
eligo/infrastructure/        (repositories + atomic_writer)
domain/repositories.py       (interfaces)
main.py
data/*.json & *.bak
```

**Quick Start:**
1. Clone repo (lihat [Quick Start Git](QUICK_START_GIT.md))
2. Baca area tugas di [Task Division](TASK_DIVISION.md)
3. Mulai kerja di branch sendiri

**Daily Workflow:**
```bash
bash scripts/git-helper.sh start-work
# [kerja di infrastructure layer]
bash scripts/git-helper.sh quick-commit
bash scripts/git-helper.sh ready-pr
```

---

### ‍ Developer (Fadli - Application Services + CSV)

**Area Kerja (30%):**
```
eligo/application/           (semua services)
eligo/infrastructure/        (csv_parser.py)
```

**Quick Start:**
1. Clone repo (lihat [Quick Start Git](QUICK_START_GIT.md))
2. Baca area tugas di [Task Division](TASK_DIVISION.md)
3. Mulai kerja di branch sendiri

**Daily Workflow:**
```bash
bash scripts/git-helper.sh daily-sync  # Setiap pagi!
# [kerja di domain layer]
bash scripts/git-helper.sh quick-commit
```

---

### ‍ Developer (Ghaida - Domain Core + Algorithms)

**Area Kerja (30%):**
```
eligo/domain/                (semua domain logic)
eligo/application/           (ranking_service.py)
```

**Quick Start:**
1. Clone repo (lihat [Quick Start Git](QUICK_START_GIT.md))
2. Baca area tugas di [Task Division](TASK_DIVISION.md)
3. Mulai kerja di branch sendiri

**Daily Workflow:**
```bash
bash scripts/git-helper.sh start-work
# [kerja di presentation layer]
bash scripts/git-helper.sh quick-commit
```

---

## ️ Git Helper Scripts

Semua script ada di folder `scripts/`:

### `git-helper.sh` - Main Helper

```bash
bash scripts/git-helper.sh help           # Lihat semua command
bash scripts/git-helper.sh start-work     # Mulai fitur baru
bash scripts/git-helper.sh daily-sync     # Sync dengan dev
bash scripts/git-helper.sh quick-commit   # Quick commit
bash scripts/git-helper.sh ready-pr       # Prepare for PR
bash scripts/git-helper.sh cleanup        # Hapus merged branches
bash scripts/git-helper.sh status         # Status detail
```

### `setup-git-local.sh` - Initial Setup

```bash
bash scripts/setup-git-local.sh
# Jalankan sekali untuk initialize git repository
```

---

## Daily Checklist

### Pagi (Sebelum Mulai Kerja)

```
□ Buka terminal & masuk ke folder Eligo
□ Aktivasi virtual environment
□ Jalankan: bash scripts/git-helper.sh daily-sync
□ Kasih tau tim di grup: "Hari ini kerja di X"
□ Lihat PR yang perlu direview
```

### Selama Kerja

```
□ Edit code di area kamu
□ Test perubahan: python main.py
□ Commit setiap 1-2 jam:
   bash scripts/git-helper.sh quick-commit
□ Push progress: git push origin feature/branch-kamu
```

### Sore (Sebelum Pulang)

```
□ Commit semua perubahan
□ Push ke remote
□ Update status di project board
□ Review minimal 1 PR dari teman
□ Kasih tau progress di grup
```

---

## Troubleshooting

### Problem: Git command tidak jalan

**Solusi:**
```bash
# Cek apakah di folder yang benar
pwd

# Cek git status
git status

# Lihat panduan: docs/GIT_WORKFLOW.md → Troubleshooting
```

### Problem: Merge Conflict

**Solusi:**
```bash
# Lihat file yang conflict
git status

# Baca panduan: docs/TEAM_COORDINATION.md → Menangani Conflict
# Atau docs/GIT_QUICK_REFERENCE.md → Resolve Conflict
```

### Problem: Lupa Command

**Solusi:**
```bash
# Lihat cheat sheet
cat docs/GIT_QUICK_REFERENCE.md

# Atau gunakan helper
bash scripts/git-helper.sh help
```

### Problem: Tidak Tahu Harus Ngapain

**Solusi:**
1. Baca [Quick Start Git](QUICK_START_GIT.md)
2. Baca [Task Division](TASK_DIVISION.md) - cari area kerja kamu
3. Tanya di grup tim
4. Pair programming dengan teman

---

## Komunikasi

### Daily Communication:
- **WhatsApp/Telegram Group**: Quick questions, updates
- **GitHub PR Comments**: Code review
- **GitHub Issues**: Bug reports, feature requests

### Meetings:
- **Daily Standup (15 min)**: Setiap pagi
- **Weekly Review (1 hour)**: Setiap Jumat
- **Pair Programming**: As needed

---

## Learning Path

### Week 1: Basics 
```
□ Setup environment
□ Clone repository
□ Buat branch pertama
□ Commit & push
□ Buat PR pertama
```

### Week 2: Workflow 
```
□ Daily sync routine
□ Review PR orang lain
□ Resolve simple conflict
□ Coordinate dengan tim
```

### Week 3+: Advanced 
```
□ Cherry-pick commit
□ Rebase branch
□ Git hooks
□ Advanced conflict resolution
```

---

## Resources External

### Git Learning:
- [Git Official Docs](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)

### Python:
- [Python Official Docs](https://docs.python.org/3/)
- [Real Python](https://realpython.com/)

### Clean Architecture:
- Robert C. Martin - Clean Architecture book
- [Clean Coder Blog](https://blog.cleancoder.com/)

---

## Diagram Workflow

### Git Branch Flow:

```
main (production)
  └── dev (integration)
       ├── feature/241101-school-crud-rafliza
       │    └── (work here) → PR → merge to dev
       │
       ├── feature/241101-calculator-ghaida
       │    └── (work here) → PR → merge to dev
       │
       └── feature/241101-menu-ui-fadli
            └── (work here) → PR → merge to dev
```

### Daily Workflow:

```
Morning:
  git pull origin dev
  git checkout -b feature/new-feature
     ↓
Working:
  [edit code]
  git add .
  git commit -m "..."
  [repeat]
     ↓
Evening:
  git push origin feature/new-feature
  [create PR on GitHub]
     ↓
After Review:
  [merge PR]
  git checkout dev
  git pull origin dev
  git branch -d feature/new-feature
```

---

## Success Checklist

### Repository Setup 
```
□ GitHub repository created
□ All members invited & accepted
□ Branch protection enabled
□ Default branch set to dev
□ PR template working
```

### Team Onboarding 
```
□ All members cloned repository
□ Virtual environment setup
□ Can run application locally
□ First branch & commit successful
□ First PR created & merged
```

### Workflow Established 
```
□ Daily standup routine
□ PR review process working
□ Zero to minimal conflicts
□ Documentation being updated
□ Good commit message quality
```

---

## Best Practices Summary

### Git:
1. **Pull before push** - Always sync first
2. **Commit often** - Small, focused commits
3. **Clear messages** - Use conventional commit format
4. **Review promptly** - Don't let PRs sit
5. **Test before commit** - Code should work

### Team:
1. **Communicate early** - Don't surprise teammates
2. **Own your area** - Take responsibility for your layer
3. **Help others** - Review PRs, answer questions
4. **Document changes** - Update docs when needed
5. **Learn together** - Share knowledge

### Code:
1. **Follow structure** - Respect layer boundaries
2. **Write tests** - Test your code
3. **Type hints** - Use Python type annotations
4. **Docstrings** - Document functions/classes
5. **Lint & format** - Run ruff & mypy

---

## Quick Links

| Dokumen | Link |
|---------|------|
| Quick Start | [QUICK_START_GIT.md](QUICK_START_GIT.md) |
| Git Workflow | [GIT_WORKFLOW.md](GIT_WORKFLOW.md) |
| Cheat Sheet | [GIT_QUICK_REFERENCE.md](GIT_QUICK_REFERENCE.md) |
| Team Coordination | [TEAM_COORDINATION.md](TEAM_COORDINATION.md) |
| Task Division | [TASK_DIVISION.md](TASK_DIVISION.md) |
| Team Breakdown | [TEAM_BREAKDOWN.md](TEAM_BREAKDOWN.md) |
| GitHub Setup | [GITHUB_SETUP.md](GITHUB_SETUP.md) |
| Project Structure | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |

---

## Notes

- **Semua dokumentasi dalam Bahasa Indonesia** untuk kemudahan tim
- **Update dokumentasi** jika ada perubahan workflow
- **Feedback welcome** - suggest improvements via PR or Issues

---

**Dibuat dengan ️ untuk Tim Eligo**

Last Updated: 2026-11-01

---

## Tidak Menemukan yang Dicari?

1. Cek index di atas
2. Search di GitHub repository
3. Tanya di grup tim
4. Buat issue di GitHub untuk suggest dokumentasi baru

**Happy Coding! **
