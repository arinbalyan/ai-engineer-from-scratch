## Lesson 10: Terminal & Shell

### What I Learned

The terminal is the primary interface for AI work. Key skills: piping/redirects for log processing, tmux for persistent training sessions, monitoring with htop/nvtop, and SSH/rsync for remote GPU boxes.

### Key Tools

- **Pipes and redirects**: `|` chains commands, `>` writes stdout, `2>` writes stderr, `2>&1` merges both, `tee` writes to file and shows output
- **tmux**: Named sessions survive terminal close. `tmux new -s name`, `C-b "` (split horiz), `C-b %` (split vert), `C-b d` (detach), `tmux attach -t name`
- **nohup**: `nohup cmd &` survives terminal close but can't reattach (check log file)
- **SSH**: `ssh user@host`, `scp` for files, `rsync -avz` for directories, `ssh -L 8888:localhost:8888` for port forwarding
- **Monitoring**: `htop` (system), `nvidia-smi` (GPU quick check), `watch -n1 nvidia-smi` (live GPU)

### Aliases (code/shell_aliases.sh)

The aliases file covers GPU monitoring, training control, venv management, log watching, disk cleanup, tmux shortcuts, SSH helpers, experiment management, and process management. Compatible with bash and zsh.

To use: `source phases/00-setup-and-tooling/10-terminal-and-shell/code/shell_aliases.sh`

### Common AI Terminal Patterns

- `python train.py 2>&1 | tee train.log` -- log everything and see it live
- `diff <(grep "acc" exp1.log) <(grep "acc" exp2.log)` -- compare experiments
- `find . -name "*.pt" | xargs du -h | sort -rh | head -20` -- find largest models
- `env | grep -i cuda` -- check CUDA environment before training

### Key Shortcuts

- `C-r` -- reverse history search (most useful)
- `C-c` -- kill running command
- `C-z` -- suspend (resume with `fg`)
- `C-l` -- clear terminal
