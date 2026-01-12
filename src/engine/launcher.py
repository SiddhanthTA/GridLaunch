import webbrowser
import subprocess
import time
import os

from engine.window_manager import get_foreground_window, move_window
from engine.logger import log

CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"




def launch_website(url):

    log(f"Website launch requested: raw_value={repr(url)}", "WEBSITE")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    log(f"Resolved website URL: {url}", "WEBSITE")
    
    if os.path.exists(CHROME_PATH):
        try:
            subprocess.Popen([
            CHROME_PATH, "--new-window", url
            ])
            log(f"Launched website in Chrome: {url}", "WEBSITE")
            return True
        except Exception as e:
            log(f"Failed to launch website in Chrome: {e}", "WEBSITE")
            return False    
    else:
        log("Chrome not found, launching with default browser", "WEBSITE")
        print("Chrome not found. Cannot launch website.")
        webbrowser.open(url)
        return False


def launch_application(app):
    log(f"Application launch requested: {app}", "APPLICATION")
    try:
        os.startfile(app)
        log(f"Launched application: {app}", "APPLICATION")
        return True
    except Exception as e:
        log(f"Failed to launch application: {e}", "APPLICATION")
        log(f"Value was: {repr(app)}", "ERROR")
        log(f"Exception: {repr(e)}", "ERROR")
        print(f"Failed to launch application: {app}")
        return False


def launch_profile(profile, layout_rects):
    panes = profile.get("panes", [])
    rects = layout_rects[:]

    for pane in panes:
        if not rects:
            break

        rect = rects.pop(0)
        pane_type = pane.get("type")
        value = pane.get("value")

        log(f"Launching pane: type={pane_type}, value={repr(value)}", "PROFILE")

        if value == "__none__":
            log("Pane value is '__none__', skipping launch", "PROFILE")
            continue

        if pane_type == "website":
            if launch_website(value):
                from engine.window_manager import get_all_windows, get_new_window
                existing_windows = get_all_windows()

                # launch app or website here

                time.sleep(0.8)
                new_hwnd = get_new_window(existing_windows)


                if new_hwnd:
                    log(f"New window detected: hwnd={new_hwnd}", "WINDOW")
                    move_window(new_hwnd, rect)
                else:
                    log("No new window detected after launching website", "WINDOW")



        if pane_type == "application":
            if launch_application(value):
                from engine.window_manager import get_all_windows, get_new_window
                existing_windows = get_all_windows()

                # launch app or website here

                time.sleep(0.8)
                new_hwnd = get_new_window(existing_windows)

                if new_hwnd:
                    log(f"New window detected: hwnd={new_hwnd}", "WINDOW")
                    move_window(new_hwnd, rect)
                else:
                    log("No new window detected after launching application", "WINDOW")

def launch_single_profile(profile):
    """
    Launches a Single Mode Chrome workspace:
    - One fresh Chrome window
    - Mandatory chrome profile
    - 1–5 tabs
    - Fullscreen
    """

    chrome_profile = profile.get("chrome_profile")
    tabs = profile.get("tabs", [])

    # ---- Validation ----
    if not chrome_profile:
        log("Single Mode launch failed: chrome_profile missing", "SINGLE")
        return False

    if not tabs or len(tabs) == 0:
        log("Single Mode launch failed: no tabs provided", "SINGLE")
        print("Single Mode error: enter at least one tab")
        return False

    if len(tabs) > 5:
        log(f"Single Mode launch failed: too many tabs ({len(tabs)})", "SINGLE")
        print("Single Mode error: maximum 5 tabs allowed")
        return False

    if not os.path.exists(CHROME_PATH):
        log("Chrome not found for Single Mode launch", "SINGLE")
        return False

    # ---- Normalize URLs ----
    urls = []
    for url in tabs:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        urls.append(url)

    # ---- Build Chrome command ----
    cmd = [
        CHROME_PATH,
        "--new-window",
        f"--profile-directory={chrome_profile}",
    ] + urls

    log(
        f"Launching Single Mode Chrome: profile={chrome_profile}, tabs={len(urls)}",
        "SINGLE"
    )

    try:
        subprocess.Popen(cmd)
    except Exception as e:
        log(f"Single Mode Chrome launch failed: {e}", "SINGLE")
        return False

    # ---- Fullscreen the new window ----
    try:
        from engine.window_manager import get_all_windows, get_new_window

        existing_windows = get_all_windows()
        time.sleep(1.2)  # Chrome needs a bit more time

        new_hwnd = get_new_window(existing_windows)
        if new_hwnd:
            import win32gui
            win32gui.ShowWindow(new_hwnd, 3)  # SW_MAXIMIZE
            log(f"Single Mode Chrome fullscreened: hwnd={new_hwnd}", "SINGLE")
        else:
            log("Single Mode: no new Chrome window detected", "SINGLE")

    except Exception as e:
        log(f"Single Mode fullscreen step failed: {e}", "SINGLE")

    return True
