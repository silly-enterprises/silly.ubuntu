#!/bin/bash
# 🐧 silly.wsl - Quality-of-life Bash functions for WSL
# Source: /etc/bashrc.d/20-silly-wsl-functions.sh

# Skip if not running in WSL
if ! grep -qi microsoft /proc/version; then
  return 0 2>/dev/null || true
fi


# 🔥 Remove Zone.Identifier files (left behind when moving from Windows)
clean-zone-ids() {
  echo "[silly.wsl] Cleaning up Zone.Identifier files in $(pwd)..."
  find . -name "*Zone.Identifier" -type f -delete
  echo "[silly.wsl] Done."
}

# 📂 Open the current folder in Windows File Explorer
openwin() {
  local p=$(wslpath -w "${1:-.}")
  explorer.exe "$p"
}
