#!/usr/bin/env bash
# Elektro kurulum betiği
#
#   curl -fsSL https://raw.githubusercontent.com/0anes0/elektro/main/install.sh | bash
#   ./install.sh               # repo klasöründen kurar
#   ./install.sh --uninstall   # kaldırır
#
# Ortam değişkenleri:
#   ELEKTRO_HOME  kurulum klasörü  (varsayılan: ~/.local/share/elektro)
#   ELEKTRO_BIN   komutun konacağı klasör (varsayılan: ~/.local/bin)
#   PYTHON        kullanılacak python (varsayılan: python3)

set -euo pipefail

REPO_URL="https://github.com/0anes0/elektro"
TARBALL_URL="$REPO_URL/archive/refs/heads/main.tar.gz"
PREFIX="${ELEKTRO_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/elektro}"
BIN_DIR="${ELEKTRO_BIN:-$HOME/.local/bin}"
VENV="$PREFIX/venv"
PYTHON="${PYTHON:-python3}"

if [ -t 1 ]; then
    B=$'\033[1m'; G=$'\033[32m'; Y=$'\033[33m'; R=$'\033[31m'; C=$'\033[36m'; N=$'\033[0m'
else
    B=""; G=""; Y=""; R=""; C=""; N=""
fi
info() { printf '%s==>%s %s\n' "$C$B" "$N" "$*"; }
ok()   { printf '%s✓%s %s\n' "$G$B" "$N" "$*"; }
warn() { printf '%s!%s %s\n' "$Y$B" "$N" "$*"; }
die()  { printf '%sHata:%s %s\n' "$R$B" "$N" "$*" >&2; exit 1; }

usage() {
    cat <<'USAGE'
Kullanım: install.sh [--uninstall]

  (seçeneksiz)     Elektro'yu kurar veya yeniden kurar
  -u, --uninstall  Elektro'yu kaldırır

Ortam değişkenleri: ELEKTRO_HOME, ELEKTRO_BIN, PYTHON
USAGE
    exit 0
}

uninstall() {
    info "Elektro kaldırılıyor"
    if [ -L "$BIN_DIR/elektro" ] && [ "$(readlink "$BIN_DIR/elektro")" = "$VENV/bin/elektro" ]; then
        rm -f "$BIN_DIR/elektro"
    fi
    rm -rf "$PREFIX"
    ok "Kaldırıldı"
    exit 0
}

case "${1:-}" in
    -h|--help) usage ;;
    -u|--uninstall) uninstall ;;
    "") ;;
    *) die "bilinmeyen seçenek: $1 (yardım: --help)" ;;
esac

# --- Python kontrolü ----------------------------------------------------------
command -v "$PYTHON" >/dev/null 2>&1 || die "$PYTHON bulunamadı. Python 3.9+ kurun (örn: sudo apt install python3 / sudo pacman -S python)."

"$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 9))' \
    || die "Python 3.9 veya üstü gerekli (bulunan: $("$PYTHON" -V 2>&1))."

"$PYTHON" -c 'import venv, ensurepip' >/dev/null 2>&1 \
    || die "Python venv modülü eksik. Debian/Ubuntu: sudo apt install python3-venv"

# --- Kaynak: repo klasöründen mi, GitHub'dan mı? ------------------------------
SRC="$TARBALL_URL"
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/pyproject.toml" ] && grep -q '^name = "elektro"' "$SCRIPT_DIR/pyproject.toml"; then
        SRC="$SCRIPT_DIR"
    fi
fi

# --- Eski pipx kurulumu -------------------------------------------------------
if command -v pipx >/dev/null 2>&1 && pipx list --short 2>/dev/null | grep -q '^elektro '; then
    warn "pipx ile kurulmuş eski sürüm bulundu, kaldırılıyor"
    pipx uninstall elektro >/dev/null || warn "pipx kaldırması başarısız, devam ediliyor"
fi

# --- Kurulum ------------------------------------------------------------------
info "Sanal ortam oluşturuluyor: $VENV"
rm -rf "$VENV"
mkdir -p "$PREFIX" "$BIN_DIR"
"$PYTHON" -m venv "$VENV"

if [ "$SRC" = "$TARBALL_URL" ]; then
    info "GitHub'dan indiriliyor ve kuruluyor"
else
    info "Yerel klasörden kuruluyor: $SRC"
fi
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --upgrade pip
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check "$SRC" \
    || die "pip kurulumu başarısız"

# `elektro update` bu dosyaya bakarak kurulum türünü anlar
touch "$VENV/.elektro-install"

ln -sf "$VENV/bin/elektro" "$BIN_DIR/elektro"
VERSION="$("$BIN_DIR/elektro" --version 2>/dev/null)" || die "kurulum doğrulanamadı"
ok "$VERSION kuruldu → $BIN_DIR/elektro"

# --- PATH kontrolü ------------------------------------------------------------
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *)
        warn "$BIN_DIR PATH'te değil. Kabuğuna göre ekle:"
        case "$(basename "${SHELL:-bash}")" in
            fish) echo "    fish_add_path $BIN_DIR" ;;
            zsh)  echo "    echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.zshrc && source ~/.zshrc" ;;
            *)    echo "    echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.bashrc && source ~/.bashrc" ;;
        esac
        ;;
esac

echo
echo "  Başlamak için:        ${B}elektro${N}"
echo "  Kabuk tamamlama için: ${B}elektro --install-completion${N}"
echo "  Güncellemek için:     ${B}elektro update${N}"
echo "  Kaldırmak için:       ${B}curl -fsSL $REPO_URL/raw/main/install.sh | bash -s -- --uninstall${N}"
