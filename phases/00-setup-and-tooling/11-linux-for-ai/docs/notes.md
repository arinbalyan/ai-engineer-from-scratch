# Linux for AI (Arch Adaptation)

**Lesson:** 11 / Phase 00
**Environment:** Arch Linux (WSL2)
**Prerequisites:** None
**Time:** ~30 minutes

## Learning Objectives

- Navigate the Linux file system and perform essential file operations
- Manage file permissions with chmod and chown
- Install system packages with pacman (Arch's package manager)
- Understand Arch-specific differences versus Ubuntu (the curriculum default)
- Identify macOS-to-Linux differences

## Key Differences: Ubuntu vs Arch

The curriculum uses Ubuntu with `apt`. This environment is Arch Linux.

| Task | Ubuntu (curriculum) | Arch (this env) |
|------|-------------------|-----------------|
| Update package list | `sudo apt update` | `sudo pacman -Sy` |
| Full system update | `sudo apt upgrade` | `sudo pacman -Syu` |
| Install package | `sudo apt install htop` | `sudo pacman -S htop` |
| Remove package | `sudo apt remove htop` | `sudo pacman -R htop` |
| Remove + configs + deps | `sudo apt purge --auto-remove` | `sudo pacman -Rns` |
| Search packages | `apt search htop` | `pacman -Ss htop` |
| Check installed | `apt list --installed` | `pacman -Q` (all) / `pacman -Qs htop` |
| Package info | `apt show htop` | `pacman -Qi htop` |
| Clean cache | `sudo apt clean` | `sudo pacman -Scc` |

## File System Layout

Same as any Linux -- everything under `/`. Key paths:

| Path | Purpose |
|------|---------|
| `/home/yourname/` | Your files, repos, training runs |
| `/tmp/` | Temporary, cleared on reboot |
| `/usr/` | System programs and libraries |
| `/etc/` | Configuration files |
| `/var/log/` | System logs |
| `/mnt/` | Mounted drives (WSL2 Windows FS at `/mnt/c/`) |

## Package Management (pacman)

Arch uses `pacman`. Basic workflow:

```bash
# First time or long time no update:
sudo pacman -Syu              # Full system update

# Install a package:
sudo pacman -S htop tmux

# Remove a package (R = remove, n = no save configs, s = remove deps):
sudo pacman -Rns htop

# Search:
pacman -Ss "neural network"   # Search remote repos
pacman -Qs python             # Search installed packages

# Info:
pacman -Qi htop               # Package details
pacman -Ql htop               # Files installed by package
pacman -Qdt                   # Orphaned packages (no longer needed)
```

### AUR (Arch User Repository)

For packages not in official repos (e.g., some ML tools):

```bash
# Install an AUR helper first:
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si

# Then use yay like pacman:
yay -S python-torch-cuda-git   # Example AUR package
```

### Common AI-related Arch packages

```bash
# GPU monitoring
sudo pacman -S nvtop

# System tools
sudo pacman -S htop btop
```

## Essential Commands

(Curriculum 15 commands apply as-is on Arch -- they're standard Linux.)

**Navigation:** `pwd`, `ls`, `cd`
**File ops:** `cp`, `mv`, `rm`, `mkdir` (use `rm -rf` carefully -- no undo)
**Reading files:** `cat`, `head`, `tail -f`, `less`
**Search:** `grep -r`, `find . -name`
**Permissions:** `chmod +x`, `chmod 755`, `chown`
**Processes:** `ps aux`, `kill`, `htop`, `nvidia-smi`
**Disk:** `df -h`, `du -sh`, `du -h --max-depth=1 / | sort -hr | head -20`
**Network:** `curl`, `wget`, `scp`, `rsync -avz --progress`

## tmux

Identical across all Linux distros. Always run long training jobs inside tmux.

```bash
tmux new -s train            # Start session
Ctrl+B, D                    # Detach (training keeps running)
tmux attach -t train         # Reattach
Ctrl+B, %                    # Split pane vertically
Ctrl+B, "                    # Split pane horizontally
```

## Arch on WSL2 -- Specific Notes

This environment is **Arch Linux under WSL2**. Key differences from a native Arch install or an Ubuntu WSL2:

### systemd

**Arch WSL does NOT enable systemd by default.** The curriculum's `systemctl` examples may not work unless you explicitly enable it:

```bash
# Enable systemd in WSL2:
echo -e "[boot]\nsystemd=true" | sudo tee -a /etc/wsl.conf

# Exit WSL, in PowerShell:
wsl --shutdown
# Restart WSL
```

Without systemd, start services directly:
```bash
sudo /usr/bin/sshd &
sudo /usr/bin/cron &
```

### GPU Access

NVIDIA GPU works through Windows host drivers:
- nvidia-smi: `/usr/lib/wsl/lib/nvidia-smi` (not in standard PATH)
- CUDA toolkit: Install via `pacman -S cuda` or use bundled PyTorch CUDA runtime (cu124 wheels)
- Memory: 4GB GTX 1650 Ti

### Windows Files

Windows drives mount at `/mnt/c/`, `/mnt/d/`, etc. These are slower than the native Linux filesystem. Keep repos and data inside the Linux home directory.

## macOS to Linux Gotchas

(Unchanged from curriculum -- applies regardless of Arch vs Ubuntu)

| macOS | Linux |
|-------|-------|
| `brew install` | `sudo pacman -S` |
| `open file.txt` | `cat`, `less`, or `xdg-open` |
| `pbcopy` / `pbpaste` | Not available over SSH |
| `~/.zshrc` | `~/.bashrc` (or `~/.zshrc` if using zsh) |
| `sed -i '' 's/a/b/' file` | `sed -i 's/a/b/' file` |
| Case-insensitive FS | Case-sensitive (Model.py != model.py) |

## Exercises

1. `cd ~ && mkdir -p sandbox/project && touch sandbox/project/{train.py,config.yaml,data.csv} && ls -la sandbox/project/`
2. `pacman -Qi htop` to verify htop is installed, then run `htop` briefly (q to quit)
3. `tmux new -s test-session`, run `sleep 30`, Ctrl+B D, `tmux ls`, `tmux attach -t test-session`, then `exit`
4. `df -h /` to check disk, then `du -sh ~/ai-engineering/*/` to see project space usage
5. (Optional) `curl -s https://httpbin.org/json | python3 -m json.tool` to practice API calls from the CLI
