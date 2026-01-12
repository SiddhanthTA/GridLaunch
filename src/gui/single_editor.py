import json
import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QMessageBox,
    QHBoxLayout
)
from PySide6.QtCore import Qt

from engine.paths import get_single_profiles_path


SINGLE_PROFILE_PATH = get_single_profiles_path()


class SingleProfileEditor(QWidget):
    def __init__(self, go_back_callback,edit_profile=None,edit_index=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.edit_profile=edit_profile 
        self.edit_index=edit_index
        self.tab_inputs = []

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ---------- Title ----------
        title = QLabel("Create Single Mode Profile")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(20)

        

        # ---------- Keyword ----------
        keyword_label = QLabel("Keyword")
        keyword_label.setStyleSheet("font-weight: 600; color: #dddddd;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. work")
        self.name_input.setStyleSheet("padding: 6px; border-radius: 6px;")

        layout.addWidget(keyword_label)
        layout.addWidget(self.name_input)

        # ---------- Chrome Profile ----------
        chrome_label = QLabel("Chrome Profile")
        chrome_label.setStyleSheet("font-weight: 600; color: #dddddd;")

        self.chrome_profile = QComboBox()
        self.chrome_profile.setEditable(True)
        self.chrome_profile.setStyleSheet("padding: 6px; border-radius: 6px;")
        self.chrome_profile.addItems([
            "Default",
            "Profile 1",
            "Profile 2",
            "Profile 3",
            "Profile 4",
            "Profile 5"
        ])
        self.chrome_profile.view().setStyleSheet("""
            background-color: #1e1e1e;
            color: #white;
            selection-background-color: #3a7afe;
            border: 1px solid #444;
        """)

        layout.addSpacing(10)
        layout.addWidget(chrome_label)
        layout.addWidget(self.chrome_profile)

        chrome_hint = QLabel(
            "Specify the Chrome profile directory to use "
            "Open chrome://version/ to find your profile name."
        )
        chrome_hint.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        layout.addWidget(chrome_hint)

        # ---------- Tabs ----------
        tabs_label = QLabel("Tabs (1 to 5)")
        tabs_label.setStyleSheet("font-weight: 600; color: #dddddd;")
        layout.addSpacing(15)
        layout.addWidget(tabs_label)

        tabs_hint=QLabel("Leave unused tab fields empty.")
        tabs_hint.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        layout.addWidget(tabs_hint)

        self.tabs_container = QVBoxLayout()
        layout.addLayout(self.tabs_container)

        for _ in range(5):
            self.add_tab_input()

        # ---------- Buttons ----------
        layout.addStretch()

        save_btn = QPushButton("Save")
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a7afe;
                color: white;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2f66d0;
            }
        """)
        save_btn.clicked.connect(self.save_profile)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #dddddd;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #353535;
            }
        """)
        back_btn.clicked.connect(self.go_back_callback)

        layout.addWidget(save_btn)
        layout.addWidget(back_btn)

        scroll.setWidget(content)
        outer = QVBoxLayout()
        outer.addWidget(scroll)
        self.setLayout(outer)

        if self.edit_profile:
            self.load_profile_for_edit()

    # ---------- Helpers ----------

    def load_profile_for_edit(self):
        self.name_input.setText(self.edit_profile.get("name",""))

        self.chrome_profile.setCurrentText(
            self.edit_profile.get("chrome_profile","")
        )

        tabs=self.edit_profile.get("tabs",[])
        for i,tab in enumerate(tabs):
            if i < len(self.tab_inputs):
                self.tab_inputs[i].setText(tab)

    def add_tab_input(self):
        row = QHBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText("https://example.com")
        input_field.setStyleSheet("padding: 6px; border-radius: 6px;")

        self.tab_inputs.append(input_field)
        row.addWidget(input_field)
        self.tabs_container.addLayout(row)

    # ---------- Save ----------

    def save_profile(self):
        name = self.name_input.text().strip().lower()
        chrome_profile = self.chrome_profile.currentText().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Keyword cannot be empty.")
            return

        if not chrome_profile:
            QMessageBox.warning(self, "Validation Error", "Chrome profile is required.")
            return

        tabs = [t.text().strip() for t in self.tab_inputs if t.text().strip()]

        if len(tabs) == 0:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Enter at least one tab."
            )
            return

        if len(tabs) > 5:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Maximum of 5 tabs allowed."
            )
            return

        # Load existing
        profiles = []
        if os.path.exists(SINGLE_PROFILE_PATH):
            try:
                with open(SINGLE_PROFILE_PATH, "r") as f:
                    profiles = json.load(f)
            except Exception:
                QMessageBox.warning(
                    self,
                    "Data Error",
                    "single_profiles.json is corrupted."
                )
                return

        for i,p in enumerate(profiles):
            if p.get("name") == name:
                if self.edit_index is None and i != self.edit_index:
                    QMessageBox.warning(
                        self,
                        "Duplication Error",
                        "A single-mode profile with this keyword already exists."
                    )
                    return
            
        if self.edit_index is not None:
            profiles[self.edit_index]={
                "name": name,
                "chrome_profile": chrome_profile,
                "tabs": tabs
            }
        else:
            profiles.append({
                "name": name,
                "chrome_profile": chrome_profile,
                "tabs": tabs
            })

        with open(SINGLE_PROFILE_PATH, "w") as f:
            json.dump(profiles, f, indent=2)

        self.go_back_callback()
