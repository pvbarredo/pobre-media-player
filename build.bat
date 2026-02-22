@echo off
echo Building Pobre Media Player for Windows...
echo.

REM Install PyInstaller if not already installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building executable...
pyinstaller --onefile --windowed --name=PobreMediaPlayer --icon=NONE player.py

echo.
echo Build complete! Executable is in the dist\ folder.
echo.
pause
