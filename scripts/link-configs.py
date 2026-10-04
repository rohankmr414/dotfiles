#!/usr/bin/env python3
"""Install managed files, preserving existing files and app-owned directories."""
import argparse
from datetime import datetime
from pathlib import Path
import shutil
import uuid

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--target-home', type=Path, default=Path.home())
    args = parser.parse_args()
    home = args.target_home.expanduser().resolve()
    backup = home / '.local/state/dotfiles/backups' / (datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6])
    sources = sorted(p for p in (ROOT / 'home').rglob('*') if p.is_file())
    operations = [(p, home / p.relative_to(ROOT / 'home'), p.name == 'settings.json') for p in sources]
    # Current Vicinae searches its user data theme directory too.
    operations.append((ROOT / 'home/.config/vicinae/themes/adwaita-subdued.toml', home / '.local/share/vicinae/themes/adwaita-subdued.toml', False))
    for source, target, copy in operations:
        if not copy and target.is_symlink() and target.resolve() == source.resolve():
            continue
        if copy and target.is_file() and not target.is_symlink() and target.read_bytes() == source.read_bytes():
            continue
        print(f'{"copy" if copy else "link"}: {target}')
        if args.dry_run:
            continue
        if target.exists() or target.is_symlink():
            saved = backup / target.relative_to(home)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(saved))
        target.parent.mkdir(parents=True, exist_ok=True)
        if copy:
            # Vicinae rewrites this file through its GUI; don't let it edit the repo.
            shutil.copy2(source, target)
        else:
            target.symlink_to(source)
    if not args.dry_run:
        print(f'Existing files, if any, saved under {backup}')

if __name__ == '__main__':
    main()
