import os
import threading
import subprocess

from flask import Flask, request, jsonify
import pystray
from PIL import Image, ImageDraw
from waitress import serve

HOST = "0.0.0.0"   # Zet op "127.0.0.1" als alleen lokaal
PORT = 8765
API_TOKEN = "SecretToken"

app = Flask(__name__)
tray_icon = None


def shutdown_pc() -> None:
    subprocess.Popen(["shutdown", "/s", "/t", "10", "/f", "/c", "Shutdown by API via ShutdownTray"], shell=False)

def create_image():
    image = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((8, 8, 55, 55), outline="white", width=4)
    draw.line((16, 32, 43, 32), fill="white", width=4)
    draw.line((32, 22, 43, 32), fill="white", width=4)
    draw.line((32, 42, 43, 32), fill="white", width=4)
    return image


def authorized(req) -> bool:
    return req.headers.get("X-API-Token") == API_TOKEN


@app.route("/shutdown", methods=["POST"])
def shutdown_route():
    if not authorized(request):
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    threading.Thread(target=shutdown_pc, daemon=True).start()
    return jsonify({"ok": True, "message": "Shutdown gestart"})


def run_webserver():
    serve(app, host=HOST, port=PORT)


def menu_exit(icon, item):
    icon.stop()
    os._exit(0)


def main():
    global tray_icon

    server_thread = threading.Thread(target=run_webserver, daemon=True)
    server_thread.start()

    tray_icon = pystray.Icon(
        "ShutdownTray",
        create_image(),
        "Shutdown Tray",
        menu=pystray.Menu(
            pystray.MenuItem("Shutdown app om extern af te sluiten", lambda icon, item: None, enabled=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("App afsluiten", menu_exit)
        ),
    )

    tray_icon.run()


if __name__ == "__main__":
    main()
