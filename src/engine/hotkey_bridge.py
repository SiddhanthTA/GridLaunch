from PySide6.QtCore import QObject, Signal


class HotkeyBridge(QObject):
    # Legacy / Multi Mode
    trigger = Signal()

    # Explicit signals
    trigger_multi = Signal()
    trigger_single = Signal()

    def __init__(self):
        super().__init__()
        self.trigger_multi.connect(lambda: print("[SIGNAL] Multi-mode trigger emitted"))
        self.trigger_single.connect(lambda: print("[SIGNAL] Single-mode trigger emitted"))

hotkey_bridge = HotkeyBridge()

# Backward compatibility:
# Treat old `trigger` as multi-mode trigger
hotkey_bridge.trigger.connect(hotkey_bridge.trigger_multi.emit)
