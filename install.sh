#!/usr/bin/env bash
# imagination-octo one-command installer
#   curl -fsSL https://raw.githubusercontent.com/djfksjd/imagination-octo/main/install.sh | bash
set -u

REPO="djfksjd/imagination-octo"
INSTALLED=0

log()  { printf '\033[1;35m[imagination-octo]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[imagination-octo]\033[0m %s\n' "$*" >&2; }

try_host() {
  local name="$1"; shift
  if "$@"; then
    log "✓ ${name} installed"
    INSTALLED=$((INSTALLED + 1))
  else
    warn "✗ ${name} install failed — see the README for manual steps"
  fi
}

if command -v claude >/dev/null 2>&1; then
  try_host "Claude Code" bash -c \
    "claude plugin marketplace add ${REPO} && claude plugin install imagination-octo@djfksjd"
else
  warn "claude CLI not found — skipping Claude Code"
fi

if command -v codex >/dev/null 2>&1; then
  try_host "Codex" bash -c \
    "codex plugin marketplace add ${REPO} && codex plugin add imagination-octo@djfksjd"
else
  warn "codex CLI not found — skipping Codex"
fi

if [ "${INSTALLED}" -eq 0 ]; then
  warn "Nothing was installed. Install Claude Code or Codex first, or clone manually:"
  warn "  git clone https://github.com/${REPO}.git"
  exit 1
fi

log "Done. Start with: use \$imagination-octo on: <brief>"
