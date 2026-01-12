import time
import win32gui
import win32con


def get_all_windows():
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            windows.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return windows


def get_foreground_window(timeout=5):
    end_time = time.time() + timeout
    last_hwnd = None

    while time.time() < end_time:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd and hwnd != last_hwnd:
            return hwnd
        time.sleep(0.05)

    return None


def move_window(hwnd, rect):
    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetWindowPos(
        hwnd,
        None,
        x, y, w, h,
        win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW
    )

def get_new_window(existing_hwnds, timeout=5):
    end_time = time.time() + timeout

    while time.time() < end_time:
        def callback(hwnd, results):
            if (
                hwnd not in existing_hwnds
                and win32gui.IsWindowVisible(hwnd)
                and win32gui.GetWindowText(hwnd)
            ):
                results.append(hwnd)

        found = []
        win32gui.EnumWindows(callback, found)

        if found:
            return found[0]

        time.sleep(0.05)

    return None

