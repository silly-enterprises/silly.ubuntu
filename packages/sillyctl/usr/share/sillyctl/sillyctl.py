#! /usr/bin/env python3

"""
SILLYCTL™ v0.2 - The Config Gremlin
----------------------------------
Now with support for:
  - Multiple files per module
  - Scripts (pre/post enable/disable)
  - Modular manifest loading from /usr/share/sillyctl/modules.d
  - Future man page support!

Controls:
  - SPACE toggles entries
  - ENTER applies
  - q or ESC to quit
"""

import os
import json
import subprocess
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Checkbox, Button, Static
from textual.containers import Vertical

CONFIG_PATH = Path("/etc/silly/sillyctl.json")
MODULE_DIR = Path("/usr/share/sillyctl/modules.d")

class ToggleMenu(Vertical):
    def compose(self) -> ComposeResult:
        for module in SillyCtlApp.modules:
            checked = self.get_enabled_state(module["id"])
            yield Checkbox(module["label"], id=module["id"], value=checked)
        yield Button("Apply Changes", id="apply")

    def get_enabled_state(self, module_id: str) -> bool:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                state = json.load(f)
                return state.get(module_id, False)
        return False

class SillyCtlApp(App):
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]

    modules = []

    def compose(self) -> ComposeResult:
        self.modules = self.load_manifests()
        yield Header("SILLYCTL v0.2 - Config Gremlin Control Panel™", show_clock=True)
        yield ToggleMenu()
        yield Footer()

    def load_manifests(self):
        modules = []
        if MODULE_DIR.exists():
            for file in MODULE_DIR.glob("*.json"):
                with open(file) as f:
                    module = json.load(f)
                    modules.append(module)
        return modules

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "apply":
            self.apply_changes()

    def apply_changes(self):
        toggles = {}
        for cb in self.query(Checkbox):
            toggles[cb.id] = cb.value
            module = next((m for m in self.modules if m["id"] == cb.id), None)
            if not module:
                continue

            if cb.value:
                self.run_hook(module.get("scripts", {}).get("pre_enable"))
                for f in module.get("files", []):
                    self.enable_file(f["source"], f["target"])
                self.run_hook(module.get("scripts", {}).get("post_enable"))
            else:
                for f in module.get("files", []):
                    self.disable_file(f["target"])
                self.run_hook(module.get("scripts", {}).get("post_disable"))

        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(toggles, f, indent=2)

    def enable_file(self, src: str, dst: str):
        if not Path(dst).exists():
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.system(f"cp '{src}' '{dst}'")

    def disable_file(self, dst: str):
        if Path(dst).exists():
            os.remove(dst)

    def run_hook(self, script_path):
        if script_path and Path(script_path).exists():
            subprocess.run(["bash", script_path], check=False)

if __name__ == "__main__":
    app = SillyCtlApp()
    app.run()
