import json
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QCompleter
)
from PySide6.QtCore import Qt, QStringListModel
from engine.launcher import launch_profile
from PySide6.QtCore import QTimer
from engine.layouts import compute_layout
try:
    from engine.launcher import launch_single_profile
except ImportError:
    launch_single_profile = None
from engine.settings import load_settings
# from engine.paths import get_base_dir
# import os
from engine.paths import get_profiles_path,get_single_profiles_path



class LauncherPopup(QDialog):
    def __init__(self):
        super().__init__()

        self._completer_used = False
        self.mode = "multi"  # default, preserves existing behavior

        # Window behavior
        self.setFixedWidth(280)
        self.setFixedHeight(48)
        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.move(20, 20)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type keyword…")
        self.input.returnPressed.connect(self.handle_enter)

        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #111;
                color: #fff;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #666;
            }
        """)

        layout.addWidget(self.input)
        self.setLayout(layout)

        # Completer
        self.model = QStringListModel([])

        self.completer = QCompleter(self.model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)

        self.input.setCompleter(self.completer)
        self.completer.activated.connect(self.launch_from_completer)

    # -------------------------
    # Mode
    # -------------------------

    def set_mode(self, mode):
        # Expected values: "multi" or "single"
        self.mode = mode

    # -------------------------
    # Lifecycle
    # -------------------------

    

    def showEvent(self, event):
        super().showEvent(event)

        self.profiles=self.load_profiles()
        self.keywords=[profile["name"] for profile in self.profiles]
        self.model.setStringList(self.keywords)

        self.input.clear()

        QTimer.singleShot(0, self.force_focus)

    def force_focus(self):
        self.show()
        self.raise_()
        self.activateWindow()
        # self.requestActivate()
        self.input.setFocus(Qt.ActiveWindowFocusReason)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            return
        super().keyPressEvent(event)

    # -------------------------
    # Launching
    # -------------------------

    def launch_from_completer(self, text):
        self._completer_used = True
        self.input.setText(text)
        self.handle_enter()

    def handle_enter(self):
        if self._completer_used:
            self._completer_used = False
            return

        keyword = self.input.text().strip().lower()
        self.hide()

        # Multi Mode: existing behavior
        if self.mode == "multi":
            for profile in self.profiles:
                if profile["name"].lower() == keyword:
                    layout_rects = compute_layout(profile["layout_type"])
                    launch_profile(profile, layout_rects)
                    return

        # Single Mode: intentionally does nothing for now
        if self.mode == "single" and launch_single_profile:
            for profile in self.profiles:
                if profile["name"].lower() == keyword:
                    launch_single_profile(profile)
                    return
    # -------------------------
    # Data
    # -------------------------

    def load_profiles(self):
        path = (
            get_profiles_path()
            if self.mode == "multi"
            else get_single_profiles_path()
        )

        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return []
