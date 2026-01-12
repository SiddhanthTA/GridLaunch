import json
import os
from engine.paths import get_settings_path

SETTINGS_PATH = get_settings_path()

DEFAULT_SETTINGS = {
    "mode": "multi",
    "multi_hotkey": "ctrl+alt+l",
    "single_hotkey": "ctrl+alt+k",
}

def load_settings():
    # If file does not exist → create fresh defaults
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_PATH, "r") as f:
            data = json.load(f)
    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    migrated = False

    # ---- MIGRATION LOGIC ----

    # Old installs: "hotkey" existed, but mode-specific ones didn’t
    if "hotkey" in data:
        if "multi_hotkey" not in data:
            data["multi_hotkey"] = data["hotkey"]
        # single_hotkey still gets default if missing
        data.pop("hotkey", None)
        migrated = True

    # Ensure required keys exist
    for key, value in DEFAULT_SETTINGS.items():
        if key not in data:
            data[key] = value
            migrated = True

    if migrated:
        save_settings(data)

    return data


def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
