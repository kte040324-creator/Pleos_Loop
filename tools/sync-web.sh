#!/usr/bin/env bash
# web/ (화면 원본) → app/src/main/assets/ 로 복사. loop.html은 index.html로 바꾸고 tts-shim 주입.
# 화면을 고칠 땐 web/loop.html만 고치고 이 스크립트를 실행할 것.
set -euo pipefail
cd "$(dirname "$0")/.."
A=app/src/main/assets
find "$A" -mindepth 1 -maxdepth 1 ! -name tts-shim.js ! -name vendor ! -name fonts -exec rm -rf {} +
cp -r web/. "$A"/
mv "$A/loop.html" "$A/index.html"
python3 tools/patch_app_html.py "$A/index.html"
echo "synced → $A"
