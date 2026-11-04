#!/usr/bin/env bash
# One-command render for macOS / Linux.  Usage: bash render.sh
set -e
if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is not installed. Install the LTS version from https://nodejs.org and run this again."
  exit 1
fi
if [ ! -d node_modules ]; then
  echo "Installing dependencies (first run only)..."
  npm install
fi
echo "Rendering video..."
npx remotion render src/index.ts Main out/video.mp4
echo "Done: out/video.mp4"
