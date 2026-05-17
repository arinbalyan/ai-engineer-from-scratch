#!/bin/bash
# Linux for AI -- Arch-adapted interactive demo
# Run: bash phases/00-setup-and-tooling/11-linux-for-ai/code/linux-for-ai.sh
set -e

SEPARATOR="----------------------------------------"

echo "=== Linux for AI: Arch-adapted Quick Reference ==="
echo "Run each section interactively. Press Enter to continue."
echo

# --- 1. File System Navigation ---
echo $SEPARATOR
echo "1. FILE SYSTEM NAVIGATION"
echo $SEPARATOR
echo "pwd        : $(pwd)"
echo "whoami     : $(whoami)"
echo "home       : $HOME"
echo
echo "Try it: cd ~ && ls -la | head -5"
read -p "[Press Enter to continue]"

# --- 2. Package Management (Arch: pacman) ---
echo
echo $SEPARATOR
echo "2. PACKAGE MANAGEMENT (Arch pacman)"
echo $SEPARATOR
echo "  Unlike Ubuntu's apt, Arch uses pacman:"
echo "  sudo pacman -Syu        # Full system update"
echo "  sudo pacman -S htop     # Install a package"
echo "  sudo pacman -Rns htop   # Remove a package and deps"
echo "  pacman -Qs htop         # Search installed packages"
echo "  pacman -Qi htop         # Show package info"
echo "  pacman -Ql htop         # List package files"
echo
echo "  AUR helpers (yay/paru) for community packages:"
echo "  yay -S python-torch-cuda  # Example AUR install"
echo
echo "  Check current version of a key package:"
pacman -Qi htop 2>/dev/null | grep -E "^(Name|Version|Installed)"
echo
echo "  All system packages: $(pacman -Qq | wc -l) installed"
read -p "[Press Enter to continue]"

# --- 3. File Operations ---
echo
echo $SEPARATOR
echo "3. FILE OPERATIONS"
echo $SEPARATOR
TMPDIR=$(mktemp -d)
echo "Working in $TMPDIR"
mkdir -p "$TMPDIR/project/data"
touch "$TMPDIR/project/train.py" "$TMPDIR/project/config.yaml" "$TMPDIR/project/data/samples.csv"
echo "Created:"
find "$TMPDIR/project" -type f | sort | sed 's|.*/|  |'
echo
echo "  ls -la shows file details:"
ls -la "$TMPDIR/project/"
rm -rf "$TMPDIR"
echo "  (cleaned up)"
read -p "[Press Enter to continue]"

# --- 4. Permissions ---
echo
echo $SEPARATOR
echo "4. FILE PERMISSIONS"
echo $SEPARATOR
TMPF=$(mktemp)
echo '#!/bin/bash' > "$TMPF"
echo 'echo "Hello from script"' >> "$TMPF"
chmod 644 "$TMPF"
echo "  Before chmod +x: $(ls -l "$TMPF" | awk '{print $1}')"
chmod +x "$TMPF"
echo "  After chmod +x:  $(ls -l "$TMPF" | awk '{print $1}')"
echo "  Running:"
bash "$TMPF"
rm -f "$TMPF"
echo
echo "  chmod reference:"
echo "    755 = rwxr-xr-x (executable for everyone)"
echo "    644 = rw-r--r-- (readable, writable by owner)"
echo "    600 = rw------- (private file)"
read -p "[Press Enter to continue]"

# --- 5. Processes and GPU ---
echo
echo $SEPARATOR
echo "5. PROCESSES AND GPU"
echo $SEPARATOR
echo "  Top memory consumers right now:"
ps aux --sort=-%mem | head -6
echo
echo "  nvidia-smi (GPU status):"
if command -v nvidia-smi &>/dev/null; then
    nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu --format=csv,noheader 2>/dev/null || echo "  GPU query unavailable (WSL2)"
else
    echo "  nvidia-smi not found"
fi
echo
echo "  htop: interactive process viewer (q to quit)"
echo "  Try: htop"
read -p "[Press Enter to continue]"

# --- 6. Disk Usage ---
echo
echo $SEPARATOR
echo "6. DISK USAGE"
echo $SEPARATOR
echo "  Mounted filesystems:"
df -h / /home 2>/dev/null || df -h /
echo
echo "  Top 5 directories by size in ~/ai-engineering:"
if [ -d "$HOME/ai-engineering" ]; then
    du -sh "$HOME/ai-engineering"/*/ 2>/dev/null | sort -hr | head -5
else
    echo "  (ai-engineering dir not found at ~/ai-engineering)"
fi
read -p "[Press Enter to continue]"

# --- 7. tmux ---
echo
echo $SEPARATOR
echo "7. TMUX (Terminal Multiplexer)"
echo $SEPARATOR
echo "  tmux keeps sessions alive after SSH disconnect."
echo
echo "  Key commands:"
echo "    tmux new -s train     # Start session named 'train'"
echo "    Ctrl+B, D             # Detach (training keeps running)"
echo "    tmux ls               # List sessions"
echo "    tmux attach -t train  # Reattach to 'train'"
echo "    Ctrl+B, %             # Split pane vertically"
echo "    Ctrl+B, \"             # Split pane horizontally"
echo
echo "  tmux version: $(tmux -V 2>/dev/null || echo 'not installed')"
echo
echo "  Try: tmux new -s test-session"
echo "  Then Ctrl+B, D to detach"
echo "  Then: tmux attach -t test-session"
echo "  Then type 'exit' to close it"
read -p "[Press Enter to continue]"

# --- 8. Networking ---
echo
echo $SEPARATOR
echo "8. NETWORKING"
echo $SEPARATOR
echo "  wget / curl for downloads and API calls"
echo "  scp / rsync for file transfer between machines"
echo
echo "  Example: curl an API and pretty-print JSON:"
curl -s https://httpbin.org/json 2>/dev/null | python3 -m json.tool 2>/dev/null | head -10 || echo "  (network call failed, skip)"
echo
echo "  rsync vs scp: rsync resumes on interruption, scp restarts"
echo "  rsync -avz --progress ./dir/ user@host:/remote/dir/"
read -p "[Press Enter to continue]"

# --- 9. Arch-specific WSL2 Notes ---
echo
echo $SEPARATOR
echo "9. ARCH ON WSL2 -- IMPORTANT DIFFERENCES"
echo $SEPARATOR
echo "  This environment is Arch under WSL2."
echo
echo "  - Package manager: pacman (not apt)"
echo "  - systemd is NOT enabled by default in Arch WSL"
echo "  - systemctl commands won't work without extra config"
echo "  - GPU: NVIDIA drivers on Windows host, WSL2 passes through"
echo "  - nvidia-smi path: /usr/lib/wsl/lib/nvidia-smi"
echo "  - Windows files: /mnt/c/Users/YourName/"
echo
echo "  To enable systemd in Arch WSL:"
echo "    echo -e '[boot]\\nsystemd=true' | sudo tee -a /etc/wsl.conf"
echo "    (then exit WSL, run 'wsl --shutdown' in PowerShell, restart)"
echo
echo "  Without systemd, start services manually via:"
echo "    sudo /usr/bin/<daemon> &"
read -p "[Press Enter to complete]"

# --- Summary ---
echo
echo $SEPARATOR
echo "QUICK REFERENCE CARD"
echo $SEPARATOR
cat <<'CARD'
Navigation:     pwd, ls, cd, find
Files:          cp, mv, rm, mkdir, cat, head, tail, less
Search:         grep, find
Permissions:    chmod, chown, sudo
Packages:       pacman -Syu, pacman -S, pacman -Rns
Processes:      htop, ps, kill, nvidia-smi
Services:       systemctl start/stop/status (if systemd enabled)
Disk:           df -h, du -sh
Network:        curl, wget, scp, rsync
Sessions:       tmux new/attach/detach
Arch extra:     pacman -Qs (search), pacman -Ql (files), pacman -Qi (info)
CARD
echo
echo "=== Demo complete ==="
