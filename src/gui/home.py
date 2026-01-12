import json
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QHBoxLayout,
    QLineEdit,
    QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolButton, QMenu
from gui.about_dialog import AboutDialog
# from engine.paths import get_base_dir
from engine.paths import get_profiles_path,get_single_profiles_path
from engine.settings import load_settings
from gui.hotkey_dialog import HotkeyDialog
from engine.settings import save_settings
from gui.single_editor import SingleProfileEditor
import os

PROFILE_PATH = get_profiles_path()
SINGLE_PROFILE_PATH = get_single_profiles_path()


class HomeScreen(QWidget):
    def __init__(self, open_create_layout_callback, refresh_callback,open_edit_callback):
        super().__init__()
        self.current_page=0
        self.items_per_page=10
        self.search_text=""
        self.refresh_callback = refresh_callback
        self.open_edit_callback = open_edit_callback
        self.expanded_profiles = set()

        scroll_area=QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget=QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        top_bar=QHBoxLayout()
        menu_button=QToolButton()
        menu_button.setText("☰")
        menu_button.setStyleSheet("""
            QToolButton {
                font-size: 18px;
                padding: 4px 6px;
            }        
            QToolButton::menu-indicator {
                image: none;
            }                                   
        """)
        menu_button.setPopupMode(QToolButton.InstantPopup)

        menu=QMenu(menu_button)
        about_action=menu.addAction("About GridLaunch")
        change_multi_hotkey_action=menu.addAction("Change Multi Mode Hotkey")
        change_single_hotkey_action=menu.addAction("Change Single Mode Hotkey")
        menu_button.setMenu(menu)

        self.hotkey_label=QLabel()
        self.hotkey_label.setStyleSheet("font-size: 12px; color: #aaaaaa; font-weight: bold;")
        self.hotkey_label.setAlignment(Qt.AlignRight)

        top_bar.addWidget(menu_button, alignment=Qt.AlignLeft)
        top_bar.addStretch()
        top_bar.addWidget(self.hotkey_label)

        layout.addLayout(top_bar)

        settings = load_settings()
        self.mode=settings.get("mode","multi")
        # self.hotkey_label.setText("Hotkey: " + settings.get("hotkey", "").upper().replace("+", " + "))


        title = QLabel("GridLaunch")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        layout.addWidget(title)
        layout.addSpacing(20)

        mode_layout=QHBoxLayout()
        self.multi_btn = QPushButton("Multi Mode")
        self.single_btn = QPushButton("Single Mode")

        self.multi_btn.setCheckable(True)
        self.single_btn.setCheckable(True)

        mode_layout.addStretch()
        mode_layout.addWidget(self.multi_btn)
        mode_layout.addWidget(self.single_btn)
        mode_layout.addStretch()

        layout.addLayout(mode_layout)
        layout.addSpacing(15)

        def set_mode(mode):
            self.mode=mode

            self.multi_btn.setChecked(mode=="multi")
            self.single_btn.setChecked(mode=="single")



            settings = load_settings()
            settings["mode"]=mode
            save_settings(settings)

            self.update_hotkey_label()

            self.current_page=0
            self.search_text=""
            self.load_profiles_for_mode()
            self.render_profiles()

            # self.update_hotkey_label()



            # if mode == "single":
            #     self.create_button.setEnabled(False)
            #     self.create_button.setToolTip("Creating single profiles is not supported yet.")
            # else:
            #     self.create_button.setEnabled(True)
            #     self.create_button.setToolTip("")
            

        self.multi_btn.clicked.connect(lambda: set_mode("multi"))
        self.single_btn.clicked.connect(lambda: set_mode("single"))

             

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search profiles by keyword...")
        search_input.textChanged.connect(self.on_search_changed)

        layout.addWidget(search_input)
        layout.addSpacing(10)

        page_size_layout = QHBoxLayout()
        page_size_label = QLabel("Profiles per page:")
        page_size_combo = QComboBox()
        page_size_combo.addItems(["5", "10", "15"])
        page_size_combo.setCurrentText("10")
        page_size_combo.currentTextChanged.connect(self.on_page_size_changed)

        page_size_layout.addWidget(page_size_label)
        page_size_layout.addWidget(page_size_combo)
        page_size_layout.addStretch()

        layout.addLayout(page_size_layout)
        layout.addSpacing(10)


        self.load_profiles_for_mode()


        self.profile_container=QVBoxLayout()
        layout.addLayout(self.profile_container)


        self.render_profiles()
        layout.addStretch()

        pagination_layout=QHBoxLayout()
        prev_button=QPushButton("◀ Previous")
        next_button=QPushButton("Next ▶")
        prev_button.clicked.connect(self.prev_page)
        next_button.clicked.connect(self.next_page)

        pagination_layout.addStretch()
        pagination_layout.addWidget(prev_button)
        pagination_layout.addWidget(next_button)

        layout.addLayout(pagination_layout)
        layout.addSpacing(10)

        # def open_single_editor():
        #     editor = SingleProfileEditor(
        #         go_back_callback=self.refresh_callback
        #     )
        #     self.window().setCentralWidget(editor)

        self.create_button = QPushButton("Create Layout")
        self.create_button.setFixedHeight(40)

        def on_create_clicked():
            if self.mode == "single":
                self.open_single_editor()
            else:
                open_create_layout_callback()
        self.create_button.clicked.connect(on_create_clicked)

        layout.addWidget(self.create_button)

        set_mode(self.mode)   


        scroll_area.setWidget(content_widget)

        outer_layout=QVBoxLayout()
        outer_layout.addWidget(scroll_area)

        def show_about():
            dialog=AboutDialog(self)
            dialog.exec()

        about_action.triggered.connect(show_about)

        def change_multi_hotkey():
            dialog=HotkeyDialog("multi",self)
            if dialog.exec():
                self.update_hotkey_label()
        
        def change_single_hotkey():
            dialog=HotkeyDialog("single",self)
            if dialog.exec():
                self.update_hotkey_label()

        change_multi_hotkey_action.triggered.connect(change_multi_hotkey)
        change_single_hotkey_action.triggered.connect(change_single_hotkey)
            
        

        self.setLayout(outer_layout)

    def update_hotkey_label(self):
        settings = load_settings()
        
        if self.mode == "multi":
            hk = settings.get("multi_hotkey", "")
        else:
            hk = settings.get("single_hotkey", "")
        
        hk=hk.upper().replace("+", " + ")
        self.hotkey_label.setText("Hotkey: " + hk)

    def load_profiles_for_mode(self):
        path = PROFILE_PATH if self.mode == "multi" else SINGLE_PROFILE_PATH
        try:
            with open(path, "r") as f:
                self.profiles = json.load(f)
        except:
            self.profiles = []

    def on_search_changed(self, text):
        self.search_text=text.lower()
        self.current_page=0
        self.render_profiles()

    def on_page_size_changed(self, value):
        self.items_per_page=int(value)
        self.current_page=0
        self.render_profiles()

    def next_page(self):
        max_pages = max(
            0,
            (len(self.profiles) - 1) // self.items_per_page
        )
        if self.current_page < max_pages:    
            self.current_page+=1
            self.render_profiles()

    def prev_page(self):
        if self.current_page>0:
            self.current_page-=1
        self.render_profiles()


    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)
   
    def render_profiles(self):
        # Clear existing widgets
        self.clear_layout(self.profile_container)

        # Filter profiles by search
        filtered = [
            p for p in self.profiles
            if self.search_text in p.get("name", "").lower()
        ]

        if not filtered:
            label = QLabel("No profiles found")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #aaaaaa;")
            self.profile_container.addWidget(label)
            return

        # Pagination slice
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_items = filtered[start:end]

        for index, profile in enumerate(page_items):
            global_index = start + index

            profile_box = QVBoxLayout()
            header= QHBoxLayout()
            toggle_btn = QPushButton("+")
            toggle_btn.setFixedWidth(28)

            keyword_label = QLabel(profile["name"])
            keyword_label.setStyleSheet("font-weight: bold; font-size: 15px;")

            header.addWidget(toggle_btn)
            header.addWidget(keyword_label)
            header.addStretch()

            profile_box.addLayout(header)

            details=QVBoxLayout()

            if self.mode == "multi":
                layout_type = profile.get("layout_type", "Not set")
                layout_label = QLabel(f"Layout: {layout_type}")
                layout_label.setStyleSheet("color: #dddddd; font-size: 13px;")
                details.addWidget(layout_label)

                panes= profile.get("panes", [])
                for idx, pane in enumerate(panes, start=1):
                    pane_label = QLabel(
                        f"  {idx}. {pane['type']} → {pane['value']}"
                    )
                    pane_label.setStyleSheet("margin-left: 12px;")
                    details.addWidget(pane_label)

            else:
                chrome=profile.get("chrome_profile","Default")
                chrome_label =QLabel(f"Chrome Profile: {chrome}")
                chrome_label.setStyleSheet("color: #dddddd; font-size: 13px;")
                details.addWidget(chrome_label)

                tabs=profile.get("tabs",[])
                for idx, tab in enumerate(tabs, start=1):
                    tab_label = QLabel(
                        f"  {idx}. {tab}"
                    )
                    tab_label.setStyleSheet("margin-left: 12px;")
                    details.addWidget(tab_label)

            
            actions=QHBoxLayout()

            edit_btn = QPushButton("Edit")

            if self.mode == "single":
                edit_btn.clicked.connect(
                    lambda _, p=profile, i=global_index: self.open_single_editor(p, i)
                )
            else:
                edit_btn.clicked.connect(
                    lambda _, p=profile, i=global_index: self.open_edit_callback(p, i)
                )

            delete_btn = QPushButton("Delete")

            if self.mode == "single":
                delete_btn.clicked.connect(
                    lambda _, i=global_index: self.delete_single_profile(i)
                )
            else:
                delete_btn.clicked.connect(
                    lambda _, i=global_index: self.delete_profile(i)
                )

            actions.addStretch()
            actions.addWidget(edit_btn)
            actions.addWidget(delete_btn)

            details.addLayout(actions)

            details_widget = QWidget()
            details_widget.setLayout(details)

            is_expanded = global_index in self.expanded_profiles
            details_widget.setVisible(is_expanded)
            toggle_btn.setText("-" if is_expanded else "+")

            def toggle(_, idx=global_index, w=details_widget, btn=toggle_btn):
                if idx in self.expanded_profiles:
                    self.expanded_profiles.remove(idx)
                    w.setVisible(False)
                    btn.setText("+")
                else:
                    self.expanded_profiles.add(idx)
                    w.setVisible(True)
                    btn.setText("-")
            
            toggle_btn.clicked.connect(toggle)

            profile_box.addWidget(details_widget)

            separator = QLabel()
            separator.setFixedHeight(1)
            separator.setStyleSheet("background-color: #333333;")

            self.profile_container.addLayout(profile_box)
            self.profile_container.addWidget(separator)
            self.profile_container.addSpacing(10)


    def open_single_editor(self,profile=None,index=None):
        editor = SingleProfileEditor(
            go_back_callback=self.refresh_callback,
            edit_profile=profile,
            edit_index=index
        )
        self.window().setCentralWidget(editor)

    def delete_single_profile(self,index):
        try:
            with open(SINGLE_PROFILE_PATH, "r") as f:
                profiles = json.load(f)
        except:
            return

        if 0 <= index < len(profiles):
            profiles.pop(index)
            
            with open(SINGLE_PROFILE_PATH, "w") as f:
                json.dump(profiles, f, indent=2)

        # self.load_profiles_for_mode()
        # self.current_page = 0
        # self.render_profiles()

        # Refresh Home screen
        self.refresh_callback()

    def save_profiles(self, profiles):
        with open(PROFILE_PATH, "w") as f:
            json.dump(profiles, f, indent=2)

    def delete_profile(self, index):
        try:
            with open(PROFILE_PATH, "r") as f:
                profiles = json.load(f)
        except:
            return

        if 0 <= index < len(profiles):
            profiles.pop(index)
            self.save_profiles(profiles)

        self.profiles = profiles
        self.current_page = 0

        # Refresh Home screen
        self.refresh_callback()
        
    
