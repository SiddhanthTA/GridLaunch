from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About GridLaunch")
        self.setFixedWidth(420)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("GridLaunch")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        description = QLabel(
            "GridLaunch is a Windows productivity tool that lets you launch "
            "apps and websites using keyboard shortcuts.\n\n"

            "It has two modes:\n\n"

            "Multi Mode:\n"
            "Launch multiple applications or websites into a predefined screen layout "
            "with a single hotkey.\n\n"

            "Single Mode:\n"
            "Launch a Chrome profile with multiple tabs (up to 5) using a separate hotkey. "
            "Each profile acts as a focused browsing workspace.\n\n"

            "What it does:\n"
            "• Uses keywords to select what to launch\n"
            "• Uses two independent global hotkeys\n"
            "• Shows a popup where you type the keyword\n"
            "• Launches either a window layout (Multi Mode) or a Chrome workspace (Single Mode)\n"
        )
        description.setWordWrap(True)

        author = QLabel(
            "Author:\n"
            "Siddhanth T A\n"
            "3rd Year Computer Science Student\n\n"
            "Contact:\n"
            "sidcodes0303@gmail.com"
        )
        author.setWordWrap(True)
        author.setStyleSheet("margin-top: 12px;")

        close_button = QPushButton("Close")
        close_button.setFixedHeight(36)
        close_button.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(author)
        layout.addStretch()
        layout.addWidget(close_button)

        self.setLayout(layout)
