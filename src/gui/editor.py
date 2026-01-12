import json
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QGroupBox,
    QScrollArea,
    QFormLayout
)
from PySide6.QtCore import Qt
from engine.paths import get_profiles_path
from PySide6.QtWidgets import QCompleter
from engine.app_index import get_installed_apps

PROFILE_PATH = get_profiles_path()



class CreateLayoutScreen(QWidget):
    def __init__(self, go_back_callback,edit_profile=None, edit_index=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.edit_profile = edit_profile
        self.edit_index = edit_index

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(14)

        title = QLabel("Create Layout")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("padding: 6px; border-radius: 6px;")
        self.name_input.setPlaceholderText("Enter keyword (e.g. studying)")

        self.layout_selector = QComboBox()
        self.layout_selector.view().setStyleSheet(""" 
            background-color: #1e1e1e; 
            color: #white; 
            selection-background-color: #3a7afe; 
            border: 1px solid #444;""")
        self.layout_selector.setStyleSheet("padding: 6px; border-radius: 6px;")
        self.layout_selector.addItems([
            "Two panes (50 / 50)",
            "Left big / Right small",
            "Four panes (2x2)"
        ])
        self.layout_selector.currentTextChanged.connect(self.update_preview)

        main_layout.addWidget(title)
        main_layout.addSpacing(20)
        # main_layout.addWidget(QLabel("Keyword"))
        keyword_label = QLabel("Keyword")
        keyword_label.setStyleSheet("font-weight: 600; font-size: 14px; color: #dddddd;")
        main_layout.addWidget(keyword_label)
        main_layout.addWidget(self.name_input)
        main_layout.addSpacing(10)
        # main_layout.addWidget(QLabel("Layout type"))
        keyword_label1 = QLabel("Layout type")
        keyword_label1.setStyleSheet("font-weight: 600; font-size: 14px; color: #dddddd;")
        main_layout.addWidget(keyword_label1)
        main_layout.addWidget(self.layout_selector)

        # Preview container
        self.preview_container = QFrame()
        self.preview_container.setFrameShape(QFrame.Box)
        self.preview_container.setMinimumHeight(220)
        self.preview_layout = QVBoxLayout()
        self.preview_container.setLayout(self.preview_layout)

        main_layout.addSpacing(20)
        # main_layout.addWidget(QLabel("Layout Preview"))
        keyword_label2 = QLabel("Layout Preview")
        keyword_label2.setStyleSheet("font-weight: 600; font-size: 14px; color: #dddddd;")
        main_layout.addWidget(keyword_label2)
        main_layout.addWidget(self.preview_container)
        # Pane configuration container
        self.pane_container = QVBoxLayout()
        main_layout.addSpacing(10)
        # main_layout.addWidget(QLabel("Pane Configuration"))
        keyword_label3 = QLabel("Pane Configuration")
        keyword_label3.setStyleSheet("font-weight: 600; font-size: 14px; color: #dddddd;")
        main_layout.addWidget(keyword_label3)
        main_layout.addLayout(self.pane_container)


        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
        QPushButton {
            background-color: #3a7afe;
            color: white;
            border-radius: 6px;
            padding: 8px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #2f66d0;
        }
        """)
        save_button.setFixedHeight(40)
        save_button.clicked.connect(self.save_profile)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
        QPushButton {
            background-color: #2b2b2b;
            color: #dddddd;
            border-radius: 6px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #353535;
        }
        """)
        back_button.setFixedHeight(40)
        back_button.clicked.connect(self.go_back_callback)

        main_layout.addStretch()
        main_layout.addWidget(save_button)
        main_layout.addWidget(back_button)

        scroll_area.setWidget(content_widget)
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll_area)
        self.setLayout(outer_layout)

        self.installed_apps = get_installed_apps()
        self.app_names = [name for name, _ in self.installed_apps]
        self.app_map = {name: path for name, path in self.installed_apps}

        # Initial preview
        self.update_preview(self.layout_selector.currentText())

        if self.edit_profile:
            self.load_profile_for_edit()


    def load_profile_for_edit(self):
        # Keyword
        self.name_input.setText(self.edit_profile.get("name", ""))

        # Layout type
        layout_type = self.edit_profile.get("layout_type")
        if layout_type:
            index = self.layout_selector.findText(layout_type)
            if index != -1:
                self.layout_selector.setCurrentIndex(index)

        # Pane values
        panes = self.edit_profile.get("panes", [])
        for i, pane in enumerate(panes):
            if i < len(self.pane_inputs):
                type_selector, value_input = self.pane_inputs[i]
                type_selector.setCurrentText(pane["type"].capitalize())
                value_input.setText(pane["value"])




    def build_pane_inputs(self, count):
        # Clear existing pane inputs
        while self.pane_container.count():
            item = self.pane_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.pane_inputs = []

        for i in range(count):
            box = QGroupBox(f"Pane {i + 1}")
            form = QFormLayout()

            type_selector = QComboBox()
            type_selector.addItems(["Website", "Application"])
            type_selector.view().setStyleSheet("""
            background-color: #1e1e1e;
                                               color: #white;
                                               selection-background-color: #3a7afe;
                                                  border: 1px solid #444;
                                            """)

            value_input = QLineEdit()
            value_input.setStyleSheet("padding: 6px; border-radius: 6px;")
            value_input.setPlaceholderText("Enter URL or app name/path")

            # completer = QCompleter(self.app_names)
            # completer.setCaseSensitivity(Qt.CaseInsensitive)
            # completer.setFilterMode(Qt.MatchContains)

            # def on_app_activated(text, input_ref=value_input):
            #     if text in self.app_map:
            #         input_ref.setText(self.app_map[text])

            # # Enable / disable autocomplete based on type
            # def on_type_changed(selected_type, input_ref=value_input, comp=completer):
            #     if selected_type == "Application":
            #         input_ref.setCompleter(comp)
            #     else:
            #         input_ref.setCompleter(None)

            # completer.activated.connect(on_app_activated)
            # type_selector.currentTextChanged.connect(on_type_changed)

            completer= QCompleter(self.app_names)
            popup=completer.popup()
            popup.setStyleSheet("""
            background-color: #1e1e1e;
            color: #ffffff;
            selection-background-color: #3a7afe;
            border: 1px solid #444;
            """)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            completer.setCompletionMode(QCompleter.PopupCompletion)

            def on_app_activated(text, input_ref=value_input):
                if text in self.app_map:
                    input_ref.setText(self.app_map[text])

            def finalize_application_value(input_ref=value_input):
                text=input_ref.text()
                if text in self.app_map:
                    input_ref.setText(self.app_map[text])
            
            def on_type_changed(selected_type, input_ref=value_input, comp=completer):
                if selected_type == "Application":
                    input_ref.setCompleter(comp)
                else:
                    input_ref.setCompleter(None)
            
            completer.activated.connect(on_app_activated)
            value_input.editingFinished.connect(
                lambda ref=value_input: finalize_application_value(ref)
            )
            type_selector.currentTextChanged.connect(on_type_changed)

            on_type_changed(type_selector.currentText())

            form.addRow("Type", type_selector)
            form.addRow("Value", value_input)

            box.setLayout(form)
            self.pane_container.addWidget(box)

            self.pane_inputs.append((type_selector, value_input))

    def clear_preview(self):
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)

            widget = item.widget()
            layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif layout is not None:
                self.clear_layout(layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

        

    def create_box(self, label_text):
        box = QLabel(label_text)
        box.setAlignment(Qt.AlignCenter)
        box.setMinimumHeight(90)
        box.setStyleSheet("""
        background-color: #2d2d2d;
        color: white;
        border: 2px solid #555;
        border-radius: 6px;
        font-weight: bold;
        """)
        return box

    def update_preview(self, layout_type):
        self.clear_preview()

        if layout_type == "Two panes (50 / 50)":
            pane_count = 2
            row = QHBoxLayout()
            row.addWidget(self.create_box("Pane 1"))
            row.addWidget(self.create_box("Pane 2"))
            self.preview_layout.addLayout(row)

        elif layout_type == "Left big / Right small":
            pane_count = 2
            row = QHBoxLayout()
            left = self.create_box("Pane 1 (Big)")
            right = self.create_box("Pane 2 (Small)")
            row.addWidget(left, 2)
            row.addWidget(right, 1)
            self.preview_layout.addLayout(row)

        elif layout_type == "Four panes (2x2)":
            pane_count = 4
            top = QHBoxLayout()
            bottom = QHBoxLayout()
            top.addWidget(self.create_box("Pane 1"))
            top.addWidget(self.create_box("Pane 2"))
            bottom.addWidget(self.create_box("Pane 3"))
            bottom.addWidget(self.create_box("Pane 4"))
            self.preview_layout.addLayout(top)
            self.preview_layout.addLayout(bottom)


        self.preview_layout.setSpacing(8)
        self.build_pane_inputs(pane_count)    

    def save_profile(self):
        name = self.name_input.text().strip().lower()
        if not name:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Validation Error", "Keyword cannot be empty.")
            return
        layout_type = self.layout_selector.currentText()

        if not name:
            return

        # panes = []
        # for type_selector, value_input in self.pane_inputs:
        #     panes.append({
        #         "type": type_selector.currentText().lower(),
        #         "value": value_input.text().strip()
        #     })

        from PySide6.QtWidgets import QMessageBox

        panes=[]
        for type_selector, value_input in self.pane_inputs:
            pane_type=type_selector.currentText().lower()
            value=value_input.text().strip()

            if pane_type=="application" and not value:
                QMessageBox.warning(self, "Validation Error", "Application pane value cannot be empty.")
                return
            
            if pane_type=="website" and not value:
                QMessageBox.warning(self, "Validation Error", "Website pane value cannot be empty.")
                return
            
            panes.append({
                "type": pane_type,
                "value": value
            })



        with open(PROFILE_PATH, "r") as f:
            profiles = json.load(f)
        
        for i, profile in enumerate(profiles):
            if profile.get("name","").lower() == name:
                if self.edit_index is None or i != self.edit_index:
                    from PySide6.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Duplication Error", "A profile with this keyword already exists.")
                    return

        if self.edit_index is not None:
            profiles[self.edit_index]={
                "name": name,
                "layout_type": layout_type,
                "panes": panes
            }

        else:
            profiles.append({
            "name": name,
            "layout_type": layout_type,
            "panes": panes
            })

        with open(PROFILE_PATH, "w") as f:
            json.dump(profiles, f, indent=2)

        self.go_back_callback()