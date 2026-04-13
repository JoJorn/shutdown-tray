@echo off
setlocal

cd /d "%~dp0"

py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install pyinstaller

py -c "from shutdown_tray import create_icon_image; img = create_icon_image(); img.save('icon.ico')"

py -m PyInstaller --noconfirm --clean --onefile --windowed --icon=icon.ico --name ShutdownTray shutdown_tray.py

echo.
echo Klaar.
echo EXE: %cd%\dist\ShutdownTray.exe
pause
