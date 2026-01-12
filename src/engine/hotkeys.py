import keyboard
from engine.hotkey_bridge import hotkey_bridge
from engine.settings import load_settings

_current_hotkeys = []


def register_hotkey(hotkey_str, callback):
    print(f"[HOTKEY REGISTER] {hotkey_str} -> {callback}")
    keyboard.add_hotkey(hotkey_str, callback)
    _current_hotkeys.append(hotkey_str)
    print(f"Hotkey registered: {hotkey_str}")


def clear_hotkeys():
    print("[HOTKEY CLEAR] Removing all registered hotkeys")
    for hk in _current_hotkeys:
        try:
            keyboard.remove_hotkey(hk)
        except:
            pass
    _current_hotkeys.clear()


def start_hotkey_listener():
    print("[HOTKEY LISTENER] Starting hotkey listener")
    settings = load_settings()

    multi_hotkey = settings.get("multi_hotkey")
    single_hotkey = settings.get("single_hotkey")

    print(f"[HOTKEY LISTENER] Loaded hotkeys - Multi: {multi_hotkey}, Single: {single_hotkey}")

    clear_hotkeys()

    # Multi Mode hotkey (existing behavior)
    if multi_hotkey:
        register_hotkey(
            multi_hotkey,
            lambda: (print("[HOTKEY FIRE ] MULTI"),hotkey_bridge.trigger_multi.emit())
        )

    # Single Mode hotkey (new, isolated)
    if single_hotkey:
        register_hotkey(
            single_hotkey,
            lambda: (print("[HOTKEY FIRE ] SINGLE"),hotkey_bridge.trigger_single.emit())
        )

    keyboard.wait()
