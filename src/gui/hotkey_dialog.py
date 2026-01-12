from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
import keyboard

from engine.settings import load_settings, save_settings
from engine.hotkeys import register_hotkey
from engine.hotkeys import clear_hotkeys, start_hotkey_listener
import threading


class HotkeyDialog(QDialog):
    def __init__(self, hotkey_type,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change Hotkey")
        self.setFixedWidth(360)
        self.hotkey_type=hotkey_type

        self.current_keys = []

        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Press new hotkey combination")
        mode_name = "Multi-mode" if hotkey_type == "multi" else "Single-mode"
        title = QLabel(f"Press new {mode_name} Hotkey")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.display = QLabel("Waiting for input…")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("""
            padding: 10px;
            background-color: #2d2d2d;
            border-radius: 6px;
            font-size: 14px;
        """)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.save_hotkey)
        cancel_btn.clicked.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(self.display)
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)
        self.setModal(True)

        keyboard.hook(self.on_key_event)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def on_key_event(self, event):
        if event.event_type != "down":
            return

        key = event.name.lower()

        if key in ("enter","esc","escape"):
            return

        if key not in self.current_keys:
            self.current_keys.append(key)

        combo = "+".join(self.current_keys)
        self.display.setText(combo)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
            return
        super().keyPressEvent(event)

    def save_hotkey(self):
        if len(self.current_keys) < 2:
            QMessageBox.warning(
                self,
                "Invalid Hotkey",
                "Hotkey must include at least two keys."
            )
            return

        hotkey_str = "+".join(self.current_keys)

        settings = load_settings()

        if self.hotkey_type == "multi":
            settings["multi_hotkey"] = hotkey_str
        elif self.hotkey_type == "single":
            settings["single_hotkey"] = hotkey_str
        # settings["hotkey"] = hotkey_str
        save_settings(settings)

        clear_hotkeys()
        threading.Thread(target=start_hotkey_listener,daemon=True).start()

        self.accept()

    def closeEvent(self, event):
        keyboard.unhook_all()


