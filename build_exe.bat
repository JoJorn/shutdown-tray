@echo off
setlocal

cd /d "%~dp0"

py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --clean --onefile --windowed --name ShutdownTray shutdown_tray.py

echo.
echo Klaar.
echo EXE: %cd%\dist\ShutdownTray.exe
pause
