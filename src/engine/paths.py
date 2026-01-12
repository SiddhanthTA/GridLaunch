import os
import sys
import shutil

APP_NAME = "GridLaunch"

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_user_data_dir():
    appdata = os.getenv("APPDATA")  # C:\Users\<user>\AppData\Roaming
    path = os.path.join(appdata, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

def _ensure_file(filename):
    user_path = os.path.join(get_user_data_dir(), filename)

    if not os.path.exists(user_path):
        bundled = os.path.join(get_base_dir(), "data", filename)

        if os.path.exists(bundled):
            shutil.copy(bundled, user_path)
        else:
            # fallback
            with open(user_path, "w") as f:
                f.write("[]")

    return user_path

def get_settings_path():
    return _ensure_file("settings.json")

def get_profiles_path():
    return _ensure_file("profiles.json")

def get_single_profiles_path():
    return _ensure_file("single_profiles.json")
