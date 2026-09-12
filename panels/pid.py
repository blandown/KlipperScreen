import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ks_includes.screen_panel import ScreenPanel


class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title or _("PID Calibrations"))
        macros = {macro.lower() for macro in self._printer.get_gcode_macros()}
        self.buttons = {
            "hotend": self._gtk.Button("extruder", _("Hotend PID"), "color1"),
            "bed": self._gtk.Button("bed", _("Bed PID"), "color2"),
        }
        self.buttons["hotend"].set_sensitive("pid_hotend" in macros)
        self.buttons["bed"].set_sensitive("pid_bed" in macros)
        self.buttons["hotend"].connect("clicked", self.start, "PID_HOTEND")
        self.buttons["bed"].connect("clicked", self.start, "PID_BED")
        grid = self._gtk.HomogeneousGrid()
        grid.attach(self.buttons["hotend"], 0, 0, 1, 1)
        grid.attach(self.buttons["bed"], 1, 0, 1, 1)
        self.content.add(grid)

    def start(self, widget, command):
        self._screen._confirm_send_action(
            None, _("Start %s?") % command.replace("_", " "),
            "printer.gcode.script", {"script": command},
        )

    def process_update(self, action, data):
        if action == "notify_busy":
            for button in self.buttons.values():
                button.set_sensitive(not data)
