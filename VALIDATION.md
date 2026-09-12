# V400 hardware validation

Run this after installation, with the printer safely unloaded and an accessible emergency-stop path.

1. Start KlipperScreen and confirm the main UI appears.
2. Confirm Moonraker connects without a reconnect loop.
3. Watch the dashboard for several minutes; printer state must continue updating.
4. Heat and cool the hotend and bed; temperatures and targets must update continuously.
5. Set a heater target from the UI and confirm the command reaches Klipper.
6. Home the printer and make a small XY and Z move; confirm motion and position updates.
7. Execute a harmless configured G-code macro and confirm its response.
8. Start, pause, resume, and stop a short print; verify real-time state changes.
9. Confirm FLSUN menu entries and the V400 printer icon appear where configured.
10. Run the Z-offset macro workflow with the leveling switch and verify the saved offset.
11. Run the Delta calibration macro/workflow and verify the resulting Klipper state.
12. Run Endstop Phase calibration if the three `endstop_phase` sections and macro are configured.
13. Press Emergency Stop and confirm motion/heaters stop; reset only when safe.
14. Use Restart Klipper and confirm the UI reconnects and resumes updates.
15. Use Restart Moonraker and confirm the UI reconnects and resumes updates.
16. Leave the UI active during the above operations; verify it remains touch-responsive.
17. Check `journalctl -u KlipperScreen -b` and confirm no recurring exceptions.

Record the Pad OS, Python version, display backend, macro names, and any deviations. A software-only checkout/compile cannot prove touchscreen, GPIO, display rotation, heater, motion, or calibration safety.
