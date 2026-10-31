#!/usr/bin/env bash
# Downloads microgpt.py from Andrej Karpathy's gist, pinned to one revision,
# and refuses to keep it unless the sha256 matches the file this guide was written against.
set -euo pipefail

GIST_ID="8627fe009c40f57531cb18360106ce95"
REVISION="14fb038816c7aae0bb9342c2dbf1a51dd134a5ff"
SHA256="d47d88c2fd432c8ebdc1048beab7f7eb64ea7e0e664e11b812d72a6d95ebccee"
URL="https://gist.githubusercontent.com/karpathy/${GIST_ID}/raw/${REVISION}/microgpt.py"

cd "$(dirname "$0")"

curl -fsSL "$URL" -o microgpt.py.part
actual="$(shasum -a 256 microgpt.py.part | cut -d' ' -f1)"

if [ "$actual" != "$SHA256" ]; then
  rm -f microgpt.py.part
  echo "sha256 mismatch: expected $SHA256, got $actual" >&2
  exit 1
fi

mv microgpt.py.part microgpt.py
echo "microgpt.py ready ($(wc -l < microgpt.py | tr -d ' ') lines). Run: python3 microgpt.py"
