#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VIDEO="$ROOT/video"
LOCAL_CRIER="$ROOT/.tools/crier"

ok() { printf '  \033[32m✓\033[0m %s\n' "$*"; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }
die() { printf '  \033[31m✗\033[0m %s\n' "$*" >&2; exit 1; }

ensure_brew_package() {
  local cmd="$1" package="$2"
  command -v "$cmd" >/dev/null 2>&1 && return 0
  if [[ "$(uname)" == "Darwin" ]] && command -v brew >/dev/null 2>&1; then
    printf '  %s가 없어 Homebrew로 설치합니다.\n' "$cmd"
    brew install "$package"
  else
    die "$cmd가 필요합니다. 설치 후 다시 실행해 주세요."
  fi
}

step "영상 런타임"
ensure_brew_package git git
ensure_brew_package node node
ensure_brew_package npm node
ensure_brew_package ffmpeg ffmpeg
ensure_brew_package pdfinfo poppler
ensure_brew_package pdftoppm poppler

if ! command -v uv >/dev/null 2>&1; then
  printf '  uv가 없어 공식 설치 스크립트로 설치합니다.\n'
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
command -v uv >/dev/null 2>&1 || die "uv 설치 후에도 실행 파일을 찾지 못했습니다."
ok "Node $(node --version) · npm $(npm --version) · ffmpeg · poppler · uv 준비"

step "동적 영상 엔진"
if [[ ! -x "$VIDEO/node_modules/.bin/remotion" ]]; then
  npm install --prefix "$VIDEO" --no-audit --no-fund
fi
ok "Remotion 준비"

step "한국어 로컬 음성"
CRIER_ROOT="${CRIER_HOME:-}"
if [[ -z "$CRIER_ROOT" && -x "$HOME/.crier/bin/crier" ]]; then
  CRIER_ROOT="$HOME/.crier"
fi
if [[ -z "$CRIER_ROOT" ]]; then
  if [[ ! -d "$LOCAL_CRIER/.git" ]]; then
    git clone --depth 1 https://github.com/pg-Parunson/crier "$LOCAL_CRIER"
  fi
  CRIER_ROOT="$LOCAL_CRIER"
fi
if [[ ! -x "$CRIER_ROOT/.venv/bin/supertonic" ]]; then
  "$CRIER_ROOT/install.sh" --no-hooks
fi
"$CRIER_ROOT/bin/crier" start
ok "Crier/Supertonic F2 준비 · 로컬 실행 · API 키 없음"

CRIER_HOME="$CRIER_ROOT" python3 "$ROOT/scripts/doctor.py"

cat <<EOF

설치가 끝났습니다.
이제 다음처럼 말하면 됩니다.

  refs의 최근 기록으로 30초 주간보고 영상을 만들어줘

EOF
