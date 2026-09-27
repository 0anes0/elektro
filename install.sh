#!/usr/bin/env bash
# Elektro installer / kurulum betiği
#
#   curl -fsSL https://raw.githubusercontent.com/0anes0/elektro/main/install.sh | bash
#   ./install.sh               # install from the repo folder
#   ./install.sh --uninstall   # remove
#
# Environment variables:
#   ELEKTRO_HOME  install folder            (default: ~/.local/share/elektro)
#   ELEKTRO_BIN   folder for the command    (default: ~/.local/bin)
#   ELEKTRO_LANG  message language: en tr de ru (default: system language)
#   PYTHON        python to use             (default: python3)

set -euo pipefail

REPO_URL="https://github.com/0anes0/elektro"
TARBALL_URL="$REPO_URL/archive/refs/heads/main.tar.gz"
PREFIX="${ELEKTRO_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/elektro}"
BIN_DIR="${ELEKTRO_BIN:-$HOME/.local/bin}"
VENV="$PREFIX/venv"
MAN_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/man/man1"
PYTHON="${PYTHON:-python3}"

# --- Dil / language ------------------------------------------------------------
L="${ELEKTRO_LANG:-${LC_ALL:-${LC_MESSAGES:-${LANG:-en}}}}"
L="$(printf '%s' "$L" | cut -c1-2 | tr '[:upper:]' '[:lower:]')"
case "$L" in tr|de|ru) ;; *) L=en ;; esac

# m KEY -> printf şablonu (%s yer tutucuları ile)
m() {
    case "$L:$1" in
        en:error) echo "Error" ;;
        tr:error) echo "Hata" ;;
        de:error) echo "Fehler" ;;
        ru:error) echo "Ошибка" ;;

        en:usage) echo "Usage: install.sh [--uninstall]

  (no option)      install or reinstall elektro
  -u, --uninstall  remove elektro

Environment: ELEKTRO_HOME, ELEKTRO_BIN, ELEKTRO_LANG, PYTHON" ;;
        tr:usage) echo "Kullanım: install.sh [--uninstall]

  (seçeneksiz)     Elektro'yu kurar veya yeniden kurar
  -u, --uninstall  Elektro'yu kaldırır

Ortam değişkenleri: ELEKTRO_HOME, ELEKTRO_BIN, ELEKTRO_LANG, PYTHON" ;;
        de:usage) echo "Aufruf: install.sh [--uninstall]

  (ohne Option)    elektro installieren oder neu installieren
  -u, --uninstall  elektro entfernen

Umgebungsvariablen: ELEKTRO_HOME, ELEKTRO_BIN, ELEKTRO_LANG, PYTHON" ;;
        ru:usage) echo "Использование: install.sh [--uninstall]

  (без параметров) установить или переустановить elektro
  -u, --uninstall  удалить elektro

Переменные окружения: ELEKTRO_HOME, ELEKTRO_BIN, ELEKTRO_LANG, PYTHON" ;;

        en:removing) echo "Removing elektro" ;;
        tr:removing) echo "Elektro kaldırılıyor" ;;
        de:removing) echo "elektro wird entfernt" ;;
        ru:removing) echo "Удаление elektro" ;;
        en:removed) echo "Removed" ;;
        tr:removed) echo "Kaldırıldı" ;;
        de:removed) echo "Entfernt" ;;
        ru:removed) echo "Удалено" ;;

        en:bad_option) echo "unknown option: %s (help: --help)" ;;
        tr:bad_option) echo "bilinmeyen seçenek: %s (yardım: --help)" ;;
        de:bad_option) echo "unbekannte Option: %s (Hilfe: --help)" ;;
        ru:bad_option) echo "неизвестный параметр: %s (справка: --help)" ;;

        en:no_python) echo "%s not found. Install Python 3.9+ (e.g. sudo apt install python3 / sudo pacman -S python)." ;;
        tr:no_python) echo "%s bulunamadı. Python 3.9+ kurun (örn: sudo apt install python3 / sudo pacman -S python)." ;;
        de:no_python) echo "%s nicht gefunden. Python 3.9+ installieren (z. B. sudo apt install python3 / sudo pacman -S python)." ;;
        ru:no_python) echo "%s не найден. Установите Python 3.9+ (напр. sudo apt install python3 / sudo pacman -S python)." ;;

        en:old_python) echo "Python 3.9 or newer is required (found: %s)." ;;
        tr:old_python) echo "Python 3.9 veya üstü gerekli (bulunan: %s)." ;;
        de:old_python) echo "Python 3.9 oder neuer erforderlich (gefunden: %s)." ;;
        ru:old_python) echo "Требуется Python 3.9 или новее (найден: %s)." ;;

        en:no_venv) echo "The Python venv module is missing. Debian/Ubuntu: sudo apt install python3-venv" ;;
        tr:no_venv) echo "Python venv modülü eksik. Debian/Ubuntu: sudo apt install python3-venv" ;;
        de:no_venv) echo "Das Python-Modul venv fehlt. Debian/Ubuntu: sudo apt install python3-venv" ;;
        ru:no_venv) echo "Отсутствует модуль Python venv. Debian/Ubuntu: sudo apt install python3-venv" ;;

        en:pipx_found) echo "Found an old version installed with pipx, removing it" ;;
        tr:pipx_found) echo "pipx ile kurulmuş eski sürüm bulundu, kaldırılıyor" ;;
        de:pipx_found) echo "Alte, mit pipx installierte Version gefunden, wird entfernt" ;;
        ru:pipx_found) echo "Найдена старая версия, установленная через pipx, удаляем" ;;

        en:venv) echo "Creating virtual environment: %s" ;;
        tr:venv) echo "Sanal ortam oluşturuluyor: %s" ;;
        de:venv) echo "Virtuelle Umgebung wird erstellt: %s" ;;
        ru:venv) echo "Создание виртуального окружения: %s" ;;
        en:from_github) echo "Downloading and installing from GitHub" ;;
        tr:from_github) echo "GitHub'dan indiriliyor ve kuruluyor" ;;
        de:from_github) echo "Download und Installation von GitHub" ;;
        ru:from_github) echo "Загрузка и установка с GitHub" ;;
        en:from_local) echo "Installing from local folder: %s" ;;
        tr:from_local) echo "Yerel klasörden kuruluyor: %s" ;;
        de:from_local) echo "Installation aus lokalem Ordner: %s" ;;
        ru:from_local) echo "Установка из локальной папки: %s" ;;
        en:pip_failed) echo "pip installation failed" ;;
        tr:pip_failed) echo "pip kurulumu başarısız" ;;
        de:pip_failed) echo "pip-Installation fehlgeschlagen" ;;
        ru:pip_failed) echo "установка через pip не удалась" ;;
        en:verify_failed) echo "could not verify the installation" ;;
        tr:verify_failed) echo "kurulum doğrulanamadı" ;;
        de:verify_failed) echo "Installation konnte nicht überprüft werden" ;;
        ru:verify_failed) echo "не удалось проверить установку" ;;
        en:installed) echo "%s installed → %s" ;;
        tr:installed) echo "%s kuruldu → %s" ;;
        de:installed) echo "%s installiert → %s" ;;
        ru:installed) echo "%s установлен → %s" ;;

        en:not_in_path) echo "%s is not in PATH. Add it for your shell:" ;;
        tr:not_in_path) echo "%s PATH'te değil. Kabuğuna göre ekle:" ;;
        de:not_in_path) echo "%s ist nicht im PATH. Für deine Shell hinzufügen:" ;;
        ru:not_in_path) echo "%s нет в PATH. Добавьте для вашей оболочки:" ;;

        en:start) echo "Get started:" ;;
        tr:start) echo "Başlamak için:" ;;
        de:start) echo "Loslegen:" ;;
        ru:start) echo "Начать:" ;;
        en:manual) echo "Manual:" ;;
        tr:manual) echo "Kılavuz:" ;;
        de:manual) echo "Handbuch:" ;;
        ru:manual) echo "Руководство:" ;;
        en:completion) echo "Shell completion:" ;;
        tr:completion) echo "Kabuk tamamlama:" ;;
        de:completion) echo "Shell-Vervollständigung:" ;;
        ru:completion) echo "Автодополнение:" ;;
        en:language) echo "Change language:" ;;
        tr:language) echo "Dili değiştirmek için:" ;;
        de:language) echo "Sprache ändern:" ;;
        ru:language) echo "Сменить язык:" ;;
        en:update) echo "Update:" ;;
        tr:update) echo "Güncellemek için:" ;;
        de:update) echo "Aktualisieren:" ;;
        ru:update) echo "Обновить:" ;;
        en:uninstall) echo "Uninstall:" ;;
        tr:uninstall) echo "Kaldırmak için:" ;;
        de:uninstall) echo "Deinstallieren:" ;;
        ru:uninstall) echo "Удалить:" ;;
    esac
}

if [ -t 1 ]; then
    B=$'\033[1m'; G=$'\033[32m'; Y=$'\033[33m'; R=$'\033[31m'; C=$'\033[36m'; N=$'\033[0m'
else
    B=""; G=""; Y=""; R=""; C=""; N=""
fi
# say KEY [ARG...] : çevrilmiş mesajı biçimlendirir
say()  { local fmt; fmt="$(m "$1")"; shift; printf -- "$fmt" "$@"; }
info() { printf '%s==>%s %s\n' "$C$B" "$N" "$(say "$@")"; }
ok()   { printf '%s✓%s %s\n' "$G$B" "$N" "$(say "$@")"; }
warn() { printf '%s!%s %s\n' "$Y$B" "$N" "$(say "$@")"; }
die()  { printf '%s%s:%s %s\n' "$R$B" "$(m error)" "$N" "$(say "$@")" >&2; exit 1; }

uninstall() {
    info removing
    if [ -L "$BIN_DIR/elektro" ] && [ "$(readlink "$BIN_DIR/elektro")" = "$VENV/bin/elektro" ]; then
        rm -f "$BIN_DIR/elektro"
    fi
    rm -rf "$PREFIX"
    rm -f "$MAN_DIR/elektro.1"
    ok removed
    exit 0
}

case "${1:-}" in
    -h|--help) m usage; exit 0 ;;
    -u|--uninstall) uninstall ;;
    "") ;;
    *) die bad_option "$1" ;;
esac

# --- Python -------------------------------------------------------------------
command -v "$PYTHON" >/dev/null 2>&1 || die no_python "$PYTHON"

"$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 9))' \
    || die old_python "$("$PYTHON" -V 2>&1)"

"$PYTHON" -c 'import venv, ensurepip' >/dev/null 2>&1 || die no_venv

# --- Kaynak: repo klasörü mü, GitHub mı? --------------------------------------
SRC="$TARBALL_URL"
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/pyproject.toml" ] && grep -qE '^name = "elektro(-cli)?"' "$SCRIPT_DIR/pyproject.toml"; then
        SRC="$SCRIPT_DIR"
    fi
fi

# --- Eski pipx kurulumu -------------------------------------------------------
if command -v pipx >/dev/null 2>&1 && pipx list --short 2>/dev/null | grep -qE '^elektro(-cli)? '; then
    warn pipx_found
    for pkg in elektro elektro-cli; do pipx uninstall "$pkg" >/dev/null 2>&1 || true; done
fi

# --- Kurulum ------------------------------------------------------------------
info venv "$VENV"
rm -rf "$VENV"
mkdir -p "$PREFIX" "$BIN_DIR"
"$PYTHON" -m venv "$VENV"

if [ "$SRC" = "$TARBALL_URL" ]; then
    info from_github
else
    info from_local "$SRC"
fi
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --upgrade pip
"$VENV/bin/python" -m pip install --quiet --disable-pip-version-check "$SRC" || die pip_failed

# `elektro update` bu dosyaya bakarak kurulum türünü anlar
touch "$VENV/.elektro-install"

ln -sf "$VENV/bin/elektro" "$BIN_DIR/elektro"
VERSION="$("$BIN_DIR/elektro" --version 2>/dev/null)" || die verify_failed
ok installed "$VERSION" "$BIN_DIR/elektro"

# Man sayfası (man-db, ~/.local/bin için ~/.local/share/man'e kendiliğinden bakar)
mkdir -p "$MAN_DIR" && "$BIN_DIR/elektro" manpage > "$MAN_DIR/elektro.1" 2>/dev/null || rm -f "$MAN_DIR/elektro.1"

# --- PATH ---------------------------------------------------------------------
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *)
        warn not_in_path "$BIN_DIR"
        case "$(basename "${SHELL:-bash}")" in
            fish) echo "    fish_add_path $BIN_DIR" ;;
            zsh)  echo "    echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.zshrc && source ~/.zshrc" ;;
            *)    echo "    echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.bashrc && source ~/.bashrc" ;;
        esac
        ;;
esac

row() { printf '  %s %s\n' "$(m "$1")" "${B}$2${N}"; }
echo
row start      "elektro"
row manual     "man elektro"
row completion "elektro --install-completion"
row language   "elektro language en|tr|de|ru"
row update     "elektro update"
row uninstall  "curl -fsSL $REPO_URL/raw/main/install.sh | bash -s -- --uninstall"
