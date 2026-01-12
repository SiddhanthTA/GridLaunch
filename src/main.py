import sys
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("GridLaunch")
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt
from gui.home import HomeScreen
from gui.editor import CreateLayoutScreen
import threading
from engine.hotkeys import start_hotkey_listener
from engine.hotkey_bridge import hotkey_bridge
from engine.launcher_popup import LauncherPopup
from PySide6.QtGui import QIcon, QAction
import os
from engine.paths import get_base_dir

ICON_PATH= os.path.join(get_base_dir(), "assets", "gridlaunch.ico")


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # app.setStyleSheet("""
    # QComboBox QAbstractItemView {
    #     background-color: #1e1e1e;
    #     color: #ffffff;
    #     selection-background-color: #3a7afe;
    #     selection-color: #ffffff;
    #     border: 1px solid #444;
    #     outline: none;
    # }
    # QComboBox {
    #     background-color: #111;
    #     color: #ffffff;
    #     border: 1px solid #333;
    #     border-radius: 6px;
    #     padding: 6px;
    # }
    
    # QComboBox::drop-down {
    # border: none;
    # }
    # QComboBox::down-arrow {
    # image:none;
    # }
    #                   QComboBox QAbstractItemView::item {
    #                   padding: 6 px;
    #                   }
                      
                      
    #                   """)

    app.setApplicationName("GridLaunch")

    app.setWindowIcon(QIcon(ICON_PATH))

    tray=QSystemTrayIcon(QIcon(ICON_PATH), app)
    tray.setToolTip("GridLaunch")

    tray_menu=QMenu()

    open_action=QAction("Open GridLaunch")
    quit_action=QAction("Quit")

    tray_menu.addAction(open_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)

    tray.setContextMenu(tray_menu)
    tray.show()

    popup_multi = LauncherPopup()
    popup_single = LauncherPopup()

    def show_popup_multi():
        popup_multi.set_mode("multi")
        print("[MAIN] triggering multi-mode received - GUI Thread")
        popup_multi.show()
        popup_multi.activateWindow()
        popup_multi.raise_()
    
    def show_popup_single():
        popup_single.set_mode("single")
        print("[MAIN] triggering single-mode received - GUI Thread")
        popup_single.show()
        popup_single.activateWindow()
        popup_single.raise_()
    
    hotkey_bridge.trigger_multi.connect(show_popup_multi,Qt.QueuedConnection)
    hotkey_bridge.trigger_single.connect(show_popup_single,Qt.QueuedConnection)

    hotkey_thread = threading.Thread(
        target=start_hotkey_listener,
        daemon=True
    )
    hotkey_thread.start()

    window = QMainWindow()
    
    open_action.triggered.connect(
        lambda: (
            window.show(),
            window.raise_(),
            window.activateWindow()
        )
    )

    quit_action.triggered.connect(app.quit)

    window.setWindowTitle("GridLaunch")
    window.setWindowIcon(QIcon(ICON_PATH))
    window.resize(800, 500)

    

    def show_editor_for_edit(profile, index):
        editor = CreateLayoutScreen(
            go_back_callback=show_home,
            edit_profile=profile,
            edit_index=index
        )
        window.setCentralWidget(editor)

    def show_home():
        home = HomeScreen(
            open_create_layout_callback=show_editor,
            refresh_callback=show_home,
            open_edit_callback=show_editor_for_edit
            )
        window.setCentralWidget(home)

    def show_editor():
        editor = CreateLayoutScreen(go_back_callback=show_home)
        window.setCentralWidget(editor)

    show_home()

    def closeEvent(event):
        event.ignore()
        window.hide()
        tray.showMessage(
            "GridLaunch",
            "Application minimized to tray.",
            QSystemTrayIcon.Information,
            2000
        )

    window.closeEvent = closeEvent    

    window.show()
    sys.exit(app.exec())





if __name__ == "__main__":
    main()
