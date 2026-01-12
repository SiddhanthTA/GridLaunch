import os
import win32com.client

START_MENU_DIRS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(
        r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    ),
]

SYSTEM_APP_ALIASES ={
    "Calculator" : "calc",
    "Notepad" : "notepad",
    "Paint" : "mspaint",
    "Command Prompt" : "cmd",
    "PowerShell" : "powershell",
    "File Explorer" : "explorer",
    "None" : "__none__",
}

def get_installed_apps():
    """
    Returns a list of tuples:
    (display_name, executable_path)
    """
    shell = win32com.client.Dispatch("WScript.Shell")
    apps = []

    for base_dir in START_MENU_DIRS:
        if not os.path.exists(base_dir):
            continue

        for root, _, files in os.walk(base_dir):
            for file in files:
                if not file.lower().endswith(".lnk"):
                    continue

                shortcut_path = os.path.join(root, file)

                try:
                    shortcut = shell.CreateShortcut(shortcut_path)
                    target = shortcut.TargetPath

                    if target and os.path.exists(target):
                        name = os.path.splitext(file)[0]
                        apps.append((name, shortcut_path))
                except:
                    pass

    for name, command in SYSTEM_APP_ALIASES.items():
        apps.append((name, command))

    return apps
