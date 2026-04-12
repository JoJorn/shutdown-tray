import os
import threading
import subprocess
import ctypes

from flask import Flask, request, jsonify
import pystray
from PIL import Image, ImageDraw
from waitress import serve

app_title = "ShutdownTray"

HOST = "0.0.0.0"
PORT = 8765
API_TOKEN = "SecretToken"

app = Flask(__name__)
tray_icon = None


def shutdown_pc() -> None:
    subprocess.Popen(["shutdown", "/s", "/t", "4", "/f", "/c", "Shutdown via ShutdownTray"], shell=False)

def create_image():
    image = Image.new("RGBA", (64, 64))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, 64, 64), fill=(0, 70, 126), radius=17)
    draw.rounded_rectangle((8, 8, 56, 56), outline="white", width=4, radius=8)
    draw.line((32, 16, 32, 30), fill="white", width=6)
    draw.arc((18, 18, 46, 46), start=-50, end=230, fill="white", width=6)
    return image


def authorized(req) -> bool:
    return req.headers.get("X-API-Token") == API_TOKEN


@app.route("/shutdown", methods=["POST"])
def shutdown_route():
    if not authorized(request):
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    shutdown_pc()
    return jsonify({"ok": True, "message": "Shutdown Started"})


def run_webserver():
    print(f"Server starting on http://{HOST}:{PORT}")
    serve(app, host=HOST, port=PORT)


def menu_exit(icon, *_):
    MB_YESNO = 0x04 
    MB_ICONWARNING = 0x30
    IDYES = 6
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "Are you sure you want to exit? \n\nThis PC can no longer be shut down remotely.",
        app_title,
        MB_YESNO | MB_ICONWARNING
    )
    if result == IDYES:
        icon.stop()
        os._exit(0)


def menu_info(*_):
    MB_OK = 0x00
    MB_ICONINFORMATION = 0x40
    ctypes.windll.user32.MessageBoxW(
        None,
        "This is a simple app to shut down this PC externally.\n\nfor more information, contact your system administrator.",
        app_title,
        MB_OK | MB_ICONINFORMATION,
    )

def threaded_menu_action(target):
    def wrapper(icon, item):
        threading.Thread(target=target, args=(icon, item), daemon=True).start()
    return wrapper

def main():
    global tray_icon

    server_thread = threading.Thread(target=run_webserver, daemon=True)
    server_thread.start()
    tray_icon = pystray.Icon(
        app_title,
        create_image(),
        app_title,
        menu=pystray.Menu(
            pystray.MenuItem(f"{app_title} (app info)", threaded_menu_action(menu_info)),
            # pystray.MenuItem(
            #     "Info",
            #     pystray.Menu(
            #         pystray.MenuItem("Status: active", None),
            #         pystray.MenuItem(f"Host: {HOST}", None),
            #         pystray.MenuItem(f"Port: {PORT}", None),
            #     )
            # ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit app", threaded_menu_action(menu_exit))
        ),
    )

    tray_icon.run()


if __name__ == "__main__":
    main()
