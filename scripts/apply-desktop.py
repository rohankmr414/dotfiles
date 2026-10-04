#!/usr/bin/env python3
"""Apply curated GNOME settings in the user's desktop session."""
import argparse
import configparser
from datetime import datetime
import json
from pathlib import Path
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]

def main():
    from gi.repository import Gio, GLib
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    home = Path.home()
    source = Gio.SettingsSchemaSource.get_default()
    for directory in sorted((home / '.local/share/gnome-shell/extensions').glob('*/schemas')):
        if (directory / 'gschemas.compiled').exists():
            source = Gio.SettingsSchemaSource.new_from_directory(str(directory), source, False)
    config = configparser.ConfigParser(interpolation=None)
    config.read(ROOT / 'desktop/gnome-settings.ini')
    changes = []
    missing = []
    for section in config.sections():
        schema_id, _, path = section.partition(':')
        schema = source.lookup(schema_id, True)
        if schema is None:
            missing.append(schema_id)
            continue
        settings = Gio.Settings.new_full(schema, None, path or None)
        for key, literal in config[section].items():
            if not schema.has_key(key):
                raise RuntimeError(f'Unknown setting: {section}/{key}')
            value = GLib.Variant.parse(schema.get_key(key).get_value_type(), literal, None, None)
            changes.append((section, settings, key, value))
    media = Gio.Settings.new('org.gnome.settings-daemon.plugins.media-keys')
    paths = list(media.get_strv('custom-keybindings'))
    vicinae_path = '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/vicinae/'
    if vicinae_path not in paths:
        changes.append(('org.gnome.settings-daemon.plugins.media-keys', media, 'custom-keybindings', GLib.Variant('as', paths + [vicinae_path])))
    for section, settings, key, value in changes:
        print(f'{section}/{key} = {value.print_(True)}')
    for schema_id in missing:
        print(f'Skipping missing extension schema: {schema_id}; install the extension and rerun.')
    if args.dry_run:
        print('Dry run: no settings, extensions, service or Vesktop preferences changed.')
        return
    # Save all previous values before making any changes.
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6]
    backup = home / '.local/state/dotfiles/backups' / stamp
    backup.mkdir(parents=True, exist_ok=True)
    (backup / 'gnome-settings.json').write_text(json.dumps([
        {'section': section, 'key': key, 'value': settings.get_value(key).print_(True)}
        for section, settings, key, value in changes
    ], indent=2) + '\n')
    for section, settings, key, value in changes:
        if not settings.is_writable(key) or not settings.set_value(key, value):
            raise RuntimeError(f'Cannot write {section}/{key}; run this in your desktop terminal.')
    Gio.Settings.sync()
    if shutil.which('gnome-extensions'):
        installed = set(subprocess.check_output(['gnome-extensions', 'list'], text=True).splitlines())
        shell = Gio.Settings.new('org.gnome.shell')
        (backup / 'enabled-extensions.json').write_text(json.dumps(list(shell.get_strv('enabled-extensions'))))
        for extension in (ROOT / 'desktop/extensions.txt').read_text().splitlines():
            if extension and not extension.startswith('#'):
                if extension in installed:
                    subprocess.run(['gnome-extensions', 'enable', extension], check=True)
                else:
                    print(f'Install extension and rerun: {extension}')
    if shutil.which('vicinae'):
        subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
        subprocess.run(['systemctl', '--user', 'enable', '--now', 'vicinae.service'], check=True)
    # Merge only selected preferences; retain all other Vesktop settings.
    vesktop = home / '.config/vesktop/settings.json'
    if vesktop.exists():
        shutil.copy2(vesktop, backup / 'vesktop-settings.json')
        data = json.loads(vesktop.read_text())
        data.update(json.loads((ROOT / 'desktop/vesktop-preferences.json').read_text()))
        vesktop.write_text(json.dumps(data, indent=2) + '\n')
    print(f'Previous settings saved under {backup}. Restart affected apps to reload.')

if __name__ == '__main__':
    main()
