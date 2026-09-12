# Modern FLSUN V400 port

## Repository history

Repositories were cloned with complete history under `/tmp/klipperscreen-v400-port`:

- `upstream`: `KlipperScreen/KlipperScreen`, `master` at `3791fdf7` (2026-09-07).
- `guilouz`: `Guilouz/KlipperScreen-Flsun-Speeder-Pad`, `master` at `4a447b6c` (2024-08-30).
- `modern-v400`: based directly on upstream `master`, branch `v400-modern`.

Git calculated the merge base as `2c8436500c0700a1f7968555d61813d41d10c10c`, matching the supplied SHA. Its subject is `base_panel: fix possible causes of error in show heaters fixes #706`, dated 2022-08-21. From that point, Guilouz has 408 commits and upstream has 1,651 commits. The Guilouz side has 7 merge commits; upstream has 1.

`git cherry upstream/master master` classified 376 Guilouz-side patches as unmatched and 25 as equivalent patches already represented upstream. This is not a safe replay set: most unmatched patches are old upstream snapshots, cosmetic changes, translations, dependency churn, or fork-specific changes to obsolete infrastructure. The fork's first-parent history is dominated by Cyril's periodic upstream sync/update commits, with a smaller set of FLSUN changes interleaved.

## Guilouz customization inventory

| Feature | Original location / evidence | Modern status | Implementation |
|---|---|---|---|
| V400 move speeds and babystep increments | `ks_includes/defaults.conf`, `[printer FLSUN V400]` | PORTED | Added to current `config/defaults.conf`. |
| V400 preheat defaults | `ks_includes/defaults.conf` | PORTED | PLA/ABS defaults updated in current defaults. |
| Macro Z-offset calibration | `panels/zcalibrate.py`, `Z_OFFSET_CALIBRATION` | PORTED | Current zcalibrate discovers the macro through current `Printer.get_gcode_macros()` and sends it through current websocket API. |
| Endstop Phase workflow | `panels/zcalibrate.py`, `ENDSTOPS_CALIBRATION` | PORTED | Same current panel and API; only configured macros are offered. |
| Automatic delta workflow | `panels/zcalibrate.py`, `DELTA_CALIBRATION` | PORTED | Macro is offered alongside upstream's native `DELTA_CALIBRATE`. |
| Safety offset | `panels/zcalibrate.py`, `SECURITY_OFFSET` | PORTED | Macro is offered and confirmed before sending. |
| Native delta/manual calibration | old zcalibrate changes | ALREADY PROVIDED BY UPSTREAM | Current upstream already handles `DELTA_CALIBRATE` and `METHOD=manual`, round-bed mesh origin, and live status updates. |
| FLSUN hotend/logo LEDs | `config/main_menu.conf`, `config/print_menu.conf` | PORTED | Added current menu entries using `printer.gcode.script`. |
| PID macro panel | `panels/pid.py`, `PID_HOTEND` / `PID_BED` | PORTED | Added a small current-API panel; absent macros disable their buttons. |
| FLSUN printer icons | `styles/printers/FLSUN *.svg` | PORTED | Copied the four model icons supported by current printer-select theming. |
| GTK dropdown workaround, old busy handling, screen/network changes | `zcalibrate.py`, `screen.py`, `ks_includes/*` | INTENTIONALLY OMITTED | Current upstream has `ComboBoxPlus`, modern lifecycle/status handling, and the communication architecture. Carrying old code would reintroduce the reported static-GUI failure mode. |
| Speeder Pad installer differences | fork installer and requirements | REPLACED BY MODERN EQUIVALENT | Use current upstream installer/dependencies; the fork's changes include obsolete policy, backend, and dependency behavior unrelated to V400 UI features. |

## Port decisions

The old fork used direct calls and replaced broad portions of `screen.py`, `KlippyWebsocket.py`, REST, printer state, configuration, and panels. Those files were not copied. The port calls current `self._screen._confirm_send_action`, current `printer.gcode.script`, and current `get_gcode_macros()` APIs.

The macro workflows remain optional: a printer without the macro keeps upstream calibration entries and does not show the optional macro entry. LED menu entries intentionally follow Guilouz's behavior and assume the corresponding printer macros exist; they are printer configuration commands, not Moonraker transport code.

No Guilouz translations or old theme trees were copied. Current upstream's translation/theme layout is authoritative; the added strings fall back to the existing gettext behavior.

## Files changed on `v400-modern`

- `panels/zcalibrate.py`: optional macro discovery and dispatch, retaining all current upstream calibration behavior.
- `panels/pid.py`: minimal PID macro panel using current GTK/screen APIs.
- `config/main_menu.conf`: FLSUN LED and PID entries.
- `config/print_menu.conf`: FLSUN LED entries while printing.
- `config/defaults.conf`: V400 motion/babystep and preheat defaults.
- `styles/printers/FLSUN Q5.svg`, `FLSUN QQSP.svg`, `FLSUN SR.svg`, `FLSUN V400.svg`: printer-select assets.

## Features not copied

The fork's live communication, old Moonraker client, old service installer, old translations, unrelated BTT/other hardware changes, and wholesale theme changes are omitted. They are either already upstream, not V400-specific, or conflict with current upstream compatibility. No user printer configuration is embedded in this repository.

## Compatibility concerns

Actual Speeder Pad validation is still required. Confirm its OS provides the current upstream Python/GTK/PyGObject requirements, uses the expected X11/Wayland backend, and has a working systemd service. Confirm the exact macro names in the V400 printer configuration, especially `ENDSTOPS_CALIBRATION`, `DELTA_CALIBRATION`, `SECURITY_OFFSET`, `PID_HOTEND`, and `PID_BED`. Calibration macros must themselves contain safe homing, probe insertion/removal, and `SAVE_CONFIG` behavior appropriate to the installed hardware.

The final source remains a small additive patch over upstream and has remotes `upstream` and `guilouz`, so future upstream updates can be rebased with the FLSUN-specific files and hunks isolated.
