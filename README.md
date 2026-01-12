# GridLaunch

GridLaunch is a Windows desktop productivity launcher that lets you start entire workspaces — apps, websites, and Chrome profiles — with a single hotkey.

Instead of opening things one by one, you press a key and your whole layout appears.

---

## 🚀 Features

### Multi Mode
Launch multiple applications and websites into pre-defined window layouts.
Examples:
- Coding workspace (VS Code + Browser + Terminal)
- Studying layout (YouTube + Notes + PDF)
- Trading dashboard

Each layout opens all windows and places them automatically.

### Single Mode
Launch Google Chrome profiles with 1–5 predefined tabs.
Examples:
- Work profile
- Personal browsing
- Research
- College

Each profile opens Chrome with exactly the tabs you configured.

---

## ⌨ Global Hotkeys

GridLaunch runs in the system tray and is always available.

- Multi Mode hotkey opens the multi-layout launcher
- Single Mode hotkey opens the Chrome profile launcher

Both hotkeys are fully configurable inside the app.

---

## 🧠 How it works

GridLaunch uses:
- Python
- PySide6 (Qt)
- Windows window management
- Global keyboard hooks

It runs silently in the background and shows a fast popup when you press a hotkey.

---

## 📦 Download

Download the latest Windows executable from:

**GitHub Releases → GridLaunch.exe**

No Python required.

---

## 🛠 Development

Clone the repo, create a virtual environment, and run:

```bash
python src/main.py
