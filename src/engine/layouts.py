from PySide6.QtGui import QGuiApplication


def get_screen_size():
    screen = QGuiApplication.primaryScreen()
    geometry = screen.geometry()
    return geometry.width(), geometry.height()


def compute_layout(layout_type):
    screen_w, screen_h = get_screen_size()
    panes = []

    if layout_type == "Two panes (50 / 50)":
        w = screen_w // 2
        panes = [
            {"x": 0, "y": 0, "w": w, "h": screen_h},
            {"x": w, "y": 0, "w": w, "h": screen_h},
        ]

    elif layout_type == "Left big / Right small":
        left_w = int(screen_w * 0.66)
        right_w = screen_w - left_w
        panes = [
            {"x": 0, "y": 0, "w": left_w, "h": screen_h},
            {"x": left_w, "y": 0, "w": right_w, "h": screen_h},
        ]

    elif layout_type == "Four panes (2x2)":
        half_w = screen_w // 2
        half_h = screen_h // 2
        panes = [
            {"x": 0, "y": 0, "w": half_w, "h": half_h},
            {"x": half_w, "y": 0, "w": half_w, "h": half_h},
            {"x": 0, "y": half_h, "w": half_w, "h": half_h},
            {"x": half_w, "y": half_h, "w": half_w, "h": half_h},
        ]

    return panes
