# Dotfiles

My Fedora Workstation 44 / GNOME 50 setup: native Adwaita styling, softer
traffic-light window controls, a GNOME palette for Ghostty, and Vicinae on Alt+Space.

## Layout

- `home/`: managed configuration files, arranged like the home directory.
- `desktop/`: curated GNOME settings, extension IDs, and Vesktop preferences.
- `scripts/`: installers with dry runs and backups.
- `docs/setup.md`: dependencies, installation and known limitations.
- `archive/pre-fedora-44/`: the original i3/bspwm-era files, preserved for nostalgia.

There is no package inventory: the small set of requirements is in the setup guide.

## Install

Install the requirements in [the setup guide](docs/setup.md) first. Then, from this directory:

```sh
python3 scripts/link-configs.py --dry-run
python3 scripts/link-configs.py
python3 scripts/apply-desktop.py --dry-run
python3 scripts/apply-desktop.py
```

Run desktop setup from a terminal in your GNOME session. Quit Vicinae and Vesktop
before installing their preferences; reopen apps afterward. The archive is never installed.

Existing files and settings are backed up under `~/.local/state/dotfiles/backups/`.
No sessions, clipboard history, credentials or browser profiles are included.
