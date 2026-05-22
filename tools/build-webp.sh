#!/usr/bin/env bash
# Convert all PNG screenshots under assets/products/ to WebP (q=82) and AVIF (q=70).
# Idempotent: skips files that are already up-to-date.
#
# Requirements: macOS Homebrew → `brew install cwebp libavif`
#               or Linux → apt install webp libavif-bin
#
# Usage:  ./tools/build-webp.sh
#
# After running, drop <picture> blocks into HTML to deliver WebP/AVIF with PNG fallback:
#   <picture>
#     <source srcset="img.avif" type="image/avif">
#     <source srcset="img.webp" type="image/webp">
#     <img src="img.png" alt="…" loading="lazy" width="280" height="560">
#   </picture>

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/assets/products"

if ! command -v cwebp >/dev/null 2>&1; then
  echo "× cwebp not found. Install: brew install webp"
  exit 1
fi

count_webp=0
count_avif=0
count_skip=0

shopt -s nullglob globstar
for png in "$SRC"/**/*.png; do
  webp="${png%.png}.webp"
  avif="${png%.png}.avif"

  if [[ ! -f "$webp" || "$png" -nt "$webp" ]]; then
    cwebp -q 82 -m 6 -mt -quiet "$png" -o "$webp"
    count_webp=$((count_webp + 1))
  else
    count_skip=$((count_skip + 1))
  fi

  if command -v avifenc >/dev/null 2>&1; then
    if [[ ! -f "$avif" || "$png" -nt "$avif" ]]; then
      avifenc --min 0 --max 63 -a end-usage=q -a cq-level=24 "$png" "$avif" >/dev/null
      count_avif=$((count_avif + 1))
    fi
  fi
done

echo "✓ WebP: $count_webp converted, $count_skip skipped"
if command -v avifenc >/dev/null 2>&1; then
  echo "✓ AVIF: $count_avif converted"
else
  echo "ℹ AVIF skipped (install libavif-bin for AVIF support)"
fi
echo ""
echo "Done. Next: wrap <img> in <picture> blocks (see header comment in this script)."
