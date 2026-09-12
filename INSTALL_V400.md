# Install on an FLSUN V400 Speeder Pad

These commands run on the Speeder Pad over SSH. They stop only KlipperScreen; they do not delete printer configuration.

```bash
cd ~
sudo systemctl stop KlipperScreen
mv KlipperScreen KlipperScreen.backup.$(date +%Y%m%d-%H%M%S)
git clone https://github.com/your-fork/modern-v400.git KlipperScreen
cd KlipperScreen
git checkout v400-modern
./scripts/KlipperScreen-install.sh
sudo systemctl daemon-reload
sudo systemctl enable KlipperScreen
sudo systemctl restart KlipperScreen
```

Replace the clone URL with the location where this repository is published, or copy `/tmp/klipperscreen-v400-port/modern-v400` to the Pad with `scp` and use that checkout. Do not copy over `printer_data`, `printer.cfg`, `moonraker.conf`, or other configuration directories.

If the existing Moonraker update-manager entry points at the old checkout, back up `moonraker.conf`, then set its KlipperScreen entry to the new checkout and its `origin` to the published repository. Keep the existing `virtualenv`, `requirements`, and `managed_services` fields unless the current installer reports that a change is needed.

Rollback:

```bash
sudo systemctl stop KlipperScreen
mv ~/KlipperScreen ~/KlipperScreen.failed.$(date +%Y%m%d-%H%M%S)
mv ~/KlipperScreen.backup.YYYYMMDD-HHMMSS ~/KlipperScreen
sudo systemctl daemon-reload
sudo systemctl restart KlipperScreen
```

Use the actual backup directory name printed by `ls -dt ~/KlipperScreen.backup.* | head -1`. This restores the application tree only; printer configuration is untouched.

Inspect failures with:

```bash
systemctl status KlipperScreen --no-pager
journalctl -u KlipperScreen -b --no-pager -n 200
journalctl -u moonraker -b --no-pager -n 100
```

Install dependencies with the repository's current script, not the old Guilouz requirements. If the script fails, keep the backup checkout active and record the missing Debian package or Python version before changing the Pad OS.
