You are operating in an AI Engineering workspace. Use this reference for Linux shell operations.

## Environment

- OS: Arch Linux (under WSL2)
- Shell: zsh (default) or bash
- Package manager: pacman (NOT apt)
- GPU: NVIDIA GTX 1650 Ti 4GB, via WSL2 passthrough
- Python: uv (not system python or pip)

## Essential Commands

### Package Management (pacman)

```bash
sudo pacman -Syu                     # Full system update
sudo pacman -S <pkg>                 # Install package
sudo pacman -Rns <pkg>               # Remove package + configs + deps
pacman -Qs <keyword>                 # Search installed packages
pacman -Ss <keyword>                 # Search remote repos
pacman -Qi <pkg>                     # Package info
pacman -Qdt                          # Find orphaned packages
```

### File System

```bash
pwd              # Current directory
ls -la           # List all with details
cd ~             # Go home
mkdir -p a/b/c   # Create nested dirs
cp -r src/ dst/  # Copy directory
rm -rf dir/      # DELETE directory (no undo!)
chmod +x file    # Make executable
du -sh *         # Size of each item
```

### Processes & GPU

```bash
htop             # Interactive process viewer
ps aux | grep    # Find processes
kill -9 <PID>    # Force kill
nvidia-smi       # GPU status (WSL2: /usr/lib/wsl/lib/nvidia-smi)
```

### Sessions

```bash
tmux new -s <name>    # Start session
Ctrl+B D              # Detach
tmux attach -t <name> # Reattach
tmux ls               # List sessions
```

### Network

```bash
curl -s <url> | python3 -m json.tool     # API call with pretty-print
rsync -avz --progress src/ user@host:dst/ # Sync (resumable)
scp file user@host:/path/                 # Copy to remote
```

## This Is NOT Ubuntu

| You might think | Actually use |
|----------------|-------------|
| `sudo apt install` | `sudo pacman -S` |
| `apt update && apt upgrade` | `pacman -Syu` |
| `apt remove` | `pacman -Rns` |
| `apt list --installed` | `pacman -Q` |
| `python3 -m venv` | `uv venv` |
| `/usr/bin/python3` | `~/.local/bin/uv run python` |
| systemctl (WSL2) | May not work without /etc/wsl.conf config |
| `nvidia-smi` at PATH | May be at /usr/lib/wsl/lib/nvidia-smi |
