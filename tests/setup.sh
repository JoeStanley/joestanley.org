#!/bin/bash
# Installs what the checks and the PDF need, on Linux. Safe to run more than once.
# Run from the repo root: bash tests/setup.sh   (GitHub's checks and every Claude session start with it)
# It prints the HUGO and CHROME lines to export before running tests/check_site.py.
set -euo pipefail

HUGO_VERSION=0.141.0
BIN="${HOME}/.local/bin"
mkdir -p "$BIN"

# Hugo, extended edition, the one version the site is built and checked with.
if ! "$BIN/hugo" version 2>/dev/null | grep -q "v${HUGO_VERSION}-.*+extended"; then
  curl -sSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \
    | tar xz -C "$BIN" hugo
fi

# Python packages for the checks and tools-pm/make-pdf.py.
python3 -m pip install --quiet --break-system-packages \
  "playwright>=1.42" pyyaml Pillow numpy beautifulsoup4 pikepdf pypdfium2

# WebKit and Firefox for rule R8. Chrome itself is used as installed (google-chrome, or CHROME).
if [ "$(id -u)" = 0 ] || sudo -n true 2>/dev/null; then
  python3 -m playwright install --with-deps webkit firefox
else
  python3 -m playwright install webkit firefox
fi

# pdftotext and pdfinfo for the print rules.
if ! command -v pdftotext >/dev/null; then
  if [ "$(id -u)" = 0 ]; then apt-get install -y -qq poppler-utils; else sudo apt-get install -y -qq poppler-utils; fi
fi

# axe-core for rule A1.
npm install --prefix tests --silent

CHROME_BIN="${CHROME:-$(command -v google-chrome || command -v google-chrome-stable || true)}"
if [ -z "$CHROME_BIN" ]; then
  python3 -m playwright install chromium
  CHROME_BIN=$(python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); print(p.chromium.executable_path); p.stop()")
fi
echo "export HUGO=$BIN/hugo CHROME=$CHROME_BIN"
