#!/bin/bash
# Git Helper Script untuk Tim Eligo
# Cara pakai: bash scripts/git-helper.sh [command]

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Command: start-work
start_work() {
    print_info "Memulai pekerjaan baru..."
    
    # Pastikan di dev
    git checkout dev
    print_success "Switched to dev branch"
    
    # Pull latest
    print_info "Pulling latest changes from dev..."
    git pull origin dev
    print_success "Dev branch updated"
    
    # Minta nama branch
    echo ""
    read -p "Nama fitur yang akan dikerjakan (contoh: kandidat-crud): " feature_name
    
    # Validasi input
    if [ -z "$feature_name" ]; then
        print_error "Nama fitur tidak boleh kosong!"
        exit 1
    fi
    
    # Generate branch name dengan format tanggal
    today=$(date +%y%m%d)
    branch_name="feature/${today}-${feature_name}"
    
    # Buat dan checkout branch baru
    git checkout -b "$branch_name"
    print_success "Created and switched to branch: $branch_name"
    
    echo ""
    print_info "Siap untuk mulai coding!"
    print_info "Jangan lupa commit sering ya!"
}

# Command: daily-sync
daily_sync() {
    print_info "Syncing dengan dev branch..."
    
    # Simpan branch saat ini
    current_branch=$(git branch --show-current)
    
    if [ "$current_branch" == "dev" ] || [ "$current_branch" == "main" ]; then
        print_warning "Kamu di branch $current_branch, tidak perlu sync"
        git pull origin "$current_branch"
        exit 0
    fi
    
    print_info "Current branch: $current_branch"
    
    # Cek apakah ada uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "Ada perubahan yang belum di-commit!"
        read -p "Mau di-stash dulu? (y/n): " stash_choice
        if [ "$stash_choice" == "y" ]; then
            git stash
            print_success "Changes stashed"
        else
            print_error "Please commit or stash your changes first"
            exit 1
        fi
    fi
    
    # Update dev
    git checkout dev
    git pull origin dev
    print_success "Dev branch updated"
    
    # Kembali ke branch kerja
    git checkout "$current_branch"
    print_success "Switched back to $current_branch"
    
    # Merge dev
    print_info "Merging dev into $current_branch..."
    if git merge dev --no-edit; then
        print_success "Merge successful!"
    else
        print_error "Merge conflict detected!"
        print_info "Please resolve conflicts manually:"
        print_info "  1. Fix conflicts in marked files"
        print_info "  2. git add <resolved-files>"
        print_info "  3. git commit"
        exit 1
    fi
    
    # Restore stash if exists
    if [ "$stash_choice" == "y" ]; then
        print_info "Restoring stashed changes..."
        git stash pop
        print_success "Stash restored"
    fi
    
    echo ""
    print_success "Daily sync completed!"
}

# Command: quick-commit
quick_commit() {
    print_info "Quick commit..."
    
    # Tampilkan status
    echo ""
    print_info "File yang berubah:"
    git status --short
    echo ""
    
    # Konfirmasi
    read -p "Commit semua perubahan ini? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        print_info "Cancelled"
        exit 0
    fi
    
    # Minta commit message
    echo ""
    echo "Pilih tipe commit:"
    echo "  1. feat     - Fitur baru"
    echo "  2. fix      - Bug fix"
    echo "  3. refactor - Refactoring"
    echo "  4. test     - Update test"
    echo "  5. docs     - Update dokumentasi"
    echo "  6. chore    - Config/dependencies"
    read -p "Pilih (1-6): " commit_type
    
    case $commit_type in
        1) type_prefix="feat" ;;
        2) type_prefix="fix" ;;
        3) type_prefix="refactor" ;;
        4) type_prefix="test" ;;
        5) type_prefix="docs" ;;
        6) type_prefix="chore" ;;
        *) print_error "Invalid choice"; exit 1 ;;
    esac
    
    read -p "Deskripsi singkat: " description
    
    if [ -z "$description" ]; then
        print_error "Deskripsi tidak boleh kosong!"
        exit 1
    fi
    
    # Commit
    git add .
    git commit -m "${type_prefix}: ${description}"
    print_success "Committed: ${type_prefix}: ${description}"
    
    # Tanya mau push atau tidak
    echo ""
    read -p "Push ke remote sekarang? (y/n): " push_confirm
    if [ "$push_confirm" == "y" ]; then
        current_branch=$(git branch --show-current)
        git push origin "$current_branch"
        print_success "Pushed to origin/$current_branch"
    fi
}

# Command: ready-pr
ready_pr() {
    print_info "Preparing for Pull Request..."
    
    current_branch=$(git branch --show-current)
    
    if [ "$current_branch" == "dev" ] || [ "$current_branch" == "main" ]; then
        print_error "Tidak bisa buat PR dari branch $current_branch!"
        exit 1
    fi
    
    # Cek uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_error "Masih ada perubahan yang belum di-commit!"
        print_info "Jalankan: bash scripts/git-helper.sh quick-commit"
        exit 1
    fi
    
    # Sync dengan dev
    print_info "Syncing dengan dev terakhir kali..."
    git checkout dev
    git pull origin dev
    git checkout "$current_branch"
    git merge dev --no-edit
    print_success "Synced with dev"
    
    # Push
    print_info "Pushing branch ke remote..."
    git push origin "$current_branch"
    print_success "Pushed to origin/$current_branch"
    
    # Info
    echo ""
    print_success "Branch siap untuk PR!"
    print_info "Langkah selanjutnya:"
    print_info "  1. Buka GitHub repository"
    print_info "  2. Klik 'Pull Requests' → 'New Pull Request'"
    print_info "  3. Base: dev, Compare: $current_branch"
    print_info "  4. Isi template PR"
    print_info "  5. Minta review dari tim"
}

# Command: cleanup
cleanup() {
    print_info "Cleaning up merged branches..."
    
    # Ke dev
    git checkout dev
    git pull origin dev
    print_success "Updated dev"
    
    # List merged branches
    echo ""
    print_info "Branch yang sudah di-merge:"
    merged_branches=$(git branch --merged | grep -v "^\*" | grep -v "dev" | grep -v "main")
    
    if [ -z "$merged_branches" ]; then
        print_info "Tidak ada branch yang perlu dibersihkan"
        exit 0
    fi
    
    echo "$merged_branches"
    echo ""
    
    read -p "Hapus branch-branch ini? (y/n): " confirm
    if [ "$confirm" == "y" ]; then
        echo "$merged_branches" | xargs git branch -d
        print_success "Branch lokal dibersihkan"
        
        # Prune remote
        git remote prune origin
        print_success "Remote references dibersihkan"
    fi
}

# Command: status
show_status() {
    print_info "Git Status Summary"
    echo ""
    
    # Current branch
    current_branch=$(git branch --show-current)
    print_info "Current branch: ${GREEN}$current_branch${NC}"
    
    # Uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "Ada perubahan yang belum di-commit:"
        git status --short
    else
        print_success "Working tree clean"
    fi
    
    echo ""
    
    # Behind/ahead
    git fetch origin --quiet
    ahead=$(git rev-list --count origin/"$current_branch".."$current_branch" 2>/dev/null || echo "0")
    behind=$(git rev-list --count "$current_branch"..origin/"$current_branch" 2>/dev/null || echo "0")
    
    if [ "$ahead" -gt 0 ]; then
        print_warning "Branch kamu $ahead commit ahead of origin"
        print_info "Jangan lupa push!"
    fi
    
    if [ "$behind" -gt 0 ]; then
        print_warning "Branch kamu $behind commit behind origin"
        print_info "Jalankan: git pull origin $current_branch"
    fi
    
    if [ "$ahead" -eq 0 ] && [ "$behind" -eq 0 ]; then
        print_success "Branch kamu up-to-date dengan origin"
    fi
}

# Main menu
show_help() {
    echo ""
    echo "Git Helper"
    echo ""
    echo "Commands:"
    echo "  start-work    - Mulai pekerjaan baru (buat branch baru dari dev)"
    echo "  daily-sync    - Sync branch kamu dengan dev terbaru"
    echo "  quick-commit  - Quick commit dengan interactive prompt"
    echo "  ready-pr      - Persiapkan branch untuk Pull Request"
    echo "  cleanup       - Hapus branch lokal yang sudah di-merge"
    echo "  status        - Tampilkan status git detail"
    echo "  help          - Tampilkan help ini"
    echo ""
    echo "Contoh:"
    echo "  bash scripts/git-helper.sh start-work"
    echo "  bash scripts/git-helper.sh daily-sync"
    echo ""
}

# Main
case "${1:-help}" in
    start-work)
        start_work
        ;;
    daily-sync)
        daily_sync
        ;;
    quick-commit)
        quick_commit
        ;;
    ready-pr)
        ready_pr
        ;;
    cleanup)
        cleanup
        ;;
    status)
        show_status
        ;;
    help|*)
        show_help
        ;;
esac
