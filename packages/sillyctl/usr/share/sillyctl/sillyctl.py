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

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List
import argparse

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Checkbox, Button
from textual.containers import Vertical

CONFIG_PATH = Path("/etc/silly/sillyctl.json")
MODULE_DIR = Path("/usr/share/sillyctl/modules.d")


def load_manifests() -> List[Dict]:
    modules: List[Dict] = []
    if MODULE_DIR.exists():
        for file in sorted(MODULE_DIR.glob("*.json")):
            with open(file) as f:
                modules.append(json.load(f))
    return modules


def load_state() -> Dict[str, bool]:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def save_state(state: Dict[str, bool]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(state, f, indent=2)


def enable_file(src: str, dst: str) -> None:
    if not Path(dst).exists():
        Path(dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)


def disable_file(dst: str) -> None:
    if Path(dst).exists():
        Path(dst).unlink()


def run_hook(script_path: str) -> None:
    if script_path and Path(script_path).exists():
        subprocess.run(["bash", script_path], check=False)


def apply_module(module: Dict, enable: bool) -> None:
    if enable:
        run_hook(module.get("scripts", {}).get("pre_enable"))
        for f in module.get("files", []):
            enable_file(f["source"], f["target"])
        run_hook(module.get("scripts", {}).get("post_enable"))
    else:
        for f in module.get("files", []):
            disable_file(f["target"])
        run_hook(module.get("scripts", {}).get("post_disable"))


def set_state(module_id: str, enable: bool) -> None:
    state = load_state()
    state[module_id] = enable
    save_state(state)

class ToggleMenu(Vertical):
    def compose(self) -> ComposeResult:
        for module in SillyCtlApp.modules:
            checked = load_state().get(module["id"], False)
            yield Checkbox(module["label"], id=module["id"], value=checked)
        yield Button("Apply Changes", id="apply")


class SillyCtlApp(App):
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]

    modules = []

    def __init__(self, modules: List[Dict] | None = None) -> None:
        super().__init__()
        self.modules = modules or load_manifests()

    def compose(self) -> ComposeResult:
        yield Header("SILLYCTL v0.2 - Config Gremlin Control Panel™", show_clock=True)
        yield ToggleMenu()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "apply":
            self.apply_changes()

    def apply_changes(self):
        toggles = load_state()
        for cb in self.query(Checkbox):
            toggles[cb.id] = cb.value
            module = next((m for m in self.modules if m["id"] == cb.id), None)
            if not module:
                continue

            apply_module(module, cb.value)

        save_state(toggles)

def main() -> None:
    parser = argparse.ArgumentParser(description="Manage silly configuration modules")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("tui", help="launch the interactive TUI")

    p_enable = sub.add_parser("enable", help="enable a module")
    p_enable.add_argument("module")

    p_disable = sub.add_parser("disable", help="disable a module")
    p_disable.add_argument("module")

    sub.add_parser("list", help="list available modules")

    args = parser.parse_args()

    modules = load_manifests()

    if args.cmd in (None, "tui"):
        app = SillyCtlApp(modules)
        app.run()
        return

    if args.cmd == "list":
        state = load_state()
        for mod in modules:
            status = "enabled" if state.get(mod["id"], False) else "disabled"
            print(f"{mod['id']}: {status}")
        return

    module = next((m for m in modules if m["id"] == getattr(args, 'module', '')), None)
    if not module:
        parser.error(f"unknown module: {getattr(args, 'module', '')}")

    enable = args.cmd == "enable"
    apply_module(module, enable)
    set_state(module["id"], enable)


if __name__ == "__main__":
    main()
