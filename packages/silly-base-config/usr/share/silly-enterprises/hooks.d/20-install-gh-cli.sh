#!/bin/bash
(type -p wget >/dev/null || (sudo apt-get install wget -y))
echo "[silly-gh] Adding GitHub CLI source..."

# Set up source list and keyring
# (do NOT run apt update or install)
mkdir -p /etc/apt/keyrings
wget -qO /etc/apt/keyrings/githubcli-archive-keyring.gpg https://cli.github.com/packages/githubcli-archive-keyring.gpg
chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list

# Let user finish the job
echo
echo "GitHub CLI repo configured."
echo "👉 Run the following to install:"
echo "   sudo apt update && sudo apt install gh"
