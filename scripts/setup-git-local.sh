#!/bin/bash
# Setup Git Repository Lokal untuk Eligo
# Jalankan sekali saja untuk inisialisasi git

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Setup Git Repository Lokal - Eligo${NC}"
echo ""

# 1. Cek apakah sudah git init
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git repository sudah ada!${NC}"
    read -p "Ingin re-initialize? (y/n): " reinit
    if [ "$reinit" != "y" ]; then
        echo "Setup dibatalkan."
        exit 0
    fi
fi

# 2. Initialize git
echo -e "${BLUE}Initializing git repository...${NC}"
git init
echo -e "${GREEN}✓ Git initialized${NC}"

# 3. Setup main branch
echo -e "${BLUE}Setting up main branch...${NC}"
git branch -M main
echo -e "${GREEN}✓ Main branch created${NC}"

# 4. Add all files
echo -e "${BLUE}Adding files...${NC}"
git add .
echo -e "${GREEN}✓ Files staged${NC}"

# 5. Initial commit
echo -e "${BLUE}Creating initial commit...${NC}"
git commit -m "chore: initial commit - project setup

- Setup proyek Eligo (Sistem Pemeringkatan SNBP)
- Struktur folder: models, views, controllers, services, utils
- Setup dokumentasi: README, Git Workflow, Team Coordination
- Setup testing dengan pytest
- Setup linting dengan ruff dan mypy
- Tim: Rafliza (Data), Ghaida (Algoritma), Fadli (CLI)"

echo -e "${GREEN}✓ Initial commit created${NC}"

# 6. Create dev branch
echo -e "${BLUE}Creating dev branch...${NC}"
git checkout -b dev
echo -e "${GREEN}✓ Dev branch created${NC}"

# 7. Summary
echo ""
echo -e "${GREEN}Git setup selesai!${NC}"
echo ""
echo -e "${BLUE}Status:${NC}"
git log --oneline --all --graph --decorate
echo ""
echo -e "${BLUE}🌿 Branches:${NC}"
git branch -a
echo ""

echo -e "${YELLOW}Langkah selanjutnya:${NC}"
echo "1. Buat repository di GitHub"
echo "2. Jalankan: git remote add origin <URL-REPO>"
echo "3. Jalankan: git push -u origin main"
echo "4. Jalankan: git push -u origin dev"
echo ""
echo "Atau ikuti panduan lengkap di: docs/GITHUB_SETUP.md"
