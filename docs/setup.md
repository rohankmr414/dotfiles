# Fedora / GNOME setup

Recorded on Fedora Workstation 44 with GNOME 50.5, Ghostty 1.3.1,
Vicinae 0.29.1 and Vesktop 1.6.7. Package and extension versions can change.

## Requirements

Use the repositories available for your Fedora release. On the original installation,
Ghostty used `scottames/ghostty` COPR and Vicinae used `quadratech188/vicinae` COPR.

```sh
sudo dnf install git python3 python3-gobject zsh neovim sushi
sudo dnf copr enable scottames/ghostty
sudo dnf copr enable quadratech188/vicinae
sudo dnf install ghostty vicinae
```

Install Brave and Vesktop separately using their current installation instructions:

- Brave: https://brave.com/linux/
- Vicinae: https://docs.vicinae.com/install/linux
- Vesktop: https://github.com/Vencord/Vesktop

The shell configuration expects Oh My Zsh, its `git` and `z` plugins, and
`zsh-syntax-highlighting`. Install Oh My Zsh before installing `.zshrc`.
The highlighting plugin can be installed under its custom plugin directory:

```sh
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"
```

The Ghostty configuration changes colors only; install your preferred terminal font
separately. The original machine uses JetBrains Mono Nerd Font.

## GNOME extensions

Install these through Extension Manager or extensions.gnome.org, selecting versions
compatible with your GNOME release. The installer enables them if already installed;
it does not vendor extension code or automatically download it.

- [Dash to Dock](https://extensions.gnome.org/extension/307/dash-to-dock/)
- [Vicinae](https://extensions.gnome.org/extension/8594/vicinae/)
- [AppIndicator support](https://extensions.gnome.org/extension/615/appindicator-support/)

## Apply the configuration

Quit Vicinae and Vesktop first so they cannot overwrite newly installed preferences.
For Vicinae's service: `systemctl --user stop vicinae.service`.

```sh
python3 scripts/link-configs.py --dry-run
python3 scripts/link-configs.py
python3 scripts/apply-desktop.py --dry-run
python3 scripts/apply-desktop.py
```

`link-configs.py` backs up existing managed files and links individual files, never
whole app directories. Vicinae's `settings.json` is copied because Vicinae writes
that file through its GUI. Rerunning the installer reapplies the repository version.
After making wanted GUI changes, copy only that reviewed configuration back into the repo.
Vicinae's theme has one source file, linked into both config and data theme directories.

`apply-desktop.py` parses the curated GVariant values, saves old settings, applies
them, enables installed extensions and starts Vicinae's packaged user service.
It preserves other custom keyboard shortcuts and merges only selected Vesktop
preferences. Quit Vesktop before running it. Missing extension settings are skipped;
install those extensions and rerun to apply their preferences.

## Resulting behavior

- GNOME dark appearance and Close / Minimize / Maximize on the left.
- Soft GNOME Red 1, Yellow 1 and Green 1 traffic-light circles.
- Ghostty uses the agreed 16-color GNOME palette; normal red is Red 2.
- Vicinae uses the custom opaque Adwaita Subdued theme, softer borders, and system font.
- Alt+Space toggles Vicinae; GNOME's window-menu shortcut is released.
- Super+Shift+5 opens GNOME's screenshot/recording panel; Print still works.
- Dash to Dock uses a bottom, floating 48px dock with autohide and intellihide.
- Super+Shift+number dock shortcuts are disabled; Super+number remains available.
- AppIndicator provides top-bar tray icons. Enable the tray option inside Vesktop if needed.
- Sushi previews selected files with Space in Files.

## Application-specific notes

For Brave, choose GTK in Appearance. Fully quit it before testing:

```sh
brave-browser --gtk-version=4 --ozone-platform=wayland
```

These launch flags are documented, not added to your launcher automatically.
Chromium/Electron render window controls differently from native GTK; fractional
scaling can cause small sharpness differences. The CSS includes Chromium adjustments,
but custom title bars, Flatpaks and future GTK/Electron changes may need separate work.
Vesktop's GTK3 fallback was syntax-checked but its resulting appearance was not
confirmed before this snapshot. Calendar required a full process restart to retry styling.

The custom Vicinae theme must be discoverable in its user data theme directory.
If it falls back to another theme, open Settings with Ctrl+, and select Adwaita Subdued.

## Backups and restore

Each installer stores backups under `~/.local/state/dotfiles/backups/<timestamp>/`.
To undo file installation, remove each managed link/copy and restore its backed-up
file to the original path. The linker never modifies unlisted application files.
Desktop backups contain the previous GVariant values with their schema/path and key;
restore those using `gsettings` or `Gio.Settings`. Extension enablement is recorded
separately. Stop/disable Vicinae's service if undoing launcher startup.

Do not run the old configs from `archive/` as part of this installation.
